"""Lemma 5.1's constructive step (Brinkmann et al. 2012, proof of Lemma 5.1) as a certificate generator.
Given an alpha-labelling of T_a in which V1 (class of A = vertex 0 in T) takes labels 0..|V1|-1 and A's pendants
contain a run of >= |V1| - 1 consecutive labels with largest u: shift labels > u by +1 and give the new pendant u + 1.
Every produced labelling is re-verified from the definition (barrientos.alpha_check)."""
import subprocess, json, sys
import networkx as nx
from barrientos import alpha_check, colours
from prove_a_range import tree, threshold
from gblocks import block_search

def normalise(n, E, f):
    """Return f with V1 (class of vertex 0) on 0..|V1|-1, complementing if needed, or None."""
    adj=[set() for _ in range(n)]
    for u,v in E: adj[u].add(v); adj[v].add(u)
    c=colours(n,adj,0); V1=[v for v in range(n) if c[v]==c[0]]
    if sorted(f[v] for v in V1)==list(range(len(V1))): return f, V1
    g=[n-1-x for x in f]
    if sorted(g[v] for v in V1)==list(range(len(V1))): return g, V1
    return None, V1

def run_len(labels):
    """longest run of consecutive integers in a set, and its largest element"""
    s=set(labels); best=(0,None)
    for x in s:
        if x-1 not in s:
            y=x
            while y+1 in s: y+=1
            if y-x+1>best[0]: best=(y-x+1,y)
    return best

def seed(t, a, b, fallback=True):
    """an alpha-labelling of T_a from our search (alpha_fix, small n) or the block search; verified."""
    n,E=tree(t,a,b)
    es=",".join("%d-%d"%e for e in E)
    adj=[set() for _ in range(n)]
    for u,v in E: adj[u].add(v); adj[v].add(u)
    for thr in (4,3,2,5):
        for side in (0,1):
            try: r=block_search(n,[list(x) for x in adj],node_cap=5_000_000,t=thr,low_side=side)
            except Exception: r=None
            if isinstance(r,dict):
                sem=r["labels"]; c=colours(n,adj,0)
                for sd in (0,1):
                    low=[sem[v] for v in range(n) if c[v]==sd]
                    if sorted(low)==list(range(1,len(low)+1)):
                        K=len(low)-1; f=[(K+1-sem[v]) if c[v]==sd else sem[v]-1 for v in range(n)]
                        if alpha_check(n,E,f) is not None: return f
    if fallback and n<=48:
        pins=[]; seenp=set()
        for v in range(n):
            if len(adj[v])==1:
                p=next(iter(adj[v]))
                if p in seenp: continue
                seenp.add(p)
            pins.append(v)
        try:
            out=subprocess.run(["./alpha_fix","2000000000"],input="".join(f"{n};{es};{v};Z\n" for v in pins),capture_output=True,text=True,timeout=300).stdout
        except subprocess.TimeoutExpired:
            return None
        for line in out.splitlines():
            if line.startswith("YES"):
                f=[int(x) for x in line.split(";")[1].split(",")]
                if alpha_check(n,E,f) is not None: return f
    return None

def certify(t, b):
    p0=threshold(t,b)
    nT,ET=tree(t,0,b); G=nx.Graph(ET); col=nx.bipartite.color(G); V1size=sum(1 for v in G if col[v]==col[0])
    order=[(a0,False) for a0 in range(1,p0+1)]+[(a0,True) for a0 in range(1,p0+1)]
    for a0,fb in order:
        f=seed(t,a0,b,fallback=fb) if fb or True else None
        if fb and f is None: continue
        if f is None: continue
        n,E=tree(t,a0,b); g,V1=normalise(n,E,f)
        if g is None: continue
        A_leaves=list(range(n-b-a0, n-b))      # tree(): A's a leaves are added before B's b leaves
        L,u=run_len([g[x] for x in A_leaves])
        if L < V1size-1: continue
        certs=[a0]; cur=g; a=a0
        while a < p0:
            new=[x+1 if x>u else x for x in cur]
            n2,E2=tree(t,a+1,b)
            # the new pendant of A in tree(t, a+1, b) is vertex index n-b (inserted before B's leaves): rebuild order
            lab=new[:n-b]+[u+1]+new[n-b:]
            if alpha_check(n2,E2,lab) is None: return ("FAIL_VERIFY", a+1)
            cur=lab; a+=1; n=n2; certs.append(a)
            u=u+1                                  # run now ends at u + 1
        return ("CERT", a0, p0)
    return ("NOSEED", None, p0)

def one(tb):
    t,b=tb
    try: return t,b,certify(t,b)
    except Exception as e: return t,b,("ERROR",repr(e)[:80])
if __name__=="__main__":
    from multiprocessing import Pool
    cases=json.loads(open(sys.argv[1]).read())
    with Pool(14) as p:
        for r in p.imap_unordered(one,[tuple(c) for c in cases]): print(*r,flush=True)
