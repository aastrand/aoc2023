import unittest

from utils.grid import Grid, adjecent_3d, flood_fill_3d, inside_3d, neighbours_3d, rot_90


class TestGrid(unittest.TestCase):
    LINES = [
        ".......#................#......",
        "...#.#.....#.##.....#..#.......",
        "..#..#.#......#.#.#............",
        "....#...#...##.....#..#.....#..",
        "....#.......#.##......#...#..#.",
        "...............#.#.#.....#..#..",
        "...##...#...#..##.###...##.....",
        "##..#.#...##.....#.#..........#",
        ".#....#..#..#......#....#....#.",
    ]

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
        self.assertEqual(".", grid.get((1, 1)))
        self.assertEqual("#", grid.get((2, 2)))

        grid.set((100, 100), "#")
        self.assertEqual("#", grid.get((100, 100)))
        self.assertEqual(100, grid.maxX)
        self.assertEqual(100, grid.maxY)

    def test_flood_fill(self):
        lines = ["......", ".####.", ".#..#.", ".####.", "......"]
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
        self.assertEqual(
            [(1, 2, 2), (2, 1, 2), (2, 2, 1), (2, 2, 3), (2, 3, 2), (3, 2, 2)],
            neighbours,
        )

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
        self.assertEqual(((max(bounds[1]) + 1) ** 3) - (len(blocked) + 1), len(visited))

    def test_grid_neighbours(self):
        grid = Grid.from_lines(self.LINES)

        neighbours = [n[0] for n in grid.neighbours((0, 0))]
        self.assertEqual([(1, 0), (0, 1), (1, 1)], neighbours)
        vals = [n[1] for n in grid.neighbours((0, 0))]
        self.assertEqual([".", ".", "."], vals)

        neighbours = [n[0] for n in grid.neighbours((12, 1))]
        self.assertEqual(
            [(13, 1), (11, 1), (12, 2), (12, 0), (11, 0), (13, 2), (13, 0), (11, 2)],
            neighbours,
        )
        vals = [n[1] for n in grid.neighbours((12, 1))]
        self.assertEqual(["#", "#", ".", ".", ".", ".", ".", "."], vals)

    def test_walk(self):
        grid = Grid.from_lines(self.LINES)

        context = {"sum": 0}

        def visitor(_grid, _pos, val, context=context):
            context["sum"] += 1 if val == "#" else 0

        grid.walk(visitor)
        self.assertEqual(61, context["sum"])

    def test_rot_90(self):
        lines = ["123", "456", "789"]
        rotated = rot_90(lines)
        self.assertEqual(["741", "852", "963"], rotated)

        rotated = rot_90(rotated)
        self.assertEqual(["987", "654", "321"], rotated)

        rotated = rot_90(rotated)
        self.assertEqual(["369", "258", "147"], rotated)

        rotated = rot_90(rotated)
        self.assertEqual(["123", "456", "789"], rotated)


if __name__ == "__main__":
    unittest.main()
