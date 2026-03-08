def floyd_warshall(graph, weights):
    # Input:
    # - graph: a simple graph in adjacency list format
    # - weights: edge weights
    #
    # Output:
    # - dist: all-pairs shortest-path distances
    #   dist[u][v] is the shortest-path distance from u to v.
    #   Unreachable vertex pairs have distance inf.
    #   Values are based on the nth iteration.
    # - iter: iter[i][u][v] is the distance from u to v at the end of
    #   iteration i.
    #   This table contains iterations 0 through n.
    raise NotImplementedError("Implement floyd_warshall().")
