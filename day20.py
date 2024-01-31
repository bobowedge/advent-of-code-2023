import math


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def parse_input(d):
    switches = {}
    conjunctions = {}
    destinations = {}
    for line in d:
        line = line.replace(' ','')
        name, outputs = line.split('->')
        outputs = outputs.split(',')
        name = name.replace('%', '').replace('&', '')
        destinations[name] = outputs
        if line[0] == '%':
            switches[name] = 0
        elif line[0] == '&':
            conjunctions[name] = {}

    for name in conjunctions:
        newd = {}
        for source, dlist in destinations.items():
            if name in dlist:
                newd[source] = 0
        conjunctions[name] = newd

    return switches, conjunctions, destinations


def solution1(d):
    switches, conjunctions, destinations = parse_input(d)
    hi_pulses = 0
    lo_pulses = 0
    for i in range(1000):
        pulses = [(0, 'broadcaster', 'button')]
        while len(pulses) > 0:
            parity, dest, source = pulses.pop(0)
            if parity == 1:
                hi_pulses += 1
            else:
                lo_pulses += 1
            if dest in switches:
                if parity == 0:
                    state = switches[dest] ^ 1
                    switches[dest] = state
                    for newd in destinations[dest]:
                        pulses.append((state, newd, dest))
            elif dest in conjunctions:
                memory = conjunctions[dest]
                memory[source] = parity
                flag = 1
                for m in memory.values():
                    flag &= m
                for newd in destinations[dest]:
                    pulses.append((flag ^ 1, newd, dest))
            elif dest == 'broadcaster':
                for newd in destinations[dest]:
                    pulses.append((0, newd, dest))
    return hi_pulses * lo_pulses


def solution2(d, output):
    switches, conjunctions, destinations = parse_input(d)
    counter = 0
    # From making a diagram, we know there are 4 inputs to track
    inputs = ['xc', 'bp', 'pd', 'th']
    cycles = {}

    while len(cycles) < len(inputs):
        counter += 1
        pulses = [(0, 'broadcaster', 'button')]
        while len(pulses) > 0:
            parity, dest, source = pulses.pop(0)
            if parity == 0 and dest in inputs and dest not in cycles:
                cycles[dest] = counter
            if dest in switches:
                if parity == 0:
                    state = switches[dest] ^ 1
                    switches[dest] = state
                    for newd in destinations[dest]:
                        pulses.append((state, newd, dest))
            elif dest in conjunctions:
                memory = conjunctions[dest]
                memory[source] = parity
                flag = 1
                for m in memory.values():
                    flag &= m
                for newd in destinations[dest]:
                    pulses.append((flag ^ 1, newd, dest))
            elif dest == 'broadcaster':
                for newd in destinations[dest]:
                    pulses.append((0, newd, dest))
            elif dest == output and parity == 0:
                return counter

    nums = list(cycles.values())
    x = 1
    for i in range(4):
        x = lcm(x, nums[i])
    return x


test1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""".splitlines()
test2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".splitlines()
assert(solution1(test1) == 32000000)
assert(solution1(test2) == 11687500)
data = open("data/day20.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data, 'rx')}")
