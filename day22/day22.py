#!/usr/bin/env python3

import sys
from collections import defaultdict

from utils import io
from utils.grid import neighbours_3d


def parse(lines, chars):
    bricks = defaultdict(list)
    grid = {}
    brick = 0

    # create state and 3d grid
    zMax = 0
    for line in lines:
        s, e = line.split("~")
        x1, y1, z1 = map(int, s.split(","))
        x2, y2, z2 = map(int, e.split(","))
        assert x1 <= x2
        assert y1 <= y2
        assert z1 <= z2
        id = chr(brick + 65) if chars else brick

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    bricks[id].append([x, y, z])
                    zMax = max(zMax, z)
                    grid[(x, y, z)] = id

        brick += 1

    # let bricks settle
    zMin = 1
    moved = True

    while moved:
        moved = False

        for brick in bricks:
            for cube in bricks[brick]:
                down = (cube[0], cube[1], cube[2] - 1)
                if cube[2] == zMin or (down in grid and grid[down] != brick):
                    break
            else:
                # print("can move", brick, "down")
                for cube in bricks[brick]:
                    del grid[tuple(cube)]

                new = []
                for cube in bricks[brick]:
                    cube = (cube[0], cube[1], cube[2] - 1)
                    new.append(cube)
                    grid[tuple(cube)] = brick
                    moved = True
                bricks[brick] = new

    # create graph with neighbours in each direction
    graph = defaultdict(dict)
    for brick, cubes in bricks.items():
        for cube in cubes:
            for n in neighbours_3d(cube):
                neigh = grid.get(n)
                if neigh is not None and neigh != brick:
                    dir = (cube[0] - n[0], cube[1] - n[1], cube[2] - n[2])

                    lst = graph[brick].get(dir)
                    if lst is None:
                        lst = []
                        graph[brick][dir] = lst

                    if neigh not in lst:
                        lst.append(neigh)

    return bricks, grid, graph


def part1(filename, chars=False):
    bricks, grid, graph = parse(io.get_lines(filename), chars)

    s = 0
    for brick in bricks:
        remove = True
        above = graph[brick].get((0, 0, -1), [])

        # if the brick above is only supported by me, we can't remove it
        for a in above:
            if len(graph[a].get((0, 0, 1), [])) == 1:
                remove = False
                break

        if remove:
            s += 1

    return s


def part2(filename, chars=False):
    bricks, _, graph = parse(io.get_lines(filename), chars)

    s = 0
    q = []
    # for all bricks, walk graph upwards and find all that are not supported by anyone else
    for brick in bricks:
        above = graph[brick].get((0, 0, -1), [])
        q.extend(above)

        removed = {brick}
        while q:
            b = q.pop()

            if set(graph[b].get((0, 0, 1), [])).issubset(removed):
                s += 1
                removed.add(b)
                q.extend(graph[b].get((0, 0, -1), []))

    return s


def main():
    assert part1("example.txt", True) == 5
    print(part1("../input/2023/day22.txt"))

    assert part2("example.txt", True) == 7
    print(part2("../input/2023/day22.txt"))


if __name__ == "__main__":
    sys.exit(main())
