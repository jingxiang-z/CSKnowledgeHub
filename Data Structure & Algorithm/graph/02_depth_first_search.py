"""
Algorithm
=====================
DFS consists of two mutually recursive procedures:

explore(v):
- Mark v as visited; record pre[v] = clock++
- Assign ccnum[v] to the current connected component counter
- For each neighbor u of v:
    - If u has not been visited: set prev[u] = v, then call explore(u)
- Record post[v] = clock++

depth_first_search(graph):
- Initialize visited, ccnum, prev, pre, post, and clock
- For each vertex v in graph:
    - If v has not been visited: increment component counter, call explore(v)


Correctness
=====================
Every vertex reachable from a given starting vertex is guaranteed to be visited:
explore(v) recurses into every unvisited neighbor before returning, so no
reachable vertex is skipped. Because a vertex is marked visited before
recursing, each vertex and each edge is processed at most once, ensuring
termination and preventing infinite loops on cycles.


Runtime
=====================
DFS iterates over every vertex and edge in the graph exactly once,
so the time complexity is O(V + E) where V = number of vertices and E = number of edges.
"""


def depth_first_search(graph, start=None):
    # Input:
    # - graph: a simple graph in adjacency list format
    # - start: optional starting vertex
    #   If not provided, DFS runs over all vertices in adjacency list order,
    #   visiting each unvisited vertex as a new component root.
    #
    # Internal:
    # - visited: set of vertices already reached by explore()
    # - clock: mutable counter (list of one int) shared across all explore() calls
    # - component: mutable counter (list of one int) incremented per component root
    #
    # Output:
    # - ccnum: connected component number for each vertex (1-indexed)
    # - prev: parent of each vertex in the DFS forest; root vertices map to None
    # - pre: pre-visit clock value for each vertex
    # - post: post-visit clock value for each vertex
    visited = set()
    ccnum = {}
    prev = {}
    pre, post = {}, {}
    clock = 1
    component = 0

    def explore(v):
        nonlocal clock, component
        visited.add(v)
        pre[v] = clock
        clock += 1
        ccnum[v] = component
        for neighbor in graph[v]:
            if neighbor not in visited:
                prev[neighbor] = v
                explore(neighbor)
        post[v] = clock
        clock += 1

    if start is None:
        vertices = list(graph)
    elif isinstance(start, list):
        vertices = start
    else:
        vertices = [start]
    for v in vertices:
        if v not in visited:
            component += 1
            prev[v] = None
            explore(v)

    return ccnum, prev, pre, post


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

def test_simple_path():
    # Linear chain: 0 - 1 - 2 - 3
    # DFS from 0 visits all vertices in a straight line, so pre/post
    # timestamps nest perfectly: pre[0] < pre[1] < pre[2] < pre[3]
    # and post[3] < post[2] < post[1] < post[0].
    graph = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    ccnum, prev, pre, post = depth_first_search(graph, start=0)
    assert ccnum == {0: 1, 1: 1, 2: 1, 3: 1}
    assert prev == {0: None, 1: 0, 2: 1, 3: 2}
    assert pre[0] < pre[1] < pre[2] < pre[3]
    assert post[3] < post[2] < post[1] < post[0]


def test_disconnected_graph():
    # Two separate components: {0, 1} and {2, 3}
    # DFS with no start must visit all vertices and assign different
    # component numbers to each pair.
    graph = {0: [1], 1: [0], 2: [3], 3: [2]}
    ccnum, prev, pre, post = depth_first_search(graph)
    assert ccnum[0] == ccnum[1]          # same component
    assert ccnum[2] == ccnum[3]          # same component
    assert ccnum[0] != ccnum[2]          # different components
    assert prev[0] is None               # root of component 1
    assert prev[2] is None               # root of component 2
    assert prev[1] == 0
    assert prev[3] == 2


def test_cycle_does_not_revisit():
    # Triangle: 0 - 1 - 2 - 0
    # DFS must terminate (no infinite loop) and visit each vertex exactly once.
    # The pre/post intervals of 1 and 2 must be nested inside 0's interval,
    # confirming they are descendants of 0 in the DFS tree.
    graph = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    ccnum, prev, pre, post = depth_first_search(graph, start=0)
    assert ccnum == {0: 1, 1: 1, 2: 1}
    assert prev[0] is None
    assert pre[0] < pre[1] and post[1] < post[0]   # 1 nested inside 0
    assert pre[0] < pre[2] and post[2] < post[0]   # 2 nested inside 0


if __name__ == "__main__":
    test_simple_path()
    test_disconnected_graph()
    test_cycle_does_not_revisit()
    print("All tests passed.")
