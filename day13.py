def parse_data(d):
    patterns = []
    pattern = []
    for line in d:
        line = [0 if x == '.' else 1 for x in line.strip()]
        if len(line) == 0:
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    if len(pattern) > 0:
        patterns.append(pattern)
    return patterns


def find_reflections(p):
    horizontal = set()
    for row in range(1, len(p)):
        is_reflection = True
        for idx in range(0, row):
            if row - 1 - idx < 0 or row + idx >= len(p):
                break
            if p[row - 1 - idx] != p[row + idx]:
                is_reflection = False
                break
        if is_reflection:
            horizontal.add(row)

    vertical = set()
    for col in range(1, len(p[0])):
        is_reflection = True
        for idx in range(0, col):
            if col - 1 - idx < 0 or col + idx >= len(p[0]):
                break
            col1 = [prow[col-1-idx] for prow in p]
            col2 = [prow[col+idx] for prow in p]
            if col1 != col2:
                is_reflection = False
                break
        if is_reflection:
            vertical.add(col)

    return horizontal, vertical


def solution1(d):
    patterns = parse_data(d)
    total = 0
    for pattern in patterns:
        h, v = find_reflections(pattern)
        if len(h) > 0:
            total += 100 * h.pop()
        elif len(v) > 0:
            total += v.pop()
    return total


def solution2(d):
    patterns = parse_data(d)
    total = 0
    for pattern in patterns:
        h, v = find_reflections(pattern)
        flag = False
        for row in range(len(pattern)):
            for col in range(len(pattern[row])):
                pattern[row][col] ^= 1
                newh, newv = find_reflections(pattern)
                newh = newh.difference(h)
                newv = newv.difference(v)
                if len(newh) == 0 and len(newv) == 0:
                    pattern[row][col] ^= 1
                    continue
                elif len(newh) > 0:
                    total += 100 * newh.pop()
                elif len(newv) > 0:
                    total += newv.pop()
                flag = True
                break
            if flag:
                break
    return total
    
    
test = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".splitlines()
assert(solution1(test) == 405)
assert(solution2(test) == 400)
data = open("data/day13.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
