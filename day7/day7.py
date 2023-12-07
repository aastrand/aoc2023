#!/usr/bin/env python3

import sys

from utils import io


def to_value(label, with_joker=False):
    try:
        return int(label)
    except ValueError:
        if label == "T":
            return 10
        elif label == "J":
            return 0 if with_joker else 11
        elif label == "Q":
            return 12
        elif label == "K":
            return 13
        elif label == "A":
            return 14
        else:
            raise ValueError("Invalid label: {}".format(label))


class Hand:
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

    def __init__(self, hand, value, bid, with_joker=False):
        self.hand = hand
        self.value = value
        self.bid = bid
        self.with_joker = with_joker

    def __cmp__(self, other):
        if self.value > other.value:
            return 1
        elif self.value < other.value:
            return -1
        else:
            for i in range(5):
                if to_value(self.hand[i], self.with_joker) > to_value(
                    other.hand[i], other.with_joker
                ):
                    return 1
                elif to_value(self.hand[i], self.with_joker) < to_value(
                    other.hand[i], other.with_joker
                ):
                    return -1
            return 0

    def __gt__(self, other):
        return self.__cmp__(other) == 1

    def __lt__(self, other):
        return self.__cmp__(other) == -1

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __str__(self) -> str:
        return "{} {} {}".format(self.hand, self.value, self.bid)

    def to_hand(hand, bid, with_joker=False):
        candidates = [hand]
        if with_joker and "J" in hand:
            others = set(list(hand)) - {"J"}
            for o in others:
                candidates.append(hand.replace("J", o))

        hi = Hand.HIGH_CARD
        for c in candidates:
            hi = max(hi, Hand._to_hand(c))

        return Hand(hand, hi, bid, with_joker)

    def _to_hand(hand):
        counts = {}
        for label in hand:
            counts[label] = counts.get(label, 0) + 1

        if len(counts) == 1:
            return Hand.FIVE_OF_A_KIND
        elif len(counts) == 2:
            if 3 in counts.values():
                return Hand.FULL_HOUSE
            else:
                return Hand.FOUR_OF_A_KIND
        elif len(counts) == 3:
            if 3 in counts.values():
                return Hand.THREE_OF_A_KIND
            else:
                return Hand.TWO_PAIR
        elif len(counts) == 4:
            return Hand.ONE_PAIR
        else:
            return Hand.HIGH_CARD


def solve(filename, with_joker=False):
    input = []
    for line in io.get_lines(filename):
        hand, bid = line.split(" ")
        input.append(Hand.to_hand(hand, int(bid), with_joker))

    input.sort()

    sum = 0
    for r in range(len(input)):
        sum += input[r].bid * (r + 1)

    return sum


def main():
    assert solve("example.txt") == 6440
    print(solve("../input/2023/day7.txt"))

    assert solve("example.txt", True) == 5905
    assert Hand.to_hand("JJJJJ", 0, True) < Hand.to_hand("AAAJA", 0, True)
    print(solve("../input/2023/day7.txt", True))


if __name__ == "__main__":
    sys.exit(main())
