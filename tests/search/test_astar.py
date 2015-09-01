from unittest import TestCase

from pbdp.model.map import LogicalMap, distance_euclidean
from pbdp.model.vector2d import Vec2d
from pbdp.search.astar import astar

__author__ = 'davide'


class TestAstar(TestCase):

    def setUp(self):
        self.testing_map = LogicalMap("./maps/arena.map")

    def test_astar(self):
        # Start Equal To End
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(5, 5), distance_euclidean)
        self.assertEqual([Vec2d(5, 5)], path[0])

        # Start Unreachable
        path = astar(self.testing_map, Vec2d(0, 0), Vec2d(5, 5), distance_euclidean)
        self.assertEqual([], path[0])

        # End Unreachable
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(0, 0), distance_euclidean)
        self.assertEqual([], path[0])

        # A Good Path
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(30, 30), distance_euclidean)
        print(len(path))
        self.assertEqual(31, len(path[0]))
