from unittest import TestCase

__author__ = 'davide'

from pbdp.model.map import LogicalMap
from pbdp.model.hierarchical_map import HierarchicalMap


class TestHierarchicalMap(TestCase):
    def setUp(self):
        self.abstraction = HierarchicalMap(LogicalMap("./maps/arena.map"), 0.2)

    def test_cluster_width(self):
        self.assertEqual(5, self.abstraction.cluster_width)

    def test_cluster_height(self):
        self.assertEqual(5, self.abstraction.cluster_height)

    def test_generate_abstract_graph(self):
        self.abstraction.generate_abstract_graph()
        self.assertTrue(True)

    def test_get_all_in_cluster(self):
        self.abstraction.generate_abstract_graph()
        entrances = self.abstraction.get_all_in_cluster((0, 0))
        self.assertEqual(2, len(entrances))
        self.assertEqual({(9, 5), (5, 9)}, set(entrances))

    def test_get_tile_cluster(self):
        self.assertEqual((0, 0), self.abstraction.get_tile_cluster((5, 5)))