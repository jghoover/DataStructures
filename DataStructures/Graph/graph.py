from collections import namedtuple
from math import inf

from DataStructures import PriorityQueue


class Graph(object):
    # todo: ideally, you wouldn't have to specify a graph as weighted
    # todo: make sure the new __init__ actually works with the rewritten adding nodes/edges
    # todo: should I have a separate class for digraph/multigraph?
    # todo: add more features to make this more like networkx
    # todo: write code to be able to generate a graph from a function (implicitly generated graph)
    #    i.e. define what a node looks like and define a function that generates an edge
    def __init__(self, graph_data=None, weighted=False):

        if graph_data is None:
            graph_data = {}

        self._adj = {}
        self._pred = {}
        self._weight = {}
        self._ecc = None

        self._weighted = weighted

        # add vertices
        # for node in list(graph_data.keys()):
        #     self.add_node(node)
        # add nodes and edges
        for node in graph_data.keys():
            # add node, if not already present
            if node not in self:
                self.add_node(node)

            for adj in graph_data[node]:
                # add adj, if not already present
                if adj not in self:
                    self.add_node(adj)

                if self.weighted:
                    neighbor, weight = adj
                else:
                    neighbor = adj
                    weight = None

                self.add_directed_edge(node, neighbor, weight)

    def _maximally_connected(self):
        # return the maximally connected subset of self.vertices
        # could compute the multiplicity of 0 as an eigenvalue of the Laplacean matrix of the graph
        # probably easier to just do DFS or BFS and see if everything is reached
        pass

    @classmethod
    def induced_subgraph(cls, graph, filter_nodes=None):
        # construct a new subgraph from `graph`, based on nodes that satisfy `filter`
        if filter_nodes is None:
            filter_nodes = Graph._maximally_connected
        vertices = filter_nodes(graph.vertices)
        pass

    def __contains__(self, item):
        return item in self._adj

    def __iter__(self):
        return iter(self._adj)

    def __len__(self):
        return self.order

    @property
    def vertices(self):
        return list(self._adj.keys())

    @property
    def edges(self):
        return [(node, neighbor) for node, neighbors in self._adj.items() for neighbor in neighbors]

    @property
    def weighted(self):
        return self._weighted

    @property
    def order(self):
        return len(self.vertices)

    # in an undirected graph, indegree(n) == outdegree(n)
    def degree(self, node):
        return len(self.adj(node))

    # number of edges that end at node
    def indegree(self, node):
        return len(self.pred(node))

    # number of edges that start at node
    def outdegree(self, node):
        return self.degree(node)

    @staticmethod
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

    def adj(self, node):
        return self._adj[node]

    def pred(self, node):
        return self._pred[node]

    def is_adj(self, node1, node2):
        return node2 in self._adj[node1]

    # get the weight of an edge between node1, node2
    def weight(self, node1, node2):
        if self.is_adj(node1, node2):
            if self.weighted:
                weight = self._weight[(node1, node2)]
            else:
                weight = 1

            return weight
        else:
            raise ValueError("No such edge {0}".format(repr((node1, node2))))

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        # add an unconnected vertex to the graph
        if node not in self:
            self._adj[node] = []
            self._pred[node] = []
        else:
            raise ValueError("Node {0} already present in graph".format(repr(node)))

        self._ecc = None

    # add edges from an iterable.  elements of the iterable should be of the form (node1, node2, optional(weight))
    def add_directed_edges(self, edges):
        for edge in edges:
            try:
                node1, node2, weight = edge
            except ValueError:
                node1, node2 = edge
                weight = None

            self.add_directed_edge(node1, node2, weight)

    def add_directed_edge(self, node1, node2, weight=None):
        # add an edge between two vertices, node1 and node1, with optional weight
        for node in [node1, node2]:
            if node not in self:
                raise ValueError("Node {0} not present in the graph".format(repr(node)))
        else:
            if self.weighted:
                self._weight[(node1, node2)] = weight

            self._adj[node1].append(node2)
            self._pred[node2].append(node1)

        self._ecc = None

    def add_undirected_edges(self, edges):
        for edge in edges:
            try:
                node1, node2, weight = edge
            except ValueError:
                node1, node2 = edge
                weight = None

            self.add_undirected_edge(node1, node2, weight)

    def add_undirected_edge(self, node1, node2, weight=None):
        self.add_directed_edge(node1, node2, weight)
        self.add_directed_edge(node2, node1, weight)

    def remove_directed_edges(self, edges):
        for edge in edges:
            node1, node2 = edge
            self.remove_directed_edge(node1, node2)

    def remove_directed_edge(self, node1, node2):
        # make sure nodes are present
        for node in [node1, node2]:
            if node not in self:
                raise ValueError("Node {0} not present in graph".format(repr(node)))

        if self.is_adj(node1, node2):
            self._adj[node1].remove(node2)
            self._pred[node2].remove(node1)
            if self.weighted:
                del self._weight[(node1, node2)]
        else:
            raise ValueError("Edge {0} not present in graph".format(repr((node1, node2))))

        self._ecc = None

    def remove_undirected_edges(self, edges):
        for edge in edges:
            node1, node2 = edge
            self.remove_undirected_edge(node1, node2)

    def remove_undirected_edge(self, node1, node2):
        self.remove_directed_edge(node1, node2)
        self.remove_directed_edge(node2, node1)

    # pass an iterable of nodes to remove
    def remove_nodes(self, nodes):
        for node in nodes:
            self.remove_node(node)

    def remove_node(self, node):
        if node in self:
            # get vertices that node points to
            removal = [(node, neighbor) for neighbor in self.adj(node)]
            # get vertices that point to node
            removal.extend([(neighbor, node) for neighbor in self.pred(node)])

            # then get rid of the edges
            for x, y in removal:
                self.remove_directed_edge(x, y)

            # then clear out node's dict entries
            del self._adj[node]
            del self._pred[node]
        else:
            raise ValueError("Node {0} not present in graph".format(repr(node)))

        self._ecc = None

    # runtime O(V + E) and E \in O(V^2) so O(V^2)
    def breadth_first_search(self, node, destination=None):
        # todo: merge this into shortest_path and shortest_path_length
        level = dict.fromkeys(self.vertices, inf)
        level[node] = 0
        parent = dict.fromkeys(self.vertices, None)
        visited = {node, }
        i = 1
        frontier = [node]
        while frontier:
            nextfrontier = []
            for node in frontier:
                for neighbor in self.adj(node):
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
    def depth_first_search(self):
        return self._dfs().parent

    def topological_sort(self):
        return self._dfs().topo

    def _dfs(self):
        parent = {}
        time = 0
        topo = []

        # iterate over neighbors of node
        def dfs_visit(node, time):
            time += 1
            for neighbor in self.adj(node):
                if neighbor not in parent:
                    parent[neighbor] = node
                    dfs_visit(neighbor, time)
            topo.insert(0, node)
            time += 1

        # iterate over all nodes
        for node in self.vertices:
            if node not in parent:
                parent[node] = None
                dfs_visit(node, time)

        return namedtuple("DFS", ["parent", "topo"])(parent, topo)

    def is_cyclic(self):
        path = set()
        visited = set()

        def visit(node):
            if node in visited:
                return False

            visited.add(node)
            path.add(node)

            for neighbor in self.adj(node):
                if neighbor in path or visit(neighbor):
                    return True

            path.remove(node)

            return False

        return any(visit(node) for node in self.vertices)

    @staticmethod
    def _return_zero(*_):
        # default heuristic for a_star
        return 0

    # A* graph search algorithm
    def a_star(self, source, destination, heuristic=None):

        # default heuristic is h=0, which makes A* behave like Dijkstra's
        if heuristic is None:
            heuristic = Graph._return_zero

        closed = []
        pq = PriorityQueue()

        # for reconstructing paths
        parent = {}

        # cost of going from source to node
        dist = {source: 0}

        # total cost of getting from source to destination by passing through node
        estimate = {}

        for node in self.vertices:
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
                return Graph.reconstruct_path(destination, parent)

            closed.append(node)

            for neighbor in self.adj(node):
                if neighbor in closed:
                    continue
                if neighbor not in pq:
                    pq.insert(neighbor, estimate[neighbor])

                # check the distance from source to neighbor
                # todo: make sure that weight is what I actually want here
                length = dist[node] + self.weight(node, neighbor)

                # update!
                if length < dist[neighbor]:
                    parent[neighbor] = node
                    dist[neighbor] = length
                    estimate[neighbor] = length + heuristic(neighbor, destination)
                    pq.update_priority(neighbor, estimate[neighbor])

        # didn't find a path
        return None

    def shortest_path(self, sources=None, destinations=None):
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
            sources = self.vertices
        if destinations is None:
            # iterate over all possible destinations
            destinations = self.vertices

        if self.weighted:
            # dijkstra's
            pass
        else:
            # BFS
            pass

    def shortest_path_length(self, source=None, destination=None):
        # todo: write this
        # same as shortest_path
        if source is None:
            # iterate over all possible sources
            pass
        if destination is None:
            # iterate over all possible destinations
            pass

        if self.weighted:
            # dijkstra's
            pass
        else:
            # BFS
            pass

    # shortest path on a weighted graph. Dijkstra's Alg
    # runtime: O(E + V log V), but since E \in O(V^2), we get
    #    O(V^2) essentially.
    # Dijkstra's algorithm
    def weighted_shortest_paths(self, source):
        # todo: merge this into shortest_path and shortest_path_length
        pq = PriorityQueue()

        dist = {}
        parent = {}

        for v in self.vertices:
            if v == source:
                dist[v] = 0
            else:
                dist[v] = inf

            parent[v] = None

            pq.insert(v, dist[v])

        while pq:
            node = pq.extract()

            for neighbor in self.adj(node):
                length = dist[node] + self.weight(node, neighbor)
                # update
                if length < dist[neighbor]:
                    dist[neighbor] = length
                    parent[neighbor] = node
                    pq.update_priority(neighbor, length)

        return namedtuple("Shortest_Path", ["length", "parent"])(dist, parent)

    # note that if the graph isn't connected, every eccentricity will be infinite
    def eccentricity(self, nodes=None):
        # don't recompute eccentricity unless we absolutely need to
        if self._ecc is None:
            # start by selecting the largest lower bound
            high = False

            possibilities = self.vertices

            # ecc = dict.fromkeys(nodes, 0)
            # are these initial bounds what they should be? Does it matter?
            # if we have a connected graph G of order n, the min ecc would be 1 if G is K_n, and the max ecc would be
            # n-1 if G is P_n (i.e. complete graph on n nodes and path on n nodes respectively)
            lower = dict.fromkeys(possibilities, -inf)
            upper = dict.fromkeys(possibilities, inf)

            # choose the first node as the node which has the highest degree
            minlower = max(possibilities, key=lambda x: self.degree(x))
            # maxupper won't be used in the first time through the loop, so make it None
            maxupper = None

            while possibilities:
                if high:
                    promising = maxupper
                else:
                    promising = minlower

                # as per Takes and Kosters, alternate between choosing node with the maximum upper bound and the node
                # with the minimum lower bound.
                high = not high

                # is there a way to speed this up, instead of just doing a BFS from promising?
                bfs = self.breadth_first_search(promising)
                # compute eccentricity of promising node
                # todo: I'll have to change how this is written once I rewrite shortest_path
                ecc_promising = max(bfs.level.values())

                for node in possibilities:
                    lower[node] = max(lower[node], ecc_promising - bfs.level[node], bfs.level[node])
                    upper[node] = min(upper[node], ecc_promising + bfs.level[node])

                    # is there a good way to put a bound on how many nodes are removed every time through the loop?
                    if lower[node] == upper[node]:
                        possibilities.remove(node)

                minlower = None
                maxupper = None

                # loop through the nodes remaining in possibilities and update minlower/maxupper.
                # ties in bound are broken by selecting the node with the highest degree.
                # can I combine this for loop with the previous for loop?  make it the else clause from the if statement
                # that checks for removing nodes?
                for node in possibilities:
                    if minlower is None \
                            or (lower[node] == lower[minlower] and self.degree(node) > self.degree(minlower)) \
                            or (lower[node] < lower[minlower]):
                        minlower = node

                    if maxupper is None \
                            or (upper[node] == upper[maxupper] and self.degree(node) > self.degree(maxupper)) \
                            or (upper[node] > upper[maxupper]):
                        maxupper = node
            self._ecc = lower

        if nodes is None:
            ecc = self._ecc
        else:
            ecc = {node: self._ecc[node] for node in nodes}

        return ecc

    @property
    def radius(self):
        # min eccentricity
        return min(self.eccentricity().values())

    @property
    def diameter(self):
        # max eccentricity
        return max(self.eccentricity().values())

    @property
    def center(self):
        # those nodes whose eccentricity == radius
        return [node for node in self.vertices if self.eccentricity()[node] == self.radius]

    @property
    def periphery(self):
        # those nodes whose eccentricity == diameter
        return [node for node in self.vertices if self.eccentricity()[node] == self.diameter]

    # todo: write this
    def contract_edge(self, node1, node2):
        pass

    # todo: write this
    def classify_edges(self):
        pass
