#!/usr/bin/env python3

import sys
from collections import deque

from utils import io
from utils.grid import OFFSETS_STRAIGHT, Grid


def get_neighbours(grid, pos):
    for o in OFFSETS_STRAIGHT:
        n = (pos[0] + o[0], pos[1] + o[1])
        offset = (n[0] % (grid.maxX + 1), n[1] % (grid.maxY + 1))

        yield (n, grid.get(offset))


def find(grid, start, steps):
    visited = {start: 0}
    dist = 0
    q = deque()
    q.append((start, 0))

    while dist < steps:
        cur, dist = q.popleft()

        for n, val in get_neighbours(grid, cur):
            if val in {".", "S"} and n not in visited:
                visited[n] = dist + 1
                q.append((n, dist + 1))

    return visited


def num_visited(visited, steps):
    s = 0

    for v in visited.values():
        if v <= steps and v % 2 == steps % 2:
            s += 1

    return s


def part1(filename, steps):
    grid = Grid.from_lines(io.get_lines(filename))

    context = {}

    def visitor(grid, pos, val, context=context):
        if val == "S":
            context["start"] = pos

    grid.walk(visitor)
    start = context["start"]

    return num_visited(find(grid, start, steps), steps)


def part2(filename):
    grid = Grid.from_lines(io.get_lines(filename))
    context = {}

    def visitor(grid, pos, val, context=context):
        if val == "S":
            context["start"] = pos

    grid.walk(visitor)
    start = context["start"]
    grid.set(start, ".")

    # turns out it grows quadratically like a diamond (grid.print() showed this)
    # here's some math I absolutely did not come up wih myself
    # we can fit to a x^2 formula using the values we get when it enters a new mirror
    # the reason for this is due to how the input is structued and the magic number asked: 26501365
    # (26501300 + 65) % 131 = 0
    # that happens at 65 and every 131 steps after that, since the grid is 131x131 and we start at 65,65

    x = [start[0], start[0] + grid.maxX + 1, start[0] + ((grid.maxX + 1) * 2)]
    visited = find(grid, start, max(x))
    y = [num_visited(visited, v) for v in x]
    print(x)
    print(y)

    # feed ^ into https://www.wolframalpha.com/input?i=quadratic+fit+calculator
    # => http://tinyurl.com/efyysj2h
    # get (14909 x^2)/17161 + (29581 x)/17161 + 332832/17161 in my case
    # (which needs rounding :sweat:)

    steps = 26501365
    plots = (14909 * steps**2) / 17161 + (29581 * steps) / 17161 + 332832 / 17161

    return int(round(plots))


def main():
    assert part1("example.txt", 6) == 16
    print(part1("../input/2023/day21.txt", 64))

    # In exactly 6 steps, he can still reach 16 garden plots.
    # In exactly 10 steps, he can reach any of 50 garden plots.
    # In exactly 50 steps, he can reach 1594 garden plots.
    # In exactly 100 steps, he can reach 6536 garden plots.
    # In exactly 500 steps, he can reach 167004 garden plots.
    # In exactly 1000 steps, he can reach 668697 garden plots.
    # In exactly 5000 steps, he can reach 16733044 garden plots.
    assert part1("example.txt", 6) == 16
    assert part1("example.txt", 10) == 50
    assert part1("example.txt", 50) == 1594
    assert part1("example.txt", 100) == 6536
    # these are too slow
    # assert part1("example.txt", 500) == 167004
    # assert part1("example.txt", 1000) == 668697
    # assert part1("example.txt", 5000) == 16733044

    print(part2("../input/2023/day21.txt"))


if __name__ == "__main__":
    sys.exit(main())
