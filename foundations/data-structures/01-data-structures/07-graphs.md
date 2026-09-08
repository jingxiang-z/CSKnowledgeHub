# Graphs: Concepts and Representations

A graph models entities and their relationships. Vertices represent entities;
edges represent relationships. Graphs may be directed or undirected, weighted
or unweighted, cyclic or acyclic, and connected or disconnected.

| Representation | Space | Iterate neighbors | Test edge |
| --- | --- | --- | --- |
| Adjacency list | `O(V + E)` | `O(deg(v))` | `O(deg(v))` |
| Adjacency matrix | `O(V²)` | `O(V)` | `O(1)` |
| Edge list | `O(E)` | `O(E)` | `O(E)` |

Adjacency lists are normally best for sparse graphs and traversal. Matrices
suit dense graphs or workloads with many edge-existence checks. Store
`(neighbor, weight)` pairs for weighted adjacency lists.

For an undirected edge, add both directions. Mark a vertex visited when it is
discovered during traversal to avoid processing it repeatedly.

The dedicated [Graph Algorithms section](../03-graph-algorithms/graph/00-graph.md)
covers BFS, DFS, topological sorting, shortest paths, spanning trees, flow,
and strongly connected components.
