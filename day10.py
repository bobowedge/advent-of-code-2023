def pipe_ize(d):
    pipes = []
    start = None
    for i, line in enumerate(d):
        line = line.strip()
        pipes.append(list(line))
        if 'S' in line:
            start = (i, line.find('S'))
    return start, pipes


def find_loop(start, pipes):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    loops = [[], [], [], []]
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
            if row_diff == 1:
                if pipe == '|':
                    curr = (curr[0] + 1, curr[1])
                elif pipe == 'L':
                    curr = (curr[0], curr[1] + 1)
                elif pipe == 'J':
                    curr = (curr[0], curr[1] - 1)
                else:
                    curr = None
            elif row_diff == -1:
                if pipe == '|':
                    curr = (curr[0] - 1, curr[1])
                elif pipe == '7':
                    curr = (curr[0], curr[1] - 1)
                elif pipe == 'F':
                    curr = (curr[0], curr[1] + 1)
                else:
                    curr = None
            elif col_diff == 1:
                if pipe == '-':
                    curr = (curr[0], curr[1] + 1)
                elif pipe == '7':
                    curr = (curr[0] + 1, curr[1])
                elif pipe == 'J':
                    curr = (curr[0] - 1, curr[1])
                else:
                    curr = None
            else:
                if pipe == '-':
                    curr = (curr[0], curr[1] - 1)
                elif pipe == 'F':
                    curr = (curr[0] + 1, curr[1])
                elif pipe == 'L':
                    curr = (curr[0] - 1, curr[1])
                else:
                    curr = None
        if curr == start:
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
    start, pipes = pipe_ize(d)
    _, loop = find_loop(start, pipes)
    return len(loop) // 2


def solution2(d):
    start, pipes = pipe_ize(d)
    num_rows = len(pipes)
    num_cols = len(pipes[0])

    start_pipe, loop = find_loop(start, pipes)
    loop = set(loop)
    midloop = set()
    for (row, col) in loop:
        midloop.add((row, col, 0, 0))
        if (row, col) == start:
            pipe = start_pipe
        else:
            pipe = pipes[row][col]
        if pipe in '|LJ':
            midloop.add((row, col, -1, 0))
        if pipe in '|F7':
            midloop.add((row, col, 1, 0))
        if pipe in '-J7':
            midloop.add((row, col, 0, -1))
        if pipe in '-LF':
            midloop.add((row, col, 0, 1))
    outsides = set()
    for row in [0, num_rows - 1]:
        for col in range(num_cols):
            if (row, col) not in loop:
                outsides.add((row, col, 0, 0))
    for col in [0, num_cols - 1]:
        for row in range(num_rows):
            if (row, col) not in loop:
                outsides.add((row, col, 0, 0))
    new_points = set(outsides)
    while len(new_points) > 0:
        old_outsides = set(outsides)
        for (row, col, r2, c2) in new_points:
            if r2 == 0 and c2 == 0:
                for (x, y) in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    val = (row + x, col + y, r2, c2)
                    if ((-1 < val[0] < num_rows + 1) and
                            (-1 < val[1] < num_cols + 1) and
                            (val not in midloop)):
                        outsides.add(val)
            for x2 in [-1, 1]:
                val = (row, col, r2 + x2, c2)
                if val[2] == -2:
                    val = (row - 1, col, 0, c2)
                elif val[2] == 2:
                    val = (row + 1, col, 0, c2)
                if ((-1 < val[0] < num_rows + 1) and
                        (-1 < val[1] < num_cols + 1) and
                        (val not in midloop)):
                    outsides.add(val)
            for y2 in [-1, 1]:
                val = (row, col, r2, c2 + y2)
                if val[3] == -2:
                    val = (row, col - 1, r2, 0)
                elif val[3] == 2:
                    val = (row, col + 1, r2, 0)
                if ((-1 < val[0] < num_rows + 1) and
                        (-1 < val[1] < num_cols + 1) and
                        (val not in midloop)):
                    outsides.add(val)
        new_points = outsides.difference(old_outsides)
    inside_counts = 0
    for row in range(len(pipes)):
        for col in range(len(pipes[0])):
            if (row, col) not in loop and (row, col, 0, 0) not in outsides:
                inside_counts += 1
    return inside_counts
    
    
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
