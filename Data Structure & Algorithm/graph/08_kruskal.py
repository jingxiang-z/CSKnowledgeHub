"""
Algorithm
=====================
- Sort all edges by weight in non-decreasing order
- Initialize a Union-Find data structure with each vertex as its own component
- Iterate through the sorted edges; for each edge (u, v):
    - If u and v are already in the same component, skip the edge (would form a cycle)
    - Otherwise, union the two components and add the edge to the MST
- Stop once n-1 edges have been added to the MST

Correctness
=====================
- By the Cut Property, the minimum-weight edge crossing any cut of the graph
  must belong to some MST. Kruskal's greedily picks the lightest edge that
  doesn't form a cycle, which always satisfies this property — guaranteeing
  the result is a valid MST.
- A spanning tree of a connected graph with n vertices always has exactly n-1 edges.

Runtime
=====================
- Sorting edges:         O(m log m) = O(m log n), since m ≤ n² so log m ≤ 2 log n
- Union-Find operations: O(m · α(n)) ≈ O(m),  α is the inverse Ackermann function
- Overall:              O(m log n)
"""

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
                self.root[rootx] = rooty
            elif self.rank[rootx] > self.rank[rooty]:
                self.root[rooty] = rootx
            else:
                self.root[rooty] = rootx
                self.rank[rootx] += 1
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)


def kruskal(graph, weights):
    # Input:
    # - graph: a simple, connected, undirected graph in adjacency list format
    # - weights: edge weights
    #
    # Output:
    # - edges: a list of n - 1 edges that represent a minimum spanning tree
    #   for the input graph
    # Collect all unique edges as (weight, u, v); skip duplicates for undirected graph
    all_edges = []
    for u, neighbors in graph.items():
        for v in neighbors:
            if u < v:
                all_edges.append((weights[(u, v)], u, v))
    all_edges.sort()

    n = len(graph)
    uf = UnionFind(n)
    mst = []

    for w, u, v in all_edges:
        if not uf.connected(u, v):
            uf.union(u, v)
            mst.append((u, v))
            if len(mst) == n - 1:
                break

    return mst


if __name__ == "__main__":
    # Test 1: Simple triangle — one edge is heavier and should be excluded
    #
    #   0 --1-- 1
    #    \     /
    #     4   2
    #      \ /
    #       2
    #
    # MST should pick edges (1,2)=2 and (0,1)=1, total weight = 3
    graph1 = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    weights1 = {(0, 1): 1, (0, 2): 4, (1, 2): 2}
    mst1 = kruskal(graph1, weights1)
    assert sorted(mst1) == [(0, 1), (1, 2)], f"Test 1 failed: {mst1}"
    print("Test 1 passed:", mst1)

    # Test 2: Linear chain — only one possible spanning tree
    #
    #   0 --3-- 1 --1-- 2 --4-- 3
    #
    # MST must include all 3 edges since it's the only spanning tree
    graph2 = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    weights2 = {(0, 1): 3, (1, 2): 1, (2, 3): 4}
    mst2 = kruskal(graph2, weights2)
    assert sorted(mst2) == [(0, 1), (1, 2), (2, 3)], f"Test 2 failed: {mst2}"
    print("Test 2 passed:", mst2)

    # Test 3: Denser graph — multiple candidate edges, must pick cheapest n-1
    #
    #   0 --1-- 1
    #   |  \ /  |
    #   4   X   3
    #   |  / \  |
    #   2 --5-- 3
    #
    # Edges: (0,1)=1, (0,2)=4, (0,3)=7, (1,2)=6, (1,3)=3, (2,3)=5
    # Sorted: 1,3,4,5,6,7 → pick (0,1)=1, (1,3)=3, (0,2)=4 → MST weight = 8
    graph3 = {0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}
    weights3 = {(0, 1): 1, (0, 2): 4, (0, 3): 7, (1, 2): 6, (1, 3): 3, (2, 3): 5}
    mst3 = kruskal(graph3, weights3)
    assert sorted(mst3) == [(0, 1), (0, 2), (1, 3)], f"Test 3 failed: {mst3}"
    print("Test 3 passed:", mst3)
