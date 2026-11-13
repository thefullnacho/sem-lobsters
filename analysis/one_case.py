"""Exhaustive alpha test of one D(a, b, 1, 1; P) tree with a large cap. args: P a b cap"""
import sys, subprocess
from barrientos import rooted_trees, alpha_check
from sweep_build import build
p, a, b, cap = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
pe, ps = rooted_trees(5)[p]
n, m = build(a, b, 1, 1, pe)
E = sorted({tuple(sorted((u, v))) for u in range(n) for v in m["adj"][u]}); es = ",".join("%d-%d" % e for e in E)
st = "NO"
# one starting vertex per class of interchangeable leaves (same parent): swapping sibling leaves is an automorphism
pins, seenpar = [], set()
for v in range(n):
    if len(m["adj"][v]) == 1:
        par = next(iter(m["adj"][v]))
        if par in seenpar: continue
        seenpar.add(par)
    pins.append(v)
for v in pins:
    o = subprocess.run(["./alpha_fix", cap], input="%d;%s;%d;Z\n" % (n, es, v), capture_output=True, text=True).stdout.strip().split(";")
    if o[0] == "YES":
        assert alpha_check(n, E, [int(x) for x in o[1].split(",")]) is not None; st = "YES"; break
    if o[0] == "CAP": st = "CAP"
print("k=1 P=%d a=%d b=%d -> %s" % (p, a, b, st), flush=True)
