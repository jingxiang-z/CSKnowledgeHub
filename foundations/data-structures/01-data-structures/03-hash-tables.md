# Hash Tables

A hash table maps keys to values. A hash function selects a bucket for each
key; collisions occur when distinct keys select the same bucket. They are
expected and must be handled by the implementation.

Separate chaining stores a small collection in each bucket. Open addressing
stores entries directly in the table and probes alternative positions. Both
approaches resize when the load factor becomes too high.

| Operation | Expected | Worst case |
| --- | --- | --- |
| lookup | `O(1)` | `O(n)` |
| insert / update | `O(1)` | `O(n)` |
| delete | `O(1)` | `O(n)` |

The expected bounds rely on a well-distributed hash function and a bounded
load factor. Hash tables are excellent for membership, frequency counting, and
key lookup, but they do not provide sorted traversal or efficient range
queries.

```python
counts = {}
for value in values:
    counts[value] = counts.get(value, 0) + 1
```

In Python, dictionary keys must be hashable: mutable containers such as lists
cannot be keys, while tuples of hashable values can.
