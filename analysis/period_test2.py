"""Boundary test at a = 2b (expect alpha), 2b + 1 and 2b + 4 (expect deficit 1 if a boundary exists), t = 1..10."""
import subprocess, re, json
from multiprocessing import Pool
from to_multicode import multicode
from period_test import tree
def run(job):
    t,a,b=job; n,E=tree(t,a,b)
    if n>127: return t,a,b,None
    out=subprocess.run(["../bin/multi_alphadeficit128"],input=multicode(n,E),capture_output=True,timeout=3600).stderr
    return t,a,b,int(re.search(rb"alpha-deficit (\d+)",out).group(1))
jobs=[(t,a,b) for t in range(1,11) for b in range(1,41) for a in (2*b,2*b+1,2*b+4)]
res={}
with Pool(28) as p:
    for t,a,b,d in p.imap_unordered(run,jobs,chunksize=4): res[(t,a,b)]=d
json.dump({f"{t},{a},{b}":d for (t,a,b),d in res.items()},open("/data/sem-lobsters/period_test2.json","w"))
for t in range(1,11):
    on=[]; odd=[]
    for b in range(1,41):
        x,y,z=res[(t,2*b,b)],res[(t,2*b+1,b)],res[(t,2*b+4,b)]
        if None in (x,y,z): continue
        if (x,y,z)==(0,1,1): on.append(b)
        elif (x,y,z)!=(0,0,0): odd.append((b,(x,y,z)))
    rule=[b for b in range(1,41) if res.get((t,2*b+4,b)) is not None and (b*(b+2))%t!=0]
    print(f"t={t}: boundary at 2b+1 for b in {on}")
    print(f"      residues mod t (b >= 5): {sorted({b%t for b in on if b>=5})}   other patterns: {odd[:5]}")
    print(f"      candidate 't does not divide b(b+2)': agrees on {sum((b in on)==(b in rule) for b in range(1,41) if res.get((t,2*b+4,b)) is not None)} of {sum(1 for b in range(1,41) if res.get((t,2*b+4,b)) is not None)}")
