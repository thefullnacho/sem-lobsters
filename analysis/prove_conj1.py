"""Conjecture 1 family: stars A (a leaves) and B (b leaves) joined through x, plus x - r - c with t leaves on c.
For each (t, b) whose Lemma 5.1 threshold tree (v = A) fits in 127 vertices, compute the deficit for EVERY a = 1..p0.
Prediction: deficit 0 iff min(a, b) <= t, else 1. Resumable: appends 't a b n deficit' to OUT."""
import subprocess, re, os, sys
import networkx as nx
from multiprocessing import Pool
from to_multicode import multicode
OUT="/data/sem-lobsters/prove_conj1.txt"
def tree(t,a,b):
    E=[(0,1),(1,2),(1,3),(3,4)]; n=5           # A=0, x=1, B=2, r=3, c=4
    for h,k in ((4,t),(0,a),(2,b)):
        for _ in range(k): E.append((h,n)); n+=1
    return n,E
def threshold(t,b):
    n,E=tree(t,0,b); G=nx.Graph(E); col=nx.bipartite.color(G)
    v1=sum(1 for v in G if col[v]==col[0]); return (v1-1)*(n-v1+1)
def run(job):
    t,a,b=job; n,E=tree(t,a,b)
    exe="../bin/multi_alphadeficit" if n<=63 else "../bin/multi_alphadeficit128"
    out=subprocess.run([exe],input=multicode(n,E),capture_output=True).stderr
    return t,a,b,n,int(re.search(rb"alpha-deficit (\d+)",out).group(1))
def jobs():
    J=[]
    for t in range(1,7):
        for b in range(1,60):
            p0=threshold(t,b)
            if tree(t,p0,b)[0]<=127: J+=[(t,a,b) for a in range(1,p0+1)]
    return J
if __name__=="__main__":
    done=set()
    if os.path.exists(OUT):
        for l in open(OUT): t,a,b,n,d=map(int,l.split()); done.add((t,a,b))
    J=[j for j in jobs() if j not in done]; J.sort(key=lambda j: tree(*j)[0])
    if len(sys.argv)>1: 
        from collections import Counter
        print(len(J),"trees; (t,b) pairs:",sorted(Counter((t,b) for t,a,b in J).keys())[-1:], Counter(t for t,a,b in J), "max b per t:",{t:max(b for tt,a,b in J if tt==t) for t in range(1,7)}); sys.exit()
    print(len(J),"trees to do",flush=True)
    with Pool(int(os.environ.get("POOL","16"))) as p, open(OUT,"a") as f:
        for r in p.imap_unordered(run,J): f.write(" ".join(map(str,r))+"\n"); f.flush()
    print("finished",flush=True)
