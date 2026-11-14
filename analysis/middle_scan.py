"""Sparse sample of the middle region (both stars 30..59 leaves, n <= 126) for every landscape family, 128-bit
program, compared with predictions: the stable value for ordinary families, the exact rules for fid 126 and 206."""
import json, subprocess, re, sys, math
from multiprocessing import Pool
from to_multicode import multicode
rows=[json.loads(l) for l in open("../notes/grid/landscape_c8_n62.jsonl")]
S=(30,31,40,41,50,51,58,59)
def tree(r,a,b):
    E=[tuple(e) for e in r["core"]]; n=r["c"]
    for h,k in ((r["h1"],a),(r["h2"],b)):
        for _ in range(k): E.append((h,n)); n+=1
    return n,E
def stable(r):
    d={tuple(map(int,k.split(","))):v for k,v in r["def"].items()}
    for m in range(1,30):
        t={v for (a,b),v in d.items() if a>=m and b>=m}
        if len(t)==1: return t.pop()
def predict(fid,r,a,b):
    if fid==126: return 1 if (b%2==1 and a>=2*b+1) else 0
    if fid==206:
        if b%2==0: return 0 if (a%2==1 and a<=2*b-3) else 1
        return 1 if (a%2==0 and a<=2*math.ceil((b-1)/4)) else 0
    return stable(r)
def run(job):
    fid,a,b=job; r=rows[fid]; n,E=tree(r,a,b)
    out=subprocess.run(["../bin/multi_alphadeficit128"],input=multicode(n,E),capture_output=True,timeout=7200).stderr
    m=re.search(rb"alpha-deficit (\d+)",out)
    return fid,a,b,n,(int(m.group(1)) if m else None)
jobs=[(r["fid"],a,b) for r in rows for a in S for b in S if r["c"]+a+b<=126]
print(len(jobs),"trees",flush=True)
bad=[]
with Pool(28) as p:
    for k,(fid,a,b,n,v) in enumerate(p.imap_unordered(run,jobs)):
        pr=predict(fid,rows[fid],a,b)
        if v!=pr: bad.append((fid,a,b,n,pr,v)); print("MISMATCH",fid,a,b,"n",n,"pred",pr,"got",v,flush=True)
        if k%1000==0: print(k,flush=True)
print("done; mismatches:",len(bad),flush=True)
