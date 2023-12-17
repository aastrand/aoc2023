#!/usr/bin/env python3

import sys

from utils import io
from utils.graph import dijkstra
from utils.grid import BOTTOM, OFFSETS_STRAIGHT, RIGHT, Grid, oppoosite


def neighbours(grid, cur, part2):
    max_moves = 3 if not part2 else 10
    min_moves = None if not part2 else 4
    if part2:
        min_moves = 4

    pos, dir, count = cur

    neighbours = []

    for new_dir in OFFSETS_STRAIGHT:
        new_pos = (pos[0] + new_dir[0], pos[1] + new_dir[1])

        # bounds
        if grid.get(new_pos) is None:
            continue

        if dir == new_dir:
            new_count = count + 1
        else:
            new_count = 1

        # cant continue straight
        if new_count > max_moves:
            continue

        # must continue straight
        if min_moves and dir != new_dir and count < min_moves:
            continue

        # cant go back
        if dir == oppoosite(new_dir):
            continue

        neighbours.append((new_pos, new_dir, new_count))

    return neighbours


def get_dist(grid, _, n):
    return int(grid.get(n[0]))


def solve(filename, part2=False):
    grid = Grid.from_lines(io.get_lines(filename))
    start = (0, 0)
    end = (grid.maxX, grid.maxY)

    starts = []
    for direction in [RIGHT, BOTTOM]:
        starts.append((start, direction, 0))

    dist, _ = dijkstra(grid, starts, lambda grid, cur: neighbours(grid, cur, part2), get_dist)

    m = sys.maxsize
    for cur, val in dist.items():
        if cur[0] == end:
            m = min(m, val)

    return m


def main():
    assert solve("example.txt") == 102
    print(solve("../input/2023/day17.txt"))

    assert solve("example.txt", True) == 94
    print(solve("../input/2023/day17.txt", True))


if __name__ == "__main__":
    sys.exit(main())
