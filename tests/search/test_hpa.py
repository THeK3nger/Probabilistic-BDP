from unittest import TestCase

from pbdp.model.hierarchical_map import HierarchicalMap
from pbdp.model.map import LogicalMap, distance_euclidean
from pbdp.model.vector2d import Vec2d

from pbdp.search.hpa import hpa


class TestHpa(TestCase):

    def setUp(self):
        self.base = HierarchicalMap(LogicalMap("./maps/arena.map"), 0.2)
        self.base.generate_abstract_graph()

    def test_hpa(self):
        path = hpa(self.base, (5, 5), (40, 40), distance_euclidean)
        self._print_path(path)
        self.assertTrue(True)  # TODO: Better test. For now, graphical inspection.

    def _print_path(self, path):
        result = ""
        for r in range(self.base.original_map.height):
            for c in range(self.base.original_map.width):
                if Vec2d(r, c) in path:
                    result += "X"
                else:
                    result += str(self.base.original_map[r, c])
            result += "\n"
        print(result)