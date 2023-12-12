#!/usr/bin/env python3

import sys
from functools import cache

from utils import io


def generate(length, line):
    candidates = []

    def genbin(n, bs=""):
        if len(bs) == n:
            candidates.append(bs)
        else:
            if line[len(bs)] == "?":
                genbin(n, bs + ".")
                genbin(n, bs + "#")
            else:
                genbin(n, bs + line[len(bs)])

    genbin(length)
    return candidates


def valid_variants(line, counts):
    sum = 0

    candidates = generate(len(line), line)

    for c in candidates:
        parts = c.split(".")

        actuals = [p for p in parts if p != ""]
        lens = [len(c) for c in actuals]
        if lens != counts or len(actuals) != len(counts):
            continue

        sum += 1

    return sum


def part1(filename):
    sum = 0
    count = 0
    for line in io.get_lines(filename):
        springs, counts = line.split(" ")
        counts = [int(i) for i in counts.split(",")]

        sum += valid_variants(springs, counts)
        count += 1

    return sum


# DP solution heavily influenced by help from u/codeunveiled


@cache
def count(idx, cidx, springs, counts):
    if cidx > len(counts) - 1:
        if idx < len(springs) and "#" in springs[idx:]:
            # finns fler källor kvar men inga counts
            return 0
        return 1

    if idx > len(springs) - 1:
        # slut på input
        return 0

    if springs[idx] == "#":
        # här kan det vara en
        if "." not in springs[idx : idx + counts[cidx]] and springs[idx + counts[cidx]] != "#":
            # finns plats för den
            return count(idx + 1 + counts[cidx], cidx + 1, springs, counts)
        else:
            # får ej plats
            return 0
    elif springs[idx] == "?":
        # här kan det kanske vara en
        if "." not in springs[idx : idx + counts[cidx]] and springs[idx + counts[cidx]] != "#":
            # eftersom det är ? kan det både var en här och inte, räkna båda
            return count(idx + 1 + counts[cidx], cidx + 1, springs, counts) + count(idx + 1, cidx, springs, counts)
        else:
            # får ej plats
            return count(idx + 1, cidx, springs, counts)
    else:
        # fungerande källa, här kan det inte vara en
        return count(idx + 1, cidx, springs, counts)


def solve(filename, unfold=False):
    sum = 0
    for line in io.get_lines(filename):
        springs, counts = line.split(" ")
        counts = tuple([int(i) for i in counts.split(",")])

        if unfold:
            springs = "?".join([springs] * 5)
            counts = counts * 5

        # dodga bound checks
        springs = springs + "."

        sum += count(0, 0, springs, counts)

    return sum


def main():
    # unknowns = []
    # for line in io.get_lines("../input/2023/day12.txt"):
    #    unknowns.append(sum([1 if c == "?" else 0 for c in line]))
    # print("max", max(unknowns))
    # print("min", min(unknowns))
    # print("avg", sum(unknowns) / len(unknowns))

    assert valid_variants("???.###", [1, 1, 3]) == 1
    assert valid_variants(".??..??...?##.", [1, 1, 3]) == 4
    assert valid_variants("?#?#?#?#?#?#?#?", [1, 3, 1, 6]) == 1
    assert valid_variants("????.#...#...", [4, 1, 1]) == 1
    assert valid_variants("????.######..#####.", [1, 6, 5]) == 4
    assert valid_variants("?###????????", [3, 2, 1]) == 10

    assert solve("example.txt") == 21
    print(solve("../input/2023/day12.txt"))

    assert solve("example.txt", True) == 525152
    print(solve("../input/2023/day12.txt", True))


if __name__ == "__main__":
    sys.exit(main())
