#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import Grid

NUMS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
BASE = NUMS + ('.',)


def parse(lines):
    grid = Grid.from_lines(lines)

    nums = []

    y = grid.minY
    while y < grid.maxY + 1:
        x = grid.minX

        num = []
        while x < grid.maxX + 1:
            pos = (x, y)
            val = grid.get((x, y))

            if val in NUMS:
                num.append((val, pos))
            else:
                if len(num) > 0:
                    nums.append(num)
                    num = []

            x += 1

        if len(num) > 0:
            nums.append(num)
            num = []

        y += 1

    return grid, nums


def solve(filename):
    grid, nums = parse(io.get_lines(filename))

    sum = 0
    gears = {}
    for num in nums:
        num_coords = set([d[1] for d in num])
        adjecent = False

        found_gears = set()
        for c in num_coords:
            for n in grid.neighbours(c):
                if n[1] == '*':
                    found_gears.add(n[0])
                if n[1] not in BASE and n[0] not in num_coords:
                    adjecent = True

        if adjecent:
            part = int("".join([d[0] for d in num]))
            sum += part

            for gear in found_gears:
                if gear not in gears:
                    gears[gear] = []
                gears[gear].append(part)

    ratios = 0
    for gear, parts in gears.items():
        if len(parts) == 2:
            ratios += parts[0] * parts[1]

    return sum, ratios


def main():
    part1, part2 = solve("example.txt")
    assert part1 == 4361
    assert part2 == 467835

    part1, part2 = solve("input.txt")
    print(part1)
    print(part2)


if __name__ == "__main__":
    sys.exit(main())
