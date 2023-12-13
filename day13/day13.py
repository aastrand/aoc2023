#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import Grid


def verify_vertical(grid, candidates, flips=0):
    for c in candidates:
        flipped = 0
        o = 1
        x = c
        while x >= grid.minX and c + o <= grid.maxX and flipped <= flips:
            matches = 0
            for y in range(grid.minY, grid.maxY + 1):
                if grid.get((x, y)) == grid.get((c + o, y)):
                    matches += 1

            flipped += grid.maxY - matches + 1
            o += 1
            x -= 1

        if flipped == flips:
            return c

    return None


def verify_horizontal(grid, candidates, flips=0):
    for c in candidates:
        flipped = 0
        o = 1
        y = c
        while y >= grid.minY and c + o <= grid.maxY and flipped <= flips:
            matches = 0
            for x in range(grid.minX, grid.maxX + 1):
                if grid.get((x, y)) == grid.get((x, c + o)):
                    matches += 1

            flipped += grid.maxX - matches + 1
            o += 1
            y -= 1

        if flipped == flips:
            return c

    return None


def solve(filename, flips=0):
    sum = 0
    for pattern in io.get_input(filename).split("\n\n"):
        grid = Grid.from_lines(pattern.strip().split("\n"))

        candidates = []

        # find vertical mids
        for x in range(grid.minX, grid.maxX):
            matches = 0
            for y in range(grid.minY, grid.maxY + 1):
                if grid.get((x, y)) == grid.get((x + 1, y)):
                    matches += 1

            if matches >= grid.maxY - 1:
                candidates.append(x)

        v = verify_vertical(grid, candidates, flips)
        if v is not None:
            sum += v + 1

        candidates = []

        # find horizontal mids
        for y in range(grid.minY, grid.maxY):
            matches = 0
            for x in range(grid.minX, grid.maxX + 1):
                if grid.get((x, y)) == grid.get((x, y + 1)):
                    matches += 1

            if matches >= grid.maxX - 1:
                candidates.append(y)

        h = verify_horizontal(grid, candidates, flips)
        if h is not None:
            sum += (h + 1) * 100

    return sum


def main():
    assert solve("example.txt") == 405
    print(solve("../input/2023/day13.txt"))

    assert solve("example.txt", 1) == 400
    print(solve("../input/2023/day13.txt", 1))


if __name__ == "__main__":
    sys.exit(main())
