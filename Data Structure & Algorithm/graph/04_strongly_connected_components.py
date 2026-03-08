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
    raise NotImplementedError("Implement strongly_connected_components().")
