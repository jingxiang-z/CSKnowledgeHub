package main

import (
	"errors"
	"strconv"
	"sync"
	"testing"
	"time"
)

type fakeClock struct {
	mu  sync.Mutex
	now time.Time
}

func newFakeClock() *fakeClock {
	return &fakeClock{now: time.Date(2026, time.January, 1, 0, 0, 0, 0, time.UTC)}
}

func (c *fakeClock) Now() time.Time {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.now
}

func (c *fakeClock) Advance(duration time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.now = c.now.Add(duration)
}

func TestCacheBasics(t *testing.T) {
	cache := NewTTLCache()
	t.Cleanup(cache.Close)

	if err := cache.Set("key", 1, time.Second); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}

	val, found := cache.Get("key")
	if !found {
		t.Fatal("Get returned not found for a key that was just set")
	}
	if val != 1 {
		t.Fatalf("Get returned %d, want 1", val)
	}

	val, found = cache.Get("nonexistent")
	if found {
		t.Fatal("Get returned found for a key that was not set")
	}
}

func TestCacheExpiration(t *testing.T) {
	clock := newFakeClock()
	cache := NewTTLCacheWithClock(clock.Now)
	t.Cleanup(cache.Close)

	if err := cache.Set("key", 1, time.Second); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}
	clock.Advance(2 * time.Second)
	if _, found := cache.Get("key"); found {
		t.Error("Get returned a non-expired entry")
	}
}

func TestCacheOverwrite(t *testing.T) {
	cache := NewTTLCache()
	t.Cleanup(cache.Close)

	if err := cache.Set("key", 1, time.Second); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}
	if err := cache.Set("key", 2, time.Second); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}
	val, found := cache.Get("key")
	if !found {
		t.Fatal("Get returned not found for a key that was just set")
	}
	if val != 2 {
		t.Fatalf("Get returned %d, want 2", val)
	}
}

func TestCacheDelete(t *testing.T) {
	cache := NewTTLCache()
	t.Cleanup(cache.Close)

	if err := cache.Set("key", 1, time.Second); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}
	cache.Delete("key")
	if _, found := cache.Get("key"); found {
		t.Error("Get returned a deleted entry")
	}

	cache.Delete("nonexistent")
}

func TestCacheLen(t *testing.T) {
	cache := NewTTLCache()
	t.Cleanup(cache.Close)

	if err := cache.Set("key1", 1, time.Second); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}
	if err := cache.Set("key2", 2, time.Second); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}
	if got := cache.Len(); got != 2 {
		t.Fatalf("Len returned %d, want 2", got)
	}
}

func TestSetRejectsNonPositiveTTL(t *testing.T) {
	cache := NewTTLCache()
	t.Cleanup(cache.Close)

	for _, ttl := range []time.Duration{0, -time.Second} {
		if err := cache.Set("key", 1, ttl); !errors.Is(err, ErrInvalidTTL) {
			t.Fatalf("Set with TTL %v returned %v, want ErrInvalidTTL", ttl, err)
		}
	}

	if got := cache.Len(); got != 0 {
		t.Fatalf("Len returned %d after rejected sets, want 0", got)
	}
}

func TestConcurrentExpiredGets(t *testing.T) {
	clock := newFakeClock()
	cache := NewTTLCacheWithClock(clock.Now)
	t.Cleanup(cache.Close)

	if err := cache.Set("key", 1, time.Second); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}
	clock.Advance(2 * time.Second)

	const readers = 100
	var wg sync.WaitGroup
	wg.Add(readers)
	for range readers {
		go func() {
			defer wg.Done()
			if _, found := cache.Get("key"); found {
				t.Error("Get returned an expired entry")
			}
		}()
	}
	wg.Wait()
}

func TestBackgroundCleanup(t *testing.T) {
	clock := newFakeClock()
	cache := newTTLCache(time.Millisecond, clock.Now)
	t.Cleanup(cache.Close)

	if err := cache.Set("expired", 1, time.Second); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}
	clock.Advance(2 * time.Second)

	deadline := time.Now().Add(time.Second)
	for {
		cache.mu.RLock()
		_, valueStored := cache.cache["expired"]
		_, ttlStored := cache.ttl["expired"]
		cache.mu.RUnlock()

		if !valueStored && !ttlStored {
			break
		}
		if time.Now().After(deadline) {
			t.Fatal("cleanup worker did not remove the expired entry")
		}
		time.Sleep(time.Millisecond)
	}

	if err := cache.Set("live", 2, time.Second); err != nil {
		t.Fatalf("Set after background cleanup returned an error: %v", err)
	}
}

func TestConcurrentReaders(t *testing.T) {
	cache := NewTTLCache()
	t.Cleanup(cache.Close)

	if err := cache.Set("key", 42, time.Minute); err != nil {
		t.Fatalf("Set returned an unexpected error: %v", err)
	}

	const readers = 50
	const readsPerReader = 200
	var wg sync.WaitGroup
	wg.Add(readers)
	for range readers {
		go func() {
			defer wg.Done()
			for range readsPerReader {
				if value, found := cache.Get("key"); !found || value != 42 {
					t.Errorf("Get returned (%d, %t), want (42, true)", value, found)
					return
				}
			}
		}()
	}
	wg.Wait()
}

func TestConcurrentWriters(t *testing.T) {
	cache := NewTTLCache()
	t.Cleanup(cache.Close)

	const writers = 100
	var wg sync.WaitGroup
	wg.Add(writers)
	for i := range writers {
		go func() {
			defer wg.Done()
			key := "key-" + strconv.Itoa(i)
			if err := cache.Set(key, i, time.Minute); err != nil {
				t.Errorf("Set(%q) returned an unexpected error: %v", key, err)
			}
		}()
	}
	wg.Wait()

	if got := cache.Len(); got != writers {
		t.Fatalf("Len returned %d after concurrent writes, want %d", got, writers)
	}
}

func TestMixedConcurrentOperations(t *testing.T) {
	cache := NewTTLCache()
	t.Cleanup(cache.Close)

	const workers = 50
	const operationsPerWorker = 100
	var wg sync.WaitGroup
	wg.Add(workers)
	for worker := range workers {
		go func() {
			defer wg.Done()
			for operation := range operationsPerWorker {
				key := "key-" + strconv.Itoa(operation%10)
				if err := cache.Set(key, worker, time.Minute); err != nil {
					t.Errorf("Set(%q) returned an unexpected error: %v", key, err)
					return
				}
				cache.Get(key)
				if operation%3 == 0 {
					cache.Delete(key)
				}
			}
		}()
	}
	wg.Wait()

	if err := cache.Set("final", 99, time.Minute); err != nil {
		t.Fatalf("final Set returned an unexpected error: %v", err)
	}
	if value, found := cache.Get("final"); !found || value != 99 {
		t.Fatalf("final Get returned (%d, %t), want (99, true)", value, found)
	}
}

func TestCloseIsIdempotent(t *testing.T) {
	cache := NewTTLCache()
	cache.Close()
	cache.Close()
}
