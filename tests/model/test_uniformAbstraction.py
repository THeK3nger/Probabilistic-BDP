from unittest import TestCase

__author__ = 'davide'

from pbdp.model.map_abstraction import UniformAbstraction
from pbdp.model.map import LogicalMap
from pbdp.model.vector2d import Vec2d

class TestUniformAbstraction(TestCase):

    def setUp(self):
        self.abstraction = UniformAbstraction(LogicalMap("./maps/arena.map"), 0.2)

    def test_generate(self):
        self.abstraction.generate()
        self.assertTrue(True)

    def test__sector_from_tile(self):
        self.assertEqual(self.abstraction._sector_from_tile(Vec2d(0, 0)), 0)
        self.assertEqual(self.abstraction._sector_from_tile(Vec2d(0, 45)), 4)
        self.assertEqual(self.abstraction._sector_from_tile(Vec2d(45, 45)), 24)
        self.assertEqual(self.abstraction._sector_from_tile(Vec2d(15, 25)), 7)

    def test__tiles_in_sector(self):
        self.assertEqual(self.abstraction._tiles_in_sector(self.abstraction._sector_from_tile(Vec2d(15, 25))),
                         [(r, c) for r in range(10, 20) for c in range(20, 30)])

    def test__identify_region(self):
        self.abstraction._identify_region(self.abstraction._sector_from_tile(Vec2d(15, 15)))
        self.assertTrue(True)