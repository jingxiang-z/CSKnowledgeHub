package main

import (
	"context"
	"errors"
	"sync"
	"testing"
	"time"
)

func TestRunPipelineConsumesEveryItem(t *testing.T) {
	counts := make(map[int]int)
	var mu sync.Mutex

	err := runPipeline(context.Background(), 3, 4, 1, 10, func(item int) {
		mu.Lock()
		counts[item]++
		mu.Unlock()
	})
	if err != nil {
		t.Fatalf("runPipeline() error = %v", err)
	}
	for item := range 10 {
		if counts[item] != 3 {
			t.Errorf("item %d consumed %d times, want 3", item, counts[item])
		}
	}
}

func TestRunPipelineEmptyInput(t *testing.T) {
	called := false
	err := runPipeline(context.Background(), 2, 3, 1, 0, func(int) {
		called = true
	})
	if err != nil || called {
		t.Fatalf("empty run: error = %v, consumer called = %v", err, called)
	}
}

func TestRunPipelineRejectsInvalidArguments(t *testing.T) {
	consume := func(int) {}
	tests := []struct {
		name      string
		ctx       context.Context
		producers int
		consumers int
		buffer    int
		items     int
		consume   func(int)
	}{
		{"nil context", nil, 1, 1, 1, 1, consume},
		{"no producers", context.Background(), 0, 1, 1, 1, consume},
		{"no consumers", context.Background(), 1, 0, 1, 1, consume},
		{"no capacity", context.Background(), 1, 1, 0, 1, consume},
		{"negative items", context.Background(), 1, 1, 1, -1, consume},
		{"nil consumer", context.Background(), 1, 1, 1, 1, nil},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if err := runPipeline(tt.ctx, tt.producers, tt.consumers, tt.buffer, tt.items, tt.consume); err == nil {
				t.Fatal("runPipeline() error = nil, want validation error")
			}
		})
	}
}

func TestRunPipelineCancellationUnblocksFullChannel(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	started := make(chan struct{})
	release := make(chan struct{})
	var once sync.Once
	done := make(chan error, 1)

	go func() {
		done <- runPipeline(ctx, 2, 1, 1, 1000, func(int) {
			once.Do(func() { close(started) })
			<-release
		})
	}()

	select {
	case <-started:
	case <-time.After(2 * time.Second):
		cancel()
		close(release)
		t.Fatal("consumer never started")
	}

	cancel()
	close(release)
	select {
	case err := <-done:
		if !errors.Is(err, context.Canceled) {
			t.Fatalf("runPipeline() error = %v, want context.Canceled", err)
		}
	case <-time.After(2 * time.Second):
		t.Fatal("runPipeline() did not stop after cancellation")
	}
}
