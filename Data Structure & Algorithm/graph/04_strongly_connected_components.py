"""
Algorithm
=====================
- Create a reverse graph G' for the original graph G
- Run DFS on the reverse graph G' to find the post-visit order
- Run DFS on the original graph G following the reversed post-visit order
- The ccnum from the DFS on the original graph reveals the strongly connected components

Correctness
=====================
Running DFS on the reverse graph G' gives us the topological order of the metagraph from sink to source
(i.e., the vertex with the highest post-visit number in G' belongs to a sink SCC of the original G).
Running DFS starting from the sink SCC of the original graph makes sure it won't find a vertex in another component,
since a sink SCC has no outgoing edges to other SCCs.

Runtime
=====================
Building the reverse graph takes O(V + E), and the two DFS passes together also take O(V + E).
Therefore, the overall time complexity remains O(V + E), where V = number of vertices and E = number of edges.
"""

import importlib.util, pathlib

_mod_path = pathlib.Path(__file__).parent / "02_depth_first_search.py"
_spec = importlib.util.spec_from_file_location("depth_first_search", _mod_path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
depth_first_search = _mod.depth_first_search

def strongly_connected_components(graph):
    # Input:
    # - graph: a simple, directed graph in adjacency list format
    #
    # Output:
    # - metagraph: the strongly connected components metagraph in adjacency list format
    #   By construction, the metagraph is a DAG with vertices sorted from
    #   sink to source. This ordering is reverse topological ordering.
    # - all outputs from the final run of depth_first_search() are also
    #   available to you: ccnum, prev, pre, and post.
    #   This data can be used to connect metagraph vertices back to the
    #   original input graph.
    graphr = {v: [] for v in graph}
    for u, neighbors in graph.items():
        for neighbor in neighbors:
            graphr[neighbor].append(u)
    _, _, _, postr = depth_first_search(graphr)
    orders = sorted(postr, key=lambda v: postr[v], reverse=True)

    ccnum, prev, pre, post = depth_first_search(graph, orders)

    metagraph = {scc: [] for scc in set(ccnum.values())}
    for u, neighbors in graph.items():
        for v in neighbors:
            if ccnum[u] != ccnum[v] and ccnum[v] not in metagraph[ccnum[u]]:
                metagraph[ccnum[u]].append(ccnum[v])

    return metagraph, ccnum, prev, pre, post


def same_scc(ccnum, u, v):
    """Return True if u and v belong to the same strongly connected component."""
    return ccnum[u] == ccnum[v]


if __name__ == "__main__":
    # Test 1: Single triangle cycle  A → B → C → A
    # Every vertex can reach every other, so there is exactly one SCC
    # and the metagraph has one node with no cross-component edges.
    graph1 = {"A": ["B"], "B": ["C"], "C": ["A"]}
    metagraph1, ccnum1, _, _, _ = strongly_connected_components(graph1)
    assert len(metagraph1) == 1, f"Test 1 failed: expected 1 SCC, got {len(metagraph1)}"
    assert list(metagraph1.values()) == [[]], f"Test 1 failed: expected no edges, got {metagraph1}"
    assert same_scc(ccnum1, "A", "B") and same_scc(ccnum1, "B", "C"), \
        f"Test 1 failed: A, B, C should be in the same SCC"
    print("Test 1 passed:", metagraph1)

    # Test 2: Linear directed chain  A → B → C
    # No back edges, so each vertex is its own SCC.
    # The metagraph is itself a linear chain with 3 nodes and 2 edges.
    graph2 = {"A": ["B"], "B": ["C"], "C": []}
    metagraph2, ccnum2, _, _, _ = strongly_connected_components(graph2)
    assert len(metagraph2) == 3, f"Test 2 failed: expected 3 SCCs, got {len(metagraph2)}"
    assert not same_scc(ccnum2, "A", "B") and not same_scc(ccnum2, "B", "C"), \
        f"Test 2 failed: A, B, C should each be their own SCC"
    total_edges2 = sum(len(v) for v in metagraph2.values())
    assert total_edges2 == 2, f"Test 2 failed: expected 2 metagraph edges, got {total_edges2}"
    print("Test 2 passed:", metagraph2)

    # Test 3: Two internal cycles bridged by one cross edge
    #   A ↔ B  (one SCC)  →  C ↔ D  (another SCC)
    # Exactly 2 SCCs and exactly 1 edge in the metagraph.
    graph3 = {"A": ["B"], "B": ["A", "C"], "C": ["D"], "D": ["C"]}
    metagraph3, ccnum3, _, _, _ = strongly_connected_components(graph3)
    assert len(metagraph3) == 2, f"Test 3 failed: expected 2 SCCs, got {len(metagraph3)}"
    assert same_scc(ccnum3, "A", "B"), "Test 3 failed: A and B should be in the same SCC"
    assert same_scc(ccnum3, "C", "D"), "Test 3 failed: C and D should be in the same SCC"
    assert not same_scc(ccnum3, "B", "C"), "Test 3 failed: {A,B} and {C,D} should be different SCCs"
    total_edges3 = sum(len(v) for v in metagraph3.values())
    assert total_edges3 == 1, f"Test 3 failed: expected 1 metagraph edge, got {total_edges3}"
    print("Test 3 passed:", metagraph3)
