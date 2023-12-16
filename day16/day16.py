#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import BOTTOM, LEFT, RIGHT, TOP, Grid


def get_next(grid, pos, old):
    dir = (pos[0] - old[0], pos[1] - old[1])
    val = grid.get(pos)

    if val is None:
        return (None, None)
    elif val == "\\":
        if dir == LEFT:
            return ((pos[0], pos[1] - 1), None)
        elif dir == RIGHT:
            return ((pos[0], pos[1] + 1), None)
        elif dir == TOP:
            return ((pos[0] - 1, pos[1]), None)
        elif dir == BOTTOM:
            return ((pos[0] + 1, pos[1]), None)
        else:
            raise ValueError(f"Invalid direction {dir} at {pos}")
    elif val == "/":
        if dir == LEFT:
            return ((pos[0], pos[1] + 1), None)
        elif dir == RIGHT:
            return ((pos[0], pos[1] - 1), None)
        elif dir == TOP:
            return ((pos[0] + 1, pos[1]), None)
        elif dir == BOTTOM:
            return ((pos[0] - 1, pos[1]), None)
        else:
            raise ValueError(f"Invalid direction {dir} at {pos}")
    elif val == "|":
        if dir in {LEFT, RIGHT}:
            return ((pos[0], pos[1] - 1), (pos[0], pos[1] + 1))
        elif dir in {TOP, BOTTOM}:
            return ((pos[0] + dir[0], pos[1] + dir[1]), None)
        else:
            raise ValueError(f"Invalid direction {dir} at {pos}")
    elif val == "-":
        if dir in {TOP, BOTTOM}:
            return ((pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]))
        elif dir in {LEFT, RIGHT}:
            return ((pos[0] + dir[0], pos[1] + dir[1]), None)
        else:
            raise ValueError(f"Invalid direction {dir} at {pos}")
    elif val == ".":
        return ((pos[0] + dir[0], pos[1] + dir[1]), None)
    else:
        raise ValueError(f"Invalid value {val} at {pos}")


def walk_grid(grid, old, new):
    q = []
    q.append((old, new))

    visited = Grid()
    while len(q) > 0:
        old, new = q.pop()

        while grid.get(new) is not None:
            if visited.get(new) is not None and grid.get(new) in {"|", "-"}:
                break

            visited.set(new, "#")
            # print("\033c", end="")
            # visited.print()

            nold = new
            new, split = get_next(grid, new, old)
            old = nold

            if split:
                q.append((old, split))

    context = {"sum": 0}

    def visitor(grid, pos, val, context=context):
        if val == "#":
            context["sum"] += 1

    visited.walk(visitor)

    return context["sum"]


def part1(filename):
    grid = Grid.from_lines(io.get_lines(filename))

    old = (-1, 0)
    new = (0, 0)

    return walk_grid(grid, old, new)


def part2(filename):
    grid = Grid.from_lines(io.get_lines(filename))

    candidates = []
    # top row, down
    for x in range(grid.minX, grid.maxX + 1):
        candidates.append(((x, grid.minY - 1), (x, grid.minY)))
    # bottom row, up
    for x in range(grid.minX, grid.maxX + 1):
        candidates.append(((x, grid.maxY - 1), (x, grid.maxY)))
    # left side, right
    for y in range(grid.minY, grid.maxY + 1):
        candidates.append(((grid.minX, y), (grid.minX + 1, y)))
    # right side, left
    for y in range(grid.minY, grid.maxY + 1):
        candidates.append(((grid.maxX, y), (grid.maxX - 1, y)))

    m = 0
    for c in candidates:
        m = max(m, walk_grid(grid, c[0], c[1]))

    return m


def main():
    grid = Grid()
    grid.set((0, 0), ".")
    assert get_next(grid, (0, 0), (-1, 0)) == ((1, 0), None)
    assert get_next(grid, (0, 0), (1, 0)) == ((-1, 0), None)
    assert get_next(grid, (0, 0), (0, 1)) == ((0, -1), None)
    assert get_next(grid, (0, 0), (0, -1)) == ((0, 1), None)

    grid.set((0, 0), "\\")
    assert get_next(grid, (0, 0), (1, 0)) == ((0, -1), None)
    assert get_next(grid, (0, 0), (-1, 0)) == ((0, 1), None)
    assert get_next(grid, (0, 0), (0, 1)) == ((-1, 0), None)
    assert get_next(grid, (0, 0), (0, -1)) == ((1, 0), None)

    grid.set((0, 0), "/")
    assert get_next(grid, (0, 0), (1, 0)) == ((0, 1), None)
    assert get_next(grid, (0, 0), (-1, 0)) == ((0, -1), None)
    assert get_next(grid, (0, 0), (0, 1)) == ((1, 0), None)
    assert get_next(grid, (0, 0), (0, -1)) == ((-1, 0), None)

    grid.set((0, 0), "|")
    assert get_next(grid, (0, 0), (1, 0)) == ((0, -1), (0, 1))
    assert get_next(grid, (0, 0), (-1, 0)) == ((0, -1), (0, 1))
    assert get_next(grid, (0, 0), (0, 1)) == ((0, -1), None)
    assert get_next(grid, (0, 0), (0, -1)) == ((0, 1), None)

    grid.set((0, 0), "-")
    assert get_next(grid, (0, 0), (1, 0)) == ((-1, 0), None)
    assert get_next(grid, (0, 0), (-1, 0)) == ((1, 0), None)
    assert get_next(grid, (0, 0), (0, 1)) == ((-1, 0), (1, 0))
    assert get_next(grid, (0, 0), (0, -1)) == ((-1, 0), (1, 0))

    assert part1("example.txt") == 46
    print(part1("../input/2023/day16.txt"))

    assert part2("example.txt") == 51
    print(part2("../input/2023/day16.txt"))


if __name__ == "__main__":
    sys.exit(main())
