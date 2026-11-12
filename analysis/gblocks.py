"""General block labellings: a super edge-magic labelling in which, for every support vertex v, the
leaves on v get one block of consecutive labels. Leaf edge sums at v are then one consecutive run.

block_search(n, adj) -> dict or None. Core = non-leaf vertices (for a star, the centre).
Uses the complement symmetry f -> n + 1 - f to keep f(core[0]) <= (n + 1) / 2.
"""
def block_search(n, adj, node_cap=5_000_000, t=4):
    deg = [len(a) for a in adj]
    # blocks only on vertices with >= t leaves; every other vertex is labelled on its own
    leaves = {v: [w for w in adj[v] if deg[w] == 1] for v in range(n)}
    leaves = {v: (L if len(L) >= t else []) for v, L in leaves.items()}
    inblock = {w for L in leaves.values() for w in L}
    free = [v for v in range(n) if v not in inblock]
    start = max(free, key=lambda v: len(leaves[v]))
    order = [start]; seen = {start}
    for x in order:
        for y in sorted(adj[x]):
            if y not in seen and y not in inblock:
                seen.add(y); order.append(y)
    full = (1 << (n + 1)) - 2          # labels 1..n
    f = {}; blk = {}; nodes = [0]
    sums_used = set()
    lo_hi = [10**9, -1]

    def place_sums(new):
        # new: list of sums; all must be unused and keep window <= n-2
        if len(set(new)) != len(new): return None
        if any(s in sums_used for s in new): return None
        lo = min([lo_hi[0]] + new); hi = max([lo_hi[1]] + new)
        if hi - lo > n - 2: return None
        old = tuple(lo_hi)
        lo_hi[0], lo_hi[1] = lo, hi
        sums_used.update(new)
        return old

    def undo(new, old):
        sums_used.difference_update(new); lo_hi[0], lo_hi[1] = old

    def dfs(i, used):
        nodes[0] += 1
        if nodes[0] > node_cap: raise TimeoutError
        if i == len(order):
            return used == full and len(sums_used) == n - 1
        v = order[i]; L = len(leaves[v])
        cand = range(1, n + 1) if i else range(1, (n + 1) // 2 + 1)
        for lab in cand:
            if used >> lab & 1: continue
            new = [lab + f[w] for w in adj[v] if w in f]
            old = place_sums(new)
            if old is None: continue
            f[v] = lab
            u2 = used | (1 << lab)
            if L == 0:
                if dfs(i + 1, u2): return True
            else:
                for st in range(1, n - L + 2):
                    bits = ((1 << L) - 1) << st
                    if u2 & bits: continue
                    bs = list(range(lab + st, lab + st + L))
                    o2 = place_sums(bs)
                    if o2 is None: continue
                    blk[v] = st
                    if dfs(i + 1, u2 | bits): return True
                    undo(bs, o2); del blk[v]
            undo(new, old); del f[v]
        return False

    try:
        ok = dfs(0, 0)
    except TimeoutError:
        return "CAPPED"
    if not ok: return None
    lab = [0] * n
    for v in order:
        lab[v] = f[v]
        for j, w in enumerate(sorted(leaves[v])): lab[w] = blk[v] + j
    # independent check
    assert sorted(lab) == list(range(1, n + 1))
    S = sorted(lab[u] + lab[w] for u in range(n) for w in adj[u] if u < w)
    assert all(y == x + 1 for x, y in zip(S, S[1:]))
    return dict(labels=lab, nodes=nodes[0])
