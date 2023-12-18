#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import BOTTOM, LEFT, RIGHT, TOP
from utils.math import poly_area

instructions = {
    "R": RIGHT,
    "L": LEFT,
    "U": TOP,
    "D": BOTTOM,
}


int_to_instr = {
    0: "R",
    1: "D",
    2: "L",
    3: "U",
}


def get_outline(lines, part2=False):
    pos = (0, 0)
    corners = [pos]
    outline = 0
    for line in lines:
        if not part2:
            instr = line.split("(")[0].strip().split(" ")
            dir = instructions[instr[0]]
            length = int(instr[1])
        else:
            instr = line.split("#")[1].strip()[:-1]
            length = int(instr[:-1], 16)
            dir = instructions[int_to_instr[int(instr[-1])]]

        pos = (pos[0] + dir[0] * length, pos[1] + dir[1] * length)
        outline += length
        corners.append(pos)

    return corners, outline


def solve(filename, part2=False):
    corners, outline = get_outline(io.get_lines(filename), part2)
    return int(poly_area(corners)) + outline // 2 + 1


def main():
    assert solve("example.txt") == 62
    print(solve("../input/2023/day18.txt"))

    assert solve("example.txt", True) == 952408144115
    print(solve("../input/2023/day18.txt", True))


if __name__ == "__main__":
    sys.exit(main())
