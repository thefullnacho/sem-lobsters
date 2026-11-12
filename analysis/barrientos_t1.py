"""Pendant moved into T1: T1 = star(A, a leaves) + leaf x carrying pendant P. Need an alpha-labelling
with x = lambda_1 (largest dark label). Then Lemma 2.1 with T2 = edge x-y and T3 = star(B) + y gives
an alpha-labelling of the whole k = 2 tree, for every b."""
import sys
from collections import Counter
from barrientos import alpha_with, rooted_trees

def t1(a, pedges, psize):
    # A = 0, leaves 1..a, x = a+1, pendant root = a+2 ...
    E = [(0, j) for j in range(1, a + 2)]
    base = a + 2
    E += [(base + u, base + v) for u, v in pedges]
    E.append((a + 1, base))
    return base + psize, E

amin, amax, pmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
P = rooted_trees(pmax)
res = Counter(); fails = []
for pe, ps in P:
    for a in range(amin, amax + 1):
        n, E = t1(a, pe, ps)
        x = a + 1
        r = alpha_with(n, E, {x: None} if False else {0: None} if False else {x: None}, lambda f, lam: f[x] == lam) if False else None
        # x must be dark and carry lambda; search with x fixed after lam is known: fix via condition
        r = alpha_with(n, E, {x: -1}, None) if False else None
        res_ok = None
        # alpha_with roots the colouring at the first fixed vertex and makes it dark; we pass x with its label
        # chosen as lam = (#dark - 1), computed the same way alpha_with does.
        import barrientos as B
        adj = [[] for _ in range(n)]
        for u, v in E: adj[u].append(v); adj[v].append(u)
        col = B.colours(n, adj, x); lam = col.count(0) - 1
        res_ok = alpha_with(n, E, {x: lam}, lambda f, l: True)
        res[(ps, bool(res_ok))] += 1
        if not res_ok: fails.append((a, ps, pe))
for ps in sorted({k[0] for k in res}):
    print("|P|=%d: %d ok, %d fail" % (ps, res[(ps, True)], res[(ps, False)]))
for f in fails[:40]: print("  fail a=%d |P|=%d %s" % f)
print("total fails", len(fails))
