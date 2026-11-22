
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from params import (R, PAIR_NUMBER, PAIR_I, PAIR_J, NUM_RANDOM_NETWORKS,
                    SWAP_MULTIPLIER, SEED, ROLL_NUMBERS)
from data_loader import (find_file, load_edges, load_departments,
                         top_departments, induced_subgraph)
from triads import triad_census, triad_class, verify_classes, CLASS_CODES
from zscore import run_null_model, z_scores, label
from plot import plot_zscores
from network_plot import plot_network

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
RESULTS_DIR = os.path.join(HERE, "results")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    #T1
    print("=" * 70)
    print("T1  Load and clean data")
    print("=" * 70)
    edges, raw, loops = load_edges(find_file(DATA_DIR, "email-Eu-core.txt"))
    dept_of = load_departments(find_file(DATA_DIR, "email-Eu-core-department-labels.txt"))
    print(f"Edge lines read       : {raw}")
    print(f"Self-loops removed    : {loops}")
    print(f"Duplicates removed    : {raw - loops - len(edges)}")
    print(f"Clean directed edges  : {len(edges)}")
    print(f"Nodes                 : {len(dept_of)}")
    print(f"Departments           : {len(set(dept_of.values()))}")

    top20 = top_departments(edges, dept_of, 20)
    print("\nTop-20 departments by internal edges:")
    print("  idx  dept  internal_edges")
    for idx, (d, c) in enumerate(top20):
        mark = "  <-- A" if idx == PAIR_I else ("  <-- B" if idx == PAIR_J else "")
        print(f"  {idx:3d}  {d:4d}  {c:6d}{mark}")

    dept_a = top20[PAIR_I][0]
    dept_b = top20[PAIR_J][0]
    print("\nGroup parameters:")
    print(f"  Roll numbers        : {', '.join(ROLL_NUMBERS)}")
    print(f"  R                   : {R}")
    print(f"  Pair number         : {R} mod 190 = {PAIR_NUMBER} -> ({PAIR_I}, {PAIR_J})")
    print(f"  Department A        : top-20[{PAIR_I}] = department {dept_a}")
    print(f"  Department B        : top-20[{PAIR_J}] = department {dept_b}")
    print(f"  Random networks     : 20 + ({R} mod 31) = {NUM_RANDOM_NETWORKS}")
    print(f"  Swap attempts       : (5 + ({R} mod 6)) x edges = {SWAP_MULTIPLIER} x edges")
    print(f"  Seed                : {SEED}")

    #T3
    orbits, codes = verify_classes()
    print(f"\nT3  64 configurations -> {orbits} orbits, connected codes = {codes}")
    hand = triad_class("a", "b", "c", {("a", "b"), ("a", "c"), ("b", "c")})
    print(f"    Hand example a->b, a->c, b->c  ->  Class {hand} (canonical code 11)")

    results = {"R": R, "pair_number": PAIR_NUMBER, "pair": [PAIR_I, PAIR_J],
               "num_random_networks": NUM_RANDOM_NETWORKS,
               "swap_multiplier": SWAP_MULTIPLIER, "seed": SEED,
               "top20": top20, "departments": {}}

    zs_by_dept = {}
    for name, dept in (("A", dept_a), ("B", dept_b)):
        #T2
        nodes, sub_edges = induced_subgraph(edges, dept_of, dept)
        attempts = SWAP_MULTIPLIER * len(sub_edges)
        print("\n" + "=" * 70)
        print(f"Department {name} = {dept}")
        print("=" * 70)
        print(f"T2  nodes = {len(nodes)}, edges = {len(sub_edges)}")

        network_image = os.path.join(RESULTS_DIR, f"network_dept_{dept}_R{R}.png")
        plot_network(nodes, sub_edges, dept, R, network_image)
        print(f"    Network diagram saved to {network_image}")

        #T4
        real = triad_census(nodes, sub_edges)
        print(f"T4  real census = {real}")

        # T5,T6
        print(f"T5  {NUM_RANDOM_NETWORKS} random networks, {attempts} swap attempts each")
        t0 = time.time()
        rand_censuses = run_null_model(nodes, sub_edges, NUM_RANDOM_NETWORKS,
                                       attempts, SEED)
        print(f"    (took {time.time() - t0:.1f} s, degree check passed for all)")
        zs, mus, sigmas = z_scores(real, rand_censuses)
        zs_by_dept[name] = zs

        results["departments"][name] = {
            "dept_id": dept, "nodes": len(nodes), "edges": len(sub_edges),
            "node_ids": nodes, "edge_list": sub_edges,
            "swap_attempts": attempts, "real_counts": real,
            "random_mean": mus, "random_std": sigmas, "z": zs,
            "random_censuses": rand_censuses,
        }

    #Tables
    A, B = results["departments"]["A"], results["departments"]["B"]
    lines = []
    lines.append(f"R = {R}   Department A = {dept_a}   Department B = {dept_b}")
    lines.append("")
    lines.append("T4  Triad census (real subgraphs)")
    lines.append(f"{'Class':>5} {'Code':>5} {'A count':>10} {'B count':>10}")
    for k in range(13):
        lines.append(f"{k+1:>5} {CLASS_CODES[k]:>5} {A['real_counts'][k]:>10} {B['real_counts'][k]:>10}")
    lines.append("")
    lines.append("T6  Z-scores")
    lines.append(f"{'Class':>5} {'A: N':>7} {'A: mean':>9} {'A: std':>8} {'A: Z':>8} {'':11}"
                 f"{'B: N':>7} {'B: mean':>9} {'B: std':>8} {'B: Z':>8}")
    for k in range(13):
        lines.append(
            f"{k+1:>5} {A['real_counts'][k]:>7} {A['random_mean'][k]:>9.1f} {A['random_std'][k]:>8.2f} "
            f"{A['z'][k]:>8.2f} {label(A['z'][k]):<11}"
            f"{B['real_counts'][k]:>7} {B['random_mean'][k]:>9.1f} {B['random_std'][k]:>8.2f} "
            f"{B['z'][k]:>8.2f} {label(B['z'][k])}")
    table = "\n".join(lines)
    print("\n" + table)

    with open(os.path.join(RESULTS_DIR, "tables.txt"), "w") as f:
        f.write(table + "\n")
    with open(os.path.join(RESULTS_DIR, "results.json"), "w") as f:
        json.dump(results, f, indent=1)

    # T2
    with open(os.path.join(RESULTS_DIR, "subgraphs.txt"), "w") as f:
        for name in ("A", "B"):
            dept_data = results["departments"][name]
            f.write(f"Department {name} (department {dept_data['dept_id']})\n")
            f.write(f"Nodes ({len(dept_data['node_ids'])}): {dept_data['node_ids']}\n")
            f.write(f"Directed edges ({len(dept_data['edge_list'])}):\n")
            for edge in dept_data["edge_list"]:
                f.write(f"  {edge[0]} -> {edge[1]}\n")
            f.write("\n")

    #T7
    chart = os.path.join(RESULTS_DIR, f"zscores_R{R}.png")
    plot_zscores(zs_by_dept["A"], zs_by_dept["B"], dept_a, dept_b, R, chart)
    print(f"\nT7  chart saved to {chart}")


if __name__ == "__main__":
    main()
