#!/usr/bin/env python3

import sys
from collections import defaultdict

from utils import io
from utils.graph import from_grid
from utils.grid import OFFSETS_STRAIGHT, Grid

sys.setrecursionlimit(2000)


def get_distances(graph, start):
    def recur(graph, cur, visited, stack):
        visited.add(cur)
        for n in graph[cur]:
            if n not in visited:
                recur(graph, n, visited, stack)
        stack.insert(0, cur)

    visited = set()
    stack = []
    for pos in graph:
        if pos not in visited:
            recur(graph, pos, visited, stack)

    dist = {}
    for pos in stack:
        dist[pos] = float("-inf")
    dist[start] = 0

    while stack:
        i = stack.pop(0)

        for node in graph[i]:
            if dist[node] < dist[i] + 1:
                dist[node] = dist[i] + 1

    return dist


def part1(filename):
    grid = Grid.from_lines(io.get_lines(filename))

    start = (1, 0)
    end = (grid.maxX - 1, grid.maxY)
    # grid.set(start, "S")
    # grid.set(end, "O")
    # grid.print()

    graph = defaultdict(set)
    for y in range(grid.minY, grid.maxY + 1):
        for x in range(grid.minX, grid.maxX + 1):
            pos = (x, y)
            val = grid.get(pos)
            assert val in {".", ">", "v", "#"}

            for o in OFFSETS_STRAIGHT:
                neighbour = (x + o[0], y + o[1])
                other = grid.get(neighbour)

                if val in val in {".", ">", "v"} and other == ".":
                    graph[pos].add(neighbour)

                if val == "." and other == ">" and o == (1, 0):
                    graph[pos].add(neighbour)

                if val == "." and other == "v" and o == (0, 1):
                    graph[pos].add(neighbour)

    dist = get_distances(graph, start)

    return dist[end]


def simplify(graph, dist):
    removals = set()
    for node in set(graph.keys()):
        if node in graph:
            if len(graph[node]) == 2:
                n1, n2 = graph[node]
                if len(graph[n1]) <= 2 and len(graph[n2]) <= 2:
                    graph[node] = set()
                    removals.add(node)
                    graph[n1].remove(node)
                    graph[n2].remove(node)
                    graph[n1].add(n2)
                    graph[n2].add(n1)

                    # now n1 -> n2 and n2 -> n1
                    # update dists
                    dist[(n1, n2)] = dist[(n1, node)] + dist[(node, n2)]
                    dist[(n2, n1)] = dist[(n1, node)] + dist[(node, n2)]
                    del dist[(n1, node)]
                    del dist[(node, n1)]
                    del dist[(node, n2)]
                    del dist[(n2, node)]

    for node in set(graph.keys()):
        if node in graph:
            if len(graph[node]) > 2:
                for n in set(graph[node]):
                    removals.add(n)
                    graph[node].remove(n)

                    for on in graph[n]:
                        if on != node:
                            graph[on].remove(n)
                            graph[on].add(node)
                            graph[node].add(on)

                            # update dists
                            dist[(node, on)] = dist[(node, n)] + dist[(n, on)]
                            dist[(on, node)] = dist[(node, n)] + dist[(n, on)]
                            del dist[(node, n)]
                            del dist[(n, node)]
                            del dist[(n, on)]
                            del dist[(on, n)]

    for r in removals:
        del graph[r]

    return graph, dist


def find_longest_path(graph, dist, start, end):
    def dfs(node, visited):
        if node == end:
            return 0

        if node in visited:
            return float("-inf")

        visited.add(node)

        max_length = float("-inf")
        for neighbor in graph[node]:
            length = dist[(node, neighbor)] + dfs(neighbor, visited)
            max_length = max(max_length, length)

        visited.remove(node)

        return max_length

    return dfs(start, set())


def part2(filename):
    grid = Grid.from_lines(io.get_lines(filename))

    def visitor(graph, pos, val):
        if val in {"v", ">"}:
            graph.set(pos, ".")

    grid.walk(visitor)

    start = (1, 0)
    end = (grid.maxX - 1, grid.maxY)
    graph = from_grid(grid, lambda grid, pos, val, other: other == "." and val == ".")

    dist = {}
    for node in graph:
        for n in graph[node]:
            dist[(node, n)] = 1

    graph, dist = simplify(graph, dist)

    return find_longest_path(graph, dist, start, end)


def main():
    assert part1("example.txt") == 94
    print(part1("../input/2023/day23.txt"))

    assert part2("example.txt") == 154
    print(part2("../input/2023/day23.txt"))


if __name__ == "__main__":
    sys.exit(main())
