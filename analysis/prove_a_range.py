"""For each (t, b) whose Lemma 5.1 threshold tree fits in 127 vertices, compute the deficit for EVERY a = 1..p0.
Resumable: appends 't a b n deficit' to OUT as results land."""
import subprocess, re, os
import networkx as nx
from multiprocessing import Pool
from to_multicode import multicode
OUT="/data/sem-lobsters/prove_a_range.txt"
def tree(t,a,b):
    E=[(0,5),(1,0),(1,2),(1,4),(2,3)]; n=6
    for _ in range(t): E.append((5,n)); n+=1
    for h,k in ((0,a),(4,b)):
        for _ in range(k): E.append((h,n)); n+=1
    return n,E
def threshold(t,b):
    n,E=tree(t,0,b); G=nx.Graph(E); col=nx.bipartite.color(G)
    v1=sum(1 for v in G if col[v]==col[0]); v2=n-v1
    return (v1-1)*(v2+1)
def run(job):
    t,a,b=job; n,E=tree(t,a,b)
    out=subprocess.run(["../bin/multi_alphadeficit128"],input=multicode(n,E),capture_output=True).stderr
    return t,a,b,n,int(re.search(rb"alpha-deficit (\d+)",out).group(1))
if __name__=="__main__":
    done=set()
    if os.path.exists(OUT):
        for l in open(OUT): t,a,b,n,d=map(int,l.split()); done.add((t,a,b))
    jobs=[]
    for t in range(1,14):
        for b in range(1,41):
            p0=threshold(t,b)
            if tree(t,p0,b)[0]<=127:
                jobs+=[(t,a,b) for a in range(1,p0+1) if (t,a,b) not in done]
    jobs.sort(key=lambda j: tree(*j)[0])
    print(len(jobs),"trees to do",flush=True)
    with Pool(28) as p, open(OUT,"a") as f:
        for r in p.imap_unordered(run,jobs): f.write(" ".join(map(str,r))+"\n"); f.flush()
    print("finished",flush=True)
