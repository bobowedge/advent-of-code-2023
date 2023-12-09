def reduce(seq):
    return [seq[i+1] - seq[i] for i in range(len(seq)-1)]


def extrapolate1(seq):
    subseq = [seq]
    lss = len(set(seq))
    while lss > 1:
        new_seq = reduce(subseq[-1])
        lss = len(set(new_seq))
        subseq.append(new_seq)
    subseq.reverse()
    val = 0
    for seq in subseq:
        val += seq[-1]
    return val


def extrapolate2(seq):
    subseq = [seq]
    lss = len(set(seq))
    while lss > 1:
        new_seq = reduce(subseq[-1])
        lss = len(set(new_seq))
        subseq.append(new_seq)
    subseq.reverse()
    val = 0
    for seq in subseq:
        val = seq[0] - val
    return val


def solution1(d):
    total = 0
    for line in d:
        seq = [int(x) for x in line.strip().split()]
        val = extrapolate1(seq)
        total += val
    return total


def solution2(d):
    total = 0
    for line in d:
        seq = [int(x) for x in line.strip().split()]
        val = extrapolate2(seq)
        total += val
    return total
    
    
test = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".splitlines()
assert(solution1(test) == 114)
assert(solution2(test) == 2)
data = open("data/day09.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
