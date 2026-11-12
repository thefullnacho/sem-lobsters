"""Brinkmann et al., Section 4: parity property. A tree has it if (1) all vertices in each bipartition
class share a degree parity and (2) the vertex parity differs from the edge parity. Then (Cor 4.2) it has
no alpha-labelling. Vertex parity = parity of sum deg(v) l(v); under (1) it is fixed once we know which
class is dark (labels 0..lam) and which is light (lam+1..q). We require it to differ for BOTH choices."""
def tri(x): return x * (x + 1) // 2
def range_sum(lo, hi): return tri(hi) - tri(lo - 1) if hi >= lo else 0

def parity_property(n, adj):
    from barrientos import colours
    c = colours(n, adj, 0); deg = [len(a) for a in adj]
    par = {}
    for s in (0, 1):
        ps = {deg[v] % 2 for v in range(n) if c[v] == s}
        if len(ps) != 1: return False
        par[s] = ps.pop()
    q = n - 1; ep = tri(q) % 2
    size = {s: sum(1 for v in range(n) if c[v] == s) for s in (0, 1)}
    for dark in (0, 1):
        light = 1 - dark; lam = size[dark] - 1
        vp = (par[dark] * range_sum(0, lam) + par[light] * range_sum(lam + 1, q)) % 2
        if vp == ep: return False
    return True
