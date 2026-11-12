"""Do the hard two-star trees have a super edge-magic labelling in which each star's leaves get a
block of consecutive labels? Then the leaf edge sums are two consecutive runs and only the middle
(connector + pendant) has to fill the gap.

    python3 -I analysis/blocks.py data/retry_labelled_nNN.txt [limit]
"""
import sys, time
sys.setrecursionlimit(10000)
from dumbbell_match import parse, match   # same matcher, tightened below

def block_labelling(n, m):
    A, B, LA, LB = m["A"], m["B"], m["LA"], m["LB"]
    adj = m["adj"]; a, b = len(LA), len(LB)
    mid = [v for v in range(n) if v not in set(LA) | set(LB) | {A, B}]
    # order middle vertices by BFS from A so each has an assigned neighbour when reached
    order = []; seen = {A, B}; q = [A]
    for x in q:
        for y in sorted(adj[x]):
            if y not in seen and y in set(mid):
                seen.add(y); order.append(y); q.append(y)
    medges = [(u, v) for u in range(n) for v in adj[u] if u < v and u not in LA and v not in LA and u not in LB and v not in LB]
    labels = range(1, n + 1)
    for fA in labels:
        for al in range(1, n - a + 2):                 # LA = al..al+a-1
            SA = set(range(al, al + a))
            if fA in SA: continue
            IA = (fA + al, fA + al + a - 1)
            for fB in labels:
                if fB == fA or fB in SA: continue
                for be in range(1, n - b + 2):
                    SB = set(range(be, be + b))
                    if SB & SA or fA in SB or fB in SB: continue
                    IB = (fB + be, fB + be + b - 1)
                    if not (IA[1] < IB[0] or IB[1] < IA[0]): continue
                    lo, hi = min(IA[0], IB[0]), max(IA[1], IB[1])
                    if hi - lo > n - 2: continue
                    rest = sorted(set(labels) - SA - SB - {fA, fB})
                    for s in range(max(2, hi - (n - 2)), lo + 1):
                        T = set(range(s, s + n - 1)) - set(range(IA[0], IA[1] + 1)) - set(range(IB[0], IB[1] + 1))
                        if len(T) != len(medges): continue
                        f = {A: fA, B: fB}
                        used = set()
                        def dfs(i, free, Tleft):
                            if i == len(order):
                                # check edges between A and B directly if any
                                return all((f[u] + f[v]) in Tleft for u, v in medges if u in f and v in f and {u, v} == {A, B}) or True
                            v = order[i]
                            for lab in list(free):
                                ok = True; took = []
                                for w in adj[v]:
                                    if w in f:
                                        sm = lab + f[w]
                                        if sm not in Tleft: ok = False; break
                                        Tleft.discard(sm); took.append(sm)
                                if ok:
                                    f[v] = lab; free.discard(lab)
                                    if dfs(i + 1, free, Tleft): return True
                                    free.add(lab); del f[v]
                                for sm in took: Tleft.add(sm)
                            return False
                        if dfs(0, set(rest), set(T)):
                            for v in LA: pass
                            return dict(fA=fA, LA=(al, al + a - 1), fB=fB, LB=(be, be + b - 1), s=s,
                                        mid={v: f[v] for v in order})
    return None

lines = open(sys.argv[1]).read().splitlines()
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
recs = []
for line in lines:
    n, E, lab, eff = parse(line)
    m = match(n, E)
    if m: recs.append((eff, n, m))
recs.sort(key=lambda t: -t[0])
found = miss = 0; t0 = time.time()
for eff, n, m in recs[:limit]:
    r = block_labelling(n, m)
    if r:
        found += 1
        if found <= 5:
            print("n=%d a=%d b=%d k=%d |P|=%d effort=%d: f(A)=%d leaves %d..%d, f(B)=%d leaves %d..%d, sums from %d, middle %s"
                  % (n, len(m["LA"]), len(m["LB"]), m["k"], len(m["P"]), eff, r["fA"], *r["LA"], r["fB"], *r["LB"], r["s"], sorted(r["mid"].values())))
    else:
        miss += 1
        print("NO block labelling: n=%d a=%d b=%d k=%d |P|=%d effort=%d" % (n, len(m["LA"]), len(m["LB"]), m["k"], len(m["P"]), eff))
print("%s: family %d, tested %d, block labelling found %d, none %d, %.0fs" % (sys.argv[1], len(recs), found + miss, found, miss, time.time() - t0))
