/* Exhaustive alpha-labelling search with one vertex pinned.
   Input lines: "n;u-v,...;x;mode"  mode L: x is dark with label lambda (largest dark label)
                                    mode Z: x is dark with label 0
   Output: "YES;labels;nodes" or "NO;;nodes" or "CAP;;nodes". Labels 0..n-1, dark = class of x. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 48
int n, adj[MAXN][MAXN], deg[MAXN], col[MAXN], order[MAXN], lab[MAXN], usedL[MAXN], usedD[MAXN], lam, par[MAXN], symm = 1;
long long nodes, cap = 4000000000LL;
int rec(int i) {
  if (++nodes > cap) return -1;
  if (i == n) return 1;
  int v = order[i], lo = col[v] ? lam + 1 : 0, hi = col[v] ? n - 1 : lam;
  if (symm && deg[v] == 1 && i > 1) { int u = order[i - 1]; if (deg[u] == 1 && par[u] == par[v] && lab[u] + 1 > lo) lo = lab[u] + 1; }
  for (int l = lo; l <= hi; l++) {
    if (usedL[l]) continue;
    int ds[MAXN], k = 0, ok = 1;
    for (int j = 0; j < deg[v] && ok; j++) { int w = adj[v][j]; if (lab[w] < 0) continue;
      int d = abs(l - lab[w]); if (usedD[d]) { ok = 0; break; }
      for (int z = 0; z < k; z++) if (ds[z] == d) ok = 0;
      ds[k++] = d; }
    if (!ok) continue;
    lab[v] = l; usedL[l] = 1; for (int z = 0; z < k; z++) usedD[ds[z]] = 1;
    int r = rec(i + 1);
    if (r) return r;
    lab[v] = -1; usedL[l] = 0; for (int z = 0; z < k; z++) usedD[ds[z]] = 0;
  }
  return 0;
}
int main(int argc, char **argv) {
  if (argc > 1) cap = atoll(argv[1]);
  if (argc > 2) symm = atoi(argv[2]);
  static char line[16384];
  while (fgets(line, sizeof line, stdin)) {
    line[strcspn(line, "\n")] = 0;
    char *p1 = strchr(line, ';'); *p1 = 0; n = atoi(line);
    char *p2 = strchr(p1 + 1, ';'); *p2 = 0;
    char *p3 = strchr(p2 + 1, ';'); *p3 = 0; int x = atoi(p2 + 1); char mode = p3[1];
    memset(deg, 0, sizeof deg);
    for (char *t = strtok(p1 + 1, ","); t; t = strtok(NULL, ",")) { int a, b; sscanf(t, "%d-%d", &a, &b); adj[a][deg[a]++] = b; adj[b][deg[b]++] = a; }
    for (int v = 0; v < n; v++) { col[v] = -1; lab[v] = -1; usedL[v] = 0; usedD[v] = 0; }
    int h = 0, k = 0; order[k++] = x; col[x] = 0; par[x] = -1;
    while (h < k) { int u = order[h++]; for (int j = 0; j < deg[u]; j++) { int w = adj[u][j]; if (col[w] < 0) { col[w] = !col[u]; par[w] = u; order[k++] = w; } } }
    int nd = 0; for (int v = 0; v < n; v++) nd += col[v] == 0; lam = nd - 1;
    int fixl = mode == 'L' ? lam : 0;
    lab[x] = fixl; usedL[fixl] = 1; nodes = 0;
    int r = rec(1);
    if (r == 1) { printf("YES;"); for (int v = 0; v < n; v++) printf(v ? ",%d" : "%d", lab[v]); printf(";%lld\n", nodes); }
    else printf("%s;;%lld\n", r < 0 ? "CAP" : "NO", nodes);
    fflush(stdout);
  }
  return 0;
}
