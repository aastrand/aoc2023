import unittest

from utils.graph import bfs, dfs, dijkstra, floyd_warshall, from_grid
from utils.grid import Grid


class TestGraph(unittest.TestCase):

    def test_bfs_empty(self):
        visited = bfs(3, {})
        self.assertTrue(3 in visited)
        self.assertEqual(1, len(visited))

    def test_bfs(self):
        graph = {}
        graph[0] = [1, 2]
        graph[1] = [0, 2, 3, 4]
        graph[2] = [0, 1, 3, 5]
        graph[3] = [1, 2, 4, 5]
        graph[4] = [2, 3]
        graph[5] = [1, 3]
        graph[6] = [7, 8]
        graph[7] = [6]
        graph[8] = [6]

        order = []
        visited = bfs(0, graph, lambda n: order.append(n))
        self.assertEqual(6, len(visited))
        self.assertTrue(5 in visited)
        self.assertFalse(6 in visited)
        self.assertEqual([0, 1, 2, 3, 4, 5], order)

        order = []
        visited = bfs(6, graph, lambda n: order.append(n))
        self.assertEqual(3, len(visited))
        self.assertTrue(6 in visited)
        self.assertFalse(5 in visited)
        self.assertEqual([6, 7, 8], order)

        visited = bfs(6, graph)
        self.assertEqual(3, len(visited))
        self.assertTrue(6 in visited)
        self.assertFalse(5 in visited)

    def test_dfs_empty(self):
        visited = dfs(3, {})
        self.assertTrue(3 in visited)
        self.assertEqual(1, len(visited))

    def test_dfs(self):
        graph = {}
        graph[0] = [1, 2]
        graph[1] = [0, 2, 3, 4]
        graph[2] = [0, 1, 3, 5]
        graph[3] = [1, 2, 4, 5]
        graph[4] = [2, 3]
        graph[5] = [1, 3]
        graph[6] = [7, 8]
        graph[7] = [6]
        graph[8] = [6]

        order = []
        visited = dfs(0, graph, lambda n: order.append(n))
        self.assertEqual(6, len(visited))
        self.assertTrue(5 in visited)
        self.assertFalse(6 in visited)
        self.assertEqual([0, 2, 5, 3, 4, 1], order)

        order = []
        visited = dfs(6, graph, lambda n: order.append(n))
        self.assertEqual(3, len(visited))
        self.assertTrue(6 in visited)
        self.assertFalse(5 in visited)
        self.assertEqual([6, 8, 7], order)

        visited = dfs(6, graph)
        self.assertEqual(3, len(visited))
        self.assertTrue(6 in visited)
        self.assertFalse(5 in visited)

    def test_dijkstra_empty(self):
        graph = {}
        path, dist, prev = dijkstra(graph, 0, 10)

        self.assertEqual(0, len(path))
        self.assertEqual(1, len(dist))
        self.assertEqual(0, len(prev))

    def test_dijkstra(self):
        graph = {}
        graph[0] = [1, 5]
        graph[1] = [0, 2]
        graph[2] = [1, 3, 4]
        graph[3] = [2, 4]
        graph[4] = [2, 10]
        graph[5] = [0, 6, 7]
        graph[6] = [5, 7, 8, 10]
        graph[7] = [5, 6, 8]
        graph[8] = [6, 7, 9]
        graph[9] = [8]
        graph[10] = [4, 6]

        path, dist, prev = dijkstra(graph, 0, 10)

        self.assertEqual([5, 6, 10], path)
        self.assertEqual(6, prev.get(10))
        self.assertEqual(2.0, dist.get(6))

    def test_from_grid(self):
        lines = ["#####",
                 "#...#",
                 "###.#"]
        grid = Grid.from_lines(lines)
        graph = from_grid(grid, lambda p, n, v, o: v != '#' and o != '#')

        self.assertEqual(4, len(graph))
        self.assertEqual({(2, 1)}, graph.get((1, 1)))
        self.assertEqual({(1, 1), (3, 1)}, graph.get((2, 1)))
        self.assertEqual({(2, 1), (3, 2)}, graph.get((3, 1)))
        self.assertEqual({(3, 1)}, graph.get((3, 2)))

    def test_floyd_warshall(self):
        #               AA <-> CC
        #               ^      |
        #               |      |
        #               v      v
        # EE <-- DD <-> BB <-> FF <-> GG
        graph = {
            'AA': ['BB', 'CC'],
            'BB': ['AA', 'DD', 'FF'],
            'CC': ['AA', 'FF'],
            'DD': ['BB', 'EE'],
            'EE': [],
            'FF': ['GG', 'BB'],
            'GG': ['FF'],
        }

        result = floyd_warshall(graph)
        self.assertEqual(0, result[('AA', 'AA')])
        self.assertEqual(float('inf'), result[('EE', 'CC')])
        self.assertEqual(4, result[('CC', 'EE')])

        self.assertEqual(1, result[('CC', 'FF')])
        self.assertEqual(3, result[('FF', 'CC')])

        self.assertEqual(4, result[('GG', 'EE')])
        self.assertEqual(3, result[('DD', 'GG')])
        self.assertEqual(2, result[('AA', 'FF')])
        self.assertEqual(2, result[('FF', 'AA')])
