from unittest import TestCase
from random import randint

from pbdp.model.vector2d import Vec2d


class TestVec2d(TestCase):
    def test_magnitude(self):
        x1 = randint(0, 100)
        y1 = randint(0, 100)
        a = Vec2d(x1, y1)
        self.assertAlmostEqual(a.magnitude, (x1 ** 2 + y1 ** 2) ** 0.5)

    def test_is_diagonal_to(self):
        for _ in range(100):
            x1 = randint(0, 100)
            y1 = randint(0, 100)
            v = Vec2d(x1, y1)
            a = Vec2d(x1 + 1, y1 + 1)
            b = Vec2d(x1 + 1, y1)
            c = Vec2d(x1 + 12, y1 + 17)
            self.assertTrue(v.is_diagonal_to(a))
            self.assertFalse(v.is_diagonal_to(b))
            self.assertFalse(v.is_diagonal_to(c))

    def test_vector_creation(self):
        for _ in range(100):
            x1 = randint(0, 100)
            y1 = randint(0, 100)
            v_single = Vec2d(x1, y1)
            v_tuple = Vec2d((x1, y1))
            self.assertEqual(v_single.x, x1)
            self.assertEqual(v_single.y, y1)
            self.assertEqual(v_tuple.x, x1)
            self.assertEqual(v_tuple.y, y1)

    def test_algebraic_operations(self):
        for _ in range(100):
            x1 = randint(0, 100)
            x2 = randint(0, 100)
            y1 = randint(0, 100)
            y2 = randint(0, 100)
            a = Vec2d(x1, y1)
            b = Vec2d(x2, y2)

            # Test Sum
            self.assertEqual(a + b, Vec2d(x1 + x2, y1 + y2))
            self.assertEqual(a + (1, 1), Vec2d(x1 + 1, y1 + 1))
            self.assertEqual(a + 1, Vec2d(x1 + 1, y1 + 1))

            # Test Sub
            self.assertEqual(a - b, Vec2d(x1 - x2, y1 - y2))
            self.assertEqual(a - (1, 1), Vec2d(x1 - 1, y1 - 1))
            self.assertEqual(a - 1, Vec2d(x1 - 1, y1 - 1))

    def testComparison(self):
        for _ in range(100):
            x1 = randint(0, 100)
            y1 = randint(0, 100)
            a = Vec2d(x1, y1)
            b = Vec2d(x1, y1)
            self.assertEqual(a, b)
            self.assertNotEqual(a, Vec2d(200, 300))