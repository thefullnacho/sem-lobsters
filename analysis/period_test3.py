"""Resumable version of period_test2: each result is appended to OUT as 't a b n deficit' when it lands.
Boundary test at a = 2b, 2b + 1, 2b + 4 for t = 1..10, b = 1..40 (n <= 127)."""
import subprocess, re, os, sys
from multiprocessing import Pool
from to_multicode import multicode
def tree(t,a,b):
    # fid 126's core (vertices 0..5) with t leaves on vertex 5; hubs 0 and 4 get a and b leaves
    E=[(0,5),(1,0),(1,2),(1,4),(2,3)]; n=6
    for _ in range(t): E.append((5,n)); n+=1
    for h,k in ((0,a),(4,b)):
        for _ in range(k): E.append((h,n)); n+=1
    return n,E
OUT="/data/sem-lobsters/period_test3.txt"
done=set()
if os.path.exists(OUT):
    for l in open(OUT):
        t,a,b,n,d=l.split(); done.add((int(t),int(a),int(b)))
def run(job):
    t,a,b=job; n,E=tree(t,a,b)
    out=subprocess.run(["../bin/multi_alphadeficit128"],input=multicode(n,E),capture_output=True).stderr
    return t,a,b,n,int(re.search(rb"alpha-deficit (\d+)",out).group(1))
if __name__=="__main__":
  jobs=[(t,a,b) for t in range(1,11) for b in range(1,41) for a in (2*b,2*b+1,2*b+4)
        if tree(t,a,b)[0]<=127 and (t,a,b) not in done]
  jobs.sort(key=lambda j: tree(*j)[0])          # small trees first, so most results land early
  print(len(jobs),"to do,",len(done),"already done",flush=True)
  with Pool(28) as p, open(OUT,"a") as f:
      for t,a,b,n,d in p.imap_unordered(run,jobs):
          f.write(f"{t} {a} {b} {n} {d}\n"); f.flush()
  print("finished",flush=True)
