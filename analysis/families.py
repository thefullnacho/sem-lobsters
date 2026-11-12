"""Membership of leftover trees in named DS6 families.

    python3 -I analysis/families.py data/shape_nNN.tsv

banana:     a vertex v whose removal leaves only stars K_{1,m} (m >= 1), v adjacent to a leaf of each
            (for K_{1,1} either end counts as the leaf)
ext_banana: as banana, but v reaches a leaf of each star through a path (length >= 1 allowed here,
            so it contains banana); each component of T - v is a broom whose handle end touches v
firecracker: stars S_1..S_k (k >= 2, sizes free) with one chosen leaf each, the chosen leaves
            forming a path l_1 - ... - l_k
"""
import csv, sys
from collections import Counter

def build(edges, n):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    return adj

def comps_without(adj, v):
    seen = {v}; out = []
    for s in adj[v]:
        comp = {s}; stack = [s]; seen.add(s)
        while stack:
            x = stack.pop()
            for w in adj[x]:
                if w not in seen:
                    seen.add(w); comp.add(w); stack.append(w)
        out.append((s, comp))
    return out

def broom_from(adj, a, comp):
    """Handle lengths h >= 1 for which comp is a path a = x_0 .. x_h = c plus leaves hung on c
    (a star whose chosen leaf is reached from v through a path). Returns the set of valid h."""
    deg = lambda x: len(adj[x] & comp)
    if len(comp) < 2 or deg(a) != 1:
        return set()
    ok = set(); prev, cur, h, walked = None, a, 0, {a}
    while True:
        nxt = [w for w in adj[cur] & comp if w != prev]
        if prev is not None:
            # could cur be the centre? then comp = walked path + leaves of cur
            rest = (adj[cur] & comp) - {prev}
            if all(deg(x) == 1 for x in rest) and len(comp) == len(walked) + len(rest):
                ok.add(h)
        if len(nxt) != 1:
            break
        prev, cur, h = cur, nxt[0], h + 1
        walked.add(cur)
    return ok

def banana(adj, n, extended):
    for v in range(n):
        ok = True
        for a, comp in comps_without(adj, v):
            hs = broom_from(adj, a, comp)
            if not hs or (not extended and 1 not in hs):
                ok = False; break
        if ok and len(adj[v]) >= 2:
            return True
    return False

def firecracker(adj, n):
    # chosen leaves l_i: each has exactly one neighbour off the path, that neighbour is a star centre
    # all of whose other neighbours are leaves. Try every path between two vertices.
    par_cache = {}
    def path(u, w):
        if u not in par_cache:
            par = {u: None}; order = [u]
            for x in order:
                for y in adj[x]:
                    if y not in par:
                        par[y] = x; order.append(y)
            par_cache[u] = par
        par = par_cache[u]; p = [w]
        while p[-1] != u:
            p.append(par[p[-1]])
        return p
    for u in range(n):
        for w in range(u + 1, n):
            P = path(u, w)
            S = set(P); covered = set(P); good = True
            for l in P:
                off = adj[l] - S
                if len(off) != 1:
                    good = False; break
                c = next(iter(off))
                others = adj[c] - {l}
                if any(len(adj[x]) != 1 for x in others):
                    good = False; break
                covered |= {c} | others
            if good and len(covered) == n:
                return P
    return False

rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
cnt = Counter(); examples = {}
for r in rows:
    n = int(r["n"])
    edges = [tuple(map(int, e.split("-"))) for e in r["g6edges"].split(",")]
    adj = build(edges, n)
    tags = []
    if banana(adj, n, False): tags.append("banana")
    elif banana(adj, n, True): tags.append("ext_banana")
    if firecracker(adj, n): tags.append("firecracker")
    key = (r["class"], "+".join(tags) or "none")
    cnt[key] += 1
    examples.setdefault(key, r["g6edges"])
    r["family"] = key[1]
print(sys.argv[1], len(rows))
for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
    print("  %-8s %-22s %6d" % (k[0], k[1], v))
H = sorted(rows, key=lambda r: int(r["effort"] or 0), reverse=True)[:20]
print("  hardest 20 by family:", Counter(r["family"] for r in H).most_common())
