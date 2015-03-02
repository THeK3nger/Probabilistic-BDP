from unittest import TestCase
from pbdp.model.map import LogicalMap
from pbdp.model.vector2d import Vec2d

__author__ = 'davide'


class TestLogicalMap(TestCase):

    def setUp(self):
        self.testing_map = LogicalMap("../maps/arena.map")

    def test_cost(self):
        self.assertEqual(self.testing_map.cost(Vec2d(5, 5), Vec2d(6, 5)), 1)
        self.assertEqual(self.testing_map.cost(Vec2d(5, 5), Vec2d(6, 6)), 2**0.5)
        self.assertEqual(self.testing_map.cost(Vec2d(0, 0), Vec2d(0, 1)), float('inf'))
        self.assertEqual(self.testing_map.cost(Vec2d(2, 2), Vec2d(1, 3)), float('inf'))

    def test_enumerate(self):
        for t in self.testing_map.enumerate():
            (map_val, position) = t
            self.assertEqual(map_val, self.testing_map[position])

    def test_is_traversable(self):
        self.assertTrue(self.testing_map.is_traversable((5, 5)))
        self.assertFalse(self.testing_map.is_traversable((0, 0)))