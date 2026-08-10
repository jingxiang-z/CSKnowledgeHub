# Data Structures

Data structures determine how information is stored and which operations can be
performed efficiently. Select one by starting with the operations a problem
needs most often—not by the shape of the input alone.

Unless noted otherwise, the costs in this guide are worst-case costs. Hash-table
costs are expected costs and balanced-tree costs assume the balancing invariant
is maintained.

## Core Questions

Before choosing a structure, identify:

1. Whether the data needs indexed access, ordered traversal, key lookup, or
   relationship traversal.
2. Whether insertion and deletion occur mainly at an end, in the middle, or by
   key.
3. Whether ordering must be preserved, sorted, or is unnecessary.
4. Whether the workload is read-heavy, write-heavy, or needs fast minimum or
   maximum retrieval.

## Common Trade-offs

| Structure | Strength | Typical operation cost |
| --- | --- | --- |
| Array / dynamic array | Fast indexed access | Access `O(1)`; middle insertion or deletion `O(n)` |
| Linked list | Local insertion and deletion | Access `O(n)`; insertion or deletion with a node reference `O(1)` |
| Hash table | Key-based lookup | Average lookup, insert, and delete `O(1)` |
| Stack / queue | Last-in-first-out or first-in-first-out processing | Insert and remove at an end `O(1)` |
| Heap | Repeated minimum or maximum retrieval | Peek `O(1)`; insert and remove extremum `O(log n)` |
| Balanced binary search tree | Ordered keys and range queries | Search, insert, and delete `O(log n)` |
| Trie | Prefix lookup over strings | Proportional to key length |
| Union-find | Dynamic disjoint-set membership | Near-constant amortized union and find |
| Graph representation | Relationships between entities | Depends on adjacency-list or adjacency-matrix representation |

## Notes in This Section

- [Arrays and Linked Lists](01-arrays-and-linked-lists.md)
- [Stacks and Queues](02-stacks-and-queues.md)
- [Hash Tables](03-hash-tables.md)
- [Heaps and Priority Queues](04-heaps-and-priority-queues.md)
- [Trees and Tries](05-trees-and-tries.md)
- [Union-Find](06-union-find.md)
- [Graphs: Concepts and Representations](07-graphs.md)

## Suggested Learning Order

Start with arrays, linked lists, stacks, queues, and hash tables. Next learn
heaps and trees, then union-find and graph representations. The algorithm
techniques and graph-algorithms sections build on those foundations.
