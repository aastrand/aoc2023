#!/usr/bin/env python3

import sys
from collections import defaultdict

from networkx import Graph
from networkx.algorithms.connectivity.cuts import minimum_edge_cut
from networkx.algorithms.traversal import bfs_tree
from utils import io
from utils.graph import bfs, create_dotfile


def part1(filename, example=False):
    graph = defaultdict(set)
    for line in io.get_lines(filename):
        node, neighours = line.split(": ")
        for n in neighours.split(" "):
            graph[node].add(n)
            graph[n].add(node)

    # visualize with neato: neato -Tpng graph.dot > graph.png; open graph.png
    create_dotfile(graph)

    # look at ^, these are
    if example:
        pairs = [
            ("hfx", "pzl"),
            ("cmg", "bvb"),
            ("jqt", "nvd"),
        ]
    else:
        pairs = [
            ("gzr", "qnz"),
            ("hgk", "pgz"),
            ("xgs", "lmj"),
        ]

    for p1, p2 in pairs:
        graph[p1].remove(p2)
        graph[p2].remove(p1)

    p = 1
    candidates = set(graph.keys())
    while candidates:
        visited = bfs(candidates.pop(), graph)
        p *= len(visited)
        candidates -= visited

    return p


def part1nx(filename, example=False):
    graph = Graph()
    for line in io.get_lines(filename):
        node, neighours = line.split(": ")
        for n in neighours.split(" "):
            graph.add_edge(node, n)

    for p1, p2 in minimum_edge_cut(graph):
        graph.remove_edge(p1, p2)

    p = 1
    candidates = set(graph.nodes())
    while candidates:
        visited = bfs_tree(graph, candidates.pop()).nodes()
        p *= len(visited)
        candidates -= visited

    return p


def main():
    assert part1("example.txt", True) == 54
    print(part1("../input/2023/day25.txt"))
    print(part1nx("../input/2023/day25.txt"))


if __name__ == "__main__":
    sys.exit(main())
