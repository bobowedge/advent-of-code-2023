NUMBERS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}


def find_digit(s):
    for x in s:
        if x.isdigit():
            return x


def solution1(d):
    total = 0
    for line in d:
        d1 = find_digit(line)
        d2 = find_digit(line[::-1])
        total += int(d1 + d2)
    return total


def find_first_digit2(s):
    for i, x in enumerate(s):
        if x.isdigit():
            return int(x)
        for n, v in NUMBERS.items():
            if s[i:i+len(n)] == n:
                return v
    raise RuntimeError("Failed to find number")


def find_last_digit2(s):
    for i in range(len(s)-1,-1,-1):
        if s[i].isdigit():
            return int(s[i])
        for n, v in NUMBERS.items():
            if s[i:i+len(n)] == n:
                return v
    raise RuntimeError("Failed to find number")


def solution2(d):
    total = 0
    for line in d:
        d1 = find_first_digit2(line)
        d2 = find_last_digit2(line)
        total += d1 * 10 + d2
    return total


test1 = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet'''.splitlines()
assert(solution1(test1) == 142)
test2 = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''.splitlines()
assert(solution2(test2) == 281)

data = open('data/day01.txt').read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
