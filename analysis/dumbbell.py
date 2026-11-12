"""Extract the hard family and lay out its labellings.

Family D(a, b, k; pendant): star centres A (a leaves) and B (b leaves), A and B joined by a path with
k interior vertices x_1..x_k, plus exactly one pendant subtree P hanging off one interior x_i.
Hubs carry only leaves besides the connector; other interior vertices have degree 2.

    python3 -I analysis/dumbbell.py data/retry_labelled_nNN.txt [max_print]
"""
import sys
from collections import Counter

def parse(line):
    p = line.strip().split(";")
    n = int(p[0]); E = [tuple(map(int, e.split("-"))) for e in p[1].split(",")]
    lab = [int(x) for x in p[2].split(",")]
    return n, E, lab, int(p[3]) if len(p) > 3 and p[3] else 0

def match(n, E):
    adj = [set() for _ in range(n)]
    for u, v in E: adj[u].add(v); adj[v].add(u)
    deg = [len(x) for x in adj]
    leafy = [v for v in range(n) if sum(deg[w] == 1 for w in adj[v]) >= deg[v] - 1 and deg[v] >= 3]
    # hubs: vertices whose neighbours are all leaves except exactly one
    hubs = [v for v in leafy if sum(deg[w] > 1 for w in adj[v]) == 1]
    best = None
    for i in range(len(hubs)):
        for j in range(i + 1, len(hubs)):
            A, B = hubs[i], hubs[j]
            par = {A: None}; q = [A]
            for x in q:
                for y in adj[x]:
                    if y not in par: par[y] = x; q.append(y)
            path = [B]
            while path[-1] != A: path.append(par[path[-1]])
            path.reverse(); inner = path[1:-1]
            if not inner: continue
            extra = [x for x in inner if deg[x] > 2]
            if len(extra) != 1: continue
            x = extra[0]
            # pendant = everything hanging off x away from the path
            P = set(); roots = adj[x] - set(path)
            if len(roots) != 1: continue
            r = next(iter(roots)); st = [r]; P.add(r)
            while st:
                y = st.pop()
                for z in adj[y]:
                    if z != x and z not in P: P.add(z); st.append(z)
            LA = [w for w in adj[A] if deg[w] == 1]; LB = [w for w in adj[B] if deg[w] == 1]
            if len(LA) + len(LB) + len(path) + len(P) != n: continue
            cand = dict(A=A, B=B, path=path, x=x, pos=inner.index(x) + 1, k=len(inner),
                        LA=LA, LB=LB, P=P, root=r, adj=adj)
            if best is None or len(LA) + len(LB) > len(best["LA"]) + len(best["LB"]):
                best = cand
    return best

def pend_shape(m):
    adj, P, r = m["adj"], m["P"], m["root"]
    sub = {v: [w for w in adj[v] if w in P] for v in P}
    if len(P) == 1: return "K1"
    if all(len(sub[v]) <= 2 for v in P) and len(sub[r]) == 1: return "path%d" % len(P)
    if all(len(sub[v]) == 1 for v in P if v != r): return "star@root%d" % (len(P) - 1)
    c = [v for v in P if v != r and len(sub[v]) >= 2]
    if len(c) == 1 and all(len(sub[v]) == 1 for v in P if v not in (c[0],)): return "star-via-1-%d" % (len(P) - 2)
    return "tree%d" % len(P)

lines = open(sys.argv[1]).read().splitlines()
maxp = int(sys.argv[2]) if len(sys.argv) > 2 else 10
fam = Counter(); shown = 0; recs = []
for line in lines:
    n, E, lab, eff = parse(line)
    m = match(n, E)
    if not m: continue
    f = lambda v: lab[v]
    a, b = len(m["LA"]), len(m["LB"])
    if a < b: m["A"], m["B"], m["LA"], m["LB"] = m["B"], m["A"], m["LB"], m["LA"]; m["path"].reverse(); m["pos"] = m["k"] + 1 - m["pos"]; a, b = b, a
    key = (m["k"], m["pos"], pend_shape(m))
    fam[key] += 1
    recs.append((eff, n, a, b, key, m, lab))
print("%s: %d family members of %d leftovers" % (sys.argv[1], len(recs), len(lines)))
for k, v in fam.most_common(12): print("  connector interior k=%d, pendant at x_%d, pendant %s: %d" % (k[0], k[1], k[2], v))
recs.sort(key=lambda t: -t[0])
print()
for eff, n, a, b, key, m, lab in recs[:maxp]:
    s = min(lab[u] + lab[v] for u in range(n) for v in m["adj"][u] if u < v)
    fA, fB = lab[m["A"]], lab[m["B"]]
    LA = sorted(lab[v] for v in m["LA"]); LB = sorted(lab[v] for v in m["LB"])
    con = [lab[v] for v in m["path"]]
    print("n=%d a=%d b=%d k=%d pend@x%d %s effort=%d  min edge sum=%d (complement-normalised: f(A)<=n/2: %s)" % (n, a, b, key[0], key[1], key[2], eff, s, fA <= n / 2))
    print("   f(A)=%d leaves %s -> sums %s" % (fA, LA, sorted(fA + x for x in LA)))
    print("   f(B)=%d leaves %s -> sums %s" % (fB, LB, sorted(fB + x for x in LB)))
    print("   path labels A..B %s ; pendant labels %s" % (con, sorted(lab[v] for v in m["P"])))
