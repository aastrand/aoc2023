#!/usr/bin/env python3

import sys
from math import gcd

from utils import io


def parse(filename):
    parts = io.get_input(filename).split("\n\n")
    instructions = list(parts[0])
    graph = {}
    for line in parts[1].strip().split("\n"):
        node, children = line.split(" = ")
        left, right = children[1 : len(children) - 1].split(", ")
        graph[node] = {"L": left, "R": right}

    return instructions, graph


def find_steps(graph, instructions, cur, condition: lambda x: bool):
    idx = 0
    while not condition(cur):
        instr = instructions[idx % len(instructions)]
        cur = graph[cur][instr]
        idx += 1

    return idx


def part1(filename):
    instructions, graph = parse(filename)

    cur = "AAA"
    end = "ZZZ"

    return find_steps(graph, instructions, cur, lambda cur: cur == end)


def part2(filename):
    instructions, graph = parse(filename)

    curs = []
    for node in graph:
        if node[2] == "A":
            curs.append(node)

    found = [find_steps(graph, instructions, cur, lambda cur: cur[2] == "Z") for cur in curs]

    lcm = 1
    for i in found:
        lcm = lcm * i // gcd(lcm, i)

    return lcm


def main():
    assert part1("example.txt") == 2
    assert part1("example2.txt") == 6
    print(part1("../input/2023/day8.txt"))

    assert part2("example3.txt") == 6
    print(part2("../input/2023/day8.txt"))


if __name__ == "__main__":
    sys.exit(main())
