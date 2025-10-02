# Design

## Cache

### LRU

```python
class Node:
    def __init__(self, key=0, value=0, prev=None, next=None):
        self.key = key
        self.val = value
        self.prev = prev
        self.next = next

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.mapper = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _insert(self, node):
        prev = self.tail.prev
        node.prev = prev
        prev.next = node
        self.tail.prev = node
        node.next = self.tail
        self.mapper[node.key] = node
    
    def _remove(self, node):
        prev, next = node.prev, node.next
        prev.next = next
        next.prev = prev
        node.prev = None
        node.next = None
        del self.mapper[node.key]
    
    def get(self, key: int) -> int:
        if key not in self.mapper:
            return -1
       	node = self.mapper[key]
        self._remove(node)
        self._insert(node)
        return node.val
    
    def put(self, key: int, value: int) -> None:
        if key in self.mapper:
            node = self.mapper[key]
            node.val = value
            self._remove(node)
            self._insert(node)
        else:
            if len(self.mapper) == self.capacity:
                self._remove(self.head.next)
            node = Node(key, value)
            self._insert(node)
```

### LFU

## HashTable

```python
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size
    
    def _hash(self, key):
        return hash(key) % size
    
    def put(self, key, value):
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = []
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return
        self.table.append([key, value])
    
    def get(self, key):
        index = self._hash(key)
        if self.table[index] is not None:
            for item in self.table[index]:
                if item[0] == key:
                    return item[1]
        return None
    
    def remove(self, key):
        index = self._hash(key)
        if self.table[index] is not None:
            for item in self.table[index]:
                if item[0] == key:
                    self.table[index].remove(key)
                    return
```

1. Load Factor: Monitor the load factor (elements vs. slots), and expand when it exceeds a threshold (usually around 0.7 to 0.8) to avoid performance degradation.
2. Expansion Strategy: Decide how much to increase the size when expanding, with doubling the size being a common choice.
3. Rehashing: Rehash existing elements efficiently when expanding by recalculating hash codes and redistributing them.
4. Timing: Choose when to trigger expansion—immediately or deferred—to balance collision prevention and computational cost.
5. Concurrent Access: Handle expansion carefully in concurrent environments, considering synchronization.
6. Memory: Be mindful of temporary memory usage increase during expansion.
7. Performance Testing: Test and benchmark to ensure your chosen parameters align with your use case and performance requirements.

## Queue

### Heap

```python
class MinHeap:
    def __init__(self):
        self.heap = []
    
    def push(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap)-1)
    
    def pop(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root
    
    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index] < self.heap[parent]:
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            else:
                break
    
    def _heapify_down(self, index):
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            if (left < len(self.heap)) and self.heap[left] < self.heap[smallest]:
                smallest = left
            if (right < len(self.heap)) and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest != index:
                self.heap[smallest], self.heap[index] = self.heap[index], self.heap[smallest]
                index = smallest
            else:
                break
```

A linear time heapify operation can be performed by starting from the middle of the heap and working your way up to the root, ensuring that the subtree rooted at each node satisfies the heap property.

```python
def heapify(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        helper(arr, i, n)

def helper(arr, index, size):
    smallest = index
    left = 2 * index + 1
    right = 2 * index + 2
    if (left < size) and arr[left] < arr[smallest]
        smallest = left
    if (right < size) and arr[right] < arr[smallest]:
        smallest = right
    if smallest != index:
        arr[smallest], arr[index] = arr[index], arr[smallest]
        helper(arr, smallest, size)
```

### Priority Queue

```python
import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
    
    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, item))
    
    def pop(self):
        return heapq.heappop(self.heap)[1]
    
    def top(self):
        return self.heap[0][1]
```

## Stack

### Min Stack

### Max Stack

## Union-Find

```python
class UnionFind:
    def __init__(self, size):
        self.root = [i for i in range(size)]
        self.rank = [0] * size
    
    def find(self, x):
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x]) # Path compression
        return self.root[x]
    
    def union(self, x, y):
        rootx = self.find(x)
        rooty = self.find(y)
        if rootx != rooty:
            if self.rank[rootx] < self.rank[rooty]:
                self.parent[rootx] = rooty
            elif self.rank[rootx] > self.rank[rooty]:
                self.parent[rooty] = rootx
            else:
                self.parent[rooty] = rootx
                self.rank[rootx] += 1
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

## File System



