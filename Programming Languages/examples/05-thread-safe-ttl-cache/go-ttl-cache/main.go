package main

import (
	"errors"
	"fmt"
	"log"
	"sync"
	"time"
)

var ErrInvalidTTL = errors.New("ttl must be positive")

type TTLCache struct {
	cache  map[string]int
	ttl    map[string]time.Time
	mu     sync.RWMutex
	stopCh chan struct{}
	stop   sync.Once
	worker sync.WaitGroup
	now    func() time.Time
}

func NewTTLCache() *TTLCache {
	return NewTTLCacheWithClock(time.Now)
}

func NewTTLCacheWithClock(now func() time.Time) *TTLCache {
	return newTTLCache(time.Second, now)
}

func newTTLCache(cleanupInterval time.Duration, now func() time.Time) *TTLCache {
	c := &TTLCache{
		cache:  make(map[string]int),
		ttl:    make(map[string]time.Time),
		stopCh: make(chan struct{}),
		now:    now,
	}
	c.worker.Add(1)
	go c.cleanupWorker(cleanupInterval)
	return c
}

func (c *TTLCache) Get(key string) (int, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if exp, ok := c.ttl[key]; ok {
		if c.now().After(exp) {
			delete(c.cache, key)
			delete(c.ttl, key)
			return 0, false
		}
	}
	val, ok := c.cache[key]
	return val, ok
}

func (c *TTLCache) Set(key string, value int, ttl time.Duration) error {
	if ttl <= 0 {
		return ErrInvalidTTL
	}

	c.mu.Lock()
	defer c.mu.Unlock()
	c.cache[key] = value
	c.ttl[key] = c.now().Add(ttl)
	return nil
}

func (c *TTLCache) Delete(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	delete(c.cache, key)
	delete(c.ttl, key)
}

func (c *TTLCache) Len() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.clear()
	return len(c.cache)
}

func (c *TTLCache) clear() {
	now := c.now()
	for key := range c.cache {
		if now.After(c.ttl[key]) {
			delete(c.cache, key)
			delete(c.ttl, key)
		}
	}
}

func (c *TTLCache) cleanupWorker(cleanupInterval time.Duration) {
	defer c.worker.Done()
	ticker := time.NewTicker(cleanupInterval)
	defer ticker.Stop()
	for {
		select {
		case <-ticker.C:
			c.mu.Lock()
			c.clear()
			c.mu.Unlock()
		case <-c.stopCh:
			return
		}
	}
}

func (c *TTLCache) Close() {
	c.stop.Do(func() {
		close(c.stopCh)
	})
	c.worker.Wait()
}

func main() {
	cache := NewTTLCache()
	defer cache.Close()

	if err := cache.Set("answer", 42, 5*time.Second); err != nil {
		log.Fatal(err)
	}

	value, found := cache.Get("answer")
	fmt.Printf("value=%d found=%t\n", value, found)
}
