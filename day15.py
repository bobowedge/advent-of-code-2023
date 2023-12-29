def hash_alg(s):
    hash_value = 0
    for c in s:
        hash_value += ord(c)
        hash_value *= 17
        hash_value %= 256
    return hash_value


def solution1(d):
    words = d.split(",")
    total = 0
    for word in words:
        total += hash_alg(word)
    return total


def solution2(d):
    words = d.split(",")
    boxes = [[] for x in range(256)]
    for eqn in words:
        if '-' in eqn:
            new_label = eqn[:-1]
            h = hash_alg(new_label)
            idx = None
            for i, (label, lens) in enumerate(boxes[h]):
                if new_label == label:
                    idx = i
            if idx is not None:
                boxes[h].pop(idx)
        elif '=' in eqn:
            new_label, new_lens = eqn.split('=')
            new_lens = int(new_lens)
            h = hash_alg(new_label)
            idx = None
            for i, (label, lens) in enumerate(boxes[h]):
                if label == new_label:
                    idx = i
            if idx is None:
                boxes[h].append((new_label, new_lens))
            else:
                boxes[h][idx] = (new_label, new_lens)

    total = 0
    for box_num, box in enumerate(boxes):
        for idx, (label, lens) in enumerate(box):
            total += (box_num + 1) * (idx + 1) * lens
    return total
    

test0 = "HASH"
test1 = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
assert(hash_alg(test0) == 52)
assert(solution1(test1) == 1320)
assert(solution2(test1) == 145)
data = open("data/day15.txt").read()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
