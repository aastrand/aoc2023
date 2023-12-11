import unittest

from utils.math import manhattan_dist, sign


class TestMath(unittest.TestCase):
    def test_sign(self):
        self.assertEqual(-1, sign(-4))
        self.assertEqual(1, sign(8))
        self.assertEqual(0, sign(0))

    def test_manhattan_dist(self):
        self.assertEqual(1 + 10, manhattan_dist(0, 4, -10, 3))


if __name__ == "__main__":
    unittest.main()
