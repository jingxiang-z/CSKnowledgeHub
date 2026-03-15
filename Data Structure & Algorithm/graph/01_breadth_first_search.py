"""
Algorithm
=====================
- Initialize an empty queue and an empty visited set
- Mark the start vertex as visited, enqueue it
- Repeat until the queue is empty:
    - Dequeue a vertex
    - Visit all its neighbors; enqueue those not yet in the visited set and mark them visited


Correctness
=====================
BFS always visits vertices in non-decreasing order of their distance from the start vertex,
guaranteeing that the first time a vertex is reached it is via a shortest (unweighted) path.


Runtime
=====================
BFS iterates over every vertex and edge in the graph exactly once,
so the time complexity is O(V + E) where V = number of vertices and E = number of edges.
"""
from collections import deque

def breadth_first_search(graph, start):
    # Input:
    # - graph: a simple graph in adjacency list format
    # - start: starting vertex
    #
    # Output:
    # - dist: unweighted distance from start to every vertex
    #   Unreachable vertices have distance inf.
    # - prev: parent of each vertex in the BFS tree
    #   Unreachable vertices and the starting vertex have parent nil.
    dist, prev = {}, {}
    queue = deque()
    visited = set()
    visited.add(start)
    queue.append(start)
    dist[start] = 0
    prev[start] = None
    while queue:
        v = queue.popleft()
        for neighbor in graph[v]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                dist[neighbor] = dist[v] + 1
                prev[neighbor] = v
    return dist, prev


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

def test_simple_path():
    # Linear chain: 0 - 1 - 2 - 3
    # BFS from 0 should assign distances 0, 1, 2, 3 in order.
    graph = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    dist, prev = breadth_first_search(graph, 0)
    assert dist == {0: 0, 1: 1, 2: 2, 3: 3}
    assert prev == {0: None, 1: 0, 2: 1, 3: 2}


def test_shortest_path_with_shortcut():
    # Graph with two paths from 0 to 3:
    #   long path:  0 -> 1 -> 2 -> 3  (length 3)
    #   shortcut:   0 -> 3             (length 1)
    # BFS must find the shorter path.
    graph = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
    dist, prev = breadth_first_search(graph, 0)
    assert dist[3] == 1
    assert prev[3] == 0


def test_disconnected_graph():
    # Two separate components: {0, 1} and {2, 3}
    # BFS from 0 should only reach 0 and 1; 2 and 3 are unreachable.
    graph = {0: [1], 1: [0], 2: [3], 3: [2]}
    dist, prev = breadth_first_search(graph, 0)
    assert dist == {0: 0, 1: 1}
    assert 2 not in dist and 3 not in dist


if __name__ == "__main__":
    test_simple_path()
    test_shortest_path_with_shortcut()
    test_disconnected_graph()
    print("All tests passed.")
