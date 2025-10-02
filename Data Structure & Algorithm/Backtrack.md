# Backtrack

## Introduction

1. **Incremental Approach**: Solutions are built one step at a time. After each step, the algorithm checks if the current partial solution can still lead to a valid complete solution.
2. **Testing for Validity**: At each step, the algorithm tests whether the current path taken leads to a potential solution. If it violates any constraints, the algorithm backtracks and tries a different path.
3. **Depth-First Search**: Backtracking typically uses a depth-first search approach, exploring one branch to its conclusion before backtracking and trying another.
4. **Pruning the Search Space**: An essential aspect of backtracking is pruning, where the algorithm eliminates paths that cannot possibly lead to a solution, thereby reducing the search space.

## Subset Problem

### Combination

```python
def combine(n, k):
    def backtrack(start, path):
        if len(path) == k:
            results.append(path[:])
            return
        for i in range(start, n+1):
            path.append(i)
            backtrack(i+1, path)
            path.pop()
    results = []
    backtrack(1, [])
    return results
```

### Permutation

```python
def permute(n, k):
    def backtrack(path):
        if len(path) == k:
            results.append(path[:])
            return
        for i in range(1, n+1):
            if i not in path:
                path.append(i)
                backtrack(path)
                path.pop()
    results = []
    backtrack(1, [])
    return results
```

### Subset Sum

```python
def subsetSub(arr, k):
    def backtrack(start, curr):
        if curr == k:
            return True
        elif curr > k or start >= len(arr):
            return False
        include = backtrack(start + 1, curr + arr[start])
        exclude = backtrack(start + 1, curr)
        return include or exclude
    return backtrack(0, 0)
```

## Game Solver