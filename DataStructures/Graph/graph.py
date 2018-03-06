from math import inf

from DataStructures.Graph.algorithms import breadth_first_search


class Graph(object):
    # todo: write code to be able to generate a graph from a function (implicitly generated graph)
    # todo: rewrite so it works with kwargs and weight
    # todo: would it be easier to generate the graph from a list of edges?
    #    i.e. define what a node looks like and define a function that generates an edge
    def __init__(self, graph_data=None):

        if graph_data is None:
            graph_data = {}

        self._adj = {}
        self._node = {}
        self._edge = {}
        self._ecc = None

        # add nodes and edges
        for node in graph_data.keys():
            # add node, if not already present
            if node not in self:
                self.add_node(node)

            for adj in graph_data[node]:
                # add adj, if not already present
                if adj not in self:
                    self.add_node(adj)
                self.add_edge(node, adj)

    def _maximally_connected(self):
        # return the maximally connected subset of self.vertices
        # could compute the multiplicity of 0 as an eigenvalue of the Laplacean matrix of the graph
        # probably easier to just do DFS or BFS and see if everything is reached

        # do a BFS from the node with the max degree
        connected_to_node = []
        disconnected_from_node = []
        node = max(self.vertices, key=self.degree)
        discarded = []

        # todo: figure out a better conditional for this
        while len(connected_to_node) <= len(disconnected_from_node):
            # get the levels of each node
            bfs = breadth_first_search(self, node).level
            # filter out the nodes that we've already checked
            nodes = {vertex: bfs[vertex] for vertex in bfs if vertex not in discarded}
            # partition set of nodes into connected and unconnected
            connected_to_node = [node for node in nodes if nodes[node] < inf]
            disconnected_from_node = [node for node in nodes if nodes[node] == inf]
            # throw away the nodes that are connected, for the next pass through the loop
            discarded.extend(connected_to_node)
            # find the next node to search from
            if len(disconnected_from_node) <= 0:
                break
            else:
                node = max(disconnected_from_node, key=self.degree)

        return connected_to_node

    @classmethod
    def subgraph(cls, graph, filter_nodes=None, filter_edges=None):
        if filter_nodes is None:
            pass
        if filter_edges is None:
            pass

    @classmethod
    def induced_subgraph(cls, graph, filter_nodes=None):
        # construct a new subgraph from `graph`, based on nodes that satisfy `filter`
        if filter_nodes is None:
            filter_nodes = Graph._maximally_connected

        # get the vertices that we want still in the graph
        vertices = filter_nodes(graph)

        # get the edges that we want still in the graph
        # could also just construct a duplicate graph and the remove every node not in vertices, but that would be slow
        data = dict.fromkeys(vertices)
        for node in data:
            data[node] = [vertex for vertex in graph.adj(node) if vertex in vertices]

        return Graph(data)

    def __contains__(self, item):
        return item in self._adj

    def __iter__(self):
        return iter(self._adj)

    def __len__(self):
        return self.order

    def __repr__(self):
        return repr(self._adj)

    @property
    def vertices(self):
        return list(self._adj.keys())

    @property
    def edges(self):
        return [(node, neighbor) for node, neighbors in self._adj.items() for neighbor in neighbors]

    @property
    def order(self):
        return len(self.vertices)

    def degree(self, node):
        return len(self.adj(node))

    def adj(self, node):
        return self._adj[node]

    def is_adj(self, node1, node2):
        return node2 in self._adj[node1]

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        # add an unconnected vertex to the graph
        # if the node is already present, don't do anything
        if node not in self:
            self._adj[node] = []
            # eccentricity dict is no longer valid, so reset it to None
            self._ecc = None

    def add_edge(self, node1, node2):
        # make sure both nodes are present
        for node in node1, node2:
            if node not in self:
                self.add_node(node)

        # if the edge is already present, don't do anything
        # todo: investigate as to whether this can cause duplicate edges to appear
        if node2 not in self.adj(node1) and node1 not in self.adj(node2):
            self._adj[node1].append(node2)
            self._adj[node2].append(node1)

    def add_edges(self, edges):
        for node1, node2 in edges:
            self.add_edge(node1, node2)

    def remove_node(self, node):
        pass

    def remove_nodes(self, nodes):
        pass

    def remove_edge(self, node1, node2):
        pass

    def remove_edges(self, edges):
        pass

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
                # todo: make sure i'm passing args in the right way
                bfs = breadth_first_search(self, promising)
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
