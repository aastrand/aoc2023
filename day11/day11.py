#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import Grid
from utils.math import manhattan_dist


def rot_90(lst):
    return ["".join(list(reversed(x))) for x in zip(*lst)]


def parse(lines, padding=2):
    verticals = []
    for i in range(len(lines) - 1):
        verticals.append(lines[i])
        if set(list(lines[i])) == {"."}:
            for _ in range(0, padding - 1):
                verticals.append(lines[i])
    verticals.append(lines[-1])

    lines = rot_90(verticals)
    horizontals = []
    for i in range(len(lines) - 1):
        horizontals.append(lines[i])
        if set(list(lines[i])) == {"."}:
            for _ in range(0, padding - 1):
                horizontals.append(lines[i])
    horizontals.append(lines[-1])
    lines = rot_90(rot_90(rot_90(horizontals)))

    grid = Grid.from_lines(lines)

    galaxies = set()

    def visitor(_, pos, val):
        if val == "#":
            galaxies.add(pos)

    grid.walk(visitor)

    return grid, galaxies


def solve(filename, padding=2):
    _, galaxies = parse(io.get_lines(filename), padding)

    sum = 0
    galaxies = list(galaxies)
    for i in range(0, len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            sum += manhattan_dist(galaxies[i][0], galaxies[i][1], galaxies[j][0], galaxies[j][1])

    return sum


def main():
    assert solve("example.txt") == 374
    assert solve("example.txt") == 374
    assert solve("example.txt", 10) == 1030
    print(solve("../input/2023/day11.txt"))  # = 9565386

    # part 2
    # solve("example.txt", 20)  # = 1850 => 1850 - 1030 = 820
    # solve("example.txt", 30)  # = 2670 => 2670 - 1850 = 820
    # solve("example.txt", 40)  # = 3490 => 3490 - 2670 = 820
    # solve("example.txt", 50)  # = 4310 => 4310 - 3490 = 820
    # so example scales with 820 per 10
    # example2 with 100:
    # 90 / 10 = 9
    # 9 * 820 = 7380
    # 7380 + 1030 = 8410

    # lets just do the math
    # print(solve("../input/2023/day11.txt"))     # = 9565386
    # print(solve("../input/2023/day11.txt", 3))  # = 10423365
    # print(solve("../input/2023/day11.txt", 10)) # = 16429218
    # print(solve("../input/2023/day11.txt", 15)) # = 20719113
    # increases linearly after a while, let's try 20
    g1 = 20
    g2 = 30
    s1 = solve("../input/2023/day11.txt", g1)  # = 25009008
    s2 = solve("../input/2023/day11.txt", g2)  # = 33588798
    print(((1000000 - g2) // (g2 - g1)) * (s2 - s1) + s2)


if __name__ == "__main__":
    sys.exit(main())
