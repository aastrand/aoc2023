#!/usr/bin/env python3

import sys
from collections import defaultdict

from utils import io


def hash(s):
    h = 0
    for c in s:
        h = (h + ord(c)) * 17 % 256

    return h


def part1(filename):
    return sum([hash(part) for part in io.get_input(filename).strip().split(",")])


def part2(filename):
    boxes = defaultdict(dict)
    for part in io.get_input(filename).strip().split(","):
        if "=" in part:
            label, fl = part.split("=")
            boxes[hash(label)][label] = fl

        elif "-" in part:
            label = part[:-1]
            boxes[hash(label)].pop(label, None)

        else:
            raise "Unknown op"

        # print('After "' + part + '":')
        # for box in boxes.keys():
        #    print("Box " + str(box) + ": " + str(boxes[box]))

    sum = 0
    for box in boxes.keys():
        for i, val in enumerate(boxes[box].values()):
            sum += (1 + box) * (i + 1) * int(val)

    return sum


def main():
    assert hash("HASH") == 52

    assert part1("example.txt") == 1320
    print(part1("../input/2023/day15.txt"))

    assert part2("example.txt") == 145
    print(part2("../input/2023/day15.txt"))


if __name__ == "__main__":
    sys.exit(main())
