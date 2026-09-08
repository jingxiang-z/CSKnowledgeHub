# Union-Find

Union-find, also called disjoint-set union (DSU), maintains a collection of
non-overlapping groups. It supports two operations:

- `find(x)`: return the representative of the group containing `x`.
- `union(x, y)`: merge the groups containing `x` and `y`.

With path compression and union by size or rank, a sequence of operations costs
amortized `O(α(n))` per operation, where `α` grows so slowly that it is
effectively constant for practical input sizes.

```python
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, left, right):
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True
```

Use union-find for dynamic connectivity, connected-component counting, and
cycle detection in undirected graphs. It cannot efficiently remove an edge or
split a set.
