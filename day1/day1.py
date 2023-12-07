#!/usr/bin/env python3

import sys

from utils import io


def digits(line):
    digits = []

    for char in line:
        try:
            d = int(char)
            if d >= 0 and d <= 9:
                digits.append(d)
        except ValueError:
            pass

    return digits


def part1(filename):
    sum = 0

    for line in io.get_lines(filename):
        nums = digits(line)
        sum += int("%s%s" % (nums[0], nums[-1]))

    return sum


words = {
    "o": [("one", 1)],
    "t": [("two", 2), ("three", 3)],
    "f": [("four", 4), ("five", 5)],
    "s": [("six", 6), ("seven", 7)],
    "e": [("eight", 8)],
    "n": [("nine", 9)],
}


def digits_letters(line):
    digits = []

    idx = 0
    while idx < len(line):
        char = line[idx]
        try:
            d = int(char)
            if d >= 0 and d <= 9:
                digits.append(d)
        except ValueError:
            if char in words:
                for c in words[char]:
                    if idx+len(c[0]) <= len(line) and line[idx:idx+len(c[0])] == c[0]:
                        digits.append(c[1])
        idx += 1

    return digits


def part2(filename):
    sum = 0

    for line in io.get_lines(filename):
        nums = digits_letters(line)
        sum += int("%s%s" % (nums[0], nums[-1]))

    return sum


def main():
    assert part1("example.txt") == 142
    print(part1("../input/2023/day1.txt"))

    assert part2("example2.txt") == 281
    print(part2("../input/2023/day1.txt"))


if __name__ == "__main__":
    sys.exit(main())
