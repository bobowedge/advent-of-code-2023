import argparse

parser = argparse.ArgumentParser("Generate new python file and data file")
parser.add_argument("day", type=int)

args = parser.parse_args()

python_file = f"day{args.day:02}.py"
data_file = f"data/day{args.day:02}.txt"

with open(python_file, "w") as f:
    f.write('''def solution1(d):
    return 0


def solution2(d):
    return 0
    
    
test = """""".splitlines()
assert(solution1(test) == 0)
assert(solution2(test) == 0)
''')
    f.write(f'''data = open("{data_file}").read().splitlines()''')
    f.write('\nprint(f"Solution 1: {solution1(data)}")\nprint(f"Solution 2: {solution2(data)}")\n')


open(data_file, 'a').close()