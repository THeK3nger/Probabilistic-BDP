from unittest import TestCase

from pbdp.model.hierarchical_map import ExtendedAbstraction, HierarchicalMap
from pbdp.model.map import LogicalMap
from pbdp.model.vector2d import Vec2d


class TestExtendedAbstraction(TestCase):

    def setUp(self):
        self.base = HierarchicalMap(LogicalMap("./maps/arena.map"), 0.2)
        self.base.generate_abstract_graph()
        self.abstraction = ExtendedAbstraction(self.base, (5, 5), (40, 40))

    def test_neighbours(self):
        self.assertEqual(self.abstraction.neighbours((5, 5)), [(5, 9), (9, 5)])

    def test_cost(self):
        self.assertEqual(self.abstraction.cost((5, 5), (7, 7)), float('inf'))
        self.assertEqual(self.abstraction.cost((5, 5), (5, 9)), 4)