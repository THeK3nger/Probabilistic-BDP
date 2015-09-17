from unittest import TestCase

from pbdp.model.map import LogicalMap, distance_euclidean
from pbdp.model.vector2d import Vec2d
from pbdp.search.astar import astar

__author__ = 'davide'


class TestAstar(TestCase):

    def setUp(self):
        self.testing_map = LogicalMap("./maps/arena.map")

    def test_astar_path_only(self):
        config = {'path_only': True}

        # Start Equal To End
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(5, 5), distance_euclidean, config)
        self.assertEqual([Vec2d(5, 5)], path)

        # Start Unreachable
        path = astar(self.testing_map, Vec2d(0, 0), Vec2d(5, 5), distance_euclidean, config)
        self.assertEqual([], path)

        # End Unreachable
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(0, 0), distance_euclidean, config)
        self.assertEqual([], path)

        # A Good Path
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(30, 30), distance_euclidean, config)
        self.assertEqual(31, len(path))

    def test_astar_path_and_cost(self):
        config = {}  # Path Only = FALSE, Profile = FALSE

        # Start Equal To End
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(5, 5), distance_euclidean, config)
        self.assertEqual([Vec2d(5, 5)], path[0])

        # Start Unreachable
        path = astar(self.testing_map, Vec2d(0, 0), Vec2d(5, 5), distance_euclidean, config)
        self.assertEqual([], path[0])

        # End Unreachable
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(0, 0), distance_euclidean, config)
        self.assertEqual([], path[0])

        # A Good Path
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(30, 30), distance_euclidean, config)
        self.assertEqual(31, len(path[0]))

    def test_astar_profile(self):
        config = {'profile': True}  # Path Only = FALSE, Profile = TRUE

        # Start Equal To End
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(5, 5), distance_euclidean, config)
        self.assertEqual([Vec2d(5, 5)], path[0])
        self.assertTrue('expanded' in path[2])

        # Start Unreachable
        path = astar(self.testing_map, Vec2d(0, 0), Vec2d(5, 5), distance_euclidean, config)
        self.assertEqual([], path[0])
        self.assertTrue('expanded' in path[2])

        # End Unreachable
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(0, 0), distance_euclidean, config)
        self.assertEqual([], path[0])
        self.assertTrue('expanded' in path[2])

        # A Good Path
        path = astar(self.testing_map, Vec2d(5, 5), Vec2d(30, 30), distance_euclidean, config)
        self.assertEqual(31, len(path[0]))
        self.assertTrue('expanded' in path[2])
