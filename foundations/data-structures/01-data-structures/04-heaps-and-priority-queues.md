# Heaps and Priority Queues

A binary heap is a complete binary tree stored compactly in an array. In a
min-heap, every parent is no greater than its children, so the minimum item is
at the root. The heap property does not sort the whole array.

A priority queue exposes the useful heap operations:

| Operation | Cost |
| --- | --- |
| inspect best item | `O(1)` |
| insert item | `O(log n)` |
| remove best item | `O(log n)` |
| build from `n` items with bottom-up heapify | `O(n)` |

Use a heap when only the current minimum or maximum matters: task scheduling,
Dijkstra's algorithm, merging sorted streams, and top-`k` problems are common
examples. Use a balanced search tree instead when you also need ordered
iteration or arbitrary deletion.

```python
import heapq

heap = []
heapq.heappush(heap, (priority, task))
priority, task = heapq.heappop(heap)
```

Add a monotonic counter as a second tuple element if equal-priority tasks may
not be comparable.
