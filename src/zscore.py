import math

from randomize import randomize
from triads import triad_census


def mean_and_pop_std(values):
    n = len(values)
    mu = sum(values) / n
    var = sum((x - mu) ** 2 for x in values) / n
    return mu, math.sqrt(var)


def z_scores(real_counts, random_counts_list):
    zs, mus, sigmas = [], [], []
    for k in range(13):
        column = [counts[k] for counts in random_counts_list]
        mu, sigma = mean_and_pop_std(column)
        z = 0.0 if sigma == 0 else (real_counts[k] - mu) / sigma
        zs.append(z)
        mus.append(mu)
        sigmas.append(sigma)
    return zs, mus, sigmas


def label(z):
    if z > 2:
        return "motif"
    if z < -2:
        return "anti-motif"
    return ""


def run_null_model(nodes, edges, num_networks, attempts, seed, verbose=True):
    import random
    master = random.Random(seed)
    censuses = []
    for t in range(num_networks):
        sub_seed = master.randrange(2 ** 31)
        rand_edges = randomize(edges, attempts, sub_seed)
        censuses.append(triad_census(nodes, rand_edges))
        if verbose:
            print(f"    random network {t + 1:2d}/{num_networks} done", flush=True)
    return censuses
