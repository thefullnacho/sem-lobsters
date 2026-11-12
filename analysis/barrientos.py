"""Barrientos 2025, Lemma 2.1 (Utilitas Math. 123, 195-204) applied to the two-star family.

T = A-star (a leaves) - connector x_1..x_k - B-star (b leaves), pendant P (rooted tree) on x_i.
Split T into T1 = star(A) + x_1, T2 = path x_1..x_k + P, T3 = star(B) + x_k. The lemma gives an
alpha-tree if T2 has an alpha-labelling with x_1 = 0 and x_k = lambda_2 (k odd) / lambda_2 + 1 (k even).

  python3 analysis/barrientos.py PMAX KMAX      table of which (P, k, i) have that T2 labelling
"""
import sys, itertools
import networkx as nx

def alpha_check(n, edges, f):
    """f: list of labels. alpha: graceful (labels distinct in 0..q, edge differences = 1..q) and a
    threshold lam with every edge having one end <= lam and the other > lam."""
    q = n - 1
    if sorted(f) != list(range(n)): return None
    if sorted(abs(f[u] - f[v]) for u, v in edges) != list(range(1, n)): return None
    for lam in range(q):
        if all(min(f[u], f[v]) <= lam < max(f[u], f[v]) for u, v in edges):
            return lam
    return None

def colours(n, adj, root):
    c = [-1] * n; c[root] = 0; qq = [root]
    for x in qq:
        for y in adj[x]:
            if c[y] < 0: c[y] = 1 - c[x]; qq.append(y)
    return c

def alpha_with(n, edges, fixed, cond):
    """Exhaustive search for an alpha-labelling with fixed labels {v: label} and cond(f, lam)."""
    adj = [[] for _ in range(n)]
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    root = next(iter(fixed))
    col = colours(n, adj, root)                        # root's class is dark (it gets 0)
    nd = col.count(0); lam = nd - 1
    order = [root]; seen = {root}
    for x in order:
        for y in adj[x]:
            if y not in seen: seen.add(y); order.append(y)
    f = [None] * n; usedL = set(); usedD = set()
    def rec(i):
        if i == n:
            return cond(f, lam)
        v = order[i]
        rng = range(0, lam + 1) if col[v] == 0 else range(lam + 1, n)
        cands = [fixed[v]] if v in fixed else rng
        for l in cands:
            if l in usedL: continue
            ds = [abs(l - f[w]) for w in adj[v] if f[w] is not None]
            if len(set(ds)) != len(ds) or any(d in usedD or d == 0 for d in ds): continue
            f[v] = l; usedL.add(l); usedD.update(ds)
            if rec(i + 1): return True
            f[v] = None; usedL.discard(l); usedD.difference_update(ds)
        return False
    if rec(0):
        assert alpha_check(n, edges, f) is not None
        return list(f), lam
    return None

def rooted_trees(maxv):
    """All rooted trees with up to maxv vertices, up to rooted isomorphism. Yields (edges, root=0)."""
    out = [([], 1)]                                      # single vertex
    for m in range(2, maxv + 1):
        seen = set()
        for T in nx.nonisomorphic_trees(m):
            for r in T.nodes:
                key = nx.weisfeiler_lehman_graph_hash(nx.relabel_nodes(T, {r: 'R'} | {v: v for v in T if v != r}).to_undirected(), node_attr=None) if False else None
                # exact rooted canonical form (AHU)
                def canon(v, p):
                    return "(" + "".join(sorted(canon(w, v) for w in T[v] if w != p)) + ")"
                c = canon(r, None)
                if c in seen: continue
                seen.add(c)
                mp = {r: 0}; nxt = 1
                for v in nx.bfs_tree(T, r):
                    if v not in mp: mp[v] = nxt; nxt += 1
                out.append(([(mp[u], mp[v]) for u, v in T.edges], m))
    return out

def t2(k, i, pedges, psize):
    # path x_1..x_k = vertices 0..k-1, pendant root = vertex k, attached to x_i (index i-1)
    E = [(j, j + 1) for j in range(k - 1)]
    E += [(k + u, k + v) for u, v in pedges]
    E.append((i - 1, k))
    return k + psize, E

def t2_ok(k, i, pedges, psize):
    n, E = t2(k, i, pedges, psize)
    if k % 2:   # x_k same class as x_1: must be the largest dark label
        cond = lambda f, lam: f[k - 1] == lam
    else:
        cond = lambda f, lam: f[k - 1] == lam + 1
    return alpha_with(n, E, {0: 0}, cond)

if __name__ == "__main__":
    pmax, kmax = int(sys.argv[1]), int(sys.argv[2])
    P = rooted_trees(pmax)
    print("rooted pendants with <= %d vertices: %d" % (pmax, len(P)))
    from collections import Counter
    fails = []
    tot = Counter(); ok = Counter()
    for pe, ps in P:
        for k in range(2, kmax + 1):
            for i in range(1, k + 1):
                r = t2_ok(k, i, pe, ps)
                tot[(k, ps)] += 1; ok[(k, ps)] += bool(r)
                if not r: fails.append((k, i, ps, pe))
    for key in sorted(tot): print("k=%d |P|=%d: %d of %d (pendant, position) pairs have the T2 labelling" % (key[0], key[1], ok[key], tot[key]))
    print("failures (k, i, |P|, pendant edges, root 0):")
    for f in fails[:60]: print("  ", f)
    print("total failures", len(fails))
