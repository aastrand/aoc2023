#!/usr/bin/env python3

import sys

from utils import io


def part1(filename):
    lines = io.get_lines(filename)

    return 0


def part2(filename):
    lines = io.get_lines(filename)

    return 0


def main():
    assert part1("example.txt") == 0
    print(part1("../input/2023/day{{ day }}.txt"))

    assert part2("example.txt") == 0
    print(part2("../input/2023/day{{ day }}.txt"))


if __name__ == "__main__":
    sys.exit(main())
