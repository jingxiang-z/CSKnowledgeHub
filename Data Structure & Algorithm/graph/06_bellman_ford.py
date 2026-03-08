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
    #   This table contains iterations 0 through n.
    raise NotImplementedError("Implement bellman_ford().")
