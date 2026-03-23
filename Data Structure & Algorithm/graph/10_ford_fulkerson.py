"""
Algorithm
=====================
- Initialize a residual graph with the same vertices and edges as the original graph,
  where each edge's residual capacity equals its original capacity.
- Find an augmenting path from source s to sink t in the residual graph using BFS or DFS.
- Identify the bottleneck: the minimum residual capacity along the augmenting path.
- Augment flow along the path by the bottleneck value:
    - For each forward edge (u→v) on the path, decrease its residual capacity by the bottleneck.
    - For each corresponding backward edge (v→u), increase its residual capacity by the bottleneck
      (adding the backward edge if it does not already exist). This allows previously committed
      flow to be "undone" in future iterations.
- Repeat until no augmenting path from s to t exists in the residual graph.
- The total flow pushed is the maximum flow value.
- To find the minimum s-t cut: in the final residual graph, let S be the set of vertices
  reachable from s. The cut consists of all original edges crossing from S to V\S;
  by the Max-Flow Min-Cut theorem, this cut's capacity equals the maximum flow.

Correctness
=====================
Correctness follows from the Max-Flow Min-Cut theorem: in any flow network, the value of the
maximum flow from s to t equals the capacity of the minimum s-t cut. The algorithm terminates
with a valid maximum flow because:
  1. Each augmentation strictly increases total flow (bottleneck > 0 on any simple path).
  2. For integer capacities, flow increases by at least 1 per iteration, so the algorithm
     terminates in at most |f*| iterations (where |f*| is the max flow value).
  3. When no augmenting path exists, the reachability partition gives a cut whose capacity
     equals the current flow, certifying optimality.

Runtime
=====================
O(m * C), where the C is the value of the maximum flow from the starting vertex to the terminating vertex.
"""


def ford_fulkerson(graph, capacities, source, sink):
    # Input:
    # - graph: a simple, connected, directed graph in adjacency list format
    # - capacities: dict mapping (u, v) -> capacity for each edge
    # - source: source vertex
    # - sink: sink vertex
    #
    # Output:
    # - flow: dict mapping (u, v) -> flow on each original edge
    # - C: the value of the maximum flow from source to sink

    # Build residual graph: residual[u][v] = remaining capacity
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors)

    residual = {v: {} for v in vertices}
    for (u, v), cap in capacities.items():
        residual[u][v] = residual[u].get(v, 0) + cap
        if v not in residual:
            residual[v] = {}
        if u not in residual[v]:
            residual[v][u] = 0

    def bfs_find_path():
        """Return parent dict representing an augmenting path, or None if none exists."""
        visited = {source}
        parent = {source: None}
        queue = [source]
        while queue:
            u = queue.pop(0)
            for v, cap in residual[u].items():
                if v not in visited and cap > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return parent
                    queue.append(v)
        return None

    C = 0
    while True:
        parent = bfs_find_path()
        if parent is None:
            break

        # Find bottleneck along the augmenting path
        bottleneck = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, residual[u][v])
            v = u

        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] = residual[v].get(u, 0) + bottleneck
            v = u

        C += bottleneck

    # Recover per-edge flow from residual graph (flow on edge = capacity - remaining residual)
    flow = {}
    for (u, v), cap in capacities.items():
        flow[(u, v)] = cap - residual[u].get(v, 0)

    return flow, C


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

def test_simple_two_paths():
    """Two parallel paths share capacity at the source."""
    #
    #   s --10--> a --10--> t
    #   s --10--> b --10--> t
    #
    # Max flow = 20 (both paths fully used)
    graph = {'s': ['a', 'b'], 'a': ['t'], 'b': ['t'], 't': []}
    capacities = {('s', 'a'): 10, ('a', 't'): 10, ('s', 'b'): 10, ('b', 't'): 10}
    flow, C = ford_fulkerson(graph, capacities, 's', 't')
    assert C == 20, f"Expected 20, got {C}"
    assert flow[('s', 'a')] == 10
    assert flow[('s', 'b')] == 10
    print("test_simple_two_paths passed")


def test_bottleneck_edge():
    """A single bottleneck edge limits the max flow."""
    #
    #   s --10--> a --1--> b --10--> t
    #
    # Max flow = 1 (bottleneck at a->b)
    graph = {'s': ['a'], 'a': ['b'], 'b': ['t'], 't': []}
    capacities = {('s', 'a'): 10, ('a', 'b'): 1, ('b', 't'): 10}
    flow, C = ford_fulkerson(graph, capacities, 's', 't')
    assert C == 1, f"Expected 1, got {C}"
    print("test_bottleneck_edge passed")


def test_backward_edge_needed():
    """Requires the backward edge (flow cancellation) to find the true max flow."""
    #
    #        3
    #   s -------> a
    #   |          |  \
    #   3          3    3
    #   |          |      \
    #   v    3     v        v
    #   b -------> c -----> t
    #                  3
    #
    # Classic example where a greedy DFS might route s->a->c->t and s->b->c (stuck),
    # but the correct max flow of 6 requires cancelling flow through c.
    graph = {
        's': ['a', 'b'],
        'a': ['b', 't'],
        'b': ['c'],
        'c': ['t'],
        't': []
    }
    capacities = {
        ('s', 'a'): 3,
        ('s', 'b'): 3,
        ('a', 'b'): 3,
        ('a', 't'): 3,
        ('b', 'c'): 3,
        ('c', 't'): 3,
    }
    flow, C = ford_fulkerson(graph, capacities, 's', 't')
    assert C == 6, f"Expected 6, got {C}"
    print("test_backward_edge_needed passed")


if __name__ == "__main__":
    test_simple_two_paths()
    test_bottleneck_edge()
    test_backward_edge_needed()
    print("All tests passed.")
