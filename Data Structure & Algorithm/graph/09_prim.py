"""
Algorithm
=====================
- Initialize a min-heap and a visited set
- Pick an arbitrary starting vertex, mark it visited, and push all its edges
  (weight, neighbor, current) onto the heap
- While the heap is non-empty:
    - Pop the minimum-weight edge (w, v, u) where u is already visited
    - If v is already visited, skip it (would form a cycle)
    - Otherwise, mark v visited, record prev[v] = u, and push all edges
      from v to unvisited neighbors onto the heap
- Stop once all vertices are visited (n-1 edges added)

Correctness
=====================
- By the Cut Property, at each step the lightest edge crossing the cut
  (visited S, unvisited V-S) must belong to some MST. Prim's always picks
  that edge, guaranteeing the result is a valid MST.

Runtime
=====================
- Each vertex is visited once and each edge is pushed/popped from the heap at most twice
- Heap operations: O(m log m) = O(m log n)
- Overall: O(m log n)
"""

import heapq

def prim(graph, weights):
    # Input:
    # - graph: a simple, connected, undirected graph in adjacency list format
    # - weights: a dict mapping (u, v) with u < v to edge weight
    #
    # Output:
    # - prev: parent of each vertex in the minimum spanning tree
    #   The starting vertex is chosen arbitrarily and has parent None.
    start = next(iter(graph))
    visited = {start}
    prev = {start: None}

    # Heap entries: (weight, neighbor, current)
    heap = []
    for v in graph[start]:
        edge = (start, v) if start < v else (v, start)
        heapq.heappush(heap, (weights[edge], v, start))

    while heap:
        w, v, u = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        prev[v] = u
        for neighbor in graph[v]:
            if neighbor not in visited:
                edge = (v, neighbor) if v < neighbor else (neighbor, v)
                heapq.heappush(heap, (weights[edge], neighbor, v))

    return prev


if __name__ == "__main__":
    # Test 1: Simple triangle
    #
    #   0 --1-- 1
    #    \     /
    #     4   2
    #      \ /
    #       2
    #
    # MST edges: (0,1)=1, (1,2)=2  →  prev = {0: None, 1: 0, 2: 1}
    graph1 = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    weights1 = {(0, 1): 1, (0, 2): 4, (1, 2): 2}
    prev1 = prim(graph1, weights1)
    assert prev1 == {0: None, 1: 0, 2: 1}, f"Test 1 failed: {prev1}"
    print("Test 1 passed:", prev1)

    # Test 2: Linear chain — only one spanning tree
    #
    #   0 --3-- 1 --1-- 2 --4-- 3
    #
    # prev = {0: None, 1: 0, 2: 1, 3: 2}
    graph2 = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    weights2 = {(0, 1): 3, (1, 2): 1, (2, 3): 4}
    prev2 = prim(graph2, weights2)
    assert prev2 == {0: None, 1: 0, 2: 1, 3: 2}, f"Test 2 failed: {prev2}"
    print("Test 2 passed:", prev2)

    # Test 3: Dense 4-node graph
    #
    # Edges: (0,1)=1, (0,2)=4, (0,3)=7, (1,2)=6, (1,3)=3, (2,3)=5
    # MST: (0,1)=1, (1,3)=3, (0,2)=4  →  prev = {0: None, 1: 0, 3: 1, 2: 0}
    graph3 = {0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}
    weights3 = {(0, 1): 1, (0, 2): 4, (0, 3): 7, (1, 2): 6, (1, 3): 3, (2, 3): 5}
    prev3 = prim(graph3, weights3)
    assert prev3 == {0: None, 1: 0, 3: 1, 2: 0}, f"Test 3 failed: {prev3}"
    print("Test 3 passed:", prev3)
