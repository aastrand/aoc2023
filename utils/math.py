def manhattan_dist(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def sign(a):
    return (a > 0) - (a < 0)


def poly_area(p):
    return 0.5 * abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in segments(p)))


def segments(p):
    return zip(p, p[1:] + [p[0]])
