"""Run the pre-registered t = 11, 12, 13 cases (notes/period_predictions_t11_13.md), appending results as they land."""
import subprocess, re
from multiprocessing import Pool
from to_multicode import multicode
OUT="/data/sem-lobsters/period_t11_13.txt"
def tree(t,a,b):
    E=[(0,5),(1,0),(1,2),(1,4),(2,3)]; n=6
    for _ in range(t): E.append((5,n)); n+=1
    for h,k in ((0,a),(4,b)):
        for _ in range(k): E.append((h,n)); n+=1
    return n,E
B={12:[4,16,28,6,18,30,12,24,10,22,5,13], 11:[9,11,22,20,31,13,15], 13:[1,2,3,4,5,6,7,8,9,15,25]}
def run(job):
    t,a,b=job; n,E=tree(t,a,b)
    out=subprocess.run(["../bin/multi_alphadeficit128"],input=multicode(n,E),capture_output=True).stderr
    return t,a,b,n,int(re.search(rb"alpha-deficit (\d+)",out).group(1))
if __name__=="__main__":
    jobs=sorted([(t,a,b) for t,bs in B.items() for b in bs for a in (2*b,2*b+1,2*b+4)], key=lambda j: tree(*j)[0])
    with Pool(6) as p, open(OUT,"a") as f:
        for r in p.imap_unordered(run,jobs): f.write(" ".join(map(str,r))+"\n"); f.flush()
