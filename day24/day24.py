#!/usr/bin/env python3

import sys

import numpy as np
from utils import io
from utils.math import sign
from z3 import IntVector, Solver


def parse(lines):
    positions = []
    velocities = []

    for line in lines:
        pos, vel = line.split(" @ ")
        positions.append([int(p) for p in pos.split(",")])
        velocities.append([int(p) for p in vel.split(",")])

    return positions, velocities


def intersects(x1, y1, vx1, vy1, x2, y2, vx2, vy2):
    m1 = vy1 / vx1
    m2 = vy2 / vx2

    if m1 == m2:
        return (float("inf"), float("inf"))

    return np.linalg.solve([[-m1, 1], [-m2, 1]], [y1 - m1 * x1, y2 - m2 * x2])


def part1(filename, b1=7, b2=27):
    positions, velocities = parse(io.get_lines(filename))

    s = 0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            x1a = positions[i][0]
            y1a = positions[i][1]
            vxa = velocities[i][0]
            vya = velocities[i][1]

            x1b = positions[j][0]
            y1b = positions[j][1]
            vxb = velocities[j][0]
            vyb = velocities[j][1]

            x, y = intersects(x1a, y1a, vxa, vya, x1b, y1b, vxb, vyb)

            if x >= b1 and x <= b2 and y >= b1 and y <= b2:
                if sign(vxa) == -1 and x > x1a:
                    continue
                elif sign(vxa) == 1 and x < x1a:
                    continue
                elif sign(vya) == -1 and y > y1a:
                    continue
                elif sign(vya) == 1 and y < y1a:
                    continue
                elif sign(vxb) == -1 and x > x1b:
                    continue
                elif sign(vxb) == 1 and x < x1b:
                    continue
                elif sign(vyb) == -1 and y > y1b:
                    continue
                elif sign(vyb) == 1 and y < y1b:
                    continue

                s += 1

    return s


def part2(filename):
    positions, velocities = parse(io.get_lines(filename))

    x, y, z, dx, dy, dz = IntVector("rock", 6)
    t = IntVector("time", len(positions))
    solver = Solver()

    for i in range(len(positions)):
        solver.add(x + t[i] * dx == positions[i][0] + t[i] * velocities[i][0])
        solver.add(y + t[i] * dy == positions[i][1] + t[i] * velocities[i][1])
        solver.add(z + t[i] * dz == positions[i][2] + t[i] * velocities[i][2])

    solver.check()
    model = solver.model()

    return model[x].as_long() + model[y].as_long() + model[z].as_long()


def main():
    assert part1("example.txt") == 2
    print(part1("../input/2023/day24.txt", 200000000000000, 400000000000000))

    assert part2("example.txt") == 47
    print(part2("../input/2023/day24.txt"))


if __name__ == "__main__":
    sys.exit(main())
