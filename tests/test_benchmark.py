__author__ = 'davide'

from unittest import TestCase

from pbdp.model.map import LogicalMap
import pbdp.benchmark as benchmark

class TestBenchmarkTools(TestCase):

    def test_all_maps(self):
        # TODO: The "1" is temporary. This should be the amount of maps in the test folder.
        map_db = benchmark.maps_loader()
        self.assertTrue(len(map_db) == 1)

    def test_random_free(self):
        # TODO: It is hard to test that random free is a uniform distribution.
        # For now we just check if random_free returns only free tiles.
        map = LogicalMap("./maps/arena.map")
        for _ in range(100):
            random_cell = benchmark.random_free_cell(map)
            self.assertTrue(map.is_traversable(random_cell))
