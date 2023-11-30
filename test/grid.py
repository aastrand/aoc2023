import unittest

from utils.grid import (Grid, adjecent_3d, flood_fill_3d, inside_3d,
                        neighbours_3d)


class TestGrid(unittest.TestCase):

    LINES = [".......#................#......",
             "...#.#.....#.##.....#..#.......",
             "..#..#.#......#.#.#............",
             "....#...#...##.....#..#.....#..",
             "....#.......#.##......#...#..#.",
             "...............#.#.#.....#..#..",
             "...##...#...#..##.###...##.....",
             "##..#.#...##.....#.#..........#",
             ".#....#..#..#......#....#....#."]

    def test_grid_empty(self):
        grid = Grid()
        self.assertEqual(None, grid.minX)
        self.assertEqual(None, grid.maxX)
        self.assertEqual(None, grid.minY)
        self.assertEqual(None, grid.maxY)

        grid.set((10, 10), "#")
        self.assertEqual(10, grid.minX)
        self.assertEqual(10, grid.maxX)
        self.assertEqual(10, grid.minY)
        self.assertEqual(10, grid.maxY)

    def test_grid_from_lines(self):
        grid = Grid.from_lines(self.LINES)
        self.assertEqual(0, grid.minX)
        self.assertEqual(30, grid.maxX)
        self.assertEqual(0, grid.minY)
        self.assertEqual(8, grid.maxY)

    def test_grid_print_output(self):
        grid = Grid.from_lines(self.LINES)
        self.assertEqual(self.LINES, grid.print_output())

    def test_mutation(self):
        grid = Grid.from_lines(self.LINES)
        self.assertEqual(None, grid.get((-1, -1)))
        self.assertEqual('.', grid.get((1, 1)))
        self.assertEqual('#', grid.get((2, 2)))

        grid.set((100, 100), '#')
        self.assertEqual('#', grid.get((100, 100)))
        self.assertEqual(100, grid.maxX)
        self.assertEqual(100, grid.maxY)

    def test_flood_fill(self):
        lines = ["......",
                 ".####.",
                 ".#..#.",
                 ".####.",
                 "......"]
        grid = Grid.from_lines(lines)

        visitor_set = set()
        visited = grid.flood_fill((0, 0), lambda g, p: visitor_set.add(p))

        self.assertTrue((5, 4) in visited)
        self.assertTrue((1, 1) not in visited)
        self.assertTrue((2, 2) not in visited)
        self.assertEqual(18, len(visited))
        self.assertEqual(visitor_set, visited)

    def test_adjecent_3d(self):
        self.assertFalse(adjecent_3d((1, 2, 3), (6, 7, 8)))
        self.assertTrue(adjecent_3d((1, 1, 1), (2, 1, 1)))
        self.assertFalse(adjecent_3d((2, 1, 2), (2, 3, 2)))
        self.assertFalse(adjecent_3d((1, 2, 5), (2, 2, 6)))

    def test_inside_3d(self):
        bounds = ((-10, -10, -10), (10, 10, 10))
        self.assertTrue(inside_3d((2, 2, 2), bounds))
        self.assertTrue(inside_3d((10, 10, 10), bounds))
        self.assertFalse(inside_3d((-11, -11, -11), bounds))
        self.assertFalse(inside_3d((10, 10, 11), bounds))

    def test_neighbours_3d(self):
        point = (2, 2, 2)
        neighbours = sorted([n for n in neighbours_3d(point)])
        self.assertEqual([(1, 2, 2), (2, 1, 2), (2, 2, 1),
                          (2, 2, 3), (2, 3, 2), (3, 2, 2)], neighbours)

    def test_flood_fill_3d(self):
        blocked = set()

        # 3x3x3 cube
        for x in range(1, 4):
            for y in range(1, 4):
                for z in range(1, 4):
                    blocked.add((x, y, z))

        # remove middle, blocked length is now 3*3*3 - 1
        blocked.remove((2, 2, 2))

        bounds = ((0, 0, 0), (4, 4, 4))
        visited = flood_fill_3d((0, 0, 0), blocked, bounds)

        self.assertTrue((0, 0, 0) in visited)
        self.assertTrue((4, 4, 4) in visited)
        for b in blocked:
            self.assertTrue(b not in visited)

        # should not reach inner point via fill
        self.assertEqual(((max(bounds[1]) + 1)**3) -
                         (len(blocked) + 1), len(visited))


if __name__ == "__main__":
    unittest.main()
