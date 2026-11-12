# First look at the super edge-magic leftovers (2026-11-11)

Source: residue + retry labellings from run 2026-11-04-1135 (n = 23, 24, 25), copied into data/.
`analysis/classify.py` re-checked all 24,771 labellings (0 failures) and sorted each tree by shape.

| n | leftovers | lobsters | other | diameters |
|---|---|---|---|---|
| 23 | 301 | 301 | 0 | 5, 6 |
| 24 | 1,012 | 937 | 75 | 5, 6 |
| 25 | 23,458 | 15,276 | 8,182 | 5 to 8 |

No caterpillars anywhere (the ELNR construction removes them first).

## Shapes

- **Hardest trees are leafy two-hub lobsters of diameter 5 or 6:** two vertices of degree 8 to 11, the
  rest mostly leaves (19 or 20 leaves out of 24 or 25 vertices). Top 8 at n = 25 by effort: degree
  tops 8,8,5,5 / 10,9,3,3 / 11,10,3,2 / 9,8,4,3 / 8,8,6,3 / 10,9,3,3 / 9,8,5,3 / 9,9,3,3. Close to a
  double star with a few short pendant paths: the "two big stars through a connector" family.
- **Non-lobsters** (n = 24 onward): pruning leaves twice leaves a spider with one branch point
  (8,052 of 8,182 at n = 25; 130 have two). So the next class up from lobsters, still small diameter.
- Every leftover has at most 5 vertices of degree >= 5; mostly 2 or 3.

## Candidate questions

1. A construction proving super edge-magic labellings for the leafy two-hub family (diameter 5, 6),
   mined from the 23,458 checked labellings. Most direct route to a theorem.
2. Whether all lobsters are super edge-magic (literature check first: DS6 section 5.2 and beyond).
3. Why these shapes resist the search (effort vs. hub degrees), and whether the leftover share of
   all lobsters grows with n (needs a pass over the full n = 25 certificate on /data).

## Next

- Isolate the double-star-with-pendants family, look for a rule in its labellings (where the hubs'
  labels sit, how leaf labels pair with edge sums).
- Literature check on super edge-magic lobsters and double stars with pendant paths.

## Named families (Alex's research session flagged banana trees, firecrackers, double stars)

DS6 status for super edge-magic: double stars and bistars are caterpillars, so Kotzig and Rosa cover them.
Banana trees: only "various classes" (Swaminathan and Jeyanthi [3843]; Hussain, Baskoro and Slamin
[1475]); Ahmad, Ali and Baskoro [106] pose open problems on subdivided banana trees. Setiawan, Sugeng,
Silaban and Riama [3416] "gave the super edge magic total labelings for banana trees, firecrackers":
check whether that is all of them or some. Krisnawati, Ngurah, Hidayat and Alghofari [2037]: some
subdivisions of double stars have zero super edge-magic deficiency (closest to our family).

`analysis/families.py` (tested on hand-built trees; a 3-star firecracker is also a banana tree):

| n | leftovers | firecracker | banana / ext. banana | none |
|---|---|---|---|---|
| 23 | 301 | 2 | 0 | 299 |
| 24 | 1,012 | 3 | 0 | 1,009 |
| 25 | 23,458 | 147 | 49 | 23,262 |

## The hard family, precisely

Top trees at n = 25: two all-leaf stars (centre degrees 8 to 11) whose centres are joined by a short
path (length 2 or 3 in 414 of the hardest 500), plus ONE small pendant subtree (2 to 8 vertices) hanging
off a connector vertex. Without that pendant it is a caterpillar (known super edge-magic); the single
pendant on the connector is what makes it hard. Working name: a double broom with a pendant on the
connector, close to the subdivided double stars of [2037].

## Block labellings (2026-11-11 evening)

Idea: a labelling where each big star's leaves take one block of consecutive labels, so their edge sums
are one consecutive run and only the small middle (connector + pendant) has to fit around them. That is
the shape of a construction one can prove.

- Observed family (two stars with >= 4 leaves each, pendant <= n/3): n = 24: 13 of 13 have one;
  n = 25: 542 of 543 (the exception: a = 9, b = 6, k = 1, |P| = 7). The 20 hardest n = 25 trees, which
  took the plain search up to 1.4e10 nodes, take seconds this way. Frequent shape: f(A) = 1 with A's
  leaves in a high block, B's leaves from 2 up, f(B) high.
- Constructed sweep a, b <= 7, k <= 2, all 8 pendants with <= 4 vertices: 224 of 240 have block
  labellings. All 16 failures have k = 1 (one connector vertex) carrying a 3- or 4-vertex pendant,
  mostly K_{1,3}. Two separate searches (`blocks.py`, `gblocks.py` with t = 4) agree on the same 16.
- Forcing blocks on every leaf group is too strict (58 failures); blocks only on stars with >= 4 leaves.
- Running: sweep a, b <= 12, k <= 4 (`notes/sweep_a12_k4_t4.txt`).

Candidate statement to aim at: for k >= 2 (connector of length >= 3), D(a, b, k, i; P) with small P has a
block super edge-magic labelling for all a, b >= 4, with an explicit formula; k = 1 needs separate cases.
