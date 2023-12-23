import sys
from collections import defaultdict
from heapq import heappop, heappush

from .grid import OFFSETS_STRAIGHT


def bfs(start, graph, visitor=lambda n: ()):
    visited = set()
    q = []

    q.append(start)
    visited.add(start)

    while len(q) > 0:
        cur = q.pop(0)
        visitor(cur)
        for n in graph.get(cur, []):
            if n not in visited:
                q.append(n)
                visited.add(n)

    return visited


def dfs(start, graph, visitor=lambda n: ()):
    visited = set()
    q = []

    q.append(start)

    while len(q) > 0:
        cur = q.pop()
        if cur not in visited:
            visited.add(cur)
            visitor(cur)

        for n in graph.get(cur, []):
            if n not in visited:
                q.append(n)

    return visited


def get_path(prev, start, end):
    path = []
    u = end
    if u in prev or u == start:
        while u:
            path.insert(0, u)
            u = prev.get(u)

    return path


def dijkstra(grid, starts, neighbours: lambda grid, cur: [], get_dist: lambda grid, pos, n: 0):
    dist = {}
    prev = {}
    pq = []

    for start in starts:
        heappush(pq, (0, start))

    while len(pq) > 0:
        (val, cur) = heappop(pq)

        for n in neighbours(grid, cur):
            if n not in dist:
                new_val = val + get_dist(grid, cur, n)
                if new_val < dist.get(n, sys.maxsize):
                    if n not in dist:
                        dist[n] = new_val
                        prev[n] = cur
                        heappush(pq, (new_val, n))

    return dist, prev


def from_grid(grid, condition):
    graph = defaultdict(set)
    for y in range(grid.minY, grid.maxY + 1):
        for x in range(grid.minX, grid.maxX + 1):
            pos = (x, y)
            val = grid.get(pos)
            for o in OFFSETS_STRAIGHT:
                neighbour = (x + o[0], y + o[1])
                other = grid.get(neighbour)
                if other and condition(pos, neighbour, val, other):
                    graph[pos].add(neighbour)

    return graph


def floyd_warshall(graph):
    distance = defaultdict(int)
    for n, neighbours in graph.items():
        for other, _ in graph.items():
            if n != other:
                distance[(n, other)] = 1 if other in neighbours else float("inf")

    for k in graph.keys():
        for i in graph.keys():
            for j in graph.keys():
                if i != j and j != k:
                    distance[(i, j)] = min(distance[(i, j)], distance[(i, k)] + distance[(k, j)])

    return distance
