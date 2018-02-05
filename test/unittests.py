import unittest
from unittest import TestCase
import DataStructures


class GraphTestCase(TestCase):

    def setUp(self):

        # empty graph
        self.empty = DataStructures.Graph()

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

        # non simple, directed graph (cyclic)
        self.digraphdata = {"a": ["b", "d"],
                            "b": ["e"],
                            "c": ["e", "f"],
                            "d": ["b"],
                            "e": ["d"],
                            "f": ["f"],
                            }

        # directed acyclic graph
        self.DAGdata = {"a": ["b", "d"],
                        "b": ["e"],
                        "c": ["e", "f"],
                        "d": [],
                        "e": ["d"],
                        "f": [],
                        }

        self.graph = DataStructures.Graph(self.graphdata)
        self.digraph = DataStructures.Graph(self.digraphdata)
        self.DAG = DataStructures.Graph(self.DAGdata)

    def test_vertices(self):
        # make sure that empty.vertices is an empty list
        self.assertEquals(len(self.empty.vertices), 0, "unexpected empty graph vertices")

        # test graph vertices
        nodes = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for node in nodes:
            with self.subTest(node=node):
                self.assertIn(node, self.graph.vertices,
                              "node {0} unexpectedly not in graph".format(repr(node)))

        self.assertCountEqual(self.graph.vertices, nodes, "unexpected nodes in graph")

        nodes = ["a", "b", "c", "d", "e", "f"]
        for node in nodes:
            with self.subTest(node=node):
                self.assertIn(node, self.digraph.vertices,
                              "node {0} unexpectedly not in digraph".format(repr(node)))

                self.assertIn(node, self.DAG.vertices,
                              "node {0} unexpectedly not in DAG".format(repr(node)))

        self.assertCountEqual(self.digraph.vertices, nodes, "unexpected nodes in digraph")
        self.assertCountEqual(self.DAG.vertices, nodes, "unexpected nodes in DAG")

    def test_edges(self):

        # empty graph
        self.assertEquals(len(self.empty.edges), 0, "unexpected empty graph edges present")

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

        # test digraph edges
        edges = [("a", "b"), ("a", "d"),
                 ("b", "e"),
                 ("c", "e"), ("c", "f"),
                 ("d", "b"),
                 ("e", "d"),
                 ("f", "f"),
                 ]

        for edge in edges:
            with self.subTest(edge=edge):
                self.assertIn(edge, self.digraph.edges,
                              "edge {0} unexpectedly not present in digraph".format(repr(edge)))

        self.assertCountEqual(self.digraph.edges, edges, "unexpected digraph edges present")

        # test DAG edges
        edges = [("a", "b"), ("a", "d"),
                 ("b", "e"),
                 ("c", "e"), ("c", "f"),
                 ("e", "d"),
                 ]

        for edge in edges:
            with self.subTest(edge=edge):
                self.assertIn(edge, self.DAG.edges,
                              "edge {0} unexpectedly not present in DAG".format(repr(edge)))

        self.assertCountEqual(self.DAG.edges, edges, "unexpected dag edges")

    def test_adj(self):
        for node in self.graphdata:
            with self.subTest(node=node):
                self.assertEqual(self.graph.adj(node), self.graphdata[node],
                                 "node {0} graph adj incorrect".format(repr(node)))

        for node in self.digraphdata:
            with self.subTest(node=node):
                self.assertEqual(self.digraph.adj(node), self.digraphdata[node],
                                 "node {0} digraph adj incorrect".format(repr(node)))

        for node in self.DAGdata:
            with self.subTest(node=node):
                self.assertEqual(self.DAG.adj(node), self.DAGdata[node],
                                 "node {0} DAG adj incorrect")

    def test_add_node(self):
        # add a node to the graph
        self.graph.add_node("k")
        self.assertIn("k", self.graph.vertices, "graph node not added")

        # add a note already in the graph, to the graph
        # should raise ValueError
        with self.assertRaises(ValueError, msg="ValueError not raised when adding duplicate node"):
            self.graph.add_node("a")

    def test_remove_directed_edge(self):
        # check removing an edge already present (nominal case)
        self.assertIn(("a", "b"), self.digraph.edges, "edge (a, b) unexpectedly not in graph")
        self.digraph.remove_directed_edge("a", "b")
        self.assertNotIn(("a", "b"), self.digraph.edges, "edge (a, b) unexpectedly in graph after removal")

        # check removing an edge not present, but both nodes are. should raise ValueError with message
        # "Edge {0} not present in graph"
        with self.assertRaisesRegex(ValueError, "Edge", msg="ValueError not raised when removing nonexistent edge"):
            self.digraph.remove_directed_edge("a", "b")

        # check removing an edge with node(s) not present. should raise ValueError with message
        # "Node {0} not present in graph"
        self.assertNotIn("y", self.digraph.vertices, "node y unexpectedly in graph")
        self.assertNotIn("z", self.digraph.vertices, "node z unexpectedly in graph")

        with self.assertRaisesRegex(ValueError, "Node", msg="ValueError not raised when removing"
                                    "edge with nonexistent nodes"):

            self.digraph.remove_directed_edge("y", "z")

    def test_remove_undirected_edge(self):
        self.assertIn(("a", "b"), self.graph.edges, "edge (a, b) unexpectedly not in graph")
        self.assertIn(("b", "a"), self.graph.edges, "edge (b, a) unexpectedly not in graph")
        self.graph.remove_undirected_edge("a", "b")
        self.assertNotIn(("a", "b"), self.graph.edges, "edge (a, b) unexpectedly in graph after removal")
        self.assertNotIn(("b", "a"), self.graph.edges, "edge (b, a) unexpectedly in graph after removal")

    def test_remove_node(self):
        # verify node is present before removal
        self.assertIn("g", self.graph.vertices, "vertex g unexpectedly not in graph")

        # verify edges present before removal
        for node in ["c", "d", "f", "h"]:
            with self.subTest(node=node):
                # check edge (g, node)
                self.assertIn(("g", node), self.graph.edges,
                              "edge (g, {0}) unexpectedly not in graph".format(repr(node)))
                # check edge (node, g)
                self.assertIn((node, "g"), self.graph.edges,
                              "edge ({0}, g) unexpectedly not in graph".format(repr(node)))

        # bye bye node
        self.graph.remove_node("g")

        # verify node removed
        self.assertNotIn("g", self.graph.vertices, "vertex g unexpectedly in graph")

        # verify edges removed
        for node in ["c", "d", "f", "h"]:
            with self.subTest(node=node):
                # check edge (g, node)
                self.assertNotIn(("g", node), self.graph.edges,
                                 "edge (g, {0}) unexpectedly in graph".format(repr(node)))
                # check edge (node, g)
                self.assertNotIn((node, "g"), self.graph.edges,
                                 "edge ({0}, g) unexpectedly in graph".format(repr(node)))

        # test removing node not in graph
        self.assertNotIn("z", self.graph.vertices, "node z unexpectedly in graph")
        with self.assertRaises(ValueError,
                               msg="ValueError unexpectedly not raised when removing nonexistent node"):
            self.graph.remove_node("z")

    @unittest.skip("skipping BFS...test not written")
    def test_breadth_first_search(self):
        pass

    @unittest.skip("skipping DFS...test not written")
    def test_depth_first_search(self):
        pass

    @unittest.skip("skipping topological sort...test not written")
    def test_topological_sort(self):
        pass

    @unittest.skip("skipping _dfs...test not written")
    # dfs/topo-sort helper function
    def test_dfs(self):
        pass

    def test_is_cyclic(self):
        self.assertTrue(self.graph.is_cyclic(), "graph unexpectedly acyclic")
        self.assertTrue(self.digraph.is_cyclic(), "digraph unexpectedly acyclic")
        self.assertFalse(self.DAG.is_cyclic(), "DAG unexpectedly cyclic")

    # todo: rewrite Graph.shortest_path() so that it works
    # todo: rewrite Graph so it handles weighted graphs
    @unittest.skip("skipping shortest path...graph class doesn't handle weighted edges yet")
    def test_shortest_path(self):
        pass


@unittest.skip("Skipping Heap...not written yet")
class HeapTestCase(TestCase):
    pass


class StackTestCase(TestCase):

    def setUp(self):
        self.stack = DataStructures.Stack()
        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.stack.push(letter)

        self.emptystack = DataStructures.Stack()

    def test_len(self):
        self.assertEqual(len(self.stack), 26, "Stack missing items")
        self.assertEqual(len(self.emptystack), 0, "Empty stack has something")

        # check adding an item to the stack increases its length by 1
        item = "aa"
        self.stack.push(item)
        self.emptystack.push(item)
        self.assertEqual(len(self.stack), 27)
        self.assertEqual(len(self.emptystack), 1)

        self.stack.pop()
        self.emptystack.pop()
        self.assertEquals(len(self.stack), 26)
        self.assertEquals(len(self.emptystack), 0)

    def test_str(self):
        letters = "abcdefghijklmnopqrstuvwxyz"
        string = str([letter for letter in letters])
        self.assertEqual(str(self.stack), string, "Stack string not equal")

        self.assertEqual(str(self.emptystack), str([]), "Empty stack string not equal")

    def test_bool(self):
        self.assertTrue(self.stack, "Stack is not true")
        self.assertFalse(self.emptystack, "Empty stack not false")

    def test_push(self):
        item = "aa"
        self.assertNotIn(item, self.stack._data, "item got into stack before push")
        self.stack.push(item)
        self.assertIn(item, self.stack._data, "item not in stack after push")
        self.assertEquals(item, self.stack._data[-1], "pushed item in wrong place")

    def test_pop(self):
        self.assertEqual(self.stack.pop(), "z", "Got a wrong thing from the pop")

        with self.assertRaises(IndexError, msg="Empty stack pop didn't raise IndexError"):
            self.emptystack.pop()

    def test_peek(self):
        self.assertEqual(self.stack.peek(), "z", "Got wrong item from peek")

        with self.assertRaises(IndexError, msg="Empty stack peek didn't raise IndexError"):
            self.emptystack.peek()

    def test_make_empty(self):
        self.assertTrue(self.stack)
        self.assertEqual(len(self.stack), 26)
        self.stack.make_empty()
        self.assertFalse(self.stack)
        self.assertEqual(len(self.stack), 0)
        self.assertListEqual(self.stack._data, [])
