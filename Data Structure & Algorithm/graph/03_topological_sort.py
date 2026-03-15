"""
Algorithm
=====================
- Run depth-first search on the graph and record the post-visit order
- Reverse the post-visit order to obtain the topological sort order

Correctness
=====================
In a directed acyclic graph, if there is an edge from u to v, then the post-visit number of u
is guaranteed to be greater than the post-visit number of v.
Therefore, reversing the post-visit order is guaranteed to yield a valid topological ordering.

Runtime
=====================
DFS iterates over every vertex and edge in the graph exactly once,
so the time complexity is O(V + E) where V = number of vertices and E = number of edges.
"""


def topological_sort(graph):
    # Input:
    # - graph: a simple, directed, acyclic graph in adjacency list format
    #
    # Output:
    # - order: vertices in topological order from source to sink
    #   This output is indexed numerically rather than by vertex.
    # - all outputs from the run of depth_first_search() are also available
    #   to you: ccnum, prev, pre, and post.
    visited = set()
    ccnum = {}
    prev = {}
    pre, post = {}, {}
    clock = 1
    component = 0
    def explore(v):
        nonlocal clock, component
        pre[v] = clock
        clock += 1
        visited.add(v)
        ccnum[v] = component
        for neighbor in graph[v]:
            if neighbor not in visited:
                prev[neighbor] = v
                explore(neighbor)
        post[v] = clock
        clock += 1
    vertices = list(graph)
    for v in vertices:
        if v not in visited:
            component += 1
            explore(v)
    order = sorted(post.keys(), key=lambda k: post[k], reverse=True)
    return order


def is_valid_topological_order(graph, order):
    """Return True if order respects every directed edge in graph."""
    position = {v: i for i, v in enumerate(order)}
    for u in graph:
        for v in graph[u]:
            if position[u] >= position[v]:
                return False
    return True


if __name__ == "__main__":
    # Test 1: Simple linear chain  A → B → C → D
    # Only one valid topological order exists.
    graph1 = {
        "A": ["B"],
        "B": ["C"],
        "C": ["D"],
        "D": [],
    }
    order1 = topological_sort(graph1)
    assert order1 == ["A", "B", "C", "D"], f"Test 1 failed: {order1}"
    print("Test 1 passed:", order1)

    # Test 2: Diamond  A → B, A → C, B → D, C → D
    # Multiple valid orders exist; validate the edge constraint instead of
    # checking for one specific sequence.
    graph2 = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    order2 = topological_sort(graph2)
    assert is_valid_topological_order(graph2, order2), f"Test 2 failed: {order2}"
    assert order2[0] == "A" and order2[-1] == "D", f"Test 2 boundary failed: {order2}"
    print("Test 2 passed:", order2)

    # Test 3: Two disconnected chains  A → B  and  C → D → E
    # Validates that the algorithm handles multiple connected components.
    graph3 = {
        "A": ["B"],
        "B": [],
        "C": ["D"],
        "D": ["E"],
        "E": [],
    }
    order3 = topological_sort(graph3)
    assert is_valid_topological_order(graph3, order3), f"Test 3 failed: {order3}"
    assert order3.index("C") < order3.index("D") < order3.index("E"), \
        f"Test 3 chain order failed: {order3}"
    assert order3.index("A") < order3.index("B"), \
        f"Test 3 chain order failed: {order3}"
    print("Test 3 passed:", order3)
