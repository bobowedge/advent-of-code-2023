import itertools

def det(M):
    if len(M) == 4:
        return M[0] * M[3] - M[1] * M[2]
    if len(M) == 9:
        return M[0] * det([M[4], M[5], M[7], M[8]]) - M[1] * det([M[3], M[5], M[6], M[8]]) + M[2] * det([M[3], M[4], M[6], M[7]])
    if len(M) == 16:
        val = 0
        for i in range(4):
            subM = []
            for j, m in enumerate(M):
                if j < 4 or ((j - i) % 4) == 0:
                    continue
                subM.append(m)
            val += (-1)**i * M[i] * det(subM)
        return val
    raise RuntimeError("Unknown")

def parse_input(d):
    hailstones = []
    for line in d:
        line = line.replace(' ','').replace('@',',')
        values = [int(v) for v in line.split(',')]
        hailstones.append(values)
    return hailstones


def solution1(d, boundary1, boundary2):
    hailstones = parse_input(d)

    collisions = 0
    for h1, h2 in itertools.combinations(hailstones, 2):
        h1x, h1y, _, h1dx, h1dy, _ = h1
        h2x, h2y, _, h2dx, h2dy, _ = h2
        det = - h2dy * h1dx + h1dy * h2dx
        if det != 0:
            t2 = (h1dx * (h2y - h1y) - h1dy * (h2x - h1x)) / float(det)
            x = h2x + h2dx * t2
            y = h2y + h2dy * t2
            if h1dx == 0:
                t1 = t2
            else:
                t1 = (x - h1x) / float(h1dx)
            if t1 > 0 and t2 > 0 and boundary1 <= x <= boundary2 and boundary1 <= y <= boundary2:
                collisions += 1
    return collisions

def solution2(d):
    h= parse_input(d)

    M = [h[1][1] - h[0][1], h[0][4] - h[1][4], h[0][0] - h[1][0], h[1][3] - h[0][3],
         h[2][1] - h[0][1], h[0][4] - h[2][4], h[0][0] - h[2][0], h[2][3] - h[0][3],
         h[3][1] - h[0][1], h[0][4] - h[3][4], h[0][0] - h[3][0], h[3][3] - h[0][3],
         h[4][1] - h[0][1], h[0][4] - h[4][4], h[0][0] - h[4][0], h[4][3] - h[0][3]]
    
    b = [h[0][0] * h[0][4] - h[1][0] * h[1][4] - h[0][1] * h[0][3] + h[1][1] * h[1][3],
         h[0][0] * h[0][4] - h[2][0] * h[2][4] - h[0][1] * h[0][3] + h[2][1] * h[2][3],
         h[0][0] * h[0][4] - h[3][0] * h[3][4] - h[0][1] * h[0][3] + h[3][1] * h[3][3],
         h[0][0] * h[0][4] - h[4][0] * h[4][4] - h[0][1] * h[0][3] + h[4][1] * h[4][3]]
    
    detM = det(M)

    vals = []
    for i in range(4):
        bMi = list(M)
        for j in range(4):
            bMi[i + 4*j] = b[j]
        vals.append(det(bMi))

    dx = vals[0] // detM
    x = vals[1] // detM
    dy = vals[2] // detM
    y = vals[3] // detM

    t0 = (x - h[0][0]) // (h[0][3] - dx)
    t1 = (x - h[1][0]) // (h[1][3] - dx)

    dz = (h[0][2] - h[1][2] + h[0][5] * t0 - h[1][5] * t1) // (t0 - t1)

    z = h[0][2] + h[0][5] * t0 - dz * t0

    return x + y + z
    
    
test = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""".splitlines()
assert(solution1(test, 7.0, 27.0) == 2)
assert(solution2(test) == 47)
data = open("data/day24.txt").read().splitlines()
print(f"Solution 1: {solution1(data, 200000000000000.0, 400000000000000.0)}")
print(f"Solution 2: {solution2(data)}")
