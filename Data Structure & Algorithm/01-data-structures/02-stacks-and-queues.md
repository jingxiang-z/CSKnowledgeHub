# Stacks and Queues

A **stack** is last-in, first-out (LIFO): the most recently added item is the
first removed. A **queue** is first-in, first-out (FIFO): the earliest item is
the first removed. A deque supports efficient operations at both ends.

| Structure | Add | Remove | Typical uses |
| --- | --- | --- | --- |
| Stack | push at top | pop from top | undo, nested parsing, DFS |
| Queue | enqueue at back | dequeue from front | BFS, scheduling |
| Deque | either end | either end | sliding windows, 0-1 BFS |

With an appropriate implementation, push, pop, enqueue, dequeue, and peek are
all `O(1)`.

```python
from collections import deque

stack = []
stack.append("open")       # push
top = stack.pop()          # pop

queue = deque()
queue.append("first")      # enqueue
front = queue.popleft()    # dequeue
```

Do not use `list.pop(0)` as a queue dequeue: every remaining element is shifted,
which costs `O(n)`.
