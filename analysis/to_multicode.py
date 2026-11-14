"""Write trees as Brinkmann multicode: byte n, then for vertices 1..n-1 their higher-numbered neighbours
(1-based), each list ended by 0.  Library use: multicode(n, edges) -> bytes (edges 0-based)."""
def multicode(n, edges):
    nb = [[] for _ in range(n)]
    for u, v in edges:
        a, b = min(u, v), max(u, v); nb[a].append(b)
    out = bytearray([n])
    for i in range(n - 1):
        out += bytes(sorted(j + 1 for j in nb[i])); out.append(0)
    return bytes(out)
