import random


def parse_input(d):
    graph = {}
    for line in d:
        left_node, nodes = line.split(':')
        nodes = nodes.split()
        for right_node in nodes:
            left_edges = graph.get(left_node, {})
            left_edges[right_node] = 1
            graph[left_node] = left_edges
            right_edges = graph.get(right_node, {})
            right_edges[left_node] = 1
            graph[right_node] = right_edges
    return graph


def karger(graph):
    cgraph = dict(graph)
    while len(cgraph) > 2:
        u = random.choice(list(cgraph.keys()))
        v = random.choice(list(cgraph[u].keys()))
        uv_edges = {}
        for node in cgraph.keys():
            edges = dict(cgraph[node])
            if node == u or node == v:
                for n1, v1 in edges.items():
                    if n1 !=u and n1 != v:
                        uv_edges[n1] = uv_edges.get(n1, 0) + v1
            else:    
                value = edges.get(u, 0) + edges.get(v, 0)
                if value > 0:
                    edges[u + v] = value
                    if u in edges:
                        edges.pop(u)
                    if v in edges:
                        edges.pop(v)
                cgraph[node] = edges
        del cgraph[u]
        del cgraph[v]
        cgraph[u + v] = uv_edges
    return cgraph


def solution1(d):
    graph = parse_input(d)
    mincut = 0
    result = 0
    while mincut != 3:
        cgraph = karger(graph)
        a, b = list(cgraph.keys())
        mincut = cgraph[a][b]
        result = len(a) * len(b) // 9
    return result

    
    
test = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""".splitlines()
assert(solution1(test) == 54)
data = open("data/day25.txt").read().splitlines()
print(f"Solution 1: {solution1(data)}")
