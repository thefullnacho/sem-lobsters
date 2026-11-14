"""Two-hub landscape: every core tree with <= CMAX vertices, every unordered hub pair {h1, h2} up to automorphism
(hubs carry no core leaves except each other), a leaves on h1 and b on h2, all a, b >= 1 with n <= NMAX.
alpha-deficit of every tree from Brinkmann's multi_alphadeficit, run in parallel.
   python3 landscape.py CMAX NMAX OUT.jsonl"""
import sys, json, re, subprocess, itertools
import networkx as nx
from multiprocessing import Pool
from to_multicode import multicode
CMAX, NMAX, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]

def families():
    seen = set()
    for c in range(2, CMAX + 1):
        for T in nx.nonisomorphic_trees(c):
            leaves = {v for v in T if T.degree(v) == 1}
            for h1, h2 in itertools.combinations(T.nodes, 2):
                ok = all(not (w in leaves and w not in (h1, h2)) for h in (h1, h2) for w in T[h])
                if not ok: continue
                G = T.copy(); nx.set_node_attributes(G, {v: ("H" if v in (h1, h2) else "c") for v in G}, "m")
                key = nx.weisfeiler_lehman_graph_hash(G, node_attr="m", iterations=c)
                if key in seen: continue
                seen.add(key)
                yield c, sorted(T.edges), h1, h2

def tree(core_edges, c, h1, h2, a, b):
    E = list(core_edges); n = c
    for h, k in ((h1, a), (h2, b)):
        for _ in range(k): E.append((h, n)); n += 1
    return n, E

def run(job):
    fid, c, core, h1, h2, a, b = job
    n, E = tree(core, c, h1, h2, a, b)
    r = subprocess.run(["../bin/multi_alphadeficit"], input=multicode(n, E), capture_output=True, timeout=120)
    m = re.search(rb"alpha-deficit (\d+)", r.stderr)
    return fid, a, b, n, (int(m.group(1)) if m else None)

if __name__ == "__main__":
    fams = list(families())
    jobs = [(i, c, core, h1, h2, a, b) for i, (c, core, h1, h2) in enumerate(fams)
            for a in range(1, NMAX) for b in range(1, NMAX) if c + a + b <= NMAX]
    print(f"{len(fams)} families, {len(jobs)} trees", file=sys.stderr, flush=True)
    res = {}
    with Pool(28) as p:
        for k, (fid, a, b, n, d) in enumerate(p.imap_unordered(run, jobs, chunksize=64)):
            res.setdefault(fid, {})[f"{a},{b}"] = d
            if k % 50000 == 0: print(k, file=sys.stderr, flush=True)
    with open(OUT, "w") as f:
        for i, (c, core, h1, h2) in enumerate(fams):
            f.write(json.dumps({"fid": i, "c": c, "core": core, "h1": h1, "h2": h2, "def": res.get(i, {})}) + "\n")
