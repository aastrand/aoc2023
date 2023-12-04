#!/usr/bin/env python3

import sys

from utils import io


def parse(lines):
    cards = {}
    for line in lines:
        card = line.split(" | ")
        card_num = int(card[0].split(": ")[0].split("Card ")[1])
        nums = set(
            [
                int(i)
                for i in card[0].split(": ")[1].strip().replace("  ", " ").split(" ")
            ]
        )
        winners = set([int(i) for i in card[1].strip().replace("  ", " ").split(" ")])

        copies = len(nums.intersection(winners))

        neighbours = []
        for i in range(copies):
            neighbours.append(card_num + i + 1)

        cards[card_num] = (neighbours, -1)

    return cards


def part1(filename):
    cards = parse(io.get_lines(filename))

    sum = 0
    for card in cards.keys():
        card_sum = 0
        for _ in cards[card][0]:
            if card_sum == 0:
                card_sum = 1
            else:
                card_sum *= 2

        sum += card_sum

    return sum


def find_additional(cards, current):
    neighbours, cache = cards[current]
    if cache != -1:
        return cache

    found = len(neighbours)
    for n in neighbours:
        found += find_additional(cards, n)

    cards[current] = [neighbours, found]

    return found


def part2(filename):
    cards = parse(io.get_lines(filename))

    sum = 0
    for card in cards.keys():
        sum += 1 + find_additional(cards, card)

    return sum


def main():
    assert part1("example.txt") == 13
    print(part1("input.txt"))

    assert part2("example.txt") == 30
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
