#!/usr/bin/env python3

import sys
from collections import deque, namedtuple

from utils import io

cond = namedtuple("cond", ["var", "op", "val", "dest"])


def parse(input):
    rules_input, parts_input = input.strip().split("\n\n")

    rules = {}
    for r in rules_input.strip().split("\n"):
        name, conds = r.split("{")

        lst = []
        for c in conds[:-1].split(","):
            if ":" in c:
                bool, dest = c.split(":")
                var = bool[0]
                op = bool[1]
                val = int(bool[2:])
                lst.append(cond(var, op, val, dest))
            else:
                dest = c
                lst.append(cond(None, None, None, dest))
        rules[name] = lst

    parts = []
    for p in parts_input.strip().split("\n"):
        part = {}
        for v in p[1:-1].split(","):
            var, val = v.split("=")
            part[var] = int(val)
        parts.append(part)

    return rules, parts


def accepted(rules, p):
    q = ["in"]

    while len(q) > 0:
        name = q.pop()

        if name == "A":
            return True
        elif name == "R":
            return False

        for r in rules[name]:
            if r.op is None or (r.op == "<" and p[r.var] < r.val) or (r.op == ">" and p[r.var] > r.val):
                q.append(r.dest)
                break


def part1(filename):
    rules, parts = parse(io.get_input(filename))

    s = 0
    for p in parts:
        if accepted(rules, p):
            s += sum(p.values())

    return s


def find_all_paths(graph, start):
    paths = []
    queue = deque([(start, [start])])

    while queue:
        cur, cur_path = queue.popleft()

        if cur.dest == "A":
            paths.append(cur_path)

        if cur.dest in graph:
            inverse = []
            for n in graph[cur.dest]:
                if n not in cur_path:
                    queue.append((n, cur_path + inverse + [n]))

                    if n.op is not None:
                        if n.op == "<":
                            inv = cond(n.var, ">", n.val - 1, None)
                        else:
                            inv = cond(n.var, "<", n.val + 1, None)
                        inverse.append(inv)

    return paths


def part2(filename):
    rules, _ = parse(io.get_input(filename))

    start = cond(None, None, None, "in")
    paths = find_all_paths(rules, start)

    sum = 0
    ranges = []
    for path in paths:
        r = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
        for c in path:
            if c.op is not None:
                if c.op == "<":
                    r[c.var] = (r[c.var][0], c.val - 1)
                else:
                    r[c.var] = (c.val + 1, r[c.var][1])
        # print(r)
        ranges.append(r)

    sum = 0
    for r in ranges:
        p = 1
        p *= r["x"][1] - r["x"][0] + 1
        p *= r["m"][1] - r["m"][0] + 1
        p *= r["a"][1] - r["a"][0] + 1
        p *= r["s"][1] - r["s"][0] + 1
        sum += p

    return sum


def main():
    assert part1("example.txt") == 19114
    print(part1("../input/2023/day19.txt"))

    assert part2("example.txt") == 167409079868000
    print(part2("../input/2023/day19.txt"))


if __name__ == "__main__":
    sys.exit(main())
