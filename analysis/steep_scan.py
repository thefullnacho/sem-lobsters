"""For every landscape family and b = 1..6, compare the deficit at large a (n up to ~120, 128-bit program) with
the stable value at the largest a inside the n <= 62 grid. A change means a boundary steeper than the grid shows."""
import json, subprocess, re, sys
from multiprocessing import Pool
from to_multicode import multicode
rows=[json.loads(l) for l in open("../notes/grid/landscape_c8_n62.jsonl")]
def tree(r,a,b):
    E=[tuple(e) for e in r["core"]]; n=r["c"]
    for h,k in ((r["h1"],a),(r["h2"],b)):
        for _ in range(k): E.append((h,n)); n+=1
    return n,E
def run(job):
    fid,a,b=job; r=rows[fid]; n,E=tree(r,a,b)
    try:
        out=subprocess.run(["../bin/multi_alphadeficit128"],input=multicode(n,E),capture_output=True,timeout=1800).stderr
        return fid,a,b,int(re.search(rb"alpha-deficit (\d+)",out).group(1))
    except Exception as e: return fid,a,b,None
jobs=[]; base={}
for r in rows:
    d={tuple(map(int,k.split(","))):v for k,v in r["def"].items()}
    for b in range(1,7):
        amax=max(a for (a,bb) in d if bb==b); base[(r["fid"],b)]=(amax,d[(amax,b)])
        for a in (70,85,100,115):
            if r["c"]+a+b<=126: jobs.append((r["fid"],a,b))
        # also the other orientation: fixed a = b-value, growing b
    for a in range(1,7):
        for b in (70,85,100,115):
            if r["c"]+a+b<=126: jobs.append((r["fid"],a,-b))
print(len(jobs),"trees",file=sys.stderr,flush=True)
def run2(job):
    fid,a,b=job
    if b<0: f,x,y,v=run((fid,a,-b)); return fid,a,b,v   # other orientation: hub1 gets a (small), hub2 gets -b (big)
    return run(job)
changes=[]
with Pool(28) as p:
    for fid,a,b,v in p.imap_unordered(run2,jobs):
        if b>0:
            amax,v0=base[(fid,b)]; key=f"b={b} a={a}"
        else:
            # compare with grid value at largest a-role with hub2 fixed... use row a fixed in grid orientation
            r=rows[fid]; d={tuple(map(int,k.split(","))):vv for k,vv in r["def"].items()}
            bb=-b; bmx=max(y for (x,y) in d if x==a); v0=d[(a,bmx)]; key=f"hub1={a} hub2={bb}"
        if v is None or v!=v0: changes.append((fid,key,v0,v)); print("CHANGE",fid,key,"grid",v0,"now",v,flush=True)
print("done; changes:",len(changes),flush=True)
