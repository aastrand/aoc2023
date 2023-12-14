#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import Grid, rot_90


def tilt(grid):
    for x in range(grid.minX, grid.maxX + 1):
        for y in range(grid.minY, grid.maxY + 1):
            pos = (x, y)
            val = grid.get(pos)

            if val != "O":
                continue

            # find first "." above
            min = None
            for y in range(y - 1, grid.minY - 1, -1):
                pos_to = (x, y)
                val_to = grid.get(pos_to)

                if val_to in {"#", "O"}:
                    break
                elif val_to == ".":
                    min = pos_to

            # move O there
            if min:
                grid.set(min, "O")
                grid.set(pos, ".")

    return grid


def total_load(grid):
    sum = 0

    for x in range(grid.minX, grid.maxX + 1):
        for y in range(grid.minY, grid.maxY + 1):
            pos = (x, y)
            if grid.get(pos) == "O":
                sum += grid.maxY + 1 - y

    return sum


def part1(filename):
    grid = Grid.from_lines(io.get_lines(filename))
    return total_load(tilt(grid))


def spin(grid):
    # roll north
    grid = tilt(grid)
    # west
    grid = tilt(Grid.from_lines(rot_90(grid.print_output())))
    # south
    grid = tilt(Grid.from_lines(rot_90(grid.print_output())))
    # east
    grid = tilt(Grid.from_lines(rot_90(grid.print_output())))
    # normalize
    return Grid.from_lines(rot_90(grid.print_output()))


def part2(filename):
    grid = Grid.from_lines(io.get_lines(filename))

    subseq = []
    seen = {}
    i = 0
    while True:
        grid = spin(grid)
        sum = total_load(grid)

        subseq.append(sum)
        if len(subseq) > 3:
            subseq.pop(0)

            if tuple(subseq) in seen:
                break

            seen[tuple(subseq)] = i - len(subseq)

        i += 1

    length = i - len(subseq) - seen[tuple(subseq)]
    iters = (1000000000 - seen[tuple(subseq)]) % length

    grid = Grid.from_lines(io.get_lines(filename))
    for i in range(iters + seen[tuple(subseq)]):
        grid = spin(grid)

    return total_load(grid)


def main():
    assert part1("example.txt") == 136
    print(part1("../input/2023/day14.txt"))

    assert part2("example.txt") == 64
    print(part2("../input/2023/day14.txt"))


if __name__ == "__main__":
    sys.exit(main())
