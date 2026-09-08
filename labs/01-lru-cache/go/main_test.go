package main

import (
	"reflect"
	"testing"
)

func newTestCache(t *testing.T, capacity int) *LRUCache {
	t.Helper()
	cache, err := NewLRUCache(capacity)
	if err != nil {
		t.Fatalf("NewLRUCache(%d): %v", capacity, err)
	}
	return cache
}

func assertOrder(t *testing.T, cache *LRUCache, want []int) {
	t.Helper()
	var got []int
	for node := cache.head.next; node != cache.tail; node = node.next {
		got = append(got, node.key)
	}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("recency order = %v, want %v", got, want)
	}
}

func TestLRUInsertAndGet(t *testing.T) {
	cache := newTestCache(t, 2)
	cache.Put(1, 10)
	value, found := cache.Get(1)
	if !found || value != 10 {
		t.Fatalf("Get(1) = (%d, %t), want (10, true)", value, found)
	}
	if cache.Len() != 1 {
		t.Fatalf("Len() = %d, want 1", cache.Len())
	}
}

func TestLRUGetPromotion(t *testing.T) {
	cache := newTestCache(t, 2)
	cache.Put(1, 10)
	cache.Put(2, 20)
	cache.Get(1)
	assertOrder(t, cache, []int{1, 2})
	cache.Put(3, 30)
	if _, found := cache.Get(2); found {
		t.Fatal("Get(2) found an evicted key")
	}
	assertOrder(t, cache, []int{3, 1})
}

func TestLRUPutPromotion(t *testing.T) {
	cache := newTestCache(t, 2)
	cache.Put(1, 10)
	cache.Put(2, 20)
	cache.Put(1, 100)
	assertOrder(t, cache, []int{1, 2})
	cache.Put(3, 30)
	if _, found := cache.Get(2); found {
		t.Fatal("Get(2) found an evicted key")
	}
	value, found := cache.Get(1)
	if !found || value != 100 {
		t.Fatalf("Get(1) = (%d, %t), want (100, true)", value, found)
	}
}

func TestLRUCapacityEviction(t *testing.T) {
	cache := newTestCache(t, 2)
	cache.Put(1, 10)
	cache.Put(2, 20)
	cache.Put(3, 30)
	if _, found := cache.Get(1); found {
		t.Fatal("Get(1) found the least-recently-used key after eviction")
	}
	if cache.Len() != 2 {
		t.Fatalf("Len() = %d, want 2", cache.Len())
	}
	if cache.Capacity() != 2 {
		t.Fatalf("Capacity() = %d, want 2", cache.Capacity())
	}
}

func TestLRUDelete(t *testing.T) {
	cache := newTestCache(t, 2)
	cache.Put(1, 10)
	cache.Put(2, 20)
	cache.Delete(1)
	if _, found := cache.Get(1); found {
		t.Fatal("Get(1) found a deleted key")
	}
	if cache.Len() != 1 {
		t.Fatalf("Len() = %d, want 1", cache.Len())
	}
	assertOrder(t, cache, []int{2})
}

func TestLRURejectsNonPositiveCapacity(t *testing.T) {
	for _, capacity := range []int{0, -1} {
		if _, err := NewLRUCache(capacity); err == nil {
			t.Errorf("NewLRUCache(%d) returned nil error", capacity)
		}
	}
}

func TestLRURepeatedOperationsOnOneKey(t *testing.T) {
	cache := newTestCache(t, 1)
	for value := 0; value < 5; value++ {
		cache.Put(1, value)
		got, found := cache.Get(1)
		if !found || got != value {
			t.Fatalf("Get(1) = (%d, %t), want (%d, true)", got, found, value)
		}
		if cache.Len() != 1 {
			t.Fatalf("Len() = %d, want 1", cache.Len())
		}
	}
	cache.Delete(1)
	cache.Delete(1)
	if cache.Len() != 0 {
		t.Fatalf("Len() = %d, want 0", cache.Len())
	}
}

func TestLRUStoredNegativeOneIsFound(t *testing.T) {
	cache := newTestCache(t, 1)
	cache.Put(1, -1)
	value, found := cache.Get(1)
	if !found || value != -1 {
		t.Fatalf("Get(1) = (%d, %t), want (-1, true)", value, found)
	}
}
