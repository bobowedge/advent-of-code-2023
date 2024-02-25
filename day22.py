def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def parse_line(line):
    values = []
    ends = line.split('~')
    for end in ends:
        parts = end.split(',')
        for part in parts:
            values.append(int(part))
    if len(values) != 6:
        raise RuntimeError("Bad parsing")
    return values

def make_brick(values):
    x1, y1, z1, x2, y2, z2 = values
    sgnx = sign(x2 - x1)
    sgny = sign(y2 - y1)
    sgnz = sign(z2 - z1)

    brick = set()
    brick.add((x1, y1, z1))
    while x1 != x2 or y1 != y2 or z1 != z2:
        x1 += sgnx
        y1 += sgny
        z1 += sgnz
        brick.add((x1, y1, z1))
    return brick

class Brick:
    def __init__(self, line=None):
        if line is None:
            self.zdict = None
            self.minz = None
            return
        
        self.zdict = {}
        self.minz = 2**32
        values = parse_line(line)
        brick = make_brick(values)
        for (x, y, z) in brick:
            zdict = self.zdict.get(z, set())
            zdict.add((x, y))
            self.zdict[z] = zdict
        self.minz = min(self.zdict.keys())

    def copy(self):
        new_copy = Brick()
        new_copy.zdict = dict(self.zdict)
        new_copy.minz = self.minz
        return new_copy

    def __lt__(self, other):
        return self.minz < other.minz

    def __str__(self):
        return str(self.zdict)

    def __repr__(self):
        return str(self.zdict)
    

def parse_input(d):
    bricks = []
    for line in d:
        brick = Brick(line)
        bricks.append(brick)
    bricks.sort()
    return bricks


def fall(old_bricks: list, fixed_blocks: dict = {}):
    count_fall = 0
    blocks_dict = dict(fixed_blocks)
    new_bricks = []

    for brick in old_bricks:
        new_brick = brick.copy()
        if len(blocks_dict) == 0:
            if new_brick.minz > 1:
                count_fall += 1
                if len(new_brick.zdict) == 1:
                    new_brick.zdict = {1: new_brick.zdict[new_brick.minz]}
                else:
                    zdict = {}
                    for oldz, vals in new_brick.zdict.items():
                        zdict[oldz - new_brick.minz + 1] = vals
                    new_brick.zdict = dict(zdict)
                new_brick.minz = 1
            new_bricks.append(new_brick)
            for z, vals in new_brick.zdict.items():
                blocks_dict[z] = blocks_dict.get(z, set()).union(vals)
        else:
            newminz = min(new_brick.minz, max(blocks_dict.keys()) + 1)
            zvalues = new_brick.zdict[new_brick.minz]
            while len(zvalues.intersection(blocks_dict.get(newminz - 1, set()))) == 0 and newminz > 1:
                newminz -= 1
            zdict = {}
            for oldz, vals in new_brick.zdict.items():
                newz = oldz - new_brick.minz + newminz
                zdict[newz] = vals
                blocks_dict[newz] = blocks_dict.get(newz, set()).union(vals)
            if newminz < new_brick.minz:
                new_brick.minz = newminz
                count_fall += 1
                new_brick.zdict = dict(zdict)
            new_bricks.append(new_brick)   
    return new_bricks, count_fall


def solution1(d):
    bricks = parse_input(d)
    count_fall = 1
    while count_fall > 0:
        bricks, count_fall = fall(bricks)
        bricks.sort()

    disintegratable = 0
    fixed_blocks = {}
    for i, brick in enumerate(bricks):
        test_bricks = list(bricks[i + 1:])
        _, count_fall = fall(test_bricks, fixed_blocks)
        for z, blocks in brick.zdict.items():
            fixed_blocks[z] = fixed_blocks.get(z, set()).union(blocks)
        if count_fall == 0:
            disintegratable += 1
    return disintegratable


def solution2(d):
    bricks = parse_input(d)
    count_fall = 1
    while count_fall > 0:
        bricks, count_fall = fall(bricks)
        bricks.sort()

    total_falls = 0
    fixed_blocks = {}
    for i in range(len(bricks)):
        _, falls = fall(bricks[i+1:], fixed_blocks)
        total_falls += falls
        for z, blocks in bricks[i].zdict.items():
            fixed_blocks[z] = fixed_blocks.get(z, set()).union(blocks)
    return total_falls
    
    
test = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""".splitlines()
assert(solution1(test) == 5)
assert(solution2(test) == 7)
data = open("data/day22.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
