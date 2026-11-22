import gzip
import os


def _open_text(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "r")


def find_file(data_dir, base_name):
    for candidate in (base_name, base_name + ".gz"):
        path = os.path.join(data_dir, candidate)
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"Could not find {base_name} (or .gz) in {data_dir}")


def load_edges(path):
    edges = set()
    raw = 0
    self_loops = 0
    with _open_text(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            raw += 1
            u, v = int(parts[0]), int(parts[1])
            if u == v:
                self_loops += 1
                continue
            edges.add((u, v))
    return edges, raw, self_loops


def load_departments(path):

    dept_of = {}
    with _open_text(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            dept_of[int(parts[0])] = int(parts[1])
    return dept_of


def internal_edge_counts(edges, dept_of):
    counts = {d: 0 for d in set(dept_of.values())}
    for u, v in edges:
        if dept_of[u] == dept_of[v]:
            counts[dept_of[u]] += 1
    return counts


def top_departments(edges, dept_of, k=20):
    counts = internal_edge_counts(edges, dept_of)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:k]


def induced_subgraph(edges, dept_of, dept):
    nodes = sorted(n for n, d in dept_of.items() if d == dept)
    members = set(nodes)
    sub_edges = sorted((u, v) for (u, v) in edges if u in members and v in members)
    return nodes, sub_edges
