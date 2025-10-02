[toc]

# Graph

## Concepts

A graph is a fundamental and versatile data structure used in computer science, mathematics, and various fields to represent and analyze relationships between objects or entities. It is a collection of nodes (vertices) connected by edges, where each edge represents a relationship or connection between two nodes. Graphs provide a powerful way to model and study complex systems, networks, and structures, making them a core concept in many areas of computing and science.

Here are some key characteristics and components of graphs:

1. **Nodes (Vertices):** Nodes are the fundamental building blocks of a graph and represent individual entities or elements. Each node can contain data or attributes associated with it.
2. **Edges:** Edges are connections or links between nodes and define the relationships between them. Edges may have weights or labels to represent the strength or type of connection.
3. **Directed vs. Undirected Graphs:** In a directed graph (digraph), edges have a direction, indicating a one-way relationship from one node to another. In an undirected graph, edges have no direction, representing a mutual relationship between nodes.
4. **Weighted vs. Unweighted Graphs:** In a weighted graph, each edge is assigned a numerical weight, which can represent various properties such as distance, cost, or capacity. Unweighted graphs have no weights associated with their edges.
5. **Cyclic vs. Acyclic Graphs:** A graph that contains cycles (closed loops) is called cyclic, while a graph without any cycles is called acyclic. Directed acyclic graphs (DAGs) are particularly important in various applications.

## Traversal

### BFS

1. Start at the source node and mark it as visited.

2. Enqueue the source node into a queue data structure.

3. While the queue is not empty: 

   a. Dequeue the front node from the queue. 

   b. Visit and process the node (e.g., print it or perform some operation). 

   c. Enqueue all unvisited neighbors of the current node. 

   d. Mark these neighbors as visited to avoid revisiting them.

```python
from collections import deque
def bfs(graph, u):
    visited = set()
    queue = deque()
    queue.append(u)
    visited.add(u)
    while queue:
        node = queue.popleft()
        print(node)
        for v in graph[node]:
            if v not in visited:
                queue.append(v)
                visited.add(v)
```

### DFS

1. Start at the source node and mark it as visited.
2. Visit the node (e.g., print it or perform some operation).
3. Recursively apply DFS to one unvisited neighbor of the current node.
4. If no unvisited neighbors are left, backtrack to the previous node.
5. Continue the process until all reachable nodes have been visited.

```python
def dfs(graph, u, visited):
    print(u)
    visited.add(u)
    for neighbor in graph[u]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

## Strongly Connected Component

A Strongly Connected Component (SCC) is a fundamental concept in graph theory and network analysis, primarily applied to directed graphs, also known as digraphs. An SCC is a subset of vertices within a directed graph with the distinctive property that there exists a directed path from any vertex in the subset to any other vertex within the same subset. In other words, every vertex in an SCC can be reached from every other vertex within the same SCC, making it a highly connected and cohesive substructure.

### Kosaraju's Algorithm

1. First Pass (Forward Pass):
   - Perform a depth-first search (DFS) on the original directed graph to assign finishing times to each vertex.
   - Create a list of vertices in the order they finish the DFS traversal (topological order).
2. Second Pass (Backward Pass):
   - Reverse all the edges of the original graph to create a new graph.
   - Perform another DFS on the reversed graph, starting from each vertex in the reverse topological order obtained in the first pass.
   - During this DFS, identify and group vertices that are reachable from each other. These groups represent the strongly connected components of the original graph.

```python
from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def _dfs(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self._dfs(i, visited, stack)
        stack.append(v)

    def get_transpose(self):
        g = Graph(self.V)
        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g

    def kosaraju_scc(self):
        stack = []
        visited = [False] * self.V

        # Fill the stack using the first DFS (forward pass)
        for i in range(self.V):
            if not visited[i]:
                self._dfs(i, visited, stack)

        # Create the transpose of the graph
        transposed = self.get_transpose()

        # Reset visited array for the second DFS (backward pass)
        visited = [False] * self.V

        sccs = []
        while stack:
            v = stack.pop()
            if not visited[v]:
                scc = []
                transposed._dfs(v, visited, scc)
                sccs.append(scc)

        return sccs

# Example usage:
g = Graph(8)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 0)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(4, 5)
g.add_edge(5, 3)
g.add_edge(6, 7)

sccs = g.kosaraju_scc()
print(sccs)

```

### Tarjan's Algorithm

1. Initialize data structures (stack, discovery time, low-link, and SCC list).
2. Start a DFS traversal from unvisited vertices.
   - Assign a unique discovery time and low-link value.
   - Push the vertex onto the stack.
3. Recursively explore neighbors:
   - Update low-link value based on unvisited neighbors.
   - Detect back edges and update low-link accordingly.
4. Identify SCCs:
   - When low-link equals discovery time, it's the start of an SCC.
   - Pop vertices from the stack to form an SCC.
5. Repeat steps 2-4 for all unvisited vertices.
6. The SCCs found are stored for analysis.

```python
from collections import defaultdict

class TarjanSCC:
    def __init__(self, graph):
        self.graph = graph
        self.index = 0
        self.stack = []  # Stack to keep track of vertices in the current DFS path
        self.low_link = {}  # Mapping of vertices to their low-link values
        self.index_map = {}  # Mapping of vertices to their discovery times
        self.sccs = []  # List to store the strongly connected components (SCCs)

    def find_sccs(self):
        for vertex in self.graph:
            if vertex not in self.index_map:
                self._dfs(vertex)

        return self.sccs

    def _dfs(self, v):
        # Initialize the discovery time and low-link values for the current vertex
        self.index_map[v] = self.index
        self.low_link[v] = self.index
        self.index += 1
        self.stack.append(v)

        for neighbor in self.graph[v]:
            if neighbor not in self.index_map:
                self._dfs(neighbor)
                # Update the low-link value based on the neighbor's low-link
                self.low_link[v] = min(self.low_link[v], self.low_link[neighbor])
            elif neighbor in self.stack:
                # If the neighbor is on the current stack, update the low-link value
                self.low_link[v] = min(self.low_link[v], self.index_map[neighbor])

        # If the low-link and discovery time are equal, a strongly connected component has been found
        if self.low_link[v] == self.index_map[v]:
            scc = []
            while True:
                u = self.stack.pop()
                scc.append(u)
                if u == v:
                    break
            self.sccs.append(scc)

# Example usage:
graph = {
    0: [1, 2],
    1: [3],
    2: [0],
    3: [4],
    4: [5, 6],
    5: [7],
    6: [3],
    7: [6, 8],
    8: [5]
}

tarjan = TarjanSCC(graph)
sccs = tarjan.find_sccs()
print(sccs)

```

## Shortest Path

### BFS

BFS is highly effective for finding the shortest path in scenarios where all edges have equal weight, and it is well-suited for a wide range of applications, such as navigation, network routing, game development, and more. Its level-order traversal ensures that the algorithm discovers the shortest path before exploring longer paths, making it an essential tool for solving problems related to pathfinding and optimization.

```python
from collections import deque

def bfs(graph, u, v):
    visited = set()
    queue = deque()
    parent = {}
    
    queue.append(u)
    visited.add(u)
    
    while queue:
        n = queue.popleft()
        if n == v:
            # Reconstruct the path from v to u
            path = []
            while n is not None:
                path.append(n)
                n = parent.get(n)
            return len(path) - 1, path[::-1]  # Distance and path
        for neighbor in graph[n]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = n
                queue.append(neighbor)
    
    return -1, []  # No path found
```

### Dijkstra's Algorithm

1. **Initialization**:
   - Set all vertex distances to infinity, except for the source vertex, which is set to 0.
   - Create a priority queue with the source vertex and its distance (0).
2. **Iterate**:
   - While the priority queue is not empty, dequeue the vertex with the smallest known distance.
3. **Relaxation**:
   - For each neighbor of the dequeued vertex:
     - Calculate the distance from the source to the neighbor through the dequeued vertex.
     - If it's shorter than the known distance, update the neighbor's distance.
     - Enqueue the neighbor with the updated distance.
4. **Repeat**:
   - Continue until the priority queue is empty.
5. **Path Reconstruction (Optional)**:
   - To find the shortest path, backtrack from the destination to the source using distance information and parent pointers.

```python
import heapq

def dijkstra(graph, s, d):
    dist = {v: float('inf') for v in graph}
    visited = set()
    visited.add(s)
    dist[s] = 0
    queue = [(0, s)]
    parent = {}
    
    while queue:
        curr, node = heapq.heappop(queue)
        for neighbor in graph[node]:
            distance = curr + graph[node][neighbor]
            if neighbor not in visited and dist[neighbor] > distance:
                parent[neighbor] = node
                dist[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                visited.add(neighbor)
    path = []
    while d != s:
        path.append(d)
        d = parent[d]
    path.append(d)
    return dist, path[::-1]
```

### Bellman-Ford's Algorithm

1. **Initialization**:
   - Create a list or dictionary to store the shortest distance from the source vertex to all other vertices. Initialize the distance to the source as 0 and all other distances as infinity.
   - Create a list of edges representing the graph's weighted edges.
2. **Relaxation**:
   - Iterate through all edges and update the distance to each vertex if a shorter path is found through the current edge. This step is repeated for a total of V-1 iterations, **where V is the number of vertices**. This ensures that the algorithm explores all possible paths.
3. **Negative Weight Cycle Detection**:
   - After the V-1 iterations, check for negative weight cycles. If any distances can be further reduced in the Vth iteration, it indicates the presence of a negative weight cycle. The algorithm may not terminate in this case.
4. **Path Reconstruction (Optional)**:
   - If you want to find the actual shortest path from the source to a specific destination, you can backtrack through the parent vertices using the updated distance information.

```python
def bellman_ford(graph, s):
    dist = {v: float('inf') for v in graph}
    dist[s] = 0
    edges = [(u, v, graph[u][v]) for u in graph for v in graph[u]]
    for _ in range(len(graph)-1):
        for u, v, weight in edges:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
    
    for u, v, weight in edges:
        if dist[u] + weight < dist[v]:
            raise Exception("Negative edge detected")
    
    return dist
```

### Floyd-Warshall's Algorithm

1. **Optimal Substructure:**

   - The Floyd-Warshall algorithm relies on the optimal substructure property, which means that the optimal solution to a problem can be constructed from optimal solutions to its subproblems.
   - In the context of shortest paths, if the shortest path from vertex i to vertex j involves an intermediate vertex k, then the subpaths from i to k and from k to j must also be the shortest paths.

2. **Recurrence Relation:**

   - The algorithm defines a recurrence relation to compute the shortest path distances between all pairs of vertices.

   - Let 

     ```
     dist[i][j]
     ```

      be the shortest distance from vertex i to vertex j using only the first k vertices as intermediate vertices. The recurrence relation is given by:

     ```
     cssCopy code
     dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
     ```

   - This relation states that the shortest path from i to j either goes directly from i to j or involves an intermediate vertex k.

3. **Initialization:**

   - The algorithm initializes the `dist` matrix with direct edge weights between vertices. If there is no direct edge, the distance is set to infinity.
   - The diagonal elements (distances from a vertex to itself) are set to 0.

4. **Dynamic Programming Iteration:**

   - The algorithm performs a triple-nested loop to iterate over all vertices as potential intermediate vertices (k), updating the `dist` matrix based on the recurrence relation.
   - After the iteration, the `dist` matrix contains the shortest path distances between all pairs of vertices.

5. **Result:**

   - The final `dist` matrix represents the shortest distances between all pairs of vertices in the graph.

```python
def floyd_warshall(graph):
    num_vertices = len(graph)
    dist = [[float('inf') if i != j else 0 for j in range(num_vertices)] for i in range(num_vertices)]
    for u in graph:
        for v in graph[u]:
            dist[u][v] = graph[u][v]
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

## Minimum Spanning Tree

A Minimum Spanning Tree (MST) is a fundamental concept in graph theory and network design. It is a subset of the edges of an undirected graph that connects all the vertices together without forming any cycles and has the minimum possible total edge weight. In other words, a minimum spanning tree is a tree that spans all the vertices of the graph while minimizing the sum of edge weights.

### Kurskal's Algorithm

```python
def MST(points):
    '''
    Kruskal's Algorithm for Minimum Spanning Tree
    Distance are decribed by Manhattan distance 
    Used Union-Find to decide whether two nodes connected or not
    '''
  	size = len(points)
    dists = []
    if size <= 1:
      	return 0
    for i in range(size-1):
        for j in range(i+1, size):
            dist = abs(points[j][0]-points[i][0]) + abs(points[j][1]-points[i][1])
            dists.append((i, j, dist))
    dists = sorted(dists, key=lambda x: x[2])
    res = 0
    edges = 0
    uf = UnionFind(size)
    for i, j, dist in dists:
        if uf.connected(i, j):
            continue
        uf.union(i, j)
        res += dist
        edges += 1
        if edges == size-1:
          	break
    return res
```

### Prim's Algorithm

```python
import heapq
def MST(points):
		size = len(points)
    if size <= 1:
      	return 0
    dists = []
    visited = set()
    visited.add(0)

    for j in range(1, size):
      	dist = abs(points[j][0]-points[0][0]) + abs(points[j][1]-points[0][1])
      	dists.append((dist, 0, j))

    heapq.heapify(dists)
    res = 0

    while dists and len(visited)<size:
        dist, _, j = heapq.heappop(dists)
        if j not in visited:
            visited.add(j)
            res += dist
            for i in range(size):
                if i in visited:
                    continue
                dist = abs(points[j][0]-points[i][0]) + abs(points[j][1]-points[i][1])
                heapq.heappush(dists, (dist, j, i))
    return res
```

## Topological Sort

### DFS

```python
def topological_sort(graph):
    def helper(v, visited, stack):
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                helper(neighbor, visited, stack)
        stack.append(v)

    visited = set()
    stack = []

    for v in graph:
        if v not in visited:
            helper(v, visited, stack)

    return stack[::-1]
```

### kahn's Algorithm

```python
import collections

def findOrder(numCourses, prerequisites):
    graph = collections.defaultdict(list)
    indegree = [0] * numCourses

    # Build the graph and calculate in-degrees
    for prerequisite in prerequisites:
        a, b = prerequisite[0], prerequisite[1]
        graph[b].append(a)
        indegree[a] += 1

    # Initialize the queue with vertices with in-degree 0
    queue = collections.deque()
    for i, item in enumerate(indegree):
        if item == 0:
            queue.append(i)

    res = []

    # Perform topological sort
    while queue:
        u = queue.popleft()
        res.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
        del graph[u]

    # Check if all courses can be taken
    if len(res) == numCourses:
        return res
    else:
        return []

# Example usage:
numCourses = 4
prerequisites = [[1,0],[2,0],[3,1],[3,2]]
result = findOrder(numCourses, prerequisites)
print(result)

```

