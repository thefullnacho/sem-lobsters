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

## Colour-class split (research session's point, 2026-11-11 night)

Split = one colour class takes labels 1..|class|; such a super edge-magic labelling is an alpha-labelling
with the high labels reversed (the v3 pipeline's alpha_sem stage used exactly this map; it was a quick
randomised search, 300 nodes x 200 attempts, so trees falling through it says nothing about alpha).

- Stored retry labellings: split in 2/301 (n = 23), 4/1,012 (24), 22/23,458 (25). Random labellings, so
  uninformative either way.
- Sweep a, b <= 7, k <= 2 (`notes/splitcheck_a7_k2.txt`): 144 split block labellings, 80 block but no split
  block labelling, 16 no block labelling. So block labellings are NOT always alpha in disguise.
- k = 1 does not rule out the split: pendants K1 and P4end split in all 10 cases.
- Where blocks fail to split: k = 2 only for pendants that are stars hung by their centre (P2, P3mid,
  K13centre) and only when a != b (6 of 10 pairs). With the block rule dropped, a split labelling (an
  alpha-labelling) exists in all 6 tested.
- Open: pendant sizes up to 8 and their shapes (sweep covers <= 4 vertices).

Working view: the family may simply have alpha-labellings. That moves the literature check to
alpha-labellings of lobsters / two-star trees before any proof is written.

## Barrientos 2025, Lemma 2.1 (refs/, read from the PDF)

Utilitas Math. 123 (2025) 195-204, doi 10.61091/um123-15. Alpha-trees T1, T2, T3 (lambda_i = largest
dark label): glue T1's vertex lambda_1 to T2's vertex 0; then either T2's lambda_2 to T3's 0 (case 1) or
T2's lambda_2 + 1 to T3's top label n_3 - 1 (case 2; the paper writes "n_3" in shifted terms). Result is an
alpha-tree. Remark 2.2: T3 may be any graceful tree, but then the result is only graceful.

Applied with T1 = star(A) + x_1, T2 = connector x_1..x_k + pendant, T3 = star(B) + x_k
(`analysis/barrientos.py`): T2 has the required labelling (x_1 = 0, x_k = lambda_2 or lambda_2 + 1) only
when the pendant is a single vertex; 0 of 144 (pendant, position) pairs with |P| = 2..5, k = 2..4.
Hand check: k = 2, |P| = 2 forces y = 2 and two edges of weight 2.

Better split for k = 2: pendant into T1 (T1 = star(A) + leaf x carrying P, needs x = lambda_1),
T2 = edge x-y, T3 = star(B) + y. Running (`analysis/barrientos_t1.py`).

The 16 block failures are super edge-magic: sem_direct (C, v3 pipeline) labelled all 16, re-checked.

## Lemma 2.1 with the pendant in an outer piece (k = 2), exhaustive C search (`analysis/alpha_fix.c`)

T1 = star(A) + leaf x carrying P, x pinned to lambda_1; or symmetrically T3 = star(B) + leaf y carrying P,
y pinned to 0 (case 2 after complementing). Every YES witness re-checked as an alpha-labelling in Python.
Result does not depend on the star size (a = 4..9 identical per shape), and T1 and T3 agree:
5 of the 17 rooted pendants with <= 5 vertices work (indices 0, 5, 10, 13, 14 in rooted_trees(5)), 12 do not.
So the lemma covers k = 2 only for those shapes. Running: whether the full trees with the other 12
shapes have any alpha-labelling at all.
- Full alpha-labelling existence for the 12 uncovered pendant shapes, k = 2, (a, b) in {(4,4), (5,4), (5,5)}:
  36 of 36 trees are alpha-trees (exhaustive C search pinning each vertex to 0; witnesses re-checked).
  So the family looks alpha throughout; Lemma 2.1 with star pieces explains only 5 of 17 shapes.

## First explicit formula (2026-11-11 night): k = 2, pendant = one edge r-s hung on x1

q = a + b + 5. A = 0; A's leaves q-a+1..q; r = 1; x2 = 3; B's leaves {2} U {4..b+2}; B = b+3; s = b+4;
x1 = b+5. Dark labels 0..b+2 (lambda = b+2). Differences: B-leaves {1..b-1, b+1}, x2-B b, x1-x2 b+2,
r-s b+3, x1-r b+4, A-x1 b+5, A-leaves b+6..q: each of 1..q once. Valid for a >= 1, b >= 2.
`analysis/formula_p2.py`: checked as alpha and (after l -> lambda+1-l, u -> u+1) as super edge-magic for
a = 1..60, b = 2..60, 0 failures. This shape is NOT reached by Lemma 2.1 with star pieces.
Found by reading the lexicographically first alpha-labelling from the exhaustive search at a, b = 4..7.
Note: the tree is a lobster, so check the alpha-lobster literature for it before claiming anything.
