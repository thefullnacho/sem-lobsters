"""Independent alpha certificates above 63 vertices via block-structured split SEM labellings (gblocks), converted
to alpha-labellings and verified by barrientos.alpha_check. Tries block thresholds 4, 3, 2, 5. Appends results."""
import os
from multiprocessing import Pool
from gblocks import block_search
from barrientos import alpha_check, colours
from prove_a_range import tree
OUT="/data/sem-lobsters/witness_block.txt"
def to_alpha(n,adj,sem):
    c=colours(n,adj,0)
    for side in (0,1):
        low=[sem[v] for v in range(n) if c[v]==side]
        if sorted(low)==list(range(1,len(low)+1)):
            K=len(low)-1
            return [(K+1-sem[v]) if c[v]==side else sem[v]-1 for v in range(n)]
def run(r):
    t,a,b,n,d=r; nn,E=tree(t,a,b); adj=[set() for _ in range(nn)]
    for u,v in E: adj[u].add(v); adj[v].add(u)
    L=[list(x) for x in adj]
    for thr in (4,3,2,5):
        for side in (0,1):
            try: res=block_search(nn,L,node_cap=20_000_000,t=thr,low_side=side)
            except Exception: res=None
            if isinstance(res,dict):
                f=to_alpha(nn,adj,res["labels"])
                if f is not None and alpha_check(nn,E,f) is not None: return t,a,b,nn,f"CERT_t{thr}"
    return t,a,b,nn,"NOWIT"
if __name__=="__main__":
    rows=[tuple(map(int,l.split())) for l in open("../notes/prove_a_range.txt")]
    done=set()
    if os.path.exists(OUT):
        for l in open(OUT): x=l.split(); done.add((int(x[0]),int(x[1]),int(x[2])))
    jobs=sorted([r for r in rows if r[3]>63 and r[4]==0 and (r[0],r[1],r[2]) not in done],key=lambda r:r[3])
    print(len(jobs),"to certify",flush=True)
    with Pool(28) as p, open(OUT,"a") as f:
        for r in p.imap_unordered(run,jobs): f.write(" ".join(map(str,r))+"\n"); f.flush()
    print("finished",flush=True)
