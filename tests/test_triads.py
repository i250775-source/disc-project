import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from triads import triad_class, triad_census, verify_classes, canonical_code
from randomize import randomize, degree_sequences


def test_hand_example():
    es = {("a", "b"), ("a", "c"), ("b", "c")}
    assert canonical_code("a", "b", "c", es) == 11
    assert triad_class("a", "b", "c", es) == 5
    assert triad_class("a", "b", "c", {("a", "b"), ("b", "c"), ("c", "a")}) == 9
    full = {(x, y) for x in "abc" for y in "abc" if x != y}
    assert triad_class("a", "b", "c", full) == 13
    print("hand example OK")


def test_classes():
    print("orbits / connected codes:", verify_classes())


def random_graph(n, m, seed):
    rng = random.Random(seed)
    edges = set()
    while len(edges) < m:
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:
            edges.add((u, v))
    return list(range(n)), sorted(edges)


def test_randomize_degrees():
    nodes, edges = random_graph(60, 400, 1)
    out = randomize(edges, 10 * len(edges), 2363)
    assert degree_sequences(out) == degree_sequences(edges)
    assert set(out) != set(edges)   
    print("randomize keeps all degrees OK")


def test_against_networkx():
    import networkx as nx
    nodes, edges = random_graph(80, 600, 7)
    ours = triad_census(nodes, edges)

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    theirs = nx.triadic_census(G)
    name_to_class = {}
    for name, (a, b, c) in _examples_from_nx(G).items():
        name_to_class[name] = triad_class(a, b, c, set(edges))
    for name, cls in name_to_class.items():
        if cls == 0:
            continue
        assert theirs[name] == ours[cls - 1], (name, theirs[name], ours[cls - 1])
    print("census matches networkx.triadic_census OK")


def _examples_from_nx(G):
    import networkx as nx
    from itertools import combinations
    found = {}
    for trio in combinations(list(G.nodes())[:40], 3):
        t = nx.triad_type(G.subgraph(trio))
        if t not in found:
            found[t] = trio
    return found


if __name__ == "__main__":
    test_hand_example()
    test_classes()
    test_randomize_degrees()
    test_against_networkx()
    print("ALL TESTS PASSED")
