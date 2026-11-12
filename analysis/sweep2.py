import sys, time
from sweep_build import build, PENDANTS
from gblocks import block_search
amax, kmax = int(sys.argv[1]), int(sys.argv[2]); T = int(sys.argv[3]) if len(sys.argv) > 3 else 4
tot = bad = cap = 0; t0 = time.time(); worst = 0
for a in range(4, amax + 1):
    for b in range(4, a + 1):
        for k in range(1, kmax + 1):
            for i in range(1, k + 1):
                for name, pend in PENDANTS.items():
                    n, m = build(a, b, k, i, pend)
                    r = block_search(n, m["adj"], t=T)
                    tot += 1
                    if r is None: bad += 1; print("NONE a=%d b=%d k=%d i=%d %s n=%d" % (a, b, k, i, name, n), flush=True)
                    elif r == "CAPPED": cap += 1; print("CAPPED a=%d b=%d k=%d i=%d %s n=%d" % (a, b, k, i, name, n), flush=True)
                    else: worst = max(worst, r["nodes"])
print("general blocks, a,b<=%d k<=%d: %d trees, none %d, capped %d, max nodes %d, %.0fs" % (amax, kmax, tot, bad, cap, worst, time.time() - t0))
