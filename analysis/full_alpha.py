"""Does D(a, b, k, i; P) have an alpha-labelling? Exhaustive: alpha_fix pins label 0 on each vertex in
turn; any YES is re-checked here.  python3 full_alpha.py K PMAX "a,b a,b ..." [cap]"""
import sys, subprocess
from collections import Counter
from barrientos import rooted_trees, alpha_check
from sweep_build import build
k, pmax = int(sys.argv[1]), int(sys.argv[2])
pairs = [tuple(map(int, s.split(","))) for s in sys.argv[3].split()]
cap = sys.argv[4] if len(sys.argv) > 4 else "200000000"
P = rooted_trees(pmax)
res = {}
for idx, (pe, ps) in enumerate(P):
    for a, b in pairs:
        for i in range(1, k + 1):
            n, m = build(a, b, k, i, pe)
            E = sorted({tuple(sorted((u, v))) for u in range(n) for v in m["adj"][u]})
            es = ",".join("%d-%d" % e for e in E)
            inp = "".join("%d;%s;%d;Z\n" % (n, es, v) for v in range(n))
            out = subprocess.run(["./alpha_fix", cap], input=inp, capture_output=True, text=True).stdout.splitlines()
            st = "NO"
            for o in out:
                s, labs, _ = o.split(";")
                if s == "YES":
                    assert alpha_check(n, E, [int(x) for x in labs.split(",")]) is not None
                    st = "YES"; break
                if s == "CAP": st = "CAP"
            res[(idx, ps, a, b, i)] = st
            if st != "YES": print("k=%d P=%d |P|=%d a=%d b=%d i=%d -> %s" % (k, idx, ps, a, b, i, st), flush=True)
print("k=%d pendants<=%d pairs=%s:" % (k, pmax, pairs), Counter(res.values()))
