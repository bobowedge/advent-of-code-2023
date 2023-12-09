from math import gcd


def lcm(a, b):
    return abs(a*b) // gcd(a, b)


def parse_data(d):
    directions = [0 if x == 'L' else 1 for x in list(d[0].strip())]
    graph = {}
    for line in d[2:]:
        src, dst = line.replace(' ','').split('=')
        dstL, dstR = dst.replace('(','').replace(')','').split(',')
        graph[src] = (dstL, dstR)
    return directions, graph


def solution1(d):
    directions, graph = parse_data(d)
    lendir = len(directions)
    count = 0
    loc = 'AAA'
    while loc != 'ZZZ':
        loc = graph[loc][directions[count % lendir]]
        count += 1
    return count


def find_loop_size(loc, directions, graph):
    lendir = len(directions)
    idx = 0
    while True:
        loc = graph[loc][directions[idx % lendir]]
        idx += 1
        if loc[-1] == 'Z':
            return idx


def solution2(d):
    directions, graph = parse_data(d)
    lendir = len(directions)
    locations = []
    for g in graph.keys():
        if g[-1] == 'A':
            locations.append(g)

    loop_sizes = [find_loop_size(loc, directions, graph) for loc in locations]
    i = 1
    curr_lcm = loop_sizes[0]
    while i < len(loop_sizes):
        curr_lcm = lcm(curr_lcm, loop_sizes[i])
        i += 1
    return curr_lcm
    
    
test1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""".splitlines()
test2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".splitlines()
assert(solution1(test1) == 2)
assert(solution1(test2) == 6)
test3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".splitlines()
assert(solution2(test3) == 6)

data = open("data/day08.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
