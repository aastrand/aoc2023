#!/usr/bin/env python3

import sys
from collections import defaultdict

from utils import io


def hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256

    return h


def part1(filename):
    return sum([hash(part) for part in io.get_input(filename).strip().split(",")])


def part2(filename):
    boxes = defaultdict(list)
    for part in io.get_input(filename).strip().split(","):
        if "=" in part:
            label, fl = part.split("=")
            box = boxes[hash(label)]
            fl = int(fl)

            for i in range(len(box)):
                other_label, other_fl = box[i]
                if label == other_label:
                    box.pop(i)
                    box.insert(i, (label, fl))
                    break
            else:
                box.append((label, fl))

        elif "-" in part:
            label = part[:-1]
            box = boxes[hash(label)]

            for other_label, other_fl in box:
                if label == other_label:
                    box.remove((other_label, other_fl))

        else:
            raise "Unknown op"

        # print('After "' + part + '":')
        # for box in boxes.keys():
        #    print("Box " + str(box) + ": " + str(boxes[box]))

    sum = 0
    for box in boxes.keys():
        for i in range(len(boxes[box])):
            sum += (1 + box) * (i + 1) * boxes[box][i][1]

    return sum


def main():
    assert hash("HASH") == 52

    assert part1("example.txt") == 1320
    print(part1("../input/2023/day15.txt"))

    assert part2("example.txt") == 145
    print(part2("../input/2023/day15.txt"))


if __name__ == "__main__":
    sys.exit(main())
