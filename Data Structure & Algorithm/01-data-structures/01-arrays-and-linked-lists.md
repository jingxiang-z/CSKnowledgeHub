# Arrays and Linked Lists

Arrays store elements in contiguous positions, so indexing is `O(1)`. A dynamic
array grows by allocating a larger backing store and copying values; append is
therefore amortized `O(1)`, while inserting or deleting in the middle is
`O(n)`.

A linked list stores each value in a separate node connected by references.
It does not support fast indexing: reaching position `i` costs `O(i)`.
However, inserting or removing a node is `O(1)` when the relevant node and,
for a singly linked list, its predecessor are already known.

| Need | Prefer |
| --- | --- |
| indexed reads and compact storage | array / dynamic array |
| frequent append and random access | dynamic array |
| queue operations at both ends | deque |
| insert or remove near a known node | linked list |

In Python, `list` is a dynamic array. Use `collections.deque` rather than a
list when removing frequently from the front.
