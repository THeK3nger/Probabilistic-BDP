from unittest import TestCase

__author__ = 'davide'

from pbdp.collections.graph import Graph


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