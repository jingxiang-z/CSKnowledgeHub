package main

import "fmt"

type Node struct {
	key   int
	value int
	prev  *Node
	next  *Node
}

type LRUCache struct {
	capacity int
	cache    map[int]*Node
	head     *Node
	tail     *Node
}

func NewNode(key int, value int) *Node {
	return &Node{
		key:   key,
		value: value,
		prev:  nil,
		next:  nil,
	}
}

func NewLRUCache(capacity int) (*LRUCache, error) {
	if capacity <= 0 {
		return nil, fmt.Errorf("capacity must be positive")
	}
	head := NewNode(0, 0)
	tail := NewNode(0, 0)
	head.next = tail
	tail.prev = head
	return &LRUCache{
		capacity: capacity,
		cache:    make(map[int]*Node),
		tail:     tail,
		head:     head,
	}, nil
}

func (l *LRUCache) removeFromList(node *Node) {
	node.prev.next = node.next
	node.next.prev = node.prev
	node.prev = nil
	node.next = nil
}

func (l *LRUCache) addToHead(node *Node) {
	node.prev = l.head
	node.next = l.head.next
	l.head.next.prev = node
	l.head.next = node
}

func (l *LRUCache) Get(key int) (int, bool) {
	if node, exists := l.cache[key]; exists {
		l.removeFromList(node)
		l.addToHead(node)
		return node.value, true
	}
	return 0, false
}

func (l *LRUCache) Put(key int, value int) {
	if node, exists := l.cache[key]; exists {
		node.value = value
		l.removeFromList(node)
		l.addToHead(node)
	} else {
		newNode := NewNode(key, value)
		l.addToHead(newNode)
		l.cache[key] = newNode
		if len(l.cache) > l.capacity {
			tailPrev := l.tail.prev
			l.removeFromList(tailPrev)
			delete(l.cache, tailPrev.key)
		}
	}
}

func (l *LRUCache) Delete(key int) {
	if node, exists := l.cache[key]; exists {
		l.removeFromList(node)
		delete(l.cache, key)
	}
}

func (l *LRUCache) Len() int {
	return len(l.cache)
}

func (l *LRUCache) Capacity() int {
	return l.capacity
}
