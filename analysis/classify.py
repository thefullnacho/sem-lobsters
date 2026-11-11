"""Shape census of the super edge-magic leftover trees (the residue the fast stages missed).

    python3 -I analysis/classify.py data/retry_labelled_nNN.txt  > data/shape_nNN.tsv

Re-checks every labelling, then per tree: class (caterpillar / lobster / other), diameter,
degree sequence summary, hub structure on the spine, and search effort.
"""
import sys
from collections import Counter

def check_sem(n, edges, lab):
    if sorted(lab) != list(range(1, n + 1)):
        return False
    sums = sorted(lab[u] + lab[v] for u, v in edges)
    return all(b == a + 1 for a, b in zip(sums, sums[1:]))

def prune(adj, alive):
    """remove all leaves once; returns new alive set"""
    deg = {v: sum(1 for w in adj[v] if w in alive) for v in alive}
    if len(alive) <= 2:
        return set()
    return {v for v in alive if deg[v] > 1}

def is_path(adj, alive):
    if len(alive) <= 1:
        return True
    return all(sum(1 for w in adj[v] if w in alive) <= 2 for v in alive)

def far(adj, s):
    dist = {s: 0}; order = [s]
    for v in order:
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1; order.append(w)
    end = order[-1]
    return end, dist

out = sys.stdout
out.write("n\tclass\tdiam\tmaxdeg\thubs5\thubs3\tdegs_top\tleaves\tbody_n\tbody_hubs3\teffort\tg6edges\n")
bad = 0
for line in open(sys.argv[1]):
    parts = line.strip().split(";")
    n = int(parts[0])
    edges = [tuple(map(int, e.split("-"))) for e in parts[1].split(",")]
    lab = [int(x) for x in parts[2].split(",")] if len(parts) > 2 and parts[2] else None
    effort = parts[3] if len(parts) > 3 else ""
    if lab is not None and not check_sem(n, edges, lab):
        bad += 1
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    deg = [len(a) for a in adj]
    allv = set(range(n))
    p1 = prune(adj, allv)          # remove leaves once
    p2 = prune(adj, p1)            # twice
    if is_path(adj, p1):
        cls = "caterpillar"
    elif is_path(adj, p2):
        cls = "lobster"
    else:
        cls = "other"
    a, _ = far(adj, 0); b, d = far(adj, a)
    diam = d[b]
    top = ",".join(map(str, sorted(deg, reverse=True)[:4]))
    out.write("%d\t%s\t%d\t%d\t%d\t%d\t%s\t%d\t%d\t%d\t%s\t%s\n" % (
        n, cls, diam, max(deg), sum(x >= 5 for x in deg), sum(x >= 3 for x in deg), top,
        deg.count(1), len(p2), sum(1 for v in p2 if sum(1 for w in adj[v] if w in p2) >= 3) if p2 else 0,
        effort, parts[1]))
sys.stderr.write("%s: labellings re-checked, %d failed\n" % (sys.argv[1], bad))
