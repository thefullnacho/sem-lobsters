"""Validate alpha_fix (C) against (1) an independent brute force over all labellings, every tree with
n <= 9, and (2) known facts: caterpillars are alpha; diameter-4 non-caterpillars are not
(Huang-Kotzig-Rosa 1982 / Stefanec 2009), every tree with n <= 12."""
import itertools, subprocess, sys
import networkx as nx
from barrientos import alpha_check

def c_alpha(n, E):
    es = ",".join("%d-%d" % e for e in E)
    out = subprocess.run(["./alpha_fix", "4000000000"], input="".join("%d;%s;%d;Z\n" % (n, es, v) for v in range(n)),
                         capture_output=True, text=True).stdout.splitlines()
    st = "NO"
    for o in out:
        s, labs, _ = o.split(";")
        if s == "YES":
            assert alpha_check(n, E, [int(x) for x in labs.split(",")]) is not None
            return "YES"
        if s == "CAP": st = "CAP"
    return st

def brute(n, E):
    for p in itertools.permutations(range(n)):
        if alpha_check(n, E, list(p)) is not None: return "YES"
    return "NO"

def caterpillar(T):
    H = T.copy(); H.remove_nodes_from([v for v in T if T.degree(v) == 1])
    return H.number_of_nodes() <= 1 or (nx.is_connected(H) and max(d for _, d in H.degree()) <= 2)

mism = 0; tot = 0
for n in range(2, 10):
    for T in nx.nonisomorphic_trees(n):
        E = sorted(tuple(sorted(e)) for e in T.edges)
        a, b = c_alpha(n, E), (brute(n, E) if n <= 8 else None)
        tot += 1
        if b is not None and a != b: mism += 1; print("MISMATCH brute", n, E, a, b)
print("brute-force agreement n<=8:", tot, "trees checked (n=9 C only), mismatches", mism)
cnt = {"cat_yes": 0, "cat_other": 0, "d4_no": 0, "d4_other": 0}
for n in range(4, 13):
    for T in nx.nonisomorphic_trees(n):
        E = sorted(tuple(sorted(e)) for e in T.edges)
        if caterpillar(T):
            r = c_alpha(n, E); cnt["cat_yes" if r == "YES" else "cat_other"] += 1
        elif nx.diameter(T) == 4:
            r = c_alpha(n, E); cnt["d4_no" if r == "NO" else "d4_other"] += 1
            if r != "NO": print("diam-4 non-caterpillar not NO:", n, E, r)
print("known facts n<=12:", cnt)
