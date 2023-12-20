#!/usr/bin/env python3

import sys
from collections import deque
from math import gcd

from utils import io


# % flips if it recieves a 0
# & sends 0 if it recieves a 1 and 1 if it recieves a 0
class Module:
    def __init__(self, name, type, val, input):
        self.name = name
        self.type = type
        self.val = val
        self.input = input

    def __str__(self):
        return f"{self.name} {self.type} {self.val} {self.input}"

    def __repr__(self):
        return str(self)


def parse(lines):
    graph = {}
    state = {}

    for line in lines:
        name, dests = line.split(" -> ")
        if name[0] in ("%", "&"):
            type = name[0]
            name = name[1:]
        else:
            type = None

        mod = Module(name, type, 0 if type == "%" else None, {})
        state[mod.name] = mod
        graph[mod.name] = [dest.strip() for dest in dests.split(", ")]

    # init inputs
    exits = []
    for name, mod in graph.items():
        for dest in graph[name]:
            if dest not in state:
                exits.append(dest)
            else:
                state[dest].input[name] = 0

    return graph, state, exits


def pulse(graph, state, start, cycles=0):
    q = deque()
    q.append(start)
    lo = 1
    hi = 0

    while q:
        name, val, sender = q.popleft()

        if name not in graph:
            if val == 0:
                if name not in state:
                    state[name] = 1
                else:
                    state[name] += 1
            continue

        mod = state[name]
        out = val

        # flipflop
        if mod.type == "%":
            if val == 0:
                mod.val ^= 1
                out = mod.val
            elif val == 1:
                continue
            else:
                raise ValueError("Invalid value")

        # nand or inverter
        elif mod.type == "&":
            mod.input[sender] = val
            out = int(sum(mod.input.values()) != len(mod.input))
            mod.val = out

            # part2
            if len(mod.input.values()) > 6 and out == 0:
                state[name + ".out"] = out

        for dest in graph[name]:
            # print(name, "-low" if out == 0 else "-high", "->", dest)
            if out == 0:
                lo += 1
            else:
                hi += 1

            q.append((dest, out, name))

    return lo, hi


def part1(filename):
    graph, state, _ = parse(io.get_lines(filename))

    losum = hisum = 0

    for _ in range(0, 1000):
        lo, hi = pulse(graph, state, ("broadcaster", 0, "button"))
        losum += lo
        hisum += hi

    return losum * hisum


# for understanding the problem, very useful
def create_dotfile(graph, state):
    with open("graph.dot", "w") as f:
        f.write("digraph G {\n")
        for name, dests in graph.items():
            for dest in dests:
                d = dest
                if dest in state and state[dest].type is not None:
                    d = "\\" + state[dest].type + d
                n = name
                if name in state and state[name].type is not None:
                    n = "\\" + state[name].type + n
                f.write(f'"{n}" -> "{d}";\n')
        f.write("}")


def part2(filename):
    graph, state, exits = parse(io.get_lines(filename))

    # create_dotfile(graph, state)

    # if we look at the graph above we see that the schematic revolves around 4 large counters:
    counters = {}
    for name, mod in state.items():
        if len(mod.input.values()) > 6:
            counters[name] = []

    # find the cycles of the counters, and then it's the same cycle math as day 8
    i = 0
    while True:
        pulse(graph, state, ("broadcaster", 0, "button"), i)
        i += 1
        for c in counters:
            if state.get(c + ".out", None) == 0:
                counters[c].append(i)
                state[c + ".out"] = None

        if sum([len(v) for v in counters.values()]) == len(counters) * 2:
            break

    cycles = []
    for offsets in counters.values():
        cycles.append(offsets[1] - offsets[0])

    lcm = 1
    for i in cycles:
        lcm = lcm * i // gcd(lcm, i)

    return lcm


def main():
    assert part1("example.txt") == 32000000
    assert part1("example2.txt") == 11687500
    print(part1("../input/2023/day20.txt"))

    print(part2("../input/2023/day20.txt"))


if __name__ == "__main__":
    sys.exit(main())
