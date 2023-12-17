#!/usr/bin/env python3

import sys
from heapq import heappop, heappush

from utils import io
from utils.grid import BOTTOM, LEFT, OFFSETS_STRAIGHT, RIGHT, TOP, Grid


def oppoosite(dir):
    if dir == RIGHT:
        return LEFT
    elif dir == LEFT:
        return RIGHT
    elif dir == TOP:
        return BOTTOM
    elif dir == BOTTOM:
        return TOP
    else:
        raise Exception("Unknown direction", dir)


def neighbours(grid, cur, part2=False):
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


def find(grid, start, end, part2=False):
    dist = dict()
    pq = []

    for direction in [RIGHT, BOTTOM]:
        heappush(pq, (0, (start, direction, 0)))

    while len(pq) > 0:
        (heat, cur) = heappop(pq)

        for n in neighbours(grid, cur, part2):
            if n not in dist:
                new_heat = heat + int(grid.get(n[0]))
                if new_heat < dist.get(n, sys.maxsize):
                    if n not in dist:
                        dist[n] = new_heat
                        heappush(pq, (new_heat, n))

    m = sys.maxsize
    for cur, val in dist.items():
        if cur[0] == end:
            m = min(m, val)

    return m


def solve(filename, part2=False):
    grid = Grid.from_lines(io.get_lines(filename))
    return find(grid, (0, 0), (grid.maxX, grid.maxY), part2)


def main():
    assert solve("example.txt") == 102
    print(solve("../input/2023/day17.txt"))

    assert solve("example.txt", True) == 94
    print(solve("../input/2023/day17.txt", True))


if __name__ == "__main__":
    sys.exit(main())
