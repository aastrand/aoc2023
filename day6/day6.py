#!/usr/bin/env python3

import sys

from utils import io, parse


def count_wins(time, distance):
    sum = 0
    for speed in range(1, time):
        travel_time = time - speed
        new_distance = travel_time * speed
        if new_distance > distance:
            sum += 1

    return sum


def part1(filename):
    lines = io.get_lines(filename)
    times = parse.ints(lines[0])
    distances = parse.ints(lines[1])

    prod = 1
    for idx in range(len(times)):
        time = times[idx]
        distance = distances[idx]
        prod *= count_wins(time, distance)

    return prod


def part2(time, distance):
    return count_wins(time, distance)


def main():
    assert part1("example.txt") == 288
    print(part1("../input/2023/day6.txt"))

    assert part2(71530, 940200) == 71503
    print(part2(49877895, 356137815021882))


if __name__ == "__main__":
    sys.exit(main())
