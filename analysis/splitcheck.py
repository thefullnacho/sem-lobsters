"""Block search with and without the colour-class split, on the observed family and a sweep."""
import sys, time
from gblocks import block_search
from split import is_split
from dumbbell_match import parse, match
from sweep_build import build, PENDANTS

def both(n, adj):
    a = block_search(n, adj)
    s = None
    for side in (0, 1):
        r = block_search(n, adj, low_side=side)
        if isinstance(r, dict): s = r; break
        if r == "CAPPED": s = "CAPPED"
    if isinstance(s, dict): assert is_split(n, adj, s["labels"])
    return a, s

mode = sys.argv[1]
rows = []
if mode == "observed":
    for nn in (24, 25):
        for line in open(f"../data/retry_labelled_n{nn}.txt"):
            n, E, lab, eff = parse(line); m = match(n, E)
            if m: rows.append((f"n={n} a={len(m['LA'])} b={len(m['LB'])} k={m['k']} |P|={len(m['P'])}", n, m["adj"]))
else:
    amax, kmax = int(sys.argv[2]), int(sys.argv[3])
    for a in range(4, amax + 1):
        for b in range(4, a + 1):
            for k in range(1, kmax + 1):
                for i in range(1, k + 1):
                    for name, pend in PENDANTS.items():
                        n, m = build(a, b, k, i, pend)
                        rows.append((f"a={a} b={b} k={k} i={i} {name}", n, m["adj"]))
t0 = time.time(); cnt = {}
for tag, n, adj in rows:
    a, s = both(n, adj)
    key = ("block" if isinstance(a, dict) else str(a), "split" if isinstance(s, dict) else str(s))
    cnt[key] = cnt.get(key, 0) + 1
    if key != ("block", "split"): print(tag, key, flush=True)
print(mode, len(rows), "trees:", cnt, "%.0fs" % (time.time() - t0))
