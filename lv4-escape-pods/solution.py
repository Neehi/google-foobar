"""
A multi-source multi-sink maximum flow problem.

Ford-Fulkerson algorithm
========================

    https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
    
    Input: A network G=(V,E) with capacity c, source node s,and sink node t.

    Output: A flow f from s to t of maximum value.

    Method:
        1. Set f(u,v)=0 for all edges (u,v)
        2. While there is a path p from s to to in Gf, where cf(u,v)>0 for all edges (u,v) in p:
            i. Find cf(p) = min {cf(u,v): (u,v) in p}
            ii. For each edge(u,v) in p:
                a. f(u,v) = f(u,v) + cf(p) (Send flow along the path)
                b. f(v,u) = f(v,u) = cf(p) (The flow might be 'returned' later)
 
    Conditions:
        - The flow along an edge can not exceed capacity
        - The net flow from u to v must be equal to the net flow from v to u
        - The net flow to a node is zero, except the source which produces, and the sink which consumes
        - The flow leaving s must equal the flow arriving at t

    Example:
        Entrance = 0
        Exit = 3
        Path = [
            [0, 7, 0, 0], # Room 0: Bunnies
            [0, 0, 6, 0], # Room 1: Intermediate room
            [0, 0, 0, 8], # Room 2: Intermediate room
            [9, 0, 0, 0], # Room 3: Escape pods
        ]

        Each column in the path says which node is next and the flow capacity.

            [0] -- 6/7 --> [1] -- 6/6 --> [2] -- 6/8 --> [3]

        In this example, there is a single path:
            {0,1,2,3}: the blocking capacity is 6

        So, the max flow is 6.

Multi source multi sink
=======================

    Ford-Fulkerson doesn't naturally support multi source multi sink networks, which
    are required for this problem, but this can be overcome by adding dummy source
    and sink nodes with infinite capacity that link to the original source and
    sink nodes.

    http://www.ifp.illinois.edu/~angelia/ge330fall09_maxflowl20.pdf

    Example:
    --------
        Entrances = [0, 1]
        Exits = [4, 5]
        Path = [
            [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
            [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
            [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
            [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
            [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
            [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
        ]

        The given path is transformed by adding synthetic source and sink nodes,
        as described above, and linking these to the original source and sink
        nodes with infinite capacity.

        Entrance = 0
        Exit = 7
        Path = [
            [0, I, I, 0, 0, 0, 0, 0],  # Synthetic entrance
            [0, 0, 0, 4, 6, 0, 0, 0],  # Room 0: Bunnies
            [0, 0, 0, 5, 2, 0, 0, 0],  # Room 1: Bunnies
            [0, 0, 0, 0, 0, 4, 4, 0],  # Room 2: Intermediate room
            [0, 0, 0, 0, 0, 6, 6, 0],  # Room 3: Intermediate room
            [0, 0, 0, 0, 0, 0, 0, I],  # Room 4: Escape pods
            [0, 0, 0, 0, 0, 0, 0, I],  # Room 5: Escape pods
            [0, 0, 0, 0, 0, 0, 0, 0],  # Synthetic exit
        ]

        Each column in the path says which node is next and the flow capacity.

            [0] -- 4/I --> [1] -- 4/4 --> [3] -- 4/4 --> [5] -- 4/I --> [7]
            [0] -- 6/I --> [1] -- 6/6 --> [4] -- 6/6 --> [6] -- 6/I --> [7]
            [0] -- 5/I --> [2] -- 4/5 --> [3] -- 4/4 --> [5] -- 4/I --> [7]
            [0] -- 2/I --> [2] -- 2/2 --> [4] -- 2/2 --> [6] -- 2/I --> [7]

        In this example, there are several paths:
            {0,1,3,5,7}: the blocking capacity is 4
            {0,1,4,6,7}: the blocking capacity is 6
            {1,2,3,5,7}: the blocking capacity is 4
            {1,2,4,6,7}: the blocking capacity is 2

        So, the max flow is 16.
"""

INF = 0x40000


def transform(entrances, exits, path):
    """ Transform a multi source multi sink graph into source and sink. """

    # Add dummy source and sink nodes
    path = (
        [[0] * (len(path) + 2)] +
        [[0] + row + [0] for row in path] +
        [[0] * (len(path) + 2)]
    )

    # Link dummy source to previous source nodes
    for u in entrances:
        path[0][u + 1] = INF

    # Link dummy sink to previous sink nodes
    for u in exits:
        path[u + 1][-1] = INF

    # Set a single entrance and exit
    entrances = [0]
    exits = [len(path) - 1]

    return entrances, exits, path


def bfs(C, F, s, t):
    """
    Returns a path if there is a route from s to t in the residual graph.

    Utilises a greedy algorithm to try and maximise the flow capacity each
    path iteration.

    For each node:
    - loop through each possible path from this node
    - check next node has not been previously visited
    - check flow capacity > 0
    - select largest maximum capacity
    """

    # Special case for source and sink being the same
    if s == t:
        return [s]

    # List of nodes for this path
    path = []

    # A simple queue of steps
    queue = [s]  # Start with the source

    # Simple BFS loop
    while queue:
        u = queue.pop(0)

        path.append(u)

        # Search for largest unvisited node
        next = max = 0
        for v, cf in enumerate(C[u]):
            if v in path or C[u][v] == 0:
                continue
            cf = C[u][v] - F[u][v]
            if cf > 0 and cf > max:
                max = cf
                next = v

        # If sink was reached return the path
        if next == t:
            return path

        # If a valid node was found add it to the queue
        if max:
            queue.append(next)

    # Sink wasn't reached
    return None


def solution(entrances, exits, path):
    # Check if multi source or multi sink and transform if necessary
    if len(entrances) > 1 or len(exits) > 1:
        entrances, exits, path = transform(entrances, exits, path)

    # Source and sink nodes
    s = entrances[0]
    t = exits[0]

    # Capacity and flow graphs
    C = path[:]
    F = [[0] * len(C) for j in range(len(C))]

    while True:
        # Use BFS to find a path from s to t
        path = bfs(C, F, s, t)

        if not path:
            break

        # Find the maximum flow for this path, which is actually
        # the minimum/blocking capacity for the path
        path_flow = min([
            C[path[j]][path[j + 1]] - F[path[j]][path[j + 1]]
            for j in range(len(path) - 1)
        ])

        # Update the residual graph with the max flow for this path
        for j in range(len(path) - 1):
            u, v = path[j], path[j + 1]
            F[u][v] += path_flow
            F[v][u] -= path_flow

    # Sum of the start row of the flow graph will be equal
    # to the maximum flow for
    return sum(F[s][v] for v in range(len(F)))
