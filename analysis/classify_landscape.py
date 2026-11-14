"""Classify each two-hub family's deficit table d(a, b).
Classes: ALPHA (all 0); CONST (same nonzero value everywhere); THRESH (d = 0 iff a <= s1 or b <= s2, else one
constant D); EVENTUAL (constant D once a, b >= some m, irregular below); OTHER."""
import json, sys
from collections import Counter
rows = [json.loads(l) for l in open(sys.argv[1])]
out = []
for r in rows:
    d = {tuple(map(int, k.split(","))): v for k, v in r["def"].items()}
    vals = set(d.values())
    if None in vals: cls = ("UNDECIDED",)
    elif vals == {0}: cls = ("ALPHA",)
    elif len(vals) == 1: cls = ("CONST", vals.pop())
    else:
        D = max(vals); fit = None
        if vals == {0, D}:
            for s1 in range(0, 40):
                for s2 in range(0, 40):
                    if all((v == 0) == (a <= s1 or b <= s2) for (a, b), v in d.items()):
                        fit = (s1, s2); break
                if fit: break
        if fit: cls = ("THRESH", D, fit)
        else:
            m = None
            for mm in range(1, 30):
                tail = {v for (a, b), v in d.items() if a >= mm and b >= mm}
                if len(tail) == 1: m = mm; break
            cls = ("EVENTUAL", tail.pop(), m) if m else ("OTHER",)
    out.append((cls, r))
c = Counter(x[0][0] for x in out); print("classes:", dict(c))
print("max deficit anywhere:", max(v for r in rows for v in r["def"].values() if v is not None))
for name in ("CONST", "THRESH", "EVENTUAL", "OTHER"):
    sel = [x for x in out if x[0][0] == name]
    if not sel: continue
    print(f"\n== {name} ({len(sel)})")
    for cls, r in sel[:40]:
        print("  ", cls[1:], f"core c={r['c']} edges={r['core']} hubs=({r['h1']},{r['h2']})")
