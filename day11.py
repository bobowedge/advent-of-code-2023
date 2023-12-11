def parse_universe(d):
    empty_columns = set([x for x in range(len(d))])
    empty_rows = set()
    galaxies = set()
    for row, line in enumerate(d):
        line = line.strip()
        if '#' not in line:
            empty_rows.add(row)
        col = line.find('#')
        while col >= 0:
            galaxies.add((row, col))
            empty_columns.discard(col)
            col = line.find('#', col + 1)
    return galaxies, empty_rows, empty_columns


def find_path(gal1, gal2, empty_rows, empty_columns, expansion=2):
    row1, col1 = gal1
    row2, col2 = gal2
    path = abs(row1 - row2)
    path += abs(col1 - col2)
    minrow = min(row1, row2)
    maxrow = max(row1, row2)
    for r in range(minrow, maxrow):
        if r in empty_rows:
            path += expansion - 1
    mincol = min(col1, col2)
    maxcol = max(col1, col2)
    for c in range(mincol, maxcol):
        if c in empty_columns:
            path += expansion - 1
    return path


def find_total_path(d, expansion):
    galaxies, empty_rows, empty_columns = parse_universe(d)

    total_path = 0
    for g1 in galaxies:
        for g2 in galaxies:
            if g1 <= g2:
                continue
            total_path += find_path(g1, g2, empty_rows, empty_columns, expansion)
    return total_path


def solution1(d):
    return find_total_path(d, 2)


def solution2(d, expansion):
    return find_total_path(d, expansion)
    
    
test = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".splitlines()
assert(solution1(test) == 374)
assert(solution2(test, 10) == 1030)
assert(solution2(test, 100) == 8410)
data = open("data/day11.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data, 1000000)}")
