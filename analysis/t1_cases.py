"""Emit T1 instances (star(A) + leaf x carrying pendant P; x pinned to lambda) for alpha_fix, then
re-check its answers. Usage: t1_cases.py emit AMIN AMAX PMAX > cases;  t1_cases.py check cases out"""
import sys
from barrientos import rooted_trees, alpha_check
if sys.argv[1] == "emit":
    amin, amax, pmax = map(int, sys.argv[2:5])
    for idx, (pe, ps) in enumerate(rooted_trees(pmax)):
        for a in range(amin, amax + 1):
            E = [(0, j) for j in range(1, a + 2)]; base = a + 2
            E += [(base + u, base + v) for u, v in pe]; E.append((a + 1, base))
            n = base + ps
            print("%d;%s;%d;L;#a=%d,P=%d,|P|=%d,%s" % (n, ",".join("%d-%d" % e for e in E), a + 1, a, idx, ps, pe))
else:
    from collections import Counter
    res = Counter(); fails = []
    for c, o in zip(open(sys.argv[2]), open(sys.argv[3])):
        parts = c.strip().split(";"); n = int(parts[0]); E = [tuple(map(int, e.split("-"))) for e in parts[1].split(",")]
        x = int(parts[2]); tag = parts[4]
        st, labs, nodes = o.strip().split(";")
        ps = int(tag.split("|P|=")[1].split(",")[0])
        if st == "YES":
            f = [int(v) for v in labs.split(",")]; lam = alpha_check(n, E, f)
            assert lam is not None and f[x] == lam, ("bad witness", tag)
        res[(ps, st)] += 1
        if st != "YES": fails.append((st, tag))
    for ps in sorted({k[0] for k in res}):
        print("|P|=%d: YES %d, NO %d, CAP %d" % (ps, res[(ps, "YES")], res[(ps, "NO")], res[(ps, "CAP")]))
    for f in fails[:40]: print("  ", *f)
    print("non-YES:", len(fails))
