"""Known-answer tests of the 128-bit copy above 63 vertices. Appends 'kind id n expected got' (got = TIMEOUT if
over the per-tree limit). T(a): deficit 1 for all a >= 2 (original program at a = 21 + Lemma 5.1).
Random caterpillars: deficit 0."""
import subprocess, re, random
from multiprocessing import Pool
from sweep_build import build
from to_multicode import multicode
OUT="/data/sem-lobsters/known_answer.txt"
def defic(n,E):
    try:
        out=subprocess.run(["../bin/multi_alphadeficit128"],input=multicode(n,E),capture_output=True,timeout=300).stderr
        return int(re.search(rb"alpha-deficit (\d+)",out).group(1))
    except subprocess.TimeoutExpired: return "TIMEOUT"
def job(j):
    kind,k=j
    if kind=="T":
        n,m=build(k,4,1,1,[(0,1),(1,2)]); E=sorted({tuple(sorted((u,v))) for u in range(n) for v in m["adj"][u]}); return "T",k,n,1,defic(n,E)
    rnd=random.Random(k); n=rnd.randint(64,127); spine=rnd.randint(2,n//2)
    E=[(i,i+1) for i in range(spine-1)]; v=spine
    while v<n: E.append((rnd.randrange(spine),v)); v+=1
    return "CAT",k,n,0,defic(n,E)
if __name__=="__main__":
    jobs=[("T",a) for a in range(54,118)]+[("CAT",s) for s in range(200)]
    with Pool(8) as p, open(OUT,"a") as f:
        for r in p.imap_unordered(job,jobs): f.write(" ".join(map(str,r))+"\n"); f.flush()
