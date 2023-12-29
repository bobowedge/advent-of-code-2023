import heapq


def make_heat_map(d):
    heat_map = {}
    for i, row in enumerate(d):
        for j, val in enumerate(row):
            heat_map[(i, j)] = int(val)
    return heat_map, len(d), len(d[0])


def heat_loss(heat_map, start, end, min_move, max_move):
    queue = [(0, *start, 0, 0)]
    seen = set()

    all_dirs = {(1, 0), (-1, 0), (0, 1), (0, -1)}
    while len(queue) > 0:
        heat, x, y, dir1, dir2 = heapq.heappop(queue)
        if (x, y) == end:
            return heat
        if (x, y, dir1, dir2) in seen:
            continue
        seen.add((x, y, dir1, dir2))
        not_turns = {(dir1, dir2), (-dir1, -dir2)}
        for dx, dy in all_dirs.difference(not_turns):
            new_x = x
            new_y = y
            new_heat = heat
            for i in range(1, max_move + 1):
                new_x += dx
                new_y += dy
                if (new_x, new_y) in heat_map:
                    new_heat += heat_map[(new_x, new_y)]
                    if i >= min_move:
                        heapq.heappush(queue, (new_heat, new_x, new_y, dx, dy))


def solution1(d):
    heat_map, max_row, max_col = make_heat_map(d)
    return heat_loss(heat_map, (0, 0), (max_row - 1, max_col - 1), 1, 3)


def solution2(d):
    heat_map, max_row, max_col = make_heat_map(d)
    return heat_loss(heat_map, (0, 0), (max_row - 1, max_col - 1), 4, 10)
    
    
test1 = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".splitlines()

test2 = """111111111111
999999999991
999999999991
999999999991
999999999991""".splitlines()

assert(solution1(test1) == 102)
assert(solution2(test1) == 94)
assert(solution2(test2) == 71)
data = open("data/day17.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
