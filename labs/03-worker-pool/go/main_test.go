package main

import (
	"context"
	"errors"
	"reflect"
	"sync"
	"testing"
	"time"
)

func makePool(t *testing.T, workers, queueSize int) *WorkerPool {
	t.Helper()
	pool, err := NewWorkerPool(workers, queueSize)
	if err != nil {
		t.Fatalf("NewWorkerPool: %v", err)
	}
	t.Cleanup(pool.Close)
	return pool
}

func submitJob(t *testing.T, pool *WorkerPool, job Job) {
	t.Helper()
	if err := pool.Submit(job); err != nil {
		t.Fatalf("Submit: %v", err)
	}
}

func waitFor(t *testing.T, done <-chan struct{}) {
	t.Helper()
	select {
	case <-done:
	case <-time.After(3 * time.Second):
		t.Fatal("timed out waiting for worker")
	}
}

// Keep a worker busy until release is called. Cleanup releases it before Close.
func blockedTask(t *testing.T, pool *WorkerPool) func() {
	t.Helper()
	started := make(chan struct{})
	released := make(chan struct{})
	var once sync.Once
	release := func() { once.Do(func() { close(released) }) }
	t.Cleanup(release)
	submitJob(t, pool, func(context.Context) (any, error) {
		close(started)
		<-released
		return 42, nil
	})
	waitFor(t, started)
	return release
}

// Read results only after Close or Cancel has waited for every worker.
func assertValues(t *testing.T, pool *WorkerPool, want ...any) {
	t.Helper()
	if len(pool.Results) != len(want) {
		t.Fatalf("got %d results, want %d", len(pool.Results), len(want))
	}
	for i, result := range pool.Results {
		if result.Err != nil || result.Cancelled || result.Value != want[i] {
			t.Errorf("result[%d] = %+v, want successful value %v", i, result, want[i])
		}
	}
}

func TestEmptyInput(t *testing.T) {
	pool := makePool(t, 1, 2)
	pool.Close()
	assertValues(t, pool)
}

func TestOneWorker(t *testing.T) {
	pool := makePool(t, 1, 3)
	var executed []int
	for number := 0; number < 3; number++ {
		n := number
		submitJob(t, pool, func(context.Context) (any, error) {
			executed = append(executed, n)
			return n * n, nil
		})
	}
	pool.Close()
	assertValues(t, pool, 0, 1, 4)
	if !reflect.DeepEqual(executed, []int{0, 1, 2}) {
		t.Fatalf("execution order = %v, want [0 1 2]", executed)
	}
}

func TestFewerJobsThanWorkers(t *testing.T) {
	pool := makePool(t, 4, 2)
	release := blockedTask(t, pool)
	finished := make(chan struct{})
	submitJob(t, pool, func(context.Context) (any, error) {
		close(finished)
		return 99, nil
	})
	// The second job can execute while the first is still blocked.
	waitFor(t, finished)
	release()
	pool.Close()
	// Go stores results as workers append them, not in submission order.
	if len(pool.Results) != 2 {
		t.Fatalf("got %d results, want 2", len(pool.Results))
	}
	values := map[any]int{}
	for _, result := range pool.Results {
		if result.Err != nil || result.Cancelled {
			t.Fatalf("unexpected result: %+v", result)
		}
		values[result.Value]++
	}
	if values[42] != 1 || values[99] != 1 {
		t.Fatalf("unexpected values: %v", values)
	}
}

func TestBoundedQueue(t *testing.T) {
	pool := makePool(t, 1, 1)
	release := blockedTask(t, pool)
	submitJob(t, pool, func(context.Context) (any, error) { return 99, nil })
	// Unlike Python, Go rejects submission when the waiting slot is full.
	if err := pool.Submit(func(context.Context) (any, error) { return 100, nil }); err == nil {
		t.Fatal("expected full queue error")
	}
	release()
	pool.Close()
	assertValues(t, pool, 42, 99)
}

func TestJobFailure(t *testing.T) {
	pool := makePool(t, 1, 2)
	boom := errors.New("boom")
	submitJob(t, pool, func(context.Context) (any, error) { return nil, boom })
	submitJob(t, pool, func(context.Context) (any, error) { return 99, nil })
	pool.Close()
	if len(pool.Results) != 2 {
		t.Fatalf("got %d results, want 2", len(pool.Results))
	}
	if result := pool.Results[0]; !errors.Is(result.Err, boom) || result.Cancelled {
		t.Errorf("failed job result = %+v, want boom without cancellation", result)
	}
	if result := pool.Results[1]; result.Value != 99 || result.Err != nil || result.Cancelled {
		t.Errorf("job after failure = %+v, want successful value 99", result)
	}
}

func TestCancellation(t *testing.T) {
	pool := makePool(t, 1, 1)
	// Ensure cleanup cancels a context-waiting job before closing the pool.
	t.Cleanup(pool.Cancel)
	started := make(chan struct{})
	submitJob(t, pool, func(ctx context.Context) (any, error) {
		close(started)
		<-ctx.Done()
		return nil, ctx.Err()
	})
	waitFor(t, started)
	queuedRan := false
	submitJob(t, pool, func(context.Context) (any, error) {
		queuedRan = true
		return 99, nil
	})
	pool.Cancel()
	if queuedRan {
		t.Error("queued job executed after cancellation")
	}
	if len(pool.Results) != 2 {
		t.Fatalf("got %d results, want 2", len(pool.Results))
	}
	for i, result := range pool.Results {
		if !result.Cancelled || !errors.Is(result.Err, context.Canceled) {
			t.Errorf("result[%d] = %+v, want cancellation", i, result)
		}
	}
	if err := pool.Submit(func(context.Context) (any, error) { return nil, nil }); err == nil {
		t.Error("submission after Cancel succeeded")
	}
	pool.Cancel() // Repeated cancellation must be safe.
}

func TestCleanShutdown(t *testing.T) {
	pool := makePool(t, 1, 1)
	release := blockedTask(t, pool)
	submitJob(t, pool, func(ctx context.Context) (any, error) {
		return 99, ctx.Err() // Graceful shutdown must not cancel queued work.
	})
	release()
	pool.Close()
	assertValues(t, pool, 42, 99)
	if err := pool.Submit(func(context.Context) (any, error) { return nil, nil }); err == nil {
		t.Error("submission after Close succeeded")
	}
	pool.Close() // Repeated shutdown must be safe.
}
