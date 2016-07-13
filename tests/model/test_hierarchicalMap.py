from unittest import TestCase, skipIf

import os

__author__ = 'davide'

from pbdp.model.map import LogicalMap
from pbdp.model.hierarchical_map import HierarchicalMap, PlotMap


class TestHierarchicalMap(TestCase):
    def setUp(self):
        self.abstraction = HierarchicalMap(LogicalMap("./maps/arena.map"), 0.2)
        self.abstraction.generate_abstract_graph()

    def test_cluster_width(self):
        self.assertEqual(5, self.abstraction.cluster_width)

    def test_cluster_height(self):
        self.assertEqual(5, self.abstraction.cluster_height)

    def test_generate_abstract_graph(self):
        # TODO: Check only runtime error! No validity check!
        self.abstraction.generate_abstract_graph()
        self.assertTrue(True)

    def test_get_all_in_cluster(self):
        self.abstraction.generate_abstract_graph()
        entrances = self.abstraction.get_all_in_cluster((0, 0))
        self.assertEqual(4, len(entrances))
        self.assertEqual({(9, 5), (5, 9)}, set(entrances))

    def test_get_tile_cluster(self):
        self.assertEqual((0, 0), self.abstraction.get_tile_cluster((5, 5)))

    def test_is_traversable(self):
        self.abstraction.generate_abstract_graph()
        self.assertTrue(self.abstraction.is_traversable((9,5),(5,9)))
        self.abstraction.close_edge(((9,5),(5,9)))
        self.assertFalse(self.abstraction.is_traversable((9,5),(5,9)))

    def test_is_node(self):
        self.assertTrue(self.abstraction.is_node((9, 5)))
        self.assertFalse(self.abstraction.is_node((10, 24)))


# class TestHierarchicalMapPNGWriter(TestCase):
#
#     def setUp(self):
#         self.abstraction = HierarchicalMap(LogicalMap("./maps/arena.map"), 0.2)
#         self.abstraction.generate_abstract_graph()
#         self.dumpydumper = HierarchicalMapPNGExporter(self.abstraction)
#
#     def test_image(self):
#         self.dumpydumper.dump_image()


@skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
class TestPlotMap(TestCase):

    def setUp(self):
        self.abstraction = HierarchicalMap(LogicalMap("./maps/arena.map"), 0.2)
        self.abstraction.generate_abstract_graph()
        self.plotter = PlotMap(self.abstraction)

    def test_plot(self):
        self.plotter.plot(save_to_png=True)