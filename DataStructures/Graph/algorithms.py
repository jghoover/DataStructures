from collections import namedtuple
from math import inf

from DataStructures import PriorityQueue


# todo: make sure these all work with graph and digraph objects


def reconstruct_path(destination, parent_dict):
    # todo: add code to return None if no path exists
    # todo: destination not in parent_dict should probably return None as well?
    # todo: rewrite this
    if destination not in parent_dict:
        raise ValueError("Destination {0} not present in dictionary".format(repr(destination)))

    path = [destination, ]

    while parent_dict[destination] is not None:
        path.insert(0, parent_dict[destination])
        destination = parent_dict[destination]

    return path


# runtime O(V + E) and E \in O(V^2) so O(V^2)
def breadth_first_search(graph, node, destination=None):
    # todo: merge this into shortest_path and shortest_path_length
    # todo: rewrite this so it doesn't use namedtuple
    level = dict.fromkeys(graph.vertices, inf)
    level[node] = 0
    parent = dict.fromkeys(graph.vertices, None)
    visited = {node, }
    i = 1
    frontier = [node]
    while frontier:
        nextfrontier = []
        for node in frontier:
            for neighbor in graph.adj(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    level[neighbor] = i
                    parent[neighbor] = node
                    nextfrontier.append(neighbor)
                    if neighbor == destination:
                        return namedtuple("BFS", ["level", "parent"])(level, parent)
        frontier = nextfrontier
        i += 1

    return namedtuple("BFS", ["level", "parent"])(level, parent)


# runtime: O(V + E) and E \in O(V^2) so O(V^2)
def depth_first_search(graph):
    return _dfs(graph).parent


def topological_sort(graph):
    return _dfs(graph).topo


def _dfs(graph):
    parent = {}
    time = 0
    topo = []

    # iterate over neighbors of node
    def dfs_visit(node, time):
        time += 1
        for neighbor in graph.adj(node):
            if neighbor not in parent:
                parent[neighbor] = node
                dfs_visit(neighbor, time)
        topo.insert(0, node)
        time += 1

    # iterate over all nodes
    for node in graph.vertices:
        if node not in parent:
            parent[node] = None
            dfs_visit(node, time)

    return namedtuple("DFS", ["parent", "topo"])(parent, topo)


def is_cyclic(graph):
    path = set()
    visited = set()

    def visit(node):
        if node in visited:
            return False

        visited.add(node)
        path.add(node)

        for neighbor in graph.adj(node):
            if neighbor in path or visit(neighbor):
                return True

        path.remove(node)

        return False

    return any(visit(node) for node in graph.vertices)


def _return_zero(*_):
    # default heuristic for a_star
    return 0


# A* graph search algorithm
def a_star(graph, source, destination, heuristic=None):
    # default heuristic is h=0, which makes A* behave like Dijkstra's
    if heuristic is None:
        heuristic = _return_zero

    closed = []
    pq = PriorityQueue()

    # for reconstructing paths
    parent = {}

    # cost of going from source to node
    dist = {source: 0}

    # total cost of getting from source to destination by passing through node
    estimate = {}

    # todo: rewrite to make more efficient---dict.fromkeys?
    for node in graph.vertices:
        if node == source:
            dist[node] = 0
            estimate[node] = heuristic(node, destination)
        else:
            dist[node] = inf
            estimate[node] = inf

    pq.insert(source, estimate[source])

    while pq:
        node = pq.extract()

        # yay, we made it!
        if node == destination:
            return reconstruct_path(destination, parent)

        closed.append(node)

        for neighbor in graph.adj(node):
            if neighbor in closed:
                continue
            if neighbor not in pq:
                pq.insert(neighbor, estimate[neighbor])

            # check the distance from source to neighbor
            # todo: make sure that weight is what I actually want here
            length = dist[node] + graph.weight(node, neighbor)

            # update!
            if length < dist[neighbor]:
                parent[neighbor] = node
                dist[neighbor] = length
                estimate[neighbor] = length + heuristic(neighbor, destination)
                pq.update_priority(neighbor, estimate[neighbor])

    # didn't find a path
    return None


def shortest_path(graph, sources=None, destinations=None):
    # todo: write this.
    # sources and destinations should be iterables of nodes
    # if neither source nor destination are specified, compute shortest path from every node to every other node
    #     return a dict with keys of sources and values of dicts with keys of destinations with values of lists
    #     containing the nodes in the path
    # if only source is specified, compute shortest path from source to every other node
    #     return a dict with keys of destinations and values of lists containing the nodes in the path
    # if only destination is specified, compute the shortest path from every node to destination
    #     return a dict with keys of sources and values of lists containing the nodes in the path

    # if we're finding every shortest path between every node, we can be smart about what computation we actually do
    # i.e. if we do shortest path from a node in the periphery of graph, we should get a fair amount of shortest
    # paths.  this might take a lot of extra work to implement
    # easy/inefficient way would be to write the function to just loop over every combination of source and
    # destination, but if i.e. we have a shortest path (a, b, c, d), we know that all of (a, b), (a, b, c), (b, c),
    # (b, c, d), (c, d) are ALSO shortest paths, so it's useless to compute paths from i.e. b to c and b to d
    # so we really just need to compute all shortest paths between elements of the periphery? (must be at least 2 in
    # an undirected graph)

    # for now, just code everything without helper functions, then refactor once this actually works

    paths = {}

    if sources is None:
        # iterate over all possible sources
        sources = graph.vertices
    if destinations is None:
        # iterate over all possible destinations
        destinations = graph.vertices

    if graph.weighted:
        # dijkstra's
        pass
    else:
        # BFS
        pass


def shortest_path_length(graph, source=None, destination=None):
    # todo: write this
    # same as shortest_path
    if source is None:
        # iterate over all possible sources
        pass
    if destination is None:
        # iterate over all possible destinations
        pass

    if graph.weighted:
        # dijkstra's
        pass
    else:
        # BFS
        pass


# shortest path on a weighted graph. Dijkstra's Alg
# runtime: O(E + V log V), but since E \in O(V^2), we get
#    O(V^2) essentially.
# Dijkstra's algorithm
def weighted_shortest_paths(graph, source):
    # todo: merge this into shortest_path and shortest_path_length
    pq = PriorityQueue()

    dist = {}
    parent = {}

    for v in graph.vertices:
        if v == source:
            dist[v] = 0
        else:
            dist[v] = inf

        parent[v] = None

        pq.insert(v, dist[v])

    while pq:
        node = pq.extract()

        for neighbor in graph.adj(node):
            length = dist[node] + graph.weight(node, neighbor)
            # update
            if length < dist[neighbor]:
                dist[neighbor] = length
                parent[neighbor] = node
                pq.update_priority(neighbor, length)

    return namedtuple("Shortest_Path", ["length", "parent"])(dist, parent)
