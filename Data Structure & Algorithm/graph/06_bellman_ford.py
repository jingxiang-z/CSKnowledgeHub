"""
Algorithm
=====================
Subproblem:
Let T(k, v) be the shortest path from s to v using at most k edges, for 0 <= k <= n-1,
where n is the number of vertices.

Recurrence:
- T(0, s) = 0
- T(0, v) = inf, for v in graph and v is not s
- T(k, v) = min(T(k-1, v), min over (u,v) in E of T(k-1, u) + w(u, v))

Correctness
=====================
Correct when there are no negative-weight cycles. Any simple shortest path visits at most
n-1 edges, so T(n-1, v) gives the correct distance for all reachable vertices. A negative
cycle is detectable if any distance improves on an nth iteration.

Runtime
=====================
O(V * E): there are n-1 iterations, and each iteration relaxes all E edges.
"""

def bellman_ford(graph, start, weights):
    # Input:
    # - graph: a simple graph in adjacency list format
    # - start: starting vertex
    # - weights: edge weights
    #
    # Output:
    # - dist: weighted distance from start to every vertex
    #   Unreachable vertices have distance inf.
    #   Values are based on the n - 1th iteration.
    # - prev: parent of each vertex on a shortest path
    #   Unreachable vertices and the starting vertex have parent nil.
    # - iter: iter[i][v] is the shortest-path distance from the starting
    #   vertex to v at the end of iteration i.
    #   This table contains iterations 0 through n-1.
    dist = {}
    prev = {}

    for vertex, neighbors in graph.items():
        dist[vertex] = float('inf')
        prev[vertex] = None
        for neighbor in neighbors:
            if neighbor not in dist:
                dist[neighbor] = float('inf')
                prev[neighbor] = None

    dist[start] = 0

    n = len(dist)
    iter = [{v: dist[v] for v in dist}]

    for i in range(1, n):
        prev_dist = iter[i - 1]
        for u, neighbors in graph.items():
            for v in neighbors:
                if prev_dist[u] + weights[(u, v)] < dist[v]:
                    dist[v] = prev_dist[u] + weights[(u, v)]
                    prev[v] = u
        iter.append({v: dist[v] for v in dist})

    return dist, prev, iter


def test_simple_weighted_path():
    # Linear chain: A -> B -> C -> D with total distance 6 from A to D.
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["D"],
        "D": [],
    }
    weights = {
        ("A", "B"): 1,
        ("B", "C"): 2,
        ("C", "D"): 3,
    }

    dist, prev, _ = bellman_ford(graph, "A", weights)

    assert dist == {"A": 0, "B": 1, "C": 3, "D": 6}
    assert prev == {"A": None, "B": "A", "C": "B", "D": "C"}


def test_negative_edge_weight():
    # A -> B costs 4, but A -> C -> B costs 1 + (-2) = -1.
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

    dist, prev, _ = bellman_ford(graph, "A", weights)

    assert dist["B"] == -1
    assert prev["B"] == "C"
    assert dist["D"] == 0


def test_disconnected_graph():
    # Vertices C and D are unreachable from A.
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

    dist, prev, _ = bellman_ford(graph, "A", weights)

    assert dist["A"] == 0
    assert dist["B"] == 4
    assert dist["C"] == float("inf")
    assert dist["D"] == float("inf")
    assert prev["A"] is None
    assert prev["C"] is None
    assert prev["D"] is None


def test_iter_table():
    # After iteration 0, only A is settled. After iteration 1, B is settled.
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }
    weights = {
        ("A", "B"): 2,
        ("B", "C"): 3,
    }

    _, _, itr = bellman_ford(graph, "A", weights)

    assert itr[0] == {"A": 0, "B": float("inf"), "C": float("inf")}
    assert itr[1] == {"A": 0, "B": 2, "C": float("inf")}
    assert itr[2] == {"A": 0, "B": 2, "C": 5}


if __name__ == "__main__":
    test_simple_weighted_path()
    test_negative_edge_weight()
    test_disconnected_graph()
    test_iter_table()
    print("All tests passed.")
