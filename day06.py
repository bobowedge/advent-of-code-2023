from math import sqrt, ceil, floor


def parse_data1(d):
    _, times = d[0].split(":")
    times = [int(x) for x in times.split()]
    _, distances = d[1].split(":")
    distances = [int(x) for x in distances.split()]
    return times, distances


def parse_data2(d):
    time = d[0].split(":")[1]
    time = int(time.replace(" ", ""))
    distance = d[1].split(":")[1]
    distance = int(distance.replace(" ", ""))
    return time, distance


def ways_to_beat(t, d):
    # Solve (time - held) * held - distance = 0 for held
    # h^2 - t * h + d = 0
    h1 = (t - sqrt(t*t - 4*d))/2
    h2 = (t + sqrt(t*t - 4*d))/2
    h1 = floor(h1 + 1)
    h2 = ceil(h2 - 1)
    return h2 - h1 + 1


def solution1(d):
    total = 1
    times, distances = parse_data1(d)
    for t, d in zip(times, distances):
        total *= ways_to_beat(t, d)
    return total


def solution2(d):
    time, distance = parse_data2(d)
    return ways_to_beat(time, distance)


test = '''Time:      7  15   30
Distance:  9  40  200'''.splitlines()
assert(solution1(test) == 288)
assert(solution2(test) == 71503)

data = open("data/day06.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
