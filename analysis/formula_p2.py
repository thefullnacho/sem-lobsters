"""Explicit alpha-labelling for D(a, b, 2, 1; P2): stars A (a leaves), B (b leaves), connector A-x1-x2-B,
pendant r-s hung on x1 (r adjacent to x1). q = a + b + 5.
  A = 0, A's leaves = q-a+1..q, r = 1, x2 = 3, B's leaves = {2} U {4..b+2}, B = b+3, s = b+4, x1 = b+5.
Checked here as an alpha-labelling (graceful + threshold lambda = b+2) and mapped to a super edge-magic
labelling (low l -> lambda+1-l, high u -> u+1), which is re-checked for consecutive edge sums."""
import sys
from barrientos import alpha_check
from sweep_build import build

def label(a, b):
    n, m = build(a, b, 2, 1, [(0, 1)])
    q = n - 1; f = [None] * n
    A, x1, x2, B = 0, 1, 2, 3
    r, s = sorted(m["P"])
    f[A] = 0; f[x1] = b + 5; f[x2] = 3; f[B] = b + 3; f[r] = 1; f[s] = b + 4
    for j, v in enumerate(m["LA"]): f[v] = q - a + 1 + j
    lb = [2] + list(range(4, b + 3))
    for j, v in enumerate(m["LB"]): f[v] = lb[j]
    E = sorted({tuple(sorted((u, w))) for u in range(n) for w in m["adj"][u]})
    return n, E, f

bad = 0
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
for a in range(1, N + 1):
    for b in range(2, N + 1):
        n, E, f = label(a, b)
        lam = alpha_check(n, E, f)
        ok = lam == b + 2
        if ok:
            g = [lam + 1 - x if x <= lam else x + 1 for x in f]
            S = sorted(g[u] + g[v] for u, v in E)
            ok = sorted(g) == list(range(1, n + 1)) and all(y == x + 1 for x, y in zip(S, S[1:]))
        if not ok:
            bad += 1; print("FAIL a=%d b=%d" % (a, b))
print("formula P2 on x1, k = 2: a = 1..%d, b = 2..%d: %d failures" % (N, N, bad))
