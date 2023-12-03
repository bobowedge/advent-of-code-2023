SYMBOLS = set(list('*/&-+%$@#='))


def solution1(d):
    matrix = []
    for line in d:
        line = line.strip()
        line = list(line)
        matrix.append(line)

    total = 0
    for row, line in enumerate(matrix):
        strnum = ''
        for col, char in enumerate(line):
            if char.isdigit():
                strnum += char
            if len(strnum) > 0 and (col == len(matrix[0]) - 1 or not char.isdigit()):
                num = int(strnum)
                around = set()
                minrow = max(row - 1, 0)
                mincol = max(col - len(strnum) - 1, 0)
                maxrow = min(row + 2, len(matrix))
                maxcol = min(col + 1, len(matrix[0]))
                for r in range(minrow, maxrow):
                    for c in range(mincol, maxcol):
                        around.add(matrix[r][c])
                if len(SYMBOLS.intersection(around)):
                    total += num
                strnum = ''
    return total


def solution2(d):
    matrix = []
    for line in d:
        line = line.strip()
        line = list(line)
        matrix.append(line)

    total = 0
    for row, line in enumerate(matrix):
        for col, char in enumerate(line):
            if char == '*':
                numbers = set()
                minrow = max(row - 1, 0)
                mincol = max(col - 1, 0)
                maxrow = min(row + 2, len(matrix))
                maxcol = min(col + 2, len(matrix[0]))
                for r in range(minrow, maxrow):
                    for c in range(mincol, maxcol):
                        if matrix[r][c].isdigit():
                            start = c
                            end = c
                            while start >= 0 and matrix[r][start].isdigit():
                                start -= 1
                            while end < len(matrix[0]) and matrix[r][end].isdigit():
                                end += 1
                            num = int(''.join(matrix[r][start+1:end]))
                            numbers.add(num)
                if len(numbers) == 2:
                    x = numbers.pop()
                    y = numbers.pop()
                    total += x * y
    return total


test = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''.splitlines()
assert(solution1(test) == 4361)
assert(solution2(test) == 467835)

data = open("data/day03.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")

