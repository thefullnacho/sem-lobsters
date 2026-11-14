"""Run Brinkmann's multi_alphadeficit on D(a, b, k=1; P): stars a and b joined through one vertex x, pendant P on x.
   python3 diag.py P_INDEX "a,b a,b ..." [timeout_s]   prints a, b, n, deficit, seconds"""
import sys, subprocess, time, re
from barrientos import rooted_trees
from sweep_build import build
from to_multicode import multicode
p = int(sys.argv[1]); pairs = [tuple(map(int, s.split(","))) for s in sys.argv[2].split()]
tmo = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
pe, ps = rooted_trees(5)[p]
for a, b in pairs:
    n, m = build(a, b, 1, 1, pe)
    E = sorted({tuple(sorted((u, v))) for u in range(n) for v in m["adj"][u]})
    if n > 62: print(f"P={p} a={a} b={b} n={n} too big"); continue
    t0 = time.time()
    try:
        r = subprocess.run(["../bin/multi_alphadeficit"], input=multicode(n, E), capture_output=True, timeout=tmo)
        d = re.search(rb"alpha-deficit (\d+)", r.stderr); d = int(d.group(1)) if d else None
        print(f"P={p} a={a} b={b} n={n} deficit={d} {time.time()-t0:.2f}s", flush=True)
    except subprocess.TimeoutExpired:
        print(f"P={p} a={a} b={b} n={n} TIMEOUT {tmo:.0f}s", flush=True)
