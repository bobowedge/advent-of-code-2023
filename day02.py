def parse_line(s):
    game, draws = s.split(":")
    _, game = game.split()
    draws = draws.split(";")
    maxred, maxgreen, maxblue = 0, 0, 0
    for draw in draws:
        colors = draw.split()
        for i in range(0, len(colors), 2):
            if "red" in colors[i+1]:
                maxred = max(maxred, int(colors[i]))
            elif "blue" in colors[i+1]:
                maxgreen = max(maxgreen, int(colors[i]))
            elif "green" in colors[i+1]:
                maxblue = max(maxblue, int(colors[i]))
            else:
                raise RuntimeError("Invalid color")
    return int(game), maxred, maxblue, maxgreen


def solution1(data):
    total = 0
    for line in data:
        line = line.strip()
        game, red, blue, green = parse_line(line)
        if red <= 12 and blue <= 13 and green <= 14:
            total += game
    return total


def solution2(data):
    power_total = 0
    for line in data:
        line = line.strip()
        _, red, blue, green = parse_line(line)
        power_total += red * blue * green
    return power_total


test = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''.splitlines()
assert(solution1(test) == 8)
assert(solution2(test) == 2286)

data = open("data/day02.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
