def print_rocks(rounds, cubes, rows, cols):
    for r in range(rows):
        rowstr = ""
        for c in range(cols):
            if (r, c) in rounds:
                rowstr += 'O'
            elif (r, c) in cubes:
                rowstr += '#'
            else:
                rowstr += '.'
        print(r, rowstr)


def parse_data(d):
    round_rocks = set()
    cube_rocks = set()
    for row, line in enumerate(d):
        for col, symbol in enumerate(line):
            if symbol == 'O':
                round_rocks.add((row, col))
            elif symbol == '#':
                cube_rocks.add((row, col))
    return round_rocks, cube_rocks, len(d), len(d[0])


def solution1(d):
    rounds, cubes, rows, cols = parse_data(d)

    for row in range(1, rows):
        for col in range(cols):
            if (row, col) in rounds:
                r = row
                rounds.remove((r, col))
                while (r - 1, col) not in rounds and (r-1, col) not in cubes and r > 0:
                    r -= 1
                rounds.add((r, col))

    total = 0
    for (row, col) in rounds:
        total += (rows - row)
    return total


def spin_cycle(rounds, cubes, rows, cols):
    # north
    rounds.sort()
    for i in range(len(rounds)):
        r, c = rounds[i]
        while (r - 1, c) not in cubes and (r - 1, c) not in rounds[:i] and r > 0:
            r -= 1
        rounds[i] = (r, c)

    # west
    rounds.sort(key=lambda x: x[1])
    for i in range(len(rounds)):
        r, c = rounds[i]
        while (r, c - 1) not in cubes and (r, c - 1) not in rounds[:i] and c > 0:
            c -= 1
        rounds[i] = (r, c)

    # south
    rounds.sort(reverse=True)
    for i in range(len(rounds)):
        r, c = rounds[i]
        while (r + 1, c) not in cubes and (r + 1, c) not in rounds[:i] and r < rows - 1:
            r += 1
        rounds[i] = (r, c)

    # east
    rounds.sort(key=lambda x: x[1], reverse=True)
    for i in range(len(rounds)):
        r, c = rounds[i]
        while (r, c + 1) not in cubes and (r, c + 1) not in rounds[:i] and c < cols - 1:
            c += 1
        rounds[i] = (r, c)

    return


def solution2(d):
    rounds, cubes, rows, cols = parse_data(d)
    total_cycles = 1000000000
    rounds = list(rounds)
    cycle_dict = {}
    cycle = 0
    while tuple(rounds) not in cycle_dict and cycle < total_cycles:
        cycle_dict[tuple(rounds)] = cycle
        spin_cycle(rounds, cubes, rows, cols)
        cycle += 1

    start = cycle_dict[tuple(rounds)]
    length = cycle - start
    end = (total_cycles - start) % length + start

    for k, v in cycle_dict.items():
        if v == end:
            total = 0
            for (row, col) in k:
                total += (rows - row)
            return total
    return 0


test = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".splitlines()
assert (solution1(test) == 136)
assert (solution2(test) == 64)

data = open("data/day14.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
