def parse_data(d):
    rocks = set()
    start = None
    for row, line in enumerate(d):
        for col, char in enumerate(list(line)):
            if char == 'S':
                start = (row, col)
            elif char == '#':
                rocks.add((row, col))
    return start, rocks


def solution1(d, steps=64):
    start, rocks = parse_data(d)
    positions = set()
    positions.add(start)
    for step in range(steps):
        new_positions = set()
        for (row, col) in positions:
            for npos in [(row + 1, col), (row - 1, col), (row, col - 1), (row, col + 1)]:
                if npos not in rocks:
                    new_positions.add(npos)
        positions = new_positions
    return len(positions)


def reachable(n, start, rocks, lend):
    positions = set()
    positions.add(start)
    for step in range(n):
        new_positions = set()
        for (row, col) in positions:
            for npos in [(row + 1, col), (row - 1, col), (row, col - 1), (row, col + 1)]:
                mod_npos = (npos[0] % lend, npos[1] % lend)
                if mod_npos not in rocks:
                    new_positions.add(npos)
        positions = new_positions
    return len(positions)


def solution2(d):
    start, rocks = parse_data(d)

    x0 = 0
    x1 = 1
    x2 = 2
    y0 = reachable(65, start, rocks, len(d))
    y1 = reachable(196, start, rocks, len(d))
    y2 = reachable(327, start, rocks, len(d))

    a = ((y2 - y0) + (x0 - x2) * (y1 - y0) / (x1 - x0)) / (x2 * x2 - x0 * x0 - x1 * x1 * (x2 - x0) / (x1 - x0) + x0 * x0 * (x2 - x0) / (x1 - x0))
    b = (y1 - x1 * x1 * a - y0 + x0 * x0 * a) / (x1 - x0)
    c = y0 - x0 * x0 * a - x0 * b

    def f(n):
        return a*n*n + b*n + c

    steps = 26501365
    plot_steps = (steps - 65) // 131

    return f(plot_steps)

test = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".splitlines()
assert(solution1(test, 6) == 16)
data = open("data/day21.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
