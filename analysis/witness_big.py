"""Independent certificates for the alpha verdicts above 63 vertices: our search (alpha_fix128) looks for an
alpha-labelling; each one found is verified by barrientos.alpha_check (pure Python, from the definition).
Appends 't a b n status' to OUT: CERT (verified witness), NOWIT (search ended or capped without one)."""
import subprocess, os
from multiprocessing import Pool
from barrientos import alpha_check
from prove_a_range import tree
OUT="/data/sem-lobsters/witness_big.txt"
def run(r):
    t,a,b,n,d=r; nn,E=tree(t,a,b)
    es=",".join("%d-%d"%e for e in E)
    adj=[set() for _ in range(nn)]
    for u,v in E: adj[u].add(v); adj[v].add(u)
    pins=[]; seen=set()
    for v in range(nn):
        if len(adj[v])==1:
            p=next(iter(adj[v]))
            if p in seen: continue
            seen.add(p)
        pins.append(v)
    for v in pins:
        try:
            o=subprocess.run(["./alpha_fix128","2000000000"],input=f"{nn};{es};{v};Z\n",capture_output=True,text=True,timeout=600).stdout.strip().split(";")
        except subprocess.TimeoutExpired:
            continue
        if o[0]=="YES":
            f=[int(x) for x in o[1].split(",")]
            if alpha_check(nn,E,f) is not None: return t,a,b,nn,"CERT"
            return t,a,b,nn,"BADWITNESS"
    return t,a,b,nn,"NOWIT"
if __name__=="__main__":
    rows=[tuple(map(int,l.split())) for l in open("../notes/prove_a_range.txt")]
    jobs=[r for r in rows if r[3]>63 and r[4]==0]
    done=set()
    if os.path.exists(OUT):
        for l in open(OUT): x=l.split(); done.add((int(x[0]),int(x[1]),int(x[2])))
    jobs=sorted([r for r in jobs if (r[0],r[1],r[2]) not in done],key=lambda r:r[3])
    print(len(jobs),"alpha trees above 63 to certify",flush=True)
    with Pool(28) as p, open(OUT,"a") as f:
        for r in p.imap_unordered(run,jobs): f.write(" ".join(map(str,r))+"\n"); f.flush()
    print("finished",flush=True)
