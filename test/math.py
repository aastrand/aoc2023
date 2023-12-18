import unittest

from utils.math import manhattan_dist, poly_area, sign


class TestMath(unittest.TestCase):
    def test_sign(self):
        self.assertEqual(-1, sign(-4))
        self.assertEqual(1, sign(8))
        self.assertEqual(0, sign(0))

    def test_manhattan_dist(self):
        self.assertEqual(1 + 10, manhattan_dist(0, 4, -10, 3))

    def test_poly_area(self):
        poly = [(0, 0), (0, 10), (10, 10), (10, 0)]
        self.assertEqual(100.0, poly_area(poly))

        poly = [
            (0, 0),
            (461937, 0),
            (461937, 56407),
            (818608, 56407),
            (818608, 919647),
            (1186328, 919647),
            (1186328, 1186328),
            (609066, 1186328),
            (609066, 356353),
            (497056, 356353),
            (497056, 1186328),
            (5411, 1186328),
            (5411, 500254),
            (0, 500254),
            (0, 0),
        ]
        self.assertEqual(952404941483.0, poly_area(poly))


if __name__ == "__main__":
    unittest.main()
