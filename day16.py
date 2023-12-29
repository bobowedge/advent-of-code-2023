def make_grid(d):
    grid = {}
    for i, row in enumerate(d):
        for j, val in enumerate(row):
            if val != '.':
                grid[(i, j)] = val
    return grid, len(d), len(d[0])


def find_energized(grid, max_row, max_col, start):
    beams = set()
    beams.add(start)
    visited = set()
    visited.add(start)
    while len(beams) > 0:
        row, col, dir1, dir2 = beams.pop()
        mirror = grid.get((row, col), None)
        if mirror is None or (mirror == '-' and dir1 == 0) or (mirror == '|' and dir2 == 0):
            new_val = (row + dir1, col + dir2, dir1, dir2)
            if new_val not in visited and 0 <= new_val[0] < max_row and 0 <= new_val[1] < max_col:
                beams.add(new_val)
                visited.add(new_val)
        elif mirror == '-':
            new_val1 = (row, col + 1, 0, 1)
            new_val2 = (row, col - 1, 0, -1)
            for new_val in [new_val1, new_val2]:
                if new_val not in visited and 0 <= new_val[0] < max_row and 0 <= new_val[1] < max_col:
                    beams.add(new_val)
                    visited.add(new_val)
        elif mirror == '|':
            new_val1 = (row + 1, col, 1, 0)
            new_val2 = (row - 1, col, -1, 0)
            for new_val in [new_val1, new_val2]:
                if new_val not in visited and 0 <= new_val[0] < max_row and 0 <= new_val[1] < max_col:
                    beams.add(new_val)
                    visited.add(new_val)
        else:
            if (mirror == "\\" and dir1 == 1) or (mirror == '/' and dir1 == -1):
                new_val = (row, col + 1, 0, 1)
            elif (mirror == "\\" and dir1 == -1) or (mirror == '/' and dir1 == 1):
                new_val = (row, col - 1, 0, -1)
            elif (mirror == "\\" and dir2 == 1) or (mirror == '/' and dir2 == -1):
                new_val = (row + 1, col, 1, 0)
            else:
                new_val = (row - 1, col, -1, 0)
            if new_val not in visited and 0 <= new_val[0] < max_row and 0 <= new_val[1] < max_col:
                beams.add(new_val)
                visited.add(new_val)
    energized = set()
    for x, y, _, _ in visited:
        energized.add((x, y))
    return len(energized)


def solution1(d):
    grid, max_row, max_col = make_grid(d)
    start = (0, 0, 0, 1)
    return find_energized(grid, max_row, max_col, start)


def solution2(d):
    grid, max_row, max_col = make_grid(d)
    best_energized = 0
    for col in range(max_col):
        start_top = (0, col, 1, 0)
        energized_top = find_energized(grid, max_row, max_col, start_top)
        start_bottom = (max_row - 1, col, -1, 0)
        energized_bottom = find_energized(grid, max_row, max_col, start_bottom)
        best_energized = max(best_energized, energized_top, energized_bottom)
    for row in range(max_row):
        start_left = (row, 0, 0, 1)
        start_right = (row, max_col - 1, 0, -1)
        energized_left = find_energized(grid, max_row, max_col, start_left)
        energized_right = find_energized(grid, max_row, max_col, start_right)
        best_energized = max(best_energized, energized_left, energized_right)
    return best_energized

    
test = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....'''.splitlines()
assert(solution1(test) == 46)
assert(solution2(test) == 51)
data = open("data/day16.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
