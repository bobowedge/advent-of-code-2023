def score(string, sizes, cache={}):
    key = (string, tuple(sizes))
    if key in cache:
        return cache[key]
    if len(sizes) == 1:
        total = 0
        for idx in range(len(string) - sizes[0] + 1):
            if idx > 0 and string[idx - 1] == '#':
                break
            if '.' not in string[idx:idx+sizes[0]] and '#' not in string[idx+sizes[0]:]:
                total += 1
        return total
    possibles = len(string) - sum(sizes[1:]) - len(sizes[1:]) - sizes[0] + 1
    total = 0
    for idx in range(possibles):
        if idx > 0 and string[idx - 1] == '#':
            break
        if '.' not in string[idx:idx+sizes[0]] and string[idx+sizes[0]] != '#':
            total += score(string[idx+sizes[0]+1:], sizes[1:])
        idx += 1
    cache[(string, tuple(sizes))] = total
    return total


def solution1(d):
    total = 0
    for line in d:
        string, sizes = line.strip().split()
        sizes = [int(x) for x in sizes.split(",")]
        total += score(string, sizes)
    return total


def solution2(d):
    total = 0
    for i, line in enumerate(d):
        string, sizes = line.strip().split()
        sizes = [int(x) for x in sizes.split(",")]
        string = str("?".join([string]*5))
        sizes = [sizes[idx % len(sizes)] for idx in range(len(sizes) * 5)]
        total += score(string, sizes, cache={})
    return total
    
    
test = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()
assert(solution1(test) == 21)
assert(solution2(test) == 525152)
data = open("data/day12.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
