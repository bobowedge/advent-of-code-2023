def matrix(d):
    """
    Turn data into matrix and find start
    """
    pipes = []
    start = None
    for i, line in enumerate(d):
        line = line.strip()
        pipes.append(list(line))
        if 'S' in line:
            start = (i, line.find('S'))
    return start, pipes


def find_loop(start, pipes):
    """
    Find the main loop, given the start and the pipe matrix
    Also, give the pipe type of the start
    """
    # Four directions to search from start
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    loops = [[], [], [], []]

    # Try to build a loop in each direction (two should be successful)
    for i, loop in enumerate(loops):
        loops[i].append(start)
        curr = (start[0] + directions[i][0], start[1] + directions[i][1])
        prev = start
        while curr is not None and curr != start:
            loops[i].append(curr)
            if curr[0] >= len(pipes) or curr[1] >= len(pipes[0]):
                curr = None
                break
            pipe = pipes[curr[0]][curr[1]]
            row_diff = curr[0] - prev[0]
            col_diff = curr[1] - prev[1]
            prev = curr
            # previous pipe was above
            if row_diff == 1:
                if pipe == '|':
                    curr = (curr[0] + 1, curr[1])
                elif pipe == 'L':
                    curr = (curr[0], curr[1] + 1)
                elif pipe == 'J':
                    curr = (curr[0], curr[1] - 1)
                else:
                    curr = None
            # previous pipe was below
            elif row_diff == -1:
                if pipe == '|':
                    curr = (curr[0] - 1, curr[1])
                elif pipe == '7':
                    curr = (curr[0], curr[1] - 1)
                elif pipe == 'F':
                    curr = (curr[0], curr[1] + 1)
                else:
                    curr = None
            # previous pipe was left
            elif col_diff == 1:
                if pipe == '-':
                    curr = (curr[0], curr[1] + 1)
                elif pipe == '7':
                    curr = (curr[0] + 1, curr[1])
                elif pipe == 'J':
                    curr = (curr[0] - 1, curr[1])
                else:
                    curr = None
            # previous pipe was right
            else:
                if pipe == '-':
                    curr = (curr[0], curr[1] - 1)
                elif pipe == 'F':
                    curr = (curr[0] + 1, curr[1])
                elif pipe == 'L':
                    curr = (curr[0] - 1, curr[1])
                else:
                    curr = None
        # Back to start
        if curr == start:
            # Determine starting pipe from last and first pipes in loop
            if (curr[0] - prev[0]) == 1:
                if (loops[i][1][1] - curr[1]) == 1:
                    start_pipe = 'L'
                elif (loops[i][1][1] - curr[1]) == -1:
                    start_pipe = 'J'
                else:
                    start_pipe = '|'
            elif (curr[0] - prev[0]) == -1:
                if (loops[i][1][1] - curr[1]) == 1:
                    start_pipe = 'F'
                elif (loops[i][1][1] - curr[1]) == -1:
                    start_pipe = '7'
                else:
                    start_pipe = '|'
            elif (curr[1] - prev[1]) == 1:
                if (loops[i][1][0] - curr[0]) == 1:
                    start_pipe = '7'
                elif (loops[i][1][0] - curr[0]) == -1:
                    start_pipe = 'J'
                else:
                    start_pipe = '-'
            else:
                if (loops[i][1][0] - curr[0]) == 1:
                    start_pipe = 'F'
                elif (loops[i][1][0] - curr[0]) == -1:
                    start_pipe = 'L'
                else:
                    start_pipe = '-'
            return start_pipe, loops[i]
    return None


def solution1(d):
    start, pipes = matrix(d)
    _, loop = find_loop(start, pipes)
    return len(loop) // 2


def add_to_outsides(pt, loop, nrows, ncols, oset):
    if((-1 < pt[0] < nrows + 1) and
       (-1 < pt[1] < ncols + 1) and
       (pt not in loop)):
        oset.add(pt)


def orig_solution2(d):
    start, pipes = matrix(d)
    num_rows = len(pipes)
    num_cols = len(pipes[0])

    start_pipe, loop = find_loop(start, pipes)
    loop = set(loop)
    loop_with_midpoints = set()
    for (row, col) in loop:
        loop_with_midpoints.add((row, col, 0, 0))
        if (row, col) == start:
            pipe = start_pipe
        else:
            pipe = pipes[row][col]
        # Add all possible midpoints between pipes
        if pipe in '|LJ':
            loop_with_midpoints.add((row, col, -1, 0))
        if pipe in '|F7':
            loop_with_midpoints.add((row, col, 1, 0))
        if pipe in '-J7':
            loop_with_midpoints.add((row, col, 0, -1))
        if pipe in '-LF':
            loop_with_midpoints.add((row, col, 0, 1))

    # Find the initial outsides (the edges not in the loop)
    outsides = set()
    for row in [0, num_rows - 1]:
        for col in range(num_cols):
            if (row, col) not in loop:
                outsides.add((row, col, 0, 0))
    for col in [0, num_cols - 1]:
        for row in range(num_rows):
            if (row, col) not in loop:
                outsides.add((row, col, 0, 0))

    # For each new point found in the last iteration, add the possible adjacent points
    # Continue until no new points are added
    new_points = set(outsides)
    while len(new_points) > 0:
        old_outsides = set(outsides)
        for (row, col, r2, c2) in new_points:
            if r2 == 0 and c2 == 0:
                # Full points in all directions (including diagonals)
                for (x, y) in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    val = (row + x, col + y, r2, c2)
                    add_to_outsides(val, loop_with_midpoints, num_rows, num_cols, outsides)
            # Half points left, right, up, or down
            for (x2, y2) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                val = (row, col, r2 + x2, c2 + y2)
                if val[2] == -2 or val[2] == 2:
                    val = (row + x2, col, 0, c2)
                elif val[3] == -2 or val[3] == 2:
                    val = (row, col + y2, r2, 0)
                add_to_outsides(val, loop_with_midpoints, num_rows, num_cols, outsides)
        new_points = outsides.difference(old_outsides)

    # Inside points are all those not in the loop and not in the outside set
    inside_counts = 0
    for row in range(len(pipes)):
        for col in range(len(pipes[0])):
            if (row, col, 0, 0) not in loop_with_midpoints and (row, col, 0, 0) not in outsides:
                inside_counts += 1
    return inside_counts


def solution2(d):
    start, pipes = matrix(d)
    num_rows = len(pipes)
    num_cols = len(pipes[0])

    start_pipe, loop = find_loop(start, pipes)
    loop = set(loop)
    loop_midpoints = set()
    for (row, col) in loop:
        if (row, col) == start:
            pipe = start_pipe
        else:
            pipe = pipes[row][col]
        # Add all possible midpoints between pipes
        if pipe in '|LJ':
            loop_midpoints.add((row, col, -1, 0))
        if pipe in '|F7':
            loop_midpoints.add((row, col, 1, 0))
        if pipe in '-J7':
            loop_midpoints.add((row, col, 0, -1))
        if pipe in '-LF':
            loop_midpoints.add((row, col, 0, 1))

    # Ray casting algorithm through midpoints
    inside_count = 0
    outside_count = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if (row, col) not in loop:
                counter = 0
                for r in range(row):
                    if (r, col, 0, 1) in loop_midpoints:
                        counter += 1
                if counter % 2 == 1:
                    inside_count += 1
                else:
                    outside_count += 1
    return inside_count


test1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF""".splitlines()
test2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""".splitlines()
assert(solution1(test1) == 4)
assert(solution1(test2) == 8)

test3 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""".splitlines()
test4 = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""".splitlines()
test5 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""".splitlines()
test6 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".splitlines()
assert(solution2(test3) == 4)
assert(solution2(test4) == 4)
assert(solution2(test5) == 8)
assert(solution2(test6) == 10)

data = open("data/day10.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
