def parse_input(lines):
    paths = set()
    slopes = dict()
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == '.':
                paths.add((row, col))
            elif c == '>':
                slopes[(row, col)] = (0, 1)
            elif c == '<':
                slopes[(row, col)] = (0, -1)
            elif c == 'v':
                slopes[(row, col)] = (1, 0)
            elif c == '^':
                slopes[(row, col)] = (-1, 0)
            elif c == '#':
                pass
            else:
                raise RuntimeError(f'Invalid character: {c} at {row},{col}')
    endpt = (len(lines) - 1, len(lines[0]) - 2)
    return paths, slopes, endpt

def solution1(d):
    paths, slopes, endpt = parse_input(d)

    hikes = []
    hikes.append(((0, 1), []))

    max_hike = 0
    while len(hikes) > 0:
        hike = hikes.pop()
        if hike[0] == endpt:
            hike_length = len(hike[1])
            max_hike = max(max_hike, hike_length)
            continue
        for (x, y) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            row = hike[0][0] + x
            col = hike[0][1] + y
            if (row, col) in hike[1]:
                continue
            if (row, col) in paths:
                newprev = list(hike[1])
                newprev.append(hike[0])
                hikes.append(((row, col), newprev))
            elif (row, col) in slopes:
                direction = slopes[(row, col)]
                pt2 = (row + direction[0], col + direction[1])
                if pt2 != hike[0] and pt2 in paths and pt2 not in hike[1]:
                    newprev = list(hike[1])
                    newprev.append(hike[0])
                    newprev.append((row, col))
                    hikes.append((pt2, newprev))
    return max_hike


def solution2(d):
    paths, slopes, endpt = parse_input(d)

    nodes = set()
    nodes.add((0, 1))
    nodes.add(endpt)

    for p in paths:
        slope_count = 0
        for (x, y) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (p[0] + x, p[1] + y) in slopes:
                slope_count += 1
        if slope_count == 2:
            print(p)
        if slope_count >= 2:
            nodes.add(p)

    edges = {}
    for node in nodes:
        hikes = []
        hikes.append((node, []))
        while len(hikes) > 0:
            hike = hikes.pop()
            for (x, y) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                newpt = (hike[0][0] + x, hike[0][1] + y)
                if newpt in hike[1]:
                    continue
                if newpt in nodes:
                    e = edges.get(node, {})
                    e[newpt] = len(hike[1]) + 1
                    edges[node] = e
                elif newpt in paths or newpt in slopes:
                    newprev = list(hike[1])
                    newprev.append(hike[0])
                    hikes.append((newpt, newprev))
    
    max_hike = 0
    hikes = [((0, 1), [], 0)]
    while len(hikes) > 0:
        cnode, pnodes, length = hikes.pop()
        for node, d in edges[cnode].items():
            if node in pnodes:
                continue
            if node == endpt:
                hike_length = length + d
                if hike_length == 216:
                    print(cnode, pnodes, length, d)
                max_hike = max(hike_length, max_hike)
            else:
                newpnodes = list(pnodes)
                newpnodes.append(cnode)
                newlength = length + d
                hikes.append((node, newpnodes, newlength))
    return max_hike
    
    
test = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""".splitlines()
assert(solution1(test) == 94)
assert(solution2(test) == 154)
data = open("data/day23.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
