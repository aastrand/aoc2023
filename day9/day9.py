#!/usr/bin/env python3

import sys

from utils import io


def parse(lines):
    for line in lines:
        ints = [int(i) for i in line.split(" ")]
        cur = ints
        diffs = []

        while True:
            diff = []
            for i in range(len(cur) - 1):
                diff.append(cur[i + 1] - cur[i])
            diffs.append(diff)

            if len(set(diff)) == 1 and diff[-1] == 0:
                break

            cur = diff

        yield ints, diffs


def part1(filename):
    sum = 0
    for ints, diffs in parse(io.get_lines(filename)):
        diffs[-1].append(0)
        for i in range(len(diffs) - 2, -1, -1):
            diffs[i].append(diffs[i + 1][-1] + diffs[i][-1])

        sum += ints[-1] + diffs[0][-1]

    return sum


def part2(filename):
    sum = 0
    for ints, diffs in parse(io.get_lines(filename)):
        diffs[-1].insert(0, 0)
        for i in range(len(diffs) - 2, -1, -1):
            diffs[i].insert(0, diffs[i][0] - diffs[i + 1][0])

        sum += ints[0] - diffs[0][0]

    return sum


def main():
    assert part1("example.txt") == 114
    print(part1("../input/2023/day9.txt"))

    assert part2("example.txt") == 2
    print(part2("../input/2023/day9.txt"))


if __name__ == "__main__":
    sys.exit(main())
