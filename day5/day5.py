#!/usr/bin/env python3

import sys

from utils import io


class Range:
    def __init__(self, dest, source, range):
        self.source = source
        self.dest = dest
        self.range = range

    def contains(self, value):
        return self.source <= value < self.source + self.range

    def inv_contains(self, value):
        return self.dest <= value < self.dest + self.range

    def map(self, value):
        return value + (self.dest - self.source)

    def inv_map(self, value):
        return value + (self.source - self.dest)

    def __str__(self) -> str:
        return f"{self.source} -> {self.dest} ({self.range})"


class Map:
    def __init__(self, ranges):
        self.ranges = sorted(ranges, key=lambda r: r.dest)

    def map(self, value):
        for r in self.ranges:
            if r.contains(value):
                return r.map(value)
        return value

    def inv_map(self, value):
        for r in self.ranges:
            if r.inv_contains(value):
                return r.inv_map(value)
        return value

    def __str__(self) -> str:
        return "\n".join([str(r) for r in self.ranges])


class Maps:
    def __init__(self, maps):
        self.maps = maps

    def map(self, seed):
        for m in self.maps:
            seed = m.map(seed)

        return seed

    def inv_map(self, seed):
        for m in reversed(self.maps):
            seed = m.inv_map(seed)

        return seed


def parse(file):
    input = file.split("\n\n")
    seeds = [int(i) for i in input[0].split("seeds: ")[1].split(" ")]
    maps = []
    for part in input[1:]:
        ranges = []
        for range in part.split(" map:\n")[1].strip().split("\n"):
            source, dest, range = range.split(" ")
            ranges.append(Range(int(source), int(dest), int(range)))

        maps.append(Map(ranges))

    return seeds, Maps(maps)


def part1(filename):
    seeds, maps = parse(io.get_input(filename))

    smallest = sys.maxsize
    for seed in seeds:
        seed = maps.map(seed)
        smallest = min(smallest, seed)

    return smallest


def in_intervals(value, intervals):
    for interval in intervals:
        if interval[0] <= value < interval[1]:
            return True

    return False


def part2(filename, start=1):
    seeds, maps = parse(io.get_input(filename))
    intervals = []
    for x in range(0, len(seeds), 2):
        intervals.append((seeds[x], seeds[x] + seeds[x + 1]))

    seed = start
    while True:
        if in_intervals(maps.inv_map(seed), intervals):
            break
        seed += 1

    return seed


def main():
    _, maps = parse(io.get_input("example.txt"))
    assert maps.maps[0].map(79) == 81
    assert maps.maps[0].map(14) == 14
    assert maps.maps[0].map(55) == 57
    assert maps.maps[0].map(13) == 13

    assert maps.maps[0].map(13) == 13
    assert maps.maps[1].map(13) == 52
    assert maps.maps[2].map(52) == 41
    assert maps.maps[3].map(41) == 34
    assert maps.maps[4].map(34) == 34
    assert maps.maps[5].map(34) == 35
    assert maps.maps[6].map(35) == 35

    assert maps.maps[1].map(81) == 81
    assert maps.maps[2].map(81) == 81
    assert maps.maps[3].map(81) == 74
    assert maps.maps[4].map(74) == 78
    assert maps.maps[5].map(78) == 78
    assert maps.maps[6].map(78) == 82

    assert maps.maps[0].map(14) == 14
    assert maps.maps[1].map(14) == 53
    assert maps.maps[2].map(53) == 49
    assert maps.maps[3].map(49) == 42
    assert maps.maps[4].map(42) == 42
    assert maps.maps[5].map(42) == 43
    assert maps.maps[6].map(43) == 43

    assert part1("example.txt") == 35
    print(part1("../input/2023/day5.txt"))

    assert maps.maps[6].inv_map(57) == 94
    assert maps.inv_map(35) == 13

    assert part2("example.txt") == 46
    # brute force, saving some time here
    print(part2("../input/2023/day5.txt", start=27992442))


if __name__ == "__main__":
    sys.exit(main())
