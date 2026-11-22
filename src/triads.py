from itertools import permutations
CLASS_CODES = [3, 6, 7, 10, 11, 15, 21, 23, 25, 27, 30, 31, 63]
CODE_TO_CLASS = {code: k + 1 for k, code in enumerate(CLASS_CODES)}
EDGE_ORDER = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]


def config_code(x, edge_set):
    code = 0
    for bit, (i, j) in enumerate(EDGE_ORDER):
        if (x[i], x[j]) in edge_set:
            code |= 1 << bit
    return code


def canonical_code(a, b, c, edge_set):
    return min(config_code(p, edge_set) for p in permutations((a, b, c)))


def triad_class(a, b, c, edge_set):
    return CODE_TO_CLASS.get(canonical_code(a, b, c, edge_set), 0)

def _is_connected(edge_set):
    undirected = {frozenset(e) for e in edge_set}

    return len(undirected) >= 2


def verify_classes():
    orbits = set()
    connected = set()
    for config in range(64):
        es = {EDGE_ORDER[k] for k in range(6) if config >> k & 1}
        canon = canonical_code(0, 1, 2, es)
        orbits.add(canon)
        if _is_connected(es):
            connected.add(canon)
    assert len(orbits) == 16, len(orbits)
    assert sorted(connected) == CLASS_CODES, sorted(connected)
    return len(orbits), sorted(connected)
def triad_census(nodes, edges):
    edge_set = set(edges)
    neighbours = {n: set() for n in nodes}
    for u, v in edges:
        neighbours[u].add(v)
        neighbours[v].add(u)

    seen = set()
    for u in nodes:
        nbrs = sorted(neighbours[u])
        for i in range(len(nbrs)):
            for j in range(i + 1, len(nbrs)):
                seen.add(tuple(sorted((u, nbrs[i], nbrs[j]))))

    counts = [0] * 13
    for a, b, c in seen:
        k = triad_class(a, b, c, edge_set)
        counts[k - 1] += 1       
    return counts
