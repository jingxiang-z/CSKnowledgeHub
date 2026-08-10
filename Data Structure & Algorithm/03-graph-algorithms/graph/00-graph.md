# Graph

## Introduction

Graphs model relationships between entities. A graph has vertices (nodes) and edges (connections). Many problems in routing, dependencies, scheduling, and networks can be expressed as graph problems.

**Core Principles:**
1. **Model the problem correctly**: Decide what vertices and edges represent
2. **Choose the right representation**: Use adjacency lists, matrices, or edge lists as needed
3. **Use graph properties**: Direction, weights, cycles, and connectivity affect algorithm choice
4. **Match the algorithm to the task**: Traversal, shortest path, MST, flow, and SCC are different problems

## Key Characteristics

### Directed vs. Undirected Graphs
- **Directed graphs** have one-way edges
- **Undirected graphs** have two-way edges
- This affects reachability, cycles, SCCs, and topological order

### Weighted vs. Unweighted Graphs
- **Unweighted graphs** treat all edges equally
- **Weighted graphs** attach costs, distances, or capacities to edges
- Negative weights restrict which shortest-path algorithms are valid

### Cyclic vs. Acyclic Structure
- Cycles change how traversal and path algorithms behave
- DAGs are useful for ordering and dependency problems
- Trees are connected acyclic graphs

### Sparse vs. Dense Graphs
- **Sparse graphs** have relatively few edges
- **Dense graphs** have many edges
- Density affects both memory use and runtime

## Common Graph Representations

### Adjacency List
- Stores the neighbors of each vertex
- Best general-purpose choice for sparse graphs
- Works well for BFS, DFS, and most graph algorithms
- Space complexity: **O(V + E)**

### Adjacency Matrix
- Stores edge existence or weight in a `V x V` table
- Useful for dense graphs and constant-time edge lookup
- Space complexity: **O(V^2)**

### Edge List
- Stores the graph as a list of edges
- Useful when algorithms process edges directly, such as Kruskal's algorithm

## Problem-Solving Workflow

### Step 1: Identify the Graph Structure
- Entities become vertices
- Relationships, transitions, or dependencies become edges
- Constraints may determine direction or edge weights

### Step 2: Classify the Graph
- Directed or undirected
- Weighted or unweighted
- Cyclic or acyclic
- Sparse or dense

### Step 3: Define the Objective
- Reachability
- Traversal order
- Shortest path
- Connected components or SCCs
- Cycle detection
- Minimum spanning tree
- Maximum flow
- Topological order

### Step 4: Choose the Representation and Algorithm
- Use adjacency lists for most sparse graph problems
- Use adjacency matrices when fast edge lookup matters
- Use edge lists when the algorithm works directly on edges
- Pick the algorithm that matches the graph constraints

### Step 5: Analyze Correctness and Complexity
- Explain why the graph model matches the problem
- Check that the algorithm fits the graph constraints
- Analyze runtime and space in terms of `V` and `E`

## Common Graph Patterns

### 1. Traversal and Reachability
- **BFS**: reachability and shortest paths in unweighted graphs
- **DFS**: traversal, connected components, and structural analysis

### 2. DFS-Based Structural Analysis
- **Topological sort**: ordering in DAGs
- **SCC**: groups of mutually reachable vertices in directed graphs

### 3. Single-Source Shortest Paths
- **BFS**: equal-weight edges
- **Dijkstra**: non-negative weights
- **Bellman-Ford**: negative weights and negative-cycle detection

### 4. All-Pairs Shortest Paths
- **Floyd-Warshall** computes shortest paths between all pairs of vertices

### 5. Minimum Spanning Trees
- **Kruskal** and **Prim** build a minimum spanning tree in an undirected weighted graph

### 6. Maximum Flow
- **Ford-Fulkerson** and **Edmonds-Karp** solve maximum-flow problems in directed graphs

### 7. Graph-Based Reductions
- **2-SAT** reduces satisfiability to SCC analysis on an implication graph

## Common Pitfalls to Avoid

1. **Using the wrong graph model** - Bad vertex or edge definitions lead to bad solutions
2. **Ignoring directionality** - Directed and undirected graphs behave differently
3. **Using BFS on weighted graphs** - BFS only works directly for equal-weight edges
4. **Using Dijkstra with negative weights** - Dijkstra requires non-negative edge weights
5. **Forgetting disconnected cases** - Some vertices may be unreachable
6. **Ignoring representation costs** - Adjacency lists and matrices have different trade-offs

## Implementations

| File | Algorithm | Runtime | Notes |
|------|-----------|---------|-------|
| [01_breadth_first_search.py](01_breadth_first_search.py) | BFS | O(V + E) | Shortest paths in unweighted graphs |
| [02_depth_first_search.py](02_depth_first_search.py) | DFS | O(V + E) | Pre/post timestamps, connected components |
| [03_topological_sort.py](03_topological_sort.py) | Topological Sort | O(V + E) | DAG ordering via DFS post-order |
| [04_strongly_connected_components.py](04_strongly_connected_components.py) | SCC (Kosaraju) | O(V + E) | Groups of mutually reachable vertices |
| [05_dijkstra.py](05_dijkstra.py) | Dijkstra | O((V + E) log V) | Single-source shortest paths, non-negative weights only |
| [06_bellman_ford.py](06_bellman_ford.py) | Bellman-Ford | O(VE) | Single-source shortest paths, handles negative weights |
| [07_floyd_warshall.py](07_floyd_warshall.py) | Floyd-Warshall | O(V³) | All-pairs shortest paths |
| [08_kruskal.py](08_kruskal.py) | Kruskal | O(E log E) | MST via edge sorting and Union-Find |
| [09_prim.py](09_prim.py) | Prim | O(E log V) | MST via min-heap |
| [10_ford_fulkerson.py](10_ford_fulkerson.py) | Ford-Fulkerson | O(E · C) | Maximum flow; C = max flow value |
| [11_edmonds_karp.py](11_edmonds_karp.py) | Edmonds-Karp | O(VE²) | Maximum flow with BFS guarantee on termination |
| [12_two_sat.py](12_two_sat.py) | 2-SAT | O(V + E) | Boolean satisfiability via SCC on implication graph |
