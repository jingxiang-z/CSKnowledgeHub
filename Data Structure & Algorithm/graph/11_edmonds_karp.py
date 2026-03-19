"""
Algorithm
=====================
- Build a residual graph from the original graph, where each directed edge (u, v)
  with capacity c gets a forward residual edge with capacity c and a backward
  residual edge with capacity 0
- Repeat until no augmenting path exists:
    - Use BFS to find the shortest augmenting path (fewest edges) from source to
      sink in the residual graph
    - If no path is found, stop — the maximum flow has been reached
    - Find the bottleneck: the minimum residual capacity along the path
    - Update the residual graph along the path: decrease each forward edge's
      residual capacity by the bottleneck, and increase each reverse edge's
      residual capacity by the bottleneck
- The sum of all bottleneck values sent is the maximum flow value

Correctness
=====================
By the Max-flow Min-cut theorem, a flow is maximum if and only if there is no
augmenting path in the residual graph. Edmonds-Karp is an implementation of
Ford-Fulkerson that uses BFS to always find the shortest augmenting path. This
guarantees termination and correctness because:
- Each augmentation either saturates at least one edge or increases the shortest
  path length from source to sink, both of which can only happen O(VE) times
- When BFS finds no path, the flow is provably maximum

Runtime
=====================
O(VE^2), where V = number of vertices, E = number of edges
- Each BFS traversal takes O(E)
- The number of augmenting path iterations is at most O(VE), because the
  shortest path length is non-decreasing and each edge can become a bottleneck
  (critical edge) at most O(V) times before the path length must increase
- Total: O(VE) iterations × O(E) per BFS = O(VE^2)
"""

from collections import deque

def edmonds_karp(graph, capacities, source, sink):
    # Input:
    # - graph: a simple, connected, directed graph in adjacency list format
    #          {vertex: [neighbor, ...]}
    # - capacities: dict of (u, v) -> positive integer capacity
    # - source: source vertex
    # - sink: sink vertex
    #
    # Output:
    # - flow: dict of (u, v) -> flow used on each original edge
    # - C: the value of the maximum flow from source to sink

    # Residual adjacency list: {u: {v: residual_capacity}}
    # Forward edges get the original capacity; backward edges start at 0
    residual = {}
    for (u, v), cap in capacities.items():
        residual.setdefault(u, {})[v] = cap
        residual.setdefault(v, {}).setdefault(u, 0)

    C = 0

    while True:
        # BFS: find the shortest augmenting path from source to sink
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, cap in residual.get(u, {}).items():
                if v not in parent and cap > 0:
                    parent[v] = u
                    queue.append(v)

        if sink not in parent:
            break

        # Find the bottleneck (minimum residual capacity along the path)
        bottleneck = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, residual[u][v])
            v = u

        # Update residual graph along the path
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] = residual[v].get(u, 0) + bottleneck
            v = u

        C += bottleneck

    # Flow on each original edge = original capacity minus remaining residual
    flow = {(u, v): cap - residual[u][v] for (u, v), cap in capacities.items()}
    return flow, C


if __name__ == "__main__":
    # Test 1: Two parallel paths, each with equal capacity
    # 0 --10--> 1 --10--> 3
    # 0 --10--> 2 --10--> 3
    # Expected max flow: 20
    graph1 = {0: [1, 2], 1: [3], 2: [3], 3: []}
    caps1  = {(0,1): 10, (0,2): 10, (1,3): 10, (2,3): 10}
    flow1, C1 = edmonds_karp(graph1, caps1, source=0, sink=3)
    print(f"Test 1 — Max flow: {C1} (expected 20)")
    print(f"         Edge flows: {flow1}\n")

    # Test 2: Classic bottleneck example
    # 0 --3--> 1 --2--> 3
    #  \      / \
    #  2->  1   -> 3 (cap 2, from 1->3 directly)
    #    -> 2 --3-> 3
    # Edges: 0->1(3), 0->2(2), 1->2(1), 1->3(2), 2->3(3)
    # Expected max flow: 5
    graph2 = {0: [1, 2], 1: [2, 3], 2: [3], 3: []}
    caps2  = {(0,1): 3, (0,2): 2, (1,2): 1, (1,3): 2, (2,3): 3}
    flow2, C2 = edmonds_karp(graph2, caps2, source=0, sink=3)
    print(f"Test 2 — Max flow: {C2} (expected 5)")
    print(f"         Edge flows: {flow2}\n")

    # Test 3: Single path with a tight bottleneck in the middle
    # 0 --8--> 1 --3--> 2 --7--> 3
    # Expected max flow: 3 (limited by the middle edge)
    graph3 = {0: [1], 1: [2], 2: [3], 3: []}
    caps3  = {(0,1): 8, (1,2): 3, (2,3): 7}
    flow3, C3 = edmonds_karp(graph3, caps3, source=0, sink=3)
    print(f"Test 3 — Max flow: {C3} (expected 3)")
    print(f"         Edge flows: {flow3}")
