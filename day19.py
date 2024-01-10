def parse_input(d):
    workflows = {}
    parts = []
    for line in d:
        if len(line.strip()) == 0:
            continue
        if line[0] == '{':
            part = line[1:-1].split(',')
            lcls = {"__builtins__": None}
            for setting in part:
                exec(setting, {"__builtins__": None}, lcls)
            p = {}
            for key, val in lcls.items():
                if key != '__builtins__':
                    p[key] = val
            parts.append(p)

        else:
            idx = line.find('{')
            name = line[:idx]
            flows = line[idx+1:-1].split(',')
            workflow = []
            for flow in flows[:-1]:
                condition, dest = flow.split(':')
                workflow.append((condition, dest))
            workflow.append(('True', flows[-1]))
            workflows[name] = workflow
    return workflows, parts


def solution1(d):
    workflows, parts = parse_input(d)
    total = 0
    for part in parts:
        current = 'in'
        while current not in ['A', 'R']:
            workflow = workflows[current]
            for condition, dest in workflow:
                statement = f'True if {condition} else False'
                if eval(statement, {"__builtins__": None}, part):
                    current = dest
                    break
            if current == 'A':
                total += part['x'] + part['a'] + part['m'] + part['s']
    return total


def flip_cond(cond):
    if '<' in cond:
        var, val = cond.split('<')
        val = int(val) - 1
        return f"{var}>{val}"
    elif '>' in cond:
        var, val = cond.split('>')
        val = int(val) + 1
        return f"{var}<{val}"
    else:
        raise RuntimeError(cond)

def solution2(d):
    workflows, _ = parse_input(d)
    paths = [('in', [])]
    possibles = []
    while len(paths) > 0:
        currd, currc = paths.pop(0)
        flips = list(currc)
        for condition, nextd in workflows[currd]:
            newc = list(flips)
            if condition != 'True':
                newc.append(condition)
                flips.append(flip_cond(condition))
            if nextd == 'A':
                possibles.append(newc)
            elif nextd != 'R':
                paths.append((nextd, newc))
        _, nextd = workflows[currd][-1]

    total = 0
    for pl in possibles:
        xrange = [0, 4001]
        srange = [0, 4001]
        mrange = [0, 4001]
        arange = [0, 4001]
        for c in pl:
            if c[:2] == 'x>':
                xrange[0] = max(xrange[0], int(c[2:]))
            elif c[:2] == 's>':
                srange[0] = max(srange[0], int(c[2:]))
            elif c[:2] == 'm>':
                mrange[0] = max(mrange[0], int(c[2:]))
            elif c[:2] == 'a>':
                arange[0] = max(arange[0], int(c[2:]))
            elif c[:2] == 'x<':
                xrange[1] = min(xrange[1], int(c[2:]))
            elif c[:2] == 's<':
                srange[1] = min(srange[1], int(c[2:]))
            elif c[:2] == 'm<':
                mrange[1] = min(mrange[1], int(c[2:]))
            elif c[:2] == 'a<':
                arange[1] = min(arange[1], int(c[2:]))
            else:
                raise RuntimeError(c)
        if xrange[0] < xrange[1] and srange[0] < srange[1] and mrange[0] < mrange[1] and arange[0] < arange[1]:
            total += ((xrange[1] - xrange[0] - 1) *
                      (srange[1] - srange[0] - 1) *
                      (mrange[1] - mrange[0] - 1) *
                      (arange[1] - arange[0] - 1))
    print(total)
    return total
    
    
test = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""".splitlines()
assert(solution1(test) == 19114)
assert(solution2(test) == 167409079868000)
data = open("data/day19.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
print(f"Solution 2: {solution2(data)}")
