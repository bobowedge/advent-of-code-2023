def parse_input(d):
    seeds = []
    maps = []
    new_map = []
    for line in d:
        if len(line.strip()) == 0:
            continue
        if line[:6] == 'seeds:':
            seeds = [int(x) for x in line[7:].split()]
        elif 'map' in line:
            if len(new_map) > 0:
                new_map.sort()
                maps.append(new_map)
            new_map = []
        else:
            inputs = tuple([int(x) for x in line.split()])
            new_map.append(inputs)
    if len(new_map) > 0:
        new_map.sort()
        maps.append(new_map)
    return seeds, maps


def find_loc(seed, maps):
    input_value = seed
    output_value = None
    for m in maps:
        for y1, x1, inc in m:
            if x1 <= input_value < x1 + inc:
                output_value = y1 + (input_value - x1)
        if output_value is not None:
            input_value = output_value
        output_value = None
    return input_value


def solution1(d):
    seeds, maps = parse_input(d)
    min_loc = 18446744073709551616
    for seed in seeds:
        loc = find_loc(seed, maps)
        min_loc = min(loc, min_loc)
        if min_loc is None:
            min_loc = loc
        else:
            min_loc = min(min_loc, loc)
    return min_loc


def input_ranges(out_start, out_stop, m):
    ranges = []
    for y1, x1, inc in m:
        if y1 > out_start:
            stop = min(y1, out_stop)
            ranges.append((out_start, stop))
            out_start = stop
        if y1 <= out_start < y1 + inc:
            in_start = x1 + (out_start - y1)
            stop = min(y1 + inc, out_stop)
            in_stop = x1 + (stop - y1)
            ranges.append((in_start, in_stop))
            out_start = stop
        if out_start == out_stop:
            break
    if out_start != out_stop:
        ranges.append((out_start, out_stop))
    return ranges


def solution2(d):
    seeds, maps = parse_input(d)
    ranges = [(0, maps[-1][-1][0] + maps[-1][-1][2])]
    for m in maps[::-1]:
        new_ranges = []
        for r in ranges:
            irs = input_ranges(r[0], r[1], m)
            new_ranges.extend(irs)
        ranges = new_ranges

    for r1, r2 in ranges:
        for i in range(0, len(seeds), 2):
            seed_start = seeds[i]
            seed_stop = seeds[i] + seeds[i+1]
            if (r1 <= seed_start < r2) or (seed_start <= r1 < seed_stop):
                best_seed = max(r1, seed_start)
                return find_loc(best_seed, maps)


test = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''.splitlines()
assert(solution1(test) == 35)
assert(solution2(test) == 46)


data = open("data/day05.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
