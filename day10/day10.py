#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import BOTTOM, LEFT, RIGHT, TOP, Grid

MOVES = {
    "|": (TOP, BOTTOM),
    "-": (LEFT, RIGHT),
    "L": (TOP, RIGHT),
    "J": (TOP, LEFT),
    "7": (BOTTOM, LEFT),
    "F": (BOTTOM, RIGHT),
}


def valid_moves(grid, pos):
    moves = MOVES.get(grid.get(pos), ())
    for move in moves:
        yield (pos[0] + move[0], pos[1] + move[1])


def bfs(start, grid, visitor=lambda *a, **kw: 0):
    visited = {start}
    q = [(start, 0)]
    while len(q) > 0:
        cur, length = q.pop(0)
        visitor(cur, length)
        for m in valid_moves(grid, cur):
            if m not in visited:
                visited.add(m)
                q.append((m, length + 1))

    return visited


def part1(filename, start_type="F"):
    grid = Grid.from_lines(io.get_lines(filename))

    context = {}

    def find_start(g, pos, val, context=context):
        if val == "S":
            context["start"] = pos

    grid.walk(find_start)
    start = context["start"]
    grid.set(start, start_type)

    context["max"] = 0

    def visitor(_, length, context=context):
        context["max"] = max(context["max"], length)

    bfs(start, grid, visitor)

    return context["max"]


def scale(grid):
    # vertical
    lines = grid.print_output()
    new_lines = []
    for i in range(len(lines) - 1):
        over = lines[i]
        under = lines[i + 1]
        new_line = []
        new_lines.append(lines[i])
        for j in range(len(over)):
            if over[j] == ".":
                new_line.append(".")
            elif (over[j] in {"F", "7", "|"}) and (under[j] in {"|", "L", "J"}):
                new_line.append("|")
            elif over[j] == "|" and (under[j] in {"L", "J", "|"}):
                new_line.append("|")
            elif over[j] in {"-", "L", "J"}:
                new_line.append(".")
        new_lines.append("".join(new_line))
    new_lines.append(lines[-1])

    # horizontal
    lines = new_lines
    new_lines = []
    for line in lines:
        new_line = []
        for i in range(len(line) - 1):
            new_line.append(line[i])
            if line[i] in {"F", "-", "L"}:
                new_line.append("-")
            elif line[i] in {".", "|", "7", "J"}:
                new_line.append(".")
        new_line.append(line[-1])
        new_lines.append("".join(new_line))

    # new grid, now we can floodfill with O
    new_grid = Grid.from_lines(new_lines)
    new_grid.maxX = new_grid.maxX + 1
    new_grid.minX = new_grid.minX - 1
    new_grid.maxY = new_grid.maxY + 1
    new_grid.minY = new_grid.minY - 1

    return new_grid


def part2(filename, start_type="F"):
    grid = Grid.from_lines(io.get_lines(filename))

    # find start
    context = {}

    def find_start(_, pos, val, context=context):
        if val == "S":
            context["start"] = pos

    grid.walk(find_start)
    start = context["start"]
    grid.set(start, start_type)

    # clean grid from other junk
    new_grid = Grid()
    for v in bfs(start, grid):
        new_grid.set(v, grid.get(v))
    grid = new_grid

    # blow up grid 2x to add subpixels
    grid = scale(grid)

    def visitor(grid, pos, val):
        if val is None:
            grid.set(pos, ".")

    grid.walk(visitor)
    visited = grid.flood_fill((grid.minX, grid.minY))
    for v in visited:
        grid.set(v, "O")

    # count candidates, map back to original grid
    candidates = set()

    def visitor(_, pos, val):
        if val == "." and pos[0] % 2 == 0 and pos[1] % 2 == 0:
            candidates.add((pos[0] // 2, pos[1] // 2))

    grid.walk(visitor)

    return len(candidates)


def main():
    assert part1("example.txt") == 4
    assert part1("example2.txt") == 8
    print(part1("../input/2023/day10.txt", start_type="L"))

    assert part2("example3.txt") == 4
    assert part2("example4.txt") == 8
    assert part2("example5.txt", start_type="7") == 10
    print(part2("../input/2023/day10.txt", start_type="L"))


if __name__ == "__main__":
    sys.exit(main())
