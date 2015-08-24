from unittest import TestCase

__author__ = 'davide'

from pbdp.collections.graph import Graph
from pbdp.collections.graph import ExtendedGraph


class TestGraph(TestCase):
    def test_add(self):
        graph = Graph()
        graph.add_node(1)
        graph.add_node(2, meta="Test Label")
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        self.assertIn(1, graph)
        self.assertIn(2, graph)
        self.assertIn(3, graph)
        self.assertEqual("Test Label", graph.get_vertex_label(2))

    def test_update_node_label(self):
        graph = Graph()
        graph.add_node(1)
        graph.add_node(2, meta="Test Label")
        graph.update_node_label(2, "Changed")
        self.assertEqual("Changed", graph.get_vertex_label(2))

    def test_update_edge_label(self):
        graph = Graph()
        graph.add_edge(1, 2)
        graph.update_edge_label((1, 2), "New Meta")
        self.assertEqual("New Meta", graph.get_edge_label((1, 2)))

    def test_neighbours(self):
        graph = Graph()
        graph.add_node(1)
        graph.add_node(2, meta="Test Label")
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(2, 4)
        self.assertEqual({2}, graph.neighbours(1))
        self.assertEqual({1, 3, 4}, graph.neighbours(2))


class TestExtensionGraph(TestCase):

    def setUp(self):
        self.base_graph = Graph()
        self.base_graph.add_node(1)
        self.base_graph.add_node(2)
        self.base_graph.add_node(3)
        self.base_graph.add_node(4)
        self.base_graph.add_node(5)
        self.base_graph.add_edge(1,2)
        self.base_graph.add_edge(2,3)
        self.base_graph.add_edge(3,4, "Cadolfi")
        self.base_graph.add_edge(4,1)
        self.base_graph.add_edge(1,5)
        self.base_graph.add_edge(2,5)
        self.base_graph.add_edge(3,5)
        self.base_graph.add_edge(4,5)

        self.test_graph = ExtendedGraph(self.base_graph)
        #TODO: I'm obligated to put a label for each adj node. This is bad.
        self.test_graph.add_extended_node("A", [1, 2], ["Cane", "Pizza"])
        self.test_graph.add_extended_node("B", [3, 4])

    def test_vertices(self):
        self.assertSetEqual(set(["A","B",1,2,3,4,5]), set(self.test_graph.vertices))

    def test_neighbours(self):
        self.assertSetEqual(set([1, 2]), set(self.test_graph.neighbours("A")))
        self.assertSetEqual(set(["A", 2, 4, 5]), set(self.test_graph.neighbours(1)))
        self.assertSetEqual(set([1,2,3,4]), set(self.test_graph.neighbours(5)))

    def test_get_edge_label(self):
        self.assertEqual("Cadolfi", self.test_graph.get_edge_label((3,4)))
        self.assertEqual("Cane", self.test_graph.get_edge_label(("A",1)))
        self.assertEqual("Pizza", self.test_graph.get_edge_label((2,"A")))

