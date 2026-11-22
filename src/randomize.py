

import random
from collections import Counter


def degree_sequences(edges):
    """Return (out_degree Counter, in_degree Counter)."""
    out_deg = Counter(u for u, _ in edges)
    in_deg = Counter(v for _, v in edges)
    return out_deg, in_deg


def randomize(edges, attempts, seed):

    rng = random.Random(seed)
    edge_list = list(edges)          
    edge_set = set(edge_list)        
    m = len(edge_list)
    if m < 2:
        return edge_list

    for _ in range(attempts):
        i = rng.randrange(m)
        j = rng.randrange(m)
        if i == j:                
            continue
        a, b = edge_list[i]
        c, d = edge_list[j]

        if a == d or c == b:
            continue
        if (a, d) in edge_set or (c, b) in edge_set:
            continue
        edge_set.remove((a, b))
        edge_set.remove((c, d))
        edge_set.add((a, d))
        edge_set.add((c, b))
        edge_list[i] = (a, d)
        edge_list[j] = (c, b)

    assert degree_sequences(edge_list) == degree_sequences(edges), "degree sequence changed!"
    assert len(edge_set) == m and all(u != v for u, v in edge_list)
    return edge_list
