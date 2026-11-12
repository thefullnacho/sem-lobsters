"""Is a super edge-magic labelling 'split': does one colour class of the tree take exactly the labels
1..|class|? (Such a labelling corresponds to an alpha-labelling by reversing the high labels.)"""
def colours(n, adj):
    c = [-1] * n; c[0] = 0; q = [0]
    for x in q:
        for y in adj[x]:
            if c[y] < 0: c[y] = 1 - c[x]; q.append(y)
    return c

def is_split(n, adj, lab):
    c = colours(n, adj)
    for side in (0, 1):
        X = [lab[v] for v in range(n) if c[v] == side]
        if sorted(X) == list(range(1, len(X) + 1)):
            return True
    return False
