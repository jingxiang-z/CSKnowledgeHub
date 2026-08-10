"""
Algorithm
=====================
- Initialize every vertex with distance `inf`, except the start vertex with distance `0`
- Push the start vertex into a min-heap keyed by tentative distance
- Repeat until the heap is empty:
    - Pop the vertex with the smallest tentative distance
    - If it was already finalized, skip it
    - Relax each outgoing edge by updating a neighbor's distance and parent when a shorter path is found
    - Push improved neighbors back into the heap

Correctness
=====================
Because all edge weights are non-negative, the first time a vertex is removed from the
min-heap with minimum tentative distance, that distance is final and equals the true
shortest-path distance from the start vertex. Repeating this argument for each extracted
vertex shows that Dijkstra's algorithm correctly computes shortest-path distances and a
shortest-path tree for every reachable vertex.

Runtime
=====================
Using an adjacency list and a min-heap, each edge relaxation may trigger a heap push and
each heap operation costs O(log V). Therefore, the total running time is
O((V + E) log V), where V is the number of vertices and E is the number of edges.
"""
import heapq

def dijkstra(graph, start, weights):
    # Input:
    # - graph: a simple graph in adjacency list format
    # - start: starting vertex
    # - weights: non-negative edge weights
    #
    # Output:
    # - dist: weighted distance from start to every vertex
    #   Unreachable vertices have distance inf.
    # - prev: parent of each vertex on the shortest-path tree
    #   Unreachable vertices and the starting vertex have parent nil.
    dist = {}
    prev = {}

    for vertex, neighbors in graph.items():
        dist[vertex] = float('inf')
        prev[vertex] = None
        for neighbor in neighbors:
            if neighbor not in dist:
                dist[neighbor] = float('inf')
                prev[neighbor] = None

    if start not in dist:
        dist[start] = 0
        prev[start] = None
    else:
        dist[start] = 0

    heap = [(0, start)]
    while heap:
        distance, v = heapq.heappop(heap)
        if distance != dist[v]:
            continue

        for neighbor in graph.get(v, []):
            new_distance = dist[v] + weights[(v, neighbor)]
            if dist[neighbor] > new_distance:
                dist[neighbor] = new_distance
                prev[neighbor] = v
                heapq.heappush(heap, (new_distance, neighbor))

    return dist, prev


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

    dist, prev = dijkstra(graph, "A", weights)

    assert dist == {"A": 0, "B": 1, "C": 3, "D": 6}
    assert prev == {"A": None, "B": "A", "C": "B", "D": "C"}


def test_prefers_cheaper_indirect_path():
    # The direct edge A -> B costs 10, but A -> C -> B costs only 2.
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["B", "D"],
        "D": [],
    }
    weights = {
        ("A", "B"): 10,
        ("A", "C"): 1,
        ("C", "B"): 1,
        ("B", "D"): 1,
        ("C", "D"): 5,
    }

    dist, prev = dijkstra(graph, "A", weights)

    assert dist["B"] == 2
    assert prev["B"] == "C"
    assert dist["D"] == 3
    assert prev["D"] == "B"


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

    dist, prev = dijkstra(graph, "A", weights)

    assert dist["A"] == 0
    assert dist["B"] == 4
    assert dist["C"] == float("inf")
    assert dist["D"] == float("inf")
    assert prev["A"] is None
    assert prev["B"] == "A"
    assert prev["C"] is None
    assert prev["D"] is None


if __name__ == "__main__":
    test_simple_weighted_path()
    test_prefers_cheaper_indirect_path()
    test_disconnected_graph()
    print("All tests passed.")

