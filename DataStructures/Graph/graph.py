from collections import namedtuple
from math import inf
from DataStructures import PriorityQueue


class Graph(object):
    # todo: ideally, you wouldn't have to specify a graph as weighted
    # todo: make sure the new __init__ actually works with the rewritten adding nodes/edges
    def __init__(self, graph_data=None, weighted=False):

        if graph_data is None:
            graph_data = {}

        self._adj = {}
        self._pred = {}
        self._weight = {}

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

    def __contains__(self, item):
        return item in self._adj

    def __iter__(self):
        return iter(self._adj)

    def __len__(self):
        return len(self._adj)

    @property
    def vertices(self):
        return list(self._adj.keys())

    @property
    def edges(self):
        return self._adj.items()

    @property
    def weighted(self):
        return self._weighted

    @staticmethod
    def reconstruct_path(destination, parent_dict):
        if destination not in parent_dict:
            raise ValueError("Destination {0} not present in dictionary".format(repr(destination)))

        path = []

        def recon(node):
            path.insert(0, node)

            if not parent_dict[node]:
                return path

            return recon(node, parent_dict[node])

        return recon(0, destination)

    def adj(self, node):
        return self._adj[node]

    def pred(self, node):
        return self._pred[node]

    def is_adj(self, node1, node2):
        return node2 in self._adj[node1]

    # get the weight of an edge between node1, node2
    def weight(self, node1, node2):
        if self.weighted:
            weight = self._weight[(node1, node2)]
        else:
            weight = 1

        return weight

    def add_node(self, node):
        # add an unconnected vertex to the graph
        if node not in self:
            self._adj[node] = []
            self._pred[node] = []
        else:
            raise ValueError("Node {0} already present in graph".format(repr(node)))

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

    def add_undirected_edge(self, node1, node2, weight=None):
        self.add_directed_edge(node1, node2, weight)
        self.add_directed_edge(node2, node1, weight)

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

    def remove_undirected_edge(self, node1, node2):
        self.remove_directed_edge(node1, node2)
        self.remove_directed_edge(node2, node1)

    def remove_node(self, node):
        if node in self:
            # get vertices that node points to
            removal = [(node, neighbor) for neighbor in self.adj(node)]
            # get vertices that point to node
            # todo: make sure that this doesn't screw up with undirected graphs
            removal.extend([(neighbor, node) for neighbor in self.pred(node)])

            # then get rid of the edges
            for x, y in removal:
                self.remove_directed_edge(x, y)

            # then clear out node's dict entries
            del self._adj[node]
            del self._pred[node]
        else:
            raise ValueError("Node {0} not present in graph".format(repr(node)))

    # runtime O(V + E) and E \in O(V^2) so O(V^2)
    def breadth_first_search(self, node):
        # maybe modify this so that it doesn't return the namedtuple?
        level = {node: 0}
        parent = {node: None}
        i = 1
        frontier = [node]
        while frontier:
            nextfrontier = []
            for node in frontier:
                for neighbor in self.adj(node):
                    if neighbor not in level:
                        level[neighbor] = i
                        parent[neighbor] = node
                        nextfrontier.append(neighbor)
            frontier = nextfrontier
            i += 1

        return namedtuple("BFS", ["level", "parent"])(level, parent)

    # runtime: O(V + E) and E \in O(V^2) so O(V^2)
    def depth_first_search(self):
        return self._dfs()[0]

    def topological_sort(self):
        return self._dfs()[1]

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

        return [parent, topo]

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

    # shortest path on a weighted graph. Dijkstra's Alg
    # runtime: O(E + V log V), but since E \in O(V^2), we get
    #    O(V^2) essentially.
    # Dijkstra's algorithm
    def shortest_path(self, source):
        q = PriorityQueue()

        dist = {}
        parent = {}

        for v in self.vertices:
            if v == source:
                dist[v] = 0
            else:
                dist[v] = inf

            parent[v] = None

            q.insert(v, dist[v])

        while not q.is_empty():
            node = q.extract()

            for neighbor in self.adj(node):
                length = dist[node] + self.weight(node, neighbor)
                # update
                if length < dist[neighbor]:
                    dist[neighbor] = length
                    parent[neighbor] = node
                    q.update_key(neighbor, length)

        return namedtuple("Shortest_Path", ["length", "parent"])(dist, parent)

    # todo: write this
    def contract_edge(self, node1, node2):
        pass

    # todo: write this
    def classify_edges(self):
        pass
