RIGHT = (1, 0)
LEFT = (-1, 0)
BOTTOM = (0, 1)
TOP = (0, -1)
TOP_LEFT = (-1, -1)
BOTTOM_RIGHT = (1, 1)
TOP_RIGHT = (1, -1)
BOTTOM_LEFT = (-1, 1)

OFFSETS = (RIGHT, LEFT, BOTTOM, TOP, TOP_LEFT,
           BOTTOM_RIGHT, TOP_RIGHT, BOTTOM_LEFT)
OFFSETS_STRAIGHT = (RIGHT, LEFT, TOP, BOTTOM)

RIGHT_3D = (1, 0, 0)
LEFT_3D = (-1, 0, 0)
BOTTOM_3D = (0, 1, 0)
TOP_3D = (0, -1, 0)
FRONT_3D = (0, 0, 1)
BEHIND_3D = (0, 0, -1)

OFFSETS_STRAIGHT_3D = (RIGHT_3D, LEFT_3D, TOP_3D,
                       BOTTOM_3D, FRONT_3D, BEHIND_3D)


class Grid:
    def __init__(self):
        self.data = {}
        self.minX = None
        self.maxX = None
        self.minY = None
        self.maxY = None

    def set(self, coords, val):
        self.set_at(coords[0], coords[1], val)

    def set_at(self, x, y, val):
        self.minX = min(
            self.minX if self.minX is not None else float('inf'), x)
        self.maxX = max(self.maxX if self.maxX is not None else 0, x)
        self.minY = min(
            self.minY if self.minY is not None else float('inf'), y)
        self.maxY = max(self.maxY if self.maxY is not None else 0, y)
        self.data[(x, y)] = val

    def get(self, coords):
        return self.get_at(coords[0], coords[1])

    def get_at(self, x, y):
        return self.data.get((x, y))

    def items(self):
        return self.data.items()

    def print_output(self, default="."):
        return self.print_output_from(self.minX, self.maxX, self.minY, self.maxY, default)

    def print_output_from(self, minX, maxX, minY, maxY, default="."):
        rows = []
        for y in range(minY, maxY + 1):
            r = []
            for x in range(minX, maxX + 1):
                r.append(str(self.data.get((x, y), default)))
            rows.append("".join(r))

        return rows

    def print(self, default="."):
        self.print_from(self.minX, self.maxX, self.minY, self.maxY, default)

    def print_from(self, minX, maxX, minY, maxY, default="."):
        for row in self.print_output_from(minX, maxX, minY, maxY, default):
            print(row)
        print()

    def from_lines(lines, visitor=lambda *a, **kw: 0):
        grid = Grid()
        for y in range(0, len(lines)):
            for x in range(0, len(lines[y])):
                pos = (x, y)
                val = lines[y][x]
                grid.set(pos, val)

                visitor(grid, pos, val)

        return grid

    def flood_fill(self, pos, visitor=lambda _: ()):
        q = [pos]
        visited = set()
        visited.add(pos)

        while len(q) > 0:
            pos = q.pop(0)
            visitor(self, pos)

            for o in OFFSETS_STRAIGHT:
                neighbour = (pos[0] + o[0], pos[1] + o[1])
                if self.get(neighbour) == "." and neighbour not in visited:
                    q.append(neighbour)
                    visited.add(neighbour)

        return visited


def adjecent_3d(c1, c2):
    if c1 == c2:
        return False

    diffs = []
    same = 0
    for i in range(0, 3):
        diffs.append(abs(c1[i] - c2[i]))
        if diffs[i] == 0:
            same += 1

    return same == 2 and (diffs[0] <= 1 and diffs[1] <= 1 and diffs[2] <= 1)


def inside_3d(point, bounds):
    inside = True
    for i in range(0, 3):
        inside &= (point[i] >= bounds[0][i] and
                   point[i] < bounds[1][i] + 1)

    return inside


def neighbours_3d(point):
    for o in OFFSETS_STRAIGHT_3D:
        yield (point[0] + o[0], point[1] + o[1], point[2] + o[2])


def flood_fill_3d(start, blocked, bounds):
    assert start not in blocked

    visited = set()
    q = [start]

    while len(q) > 0:
        cur = q.pop()
        visited.add(cur)

        for n in neighbours_3d(cur):
            if n not in visited and inside_3d(n, bounds) and n not in blocked:
                q.append(n)

    return visited
