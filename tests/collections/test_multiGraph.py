from unittest import TestCase

__author__ = 'davide'

from pbdp.collections.graph import MultiGraph


class TestMultiGraph(TestCase):
    def test_add(self):
        graph = MultiGraph()
        graph.add_node(1)
        graph.add_node(2, meta="Test Label")
        graph.add_edge(1, 2)
        graph.add_edge(1, 2, "bis")
        graph.add_edge(2, 3)
        self.assertIn(1, graph)
        self.assertIn(2, graph)
        self.assertIn(3, graph)
        self.assertEqual("Test Label", graph.get_vertex_label(2))

    def test_update_node_label(self):
        graph = MultiGraph()
        graph.add_node(1)
        graph.add_node(2, meta="Test Label")
        graph.update_node_label(2, "Changed")
        self.assertEqual("Changed", graph.get_vertex_label(2))

    def test_update_edge_label(self):
        graph = MultiGraph()
        graph.add_edge(1, 2, "bis")
        graph.update_edge_label(("bis", (1, 2)), "New Meta")
        self.assertEqual("New Meta", graph.get_edge_label(("bis", (1, 2))))

    def test_neighbours(self):
        graph = MultiGraph()
        graph.add_node(1)
        graph.add_node(2, meta="Test Label")
        graph.add_edge(1, 2)
        graph.add_edge(1, 2, "bis")
        graph.add_edge(2, 3)
        self.assertEqual(set([(hash((1, 2)), (1, 2)), ("bis",(1,2))]), graph.neighbours(1))