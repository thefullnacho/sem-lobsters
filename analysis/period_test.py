"""Does the boundary period equal the number t of leaves on core vertex 5? Core of fid 126 with t leaves on vertex 5,
hubs 0 and 4; a leaves on hub 0, b on hub 4. 128-bit Brinkmann program."""
import subprocess, re, sys, json
from multiprocessing import Pool
from to_multicode import multicode
def tree(t,a,b):
    E=[(0,5),(1,0),(1,2),(1,4),(2,3)]; n=6
    for _ in range(t): E.append((5,n)); n+=1
    for h,k in ((0,a),(4,b)):
        for _ in range(k): E.append((h,n)); n+=1
    return n,E
def run(job):
    t,a,b=job; n,E=tree(t,a,b)
    out=subprocess.run(["../bin/multi_alphadeficit128"],input=multicode(n,E),capture_output=True,timeout=3600).stderr
    return t,a,b,int(re.search(rb"alpha-deficit (\d+)",out).group(1))
jobs=[(t,a,b) for t in range(1,7) for b in range(1,21) for a in range(1,46)]
res={}
with Pool(28) as p:
    for t,a,b,d in p.imap_unordered(run,jobs,chunksize=16): res[(t,a,b)]=d
json.dump({f"{t},{a},{b}":d for (t,a,b),d in res.items()},open("/data/sem-lobsters/period_test.json","w"))
for t in range(1,7):
    row=[]
    for b in range(1,21):
        seq=[res[(t,a,b)] for a in range(1,46)]
        lc=0
        for i in range(1,len(seq)):
            if seq[i]!=seq[i-1]: lc=i+1
        tail=seq[-1]
        row.append(f"{lc}{'*' if tail else ''}" if lc else ("1*" if tail else "."))
    print(f"t={t}: switch point in a for b=1..20 (* = deficit 1 beyond it, . = alpha throughout):")
    print("      "+" ".join(f"{x:>3}" for x in row))
