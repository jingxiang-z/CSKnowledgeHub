"""
Algorithm
=====================
Subproblem:
Let T(k, u, v) be the shortest path from u to v whose intermediate vertices are
drawn from {1, ..., k}, for 0 <= k <= n, where vertices are labeled 1 to n.

Recurrence:
- T(0, u, v) = w(u, v) if (u, v) in E, else inf
- T(0, u, u) = 0 for all u
- T(k, u, v) = min(T(k-1, u, v), T(k-1, u, k) + T(k-1, k, v))

Correctness
=====================
Correct when there are no negative-weight cycles. After considering all n vertices
as potential intermediates, T(n, u, v) holds the true shortest-path distance for
every pair (u, v). A negative cycle is detectable if any diagonal entry dist[v][v]
is negative after the algorithm completes.

Runtime
=====================
O(V^3): three nested loops each over all n vertices.
"""

def floyd_warshall(graph, weights):
    # Input:
    # - graph: a simple graph in adjacency list format
    # - weights: edge weights
    #
    # Output:
    # - dist: all-pairs shortest-path distances
    #   dist[u][v] is the shortest-path distance from u to v.
    #   Unreachable vertex pairs have distance inf.
    #   Values are based on the nth iteration.
    # - iter: iter[i][u][v] is the distance from u to v at the end of
    #   iteration i.
    #   This table contains iterations 0 through n.
    vertices = set()
    for u, neighbors in graph.items():
        vertices.add(u)
        for v in neighbors:
            vertices.add(v)
    vertices = list(vertices)

    dist = {u: {v: float('inf') for v in vertices} for u in vertices}
    for u in vertices:
        dist[u][u] = 0
    for u, neighbors in graph.items():
        for v in neighbors:
            dist[u][v] = weights[(u, v)]

    iter = [{u: dict(dist[u]) for u in vertices}]

    for k in vertices:
        for u in vertices:
            for v in vertices:
                if dist[u][k] + dist[k][v] < dist[u][v]:
                    dist[u][v] = dist[u][k] + dist[k][v]
        iter.append({u: dict(dist[u]) for u in vertices})

    return dist, iter


def test_simple_weighted_path():
    # Linear chain: A -> B -> C, shortest path A -> C is 3.
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }
    weights = {
        ("A", "B"): 1,
        ("B", "C"): 2,
    }

    dist, _ = floyd_warshall(graph, weights)

    assert dist["A"]["A"] == 0
    assert dist["A"]["B"] == 1
    assert dist["A"]["C"] == 3
    assert dist["B"]["C"] == 2
    assert dist["B"]["A"] == float("inf")
    assert dist["C"]["A"] == float("inf")


def test_negative_edge_weight():
    # A -> C -> B costs 1 + (-2) = -1, cheaper than A -> B directly at 4.
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["B"],
        "D": [],
    }
    weights = {
        ("A", "B"): 4,
        ("A", "C"): 1,
        ("C", "B"): -2,
        ("B", "D"): 1,
    }

    dist, _ = floyd_warshall(graph, weights)

    assert dist["A"]["B"] == -1
    assert dist["A"]["D"] == 0


def test_disconnected_graph():
    # C and D are unreachable from A and B.
    graph = {
        "A": ["B"],
        "B": [],
        "C": ["D"],
        "D": [],
    }
    weights = {
        ("A", "B"): 4,
        ("C", "D"): 1,
    }

    dist, _ = floyd_warshall(graph, weights)

    assert dist["A"]["B"] == 4
    assert dist["A"]["C"] == float("inf")
    assert dist["A"]["D"] == float("inf")
    assert dist["C"]["D"] == 1
    assert dist["C"]["A"] == float("inf")


if __name__ == "__main__":
    test_simple_weighted_path()
    test_negative_edge_weight()
    test_disconnected_graph()
    print("All tests passed.")
