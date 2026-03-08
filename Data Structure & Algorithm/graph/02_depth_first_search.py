def depth_first_search(graph, start=None):
    # Input:
    # - graph: a simple graph in adjacency list format
    # - start: optional starting vertex
    #   If not provided, DFS starts from an arbitrary location.
    #
    # Internal:
    # - visited[]: tracks whether each vertex was touched by DFS
    #   All entries are true when DFS completes.
    #   This is populated by Explore, an internal subroutine of DFS.
    #
    # Output:
    # - ccnum: connected component number for each vertex
    #   Vertices reachable from the starting vertex have ccnum 1.
    # - prev: parent of each vertex in the DFS forest
    #   Unreachable vertices and the starting vertex have parent nil.
    # - pre: pre-visit number for each vertex
    # - post: post-visit number for each vertex
    raise NotImplementedError("Implement depth_first_search().")
