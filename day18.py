def trench_area(vertices, perimeter):
    npts = len(vertices)

    # Shoelace formula
    area = 0
    for i in range(npts - 1):
        area += vertices[i][0] * vertices[i+1][1] - vertices[i][1] * vertices[i+1][0]
    area += vertices[npts - 1][0] * vertices[0][1] - vertices[npts - 1][1] * vertices[0][0]

    area //= 2

    # Pick's theorem: A = i + b/2 - 1
    i = area - perimeter//2 + 1

    return perimeter + i


def solution1(d):
    x = 0
    y = 0
    perimeter = 0
    vertices = [(x, y)]
    for line in d:
        direction, length, _ = line.split()
        length = int(length)
        perimeter += length
        if direction == 'R':
            x += length
        elif direction == 'L':
            x -= length
        elif direction == 'U':
            y -= length
        else:
            y += length
        if (x, y) == (0, 0):
            break
        vertices.append((x, y))

    return trench_area(vertices, perimeter)
    

def decode_color(color):
    color = color.strip('()#')
    length = int(color[0:5], 16)
    direction = int(color[5], 16)
    return length, direction


def solution2(d):
    x = 0
    y = 0
    perimeter = 0
    vertices = [(x, y)]
    for line in d:
        _, _, color = line.split()
        length, direction = decode_color(color)
        perimeter += length
        if direction == 0:
            x += length
        elif direction == 2:
            x -= length
        elif direction == 3:
            y -= length
        else:
            y += length
        if (x, y) == (0, 0):
            break
        vertices.append((x, y))

    return trench_area(vertices, perimeter)


test = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".splitlines()
assert(solution1(test) == 62)
assert(solution2(test) == 952408144115)
data = open("data/day18.txt").read().splitlines()

print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
