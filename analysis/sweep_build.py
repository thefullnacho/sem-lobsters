"""Build D(a, b, k, i; P) directly and test for block labellings beyond the observed sizes.

    python3 analysis/sweep.py AMAX KMAX > notes/sweep_AMAX_KMAX.txt
"""
import sys, time

# small rooted pendants, root = vertex 0
PENDANTS = {
    "K1": [],
    "P2": [(0, 1)],
    "P3end": [(0, 1), (1, 2)],
    "P3mid": [(0, 1), (0, 2)],
    "P4end": [(0, 1), (1, 2), (2, 3)],
    "P4inner": [(0, 1), (1, 2), (0, 3)],
    "K13centre": [(0, 1), (0, 2), (0, 3)],
    "K13leaf": [(0, 1), (1, 2), (1, 3)],
}

def build(a, b, k, i, pend):
    # A = 0, path interior 1..k, B = k+1, leaves of A, leaves of B, pendant hung on interior vertex i
    E = [(j, j + 1) for j in range(k + 1)]
    nxt = k + 2
    LA = list(range(nxt, nxt + a)); E += [(0, x) for x in LA]; nxt += a
    LB = list(range(nxt, nxt + b)); E += [(k + 1, x) for x in LB]; nxt += b
    pn = 1 + max([max(e) for e in pend], default=0)
    base = nxt
    E += [(base + u, base + v) for u, v in pend]
    E.append((i, base)); nxt += pn
    n = nxt
    adj = [set() for _ in range(n)]
    for u, v in E: adj[u].add(v); adj[v].add(u)
    m = dict(A=0, B=k + 1, LA=LA, LB=LB, adj=adj, k=k, P=set(range(base, n)))
    return n, m

