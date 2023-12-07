#!/usr/bin/env python3

import sys

from utils import io

limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def power(maxes):
    return maxes["red"] * maxes["green"] * maxes["blue"]


def play(games):
    part1, part2 = 0, 0

    for game in games:
        game = game.split(": ")
        id = int(game[0].split("Game ")[1])
        sets = game[1].split("; ")

        impossible = False
        maxes = {}

        for set in sets:
            for cube in set.split(", "):
                value = int(cube.split(" ")[0])
                color = cube.split(" ")[1]

                if value > limits[color]:
                    impossible = True

                maxes[color] = max(maxes.get(color, value), value)

        if not impossible:
            part1 += id

        part2 += power(maxes)

    return part1, part2


def main():
    part1, part2 = play(io.get_lines("example.txt"))
    assert part1 == 8
    assert part2 == 2286

    part1, part2 = play(io.get_lines("../input/2023/day2.txt"))
    print(part1)
    print(part2)


if __name__ == "__main__":
    sys.exit(main())
