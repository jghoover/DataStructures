import unittest

from DataStructures import Graph


class GraphTestCase(unittest.TestCase):
    def setUp(self):

        # empty graph
        self.empty = Graph()

        # simple graph
        self.graphdata = {"a": ["b", "e"],
                          "b": ["a", "f"],
                          "c": ["d", "f", "g"],
                          "d": ["c", "g", "h"],
                          "e": ["a"],
                          "f": ["b", "c", "g"],
                          "g": ["c", "d", "f", "h"],
                          "h": ["d", "g"],
                          }

        self.graph = Graph(self.graphdata)

    def test_vertices(self):
        # make sure that empty.vertices is an empty list
        self.assertEqual(len(self.empty.vertices), 0, "unexpected empty graph vertices")

        # test graph vertices
        nodes = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for node in nodes:
            with self.subTest(node=node):
                self.assertIn(node, self.graph.vertices,
                              "node {0} unexpectedly not in graph".format(repr(node)))

        self.assertCountEqual(self.graph.vertices, nodes, "unexpected nodes in graph")

    def test_edges(self):

        # empty graph
        self.assertEqual(len(self.empty.edges), 0, "unexpected empty graph edges present")

        # test graph edges
        edges = [("a", "b"), ("a", "e"),
                 ("b", "a"), ("b", "f"),
                 ("c", "d"), ("c", "f"), ("c", "g"),
                 ("d", "c"), ("d", "g"), ("d", "h"),
                 ("e", "a"),
                 ("f", "b"), ("f", "c"), ("f", "g"),
                 ("g", "c"), ("g", "d"), ("g", "f"), ("g", "h"),
                 ("h", "d"), ("h", "g")
                 ]

        for edge in edges:
            with self.subTest(edge=edge):
                self.assertIn(edge, self.graph.edges,
                              "edge {0} unexpectedly not present in graph".format(repr(edge)))

        self.assertCountEqual(self.graph.edges, edges, "unexpected graph edges present")

    def test_adj(self):
        for node in self.graphdata:
            with self.subTest(node=node):
                self.assertEqual(self.graph.adj(node), self.graphdata[node],
                                 "node {0} graph adj incorrect".format(repr(node)))


