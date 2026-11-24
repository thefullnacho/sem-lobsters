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

## Literature (Alex's research session, 2026-11-11 night)

- No source found giving alpha-labellings for double stars with a pendant on the connector or for
  two-leg lobsters: the 12 uncovered shapes look new.
- Diameter-4 trees that are not caterpillars have no alpha-labelling: stated in Stefanec 2009 (student
  thesis, Bratislava), next to Huang-Kotzig-Rosa 1982, uncredited. Research session's exhaustive check:
  all 58 such trees up to 12 vertices, none alpha. With k = 1, a pendant that is a star hung by its centre
  (P2, P3mid, K13centre) gives exactly such a tree, so those can never be alpha; their SEM labellings
  are non-alpha.
- Luiz, Campos, Richter 2019 (alpha-lobsters): keywords include maximum degree 3, likely not our stars.
- Krisnawati et al.: SEM deficiency of subdivided double stars, not alpha.
- Barrientos 2019 (lobsters): joins diameter-4 caterpillars centre to centre; our shape does not fit.

## One-vertex connector, full alpha test (partial, `full_alpha.py 1 5`)

Diameter-4 cases (P2, P3mid, K13centre) all NO, as the theorem predicts. Also NO at diameter >= 5,
where the theorem says nothing: P3end (diam 5), the depth-2 pendant P=6 (diam 5), P=8 (diam 6).
If the search is right, these are non-alpha trees beyond diameter 4. Validating alpha_fix first
(`validate_alpha.py`: brute force n <= 8, caterpillars and diameter-4 facts n <= 12).

## Parity property (Brinkmann et al. Sec. 4, exact statement via research session), `analysis/parity.py`

Property = (1) each bipartition class has one degree parity, and (2) vertex parity != edge parity, where
edge parity = q(q+1)/2 mod 2 and vertex parity = sum deg(v) l(v) mod 2 (checked for both choices of dark
class). Cor 4.2: then no alpha-labelling, odd n, an even-degree class. Sanity: 7 trees with n <= 14 have
it, all satisfy Cor 4.2 (2), (3), and our exhaustive search finds none of them alpha.
On our family (a, b in 4..9): fires only for k = 1 with pendant P2 or K13centre and a, b both odd: these
are diameter-4 non-caterpillars, already non-alpha. Never fires for the beyond-diameter-4 non-alpha shapes
P=2, 6, 8, 9 (one-vertex connector), nor for any k = 2 tree. So those need a new argument.

## Block sweep a, b <= 12, k <= 4 (stopped at its 2 h limit, 21:14, partway through a = 11)
`notes/sweep_a12_k4_t4.txt`: 85 without a block labelling (k = 1: 30 K13centre, 19 K13leaf, 12 P3end;
k = 3: 24 P3mid), 110 capped by the Python search. Incomplete and superseded by the alpha analysis;
kept for the record. Redo in C only if block labellings come back into the argument.

## Bigger stars, one-vertex connector (2026-11-13)

First run (`alpha_fix` without symmetry breaking, cap 5e10): 96 of 120 cases capped. Fix: sibling leaves
(same parent) get increasing labels, and label 0 is pinned on one leaf per sibling class (swapping sibling leaves
is an automorphism, so nothing is lost). Re-validated: brute force n <= 8, all 557 caterpillars and 58 diameter-4
non-caterpillars n <= 12, and all 68 cells of `k1_alpha_table.md` identical; the old table re-decides in < 1 s.
Rerun (`notes/k1_big_v2.txt`, 140 cases, a, b in 4..10 with b <= a), agrees with all 24 first-run decisions:
- P = 2, 6, 15 (small star hung through one extra vertex): non-alpha in all 28 size pairs.
- P = 8: non-alpha in every decided pair.
- P = 9: size-dependent; non-alpha at b = 4 (except a = 5) and when a, b are both even; alpha otherwise.
Orders here are n = a + b + 2 + |P| <= 27, so nearly all sit inside Brinkmann et al.'s exhaustive range
(all trees up to 26 vertices): the individual verdicts are checkable against their data; what could be new is
the family statement and a proof for all star sizes.

## Route to an infinite family: Brinkmann et al. 2012, Lemma 5.1 (refs/brinkmann2012-alpha-deficit.pdf)

Brinkmann, Crevals, Melot, Rylands, Steffen, "alpha-Labelings and the Structure of Trees with Nonzero alpha-Deficit",
DMTCS 14(1) (2012) 159-174, doi 10.46298/dmtcs.569. Research session: the paper has no diameter-5, double-star or
two-star results; its infinite non-alpha families are comets, subdivided odd-degree trees and a max-degree-3 series;
its non-alpha lists are not published. Read here from the PDF:
- Lemma 5.1 (verbatim): T with classes V1, V2, v in V1, T_p = T plus p pendant vertices at v. For all
  p, p' >= (|V1| - 1)(|V2| + 1): alphadef(T_p) = alphadef(T_p').
- alphadef = n - 1 - (max distinct edge labels over bipartite labelings), so alphadef = 0 iff an alpha-labelling
  exists. The proof's "V1 gets the low labels" is without loss: n - 1 - l swaps the classes, same edge labels.
Applied (research session's working, checked): k = 1, pendant x - r - c with t leaves on c, v = A, base T with
A a leaf of x: V1 = {A, B, r, t leaves}, V2 = {x, c, b leaves}; threshold a >= (t + 2)(b + 3). P = 2 (t = 1),
b = 4: a >= 21 (n = 31). So: P = 2, b = 4, a = 4..21 all non-alpha => non-alpha for every a >= 4.
Run (`/data/sem-lobsters/p2_b4.out`, cap 1e14): a = 4..15 NO so far; 16..21 running.
Final for the a, b <= 10 rerun: P = 2, 6, 15 non-alpha in all 28 pairs; P = 8 non-alpha in 27, (10, 10) capped at
5e10; P = 9 alpha in 16, non-alpha in 12 (including (10, 10), both even, fitting the apparent parity rule).

## RESULT (2026-11-13): an infinite non-alpha family, computer-assisted

Tree T(a): stars A (a leaves) and B (4 leaves) joined through one vertex x (A - x - B), with a 3-vertex path
x - r - c - s hung on x. Exhaustive search (`alpha_fix`, symmetry-broken, validated): T(1) is alpha; T(a) is
non-alpha for every a = 2..21 (`notes/p2_b4.txt`, cap 1e14, none capped; a = 21 finished 2026-11-13 13:27).
Lemma 5.1 of Brinkmann et al. 2012 with v = A, threshold (t + 2)(b + 3) = 21, gives alphadef(T(a)) = alphadef(T(21))
> 0 for all a >= 21. Hence: T(a) has no alpha-labelling for every a >= 2 (diameter 5, max degree up to a + 1;
parity property never applies; not in Brinkmann et al.'s families per the research session).
Before claiming it: an independent second decider (different method, no shared code, e.g. a CP-SAT encoding)
must re-decide a = 2..21, as was done for Gallai n = 12; and a literature check for this exact tree.
Same route is open for P = 6 (threshold a >= 28) and P = 15 (a >= 35) at b = 4, and for other fixed b.

## Correction (2026-11-13, research session; Theorem 1.2 checked from the PDF)

Theorem 1.2 (Brinkmann et al. 2012): for all k, d and n >= k^2 + k, the number of trees with n vertices, alphadef = d
and maximum degree n - k is the same; its proof is Lemma 5.1 on the big vertex, i.e. our argument. Our T(a) has
n = a + 10 and maximum degree a + 1 = n - 9, so it is in the k = 9 class; Brinkmann's slides give 80 non-alpha
trees at k = 9 for n = 18..25 as "constant series" (a smallest tree plus a fan of leaves). So T(a) is very likely
one of those series: enumerated, never drawn, lists not public. Not a new infinite family. What is ours: the
explicit description and the exact boundary a >= 2. Open and outside their theorem: both stars growing together
(max degree about n/2); our data has P = 2, 6, 15 non-alpha for all a = b <= 10; needs a two-vertex Lemma 5.1.
Plan: research session drafts an email to Brinkmann (Alex sends): is T(a) in the k = 9 series; ask for their
program (it would also serve as an independent second decider). Independent CP-SAT decider on hold until then.

## Second decider: Brinkmann's own program (2026-11-14)

Gunnar Brinkmann replied within a day and sent `multi_alphadeficit.c` (refs/brinkmann-code/, shared privately:
he has since agreed to its release, see the end of this file). Built as bin/multi_alphadeficit; input is multicode
(`analysis/to_multicode.py`). Validation against our alpha_fix: non-alpha counts identical for every n = 4..14
(13,402 trees), and tree-by-tree identical at n = 13 and 14 (4,460 trees). It also reports the deficit.
On our family T(a) (stars a and 4 through one vertex x, plus path x-r-c-s): alphadef(T(1)) = 0 and
alphadef(T(a)) = 1 for every a = 2..21 (`notes/T_a_brinkmann.txt`, each well under a second). With Lemma 5.1
(threshold 21): alphadef(T(a)) = 1 for all a >= 2. Two independent deciders agree on every case.
Brinkmann could not confirm whether T(a) is in his k = 9 constant series.
His program is fast enough to explore the both-stars-growing direction far past our search's reach.

## Both stars growing: full grid with Brinkmann's program (2026-11-14)

All a >= b >= 1 with n <= 62 (the program's limit), one-vertex connector, pendants P = 2, 6, 15, 8, 9
(`analysis/diag.py`, `notes/grid/`): 3,727 trees, each well under a second, none undecided. Every tree with
n <= 22 (267) re-decided by our alpha_fix: 0 disagreements. Deficit is never above 1.

Pattern, "a star with t leaves hung on x through one vertex" (x - r - c, t leaves on c; P = 2, 6, 15 are t = 1, 2, 3):
  alpha-deficit = 0 if min(a, b) <= t, and exactly 1 otherwise. Holds in every cell, all a, b up to n = 62.
P = 8: alpha iff b <= 2. P = 9: alpha iff b = 1 or 3, or b odd >= 5 (any a >= b), or b even and a odd with
  b < a <= 2b - 3; deficit 1 otherwise.

Conjecture 1 (data to n = 62, two deciders where they overlap; proved for t = 1, b = 4 via Lemma 5.1):
  For t >= 1, the tree of two stars (a and b leaves) through one vertex x, with a t-leaf star hung on x through
  one extra vertex, has alpha-deficit 0 if min(a, b) <= t and alpha-deficit 1 otherwise.
This is the both-stars-growing direction outside Brinkmann et al.'s Theorem 1.2 (max degree about n/2).
Next: a proof. Lemma 5.1 gives, for each fixed b, constancy in a beyond (t + 2)(b + 3); a two-vertex version is
needed for the diagonal. Check larger t (4, 5) the same way.
Extension: t = 4, 5, 6 (hung star with 4, 5, 6 leaves), all a >= b >= 1 with n <= 62: 2,028 more trees, 0
violations of Conjecture 1. Total evidence: t = 1..6, 4,213 trees (P = 2, 6, 15 plus t = 4..6), every cell fits.

## Two-hub landscape (2026-11-14), `analysis/landscape.py`, `notes/landscape_c8_n62_summary.txt`

Every core tree with <= 8 vertices, every hub pair up to symmetry (hubs carry no core leaves), a and b leaves on
the hubs, all a, b >= 1 with n <= 62: 231 families, 337,989 trees, deficits from Brinkmann's program.
- ALPHA everywhere: 194. CONST deficit 1: 19. THRESH (alpha iff a <= s1 or b <= s2, else 1): 11. EVENTUAL
  (constant once a, b >= m): 7. OTHER: 0. Max deficit anywhere: 1.
- Every family is eventually constant in both a and b: evidence for a two-vertex Lemma 5.1.
- Conjecture 1's families appear as THRESH (1,1) and (2,2); the other THRESH families extend it.
- Caution: EVENTUAL with m = 18 and m = 27 rest on very few cells under n <= 62; treat as inconclusive.
Hub-pair dedupe uses a WL hash on the marked core (colour refinement is complete for trees).

## Threshold risk (2026-11-14, raised by Alex/research: "moderate confidence")

Risk: a two-star Lemma 5.1 with constants like (t + 2)(b + 3) passes 62 vertices once b ~ 10, leaving most of the
231 families unsettled; the target must be a threshold depending only on the core. Measured stabilisation point m
(deficit constant for all a, b >= m, >= 50 tail cells): 229 of 231 families have m <= 5 (most m = 1; max m by core
size: c <= 5: 1, c = 6: 2, c = 7: 3, c = 8: 5). Outliers: one family at m = 18, one with no stable region visible
inside n <= 62. So true thresholds look small and core-only; Lemma 5.1's bound is loose because its pigeonhole on
A's leaves counts B's leaves too.
Plan: (1) study the two outliers; (2) a specialised two-star decider with no 62-vertex limit: fix the core's labels,
then the remaining labels on the leaves' side split into S_A and S_B, and the question is whether S_A - f(A),
S_B - f(B) and the core's edge labels tile 1..n-1 (polynomial in a, b for a fixed core); validate against both
existing deciders; (3) after the grant: a two-star lemma with a core-only threshold.

## Correction: two families have boundaries that move with the other star (2026-11-14)

The two outliers are not slow to settle; their switch point grows linearly with the other star:
- fid 126 (c = 8, core [[0,5],[1,0],[1,2],[1,4],[2,3],[5,6],[5,7]], hubs 0, 4): b odd -> non-alpha iff a >= 2b + 1
  (3, 7, 11, ..., 27 for b = 1..13); b even -> alpha throughout the grid. Its "m = 18" was an artefact of n <= 62.
- fid 206 (c = 8, core [[0,4],[0,6],[1,0],[1,2],[1,3],[4,5],[6,7]], hubs 2, 3): parity pattern; b even: a odd alpha
  iff a <= 2b - 3 (the P = 9 rule), a even non-alpha; odd b rows have their own linear pattern.
Scan of all 231 families (rows b, a = 1..11, last change point vs the fixed coordinate): only these two move.
Rows reach about 50 leaves, so boundaries steeper than about 4:1 would be invisible here.
So the earlier "every family is eventually constant" overstated it: 229 families have small core-only thresholds
(m <= 5); 2 (both first appearing at core size 8) have linear boundaries with parity. A theorem needs two forms:
a core-only threshold for most cores, and regions cut by linear inequalities plus parity for the rest. The
specialised decider (no 62-vertex limit) is needed to see whether larger cores or steeper slopes add more.

## Past 62 vertices: 128-bit patch of Brinkmann's program (2026-11-14)

`analysis/multi_alphadeficit128.c` (local patch, NOT for redistribution: ULLI -> unsigned __int128, VERTICES 127,
two hardcoded widths). Validation: identical output to the original (deficit-0 and deficit-1 filters, counts) on
every tree n = 4..16, and on all 2,862 grid cells of the two outlier families. About 1 s at n ~ 67, ~18 s at n ~ 100-118.
Outlier rules confirmed beyond the old limit: fid 126, b = 29: alpha at a = 56..58, deficit 1 at a = 59 (= 2b + 1);
b = 30: alpha at a = 40, 61, 80 (n = 110). fid 206, b = 30: odd a alpha up to 57 (= 2b - 3), 59 non-alpha; even a non-alpha.
Steep-boundary scan (`analysis/steep_scan.py`, 128-bit program): every family, one hub fixed at 1..6 leaves, the
other at 70, 85, 100, 115 leaves (n <= 126), both orientations: 9,958 trees, 0 differ from the stable value at the
edge of the n <= 62 grid. (A first run had a bug: the second orientation repeated the first; fixed and rerun.)
With one star small the program is near-instant even at n ~ 125. So no hidden boundary with slope up to ~18:1;
the two linear-boundary families (126, 206) look like the only ones among cores up to 8 vertices.
LIMIT of the steep scan (Alex, 2026-11-14): it held one star at 1..6 leaves and pushed the other to 115, so it rules
out boundaries with slope up to about 19 that start at small b. It does NOT test the middle region where both stars
have 30 to 60 leaves, beyond the old grid: a boundary that only begins at larger b, or a steeper one, could sit there.
Next: a sparse sample of that region with the 128-bit program.
Middle region closed (2026-11-14, `analysis/middle_scan.py`): every family, ordered pairs a, b in
{30, 31, 40, 41, 50, 51, 58, 59} (both parities), n <= 126, 128-bit program: 14,784 trees, 0 mismatches against the
predictions (stable value for the 229 ordinary families; exact rules for fid 126 and 206, including 206's b-odd rule
"non-alpha iff a even and a <= 2*ceil((b - 1)/4)", which predicts a = 30, b = 59 non-alpha). Remaining untested:
boundaries that begin beyond about 60 leaves on both stars, and cores with more than 8 vertices.

## Cores up to 9 vertices (2026-11-14)

635 families, 894,701 trees, n <= 62 (`notes/landscape_c9_n62_summary.txt`). All 231 c <= 8 families reproduce with
identical tables. Classes: ALPHA 552, CONST 37, THRESH 19, EVENTUAL 27; max deficit 1. Settling point for c = 9:
376 of 404 at m = 1, the rest by m = 8, plus three outliers (one at 18, two none visible).
Moving boundaries: 4 of 635 families. New at c = 9:
- fid 440: fid 126's core with one more leaf on vertex 5 (3 leaves instead of 2). Boundary a >= 2b + 1 at
  b = 2, 5, 8, 11 (b = 2 mod 3), and at b = 1 (a >= 3); none at b = 3, 4, 6, 7, 9, 10. Period 3 vs fid 126's period 2.
  Clue: the period equals the number of leaves on that one core vertex.
- fid 600: boundary 2b - 3 for odd b >= 5; a fixed point (a = 6) for even b >= 8.
Not yet done for the two new families: checks past n = 62 (128-bit program) and the middle region.
Families 440 and 600 past 62 vertices (2026-11-14, `notes/fam440_600_past62.txt`), predictions stated before the run:
- 440: non-alpha iff b = 2 (mod 3) and a >= 2b + 1 (b >= 2).
- 600 (b >= 5): b odd -> non-alpha iff (a odd and a >= 5) or a >= 2b - 2; b even -> non-alpha iff a odd and
  5 <= a <= 2*floor(b/4) + 1.
27 trees at b = 29, 30, 31, n up to 119: 27 of 27 as predicted.
Period test, fid 126's core with t leaves on vertex 5 (`analysis/period_test.py`, t = 1..6, b <= 20): wherever a
boundary exists it is at a = 2b + 1; which b have one is periodic in b with period t for b >= 5: t=1 none; t=2
b = 1 (mod 2); t=3 b = 2 (mod 3); t=4 none; t=5 b = 1, 2, 4 (mod 5); t=6 b = 1, 2, 3, 5 (mod 6). Candidate "t does not
divide b(b + 2)" fits t = 1, 2, 3, 5, 6 for larger b but not t = 4 or some small b: unconfirmed. Wider test running.

## Period test, t = 1..10, b up to ~30-35 (2026-11-14, `analysis/period_test3.py`, `notes/period_test3_partial.txt`)

1,018 of 1,128 trees (the largest, near n = 127, still running). Boundary at a = 2b + 1 or none; no other patterns.
"t does not divide b(b + 2)" is WRONG (fails t = 4, 7, 8, 9, 10). Rule that fits every completed case:
- t != 1 (mod 3) (t = 2, 3, 5, 6, 8, 9): boundary iff t does not divide b and t does not divide b + 2; exception: the
  first b with b + 2 = t (b = 1, 3, 4, 6, 7 for t = 3, 5, 6, 8, 9) still has the boundary. Off-residues {0, t - 2}.
- t = 1 (mod 3) (t = 1, 4, 7, 10): no boundary once b is past a few small values (t = 4: only b = 1; t = 7: b <= 3;
  t = 10: b <= 5; t = 1: none).
Conjecture shaped by this data; needs fresh predictions (larger t, larger b) before trusting it.
Review (research session, 2026-11-14): the new rule and "t does not divide b(b+2)" differ only when t has a repeated
factor of 2 to split: t = 8 at b = 2, 10, 18, 26 (data: boundary at all four, so the new rule wins) and t = 12 at
b = 4, 6 (mod 12). "30 trees past 62 vertices" in my message was a miscount: the run had 27 cases, all reported.
The 110 large trees still running are a held-out test, scored against the rule as committed in cc6dec9, no refit.
Pre-registered predictions for t = 11, 12, 13: `notes/period_predictions_t11_13.md`.
Reading lead (not checked): Brinkmann et al. give comets alpha-deficit floor(m/3); a period of 3 has appeared here before.

## Period rule: held-out and pre-registered tests PASS (2026-11-15)

- Pre-registered t = 11, 12, 13 (`notes/period_predictions_t11_13.md`, committed d8d178d before running;
  results `notes/period_t11_13.txt`): 30 of 30 as predicted. t = 12 at b = 4, 16, 28, 6, 18, 30 (where the old guess
  "t does not divide b(b+2)" says no boundary): boundary at all six. t = 11: exception b = 9 has it; 11, 20, 22, 31 do
  not. t = 13: boundary for b = 1..7, none at 8, 9, 15, 25 (cutoff (2t - 5)/3 = 7 exactly).
- Held-out (results that landed after cc6dec9, scored against the rule as committed, no refit): 35 of 35 complete
  cases agree. The other cases near b = 37-40 exceed the 127-vertex limit and were never run.
Rule (family: fid 126's core with t leaves on vertex 5; boundary means non-alpha iff a >= 2b + 1):
  t != 1 (mod 3): boundary iff t divides neither b nor b + 2, plus the first b with b + 2 = t.
  t = 1 (mod 3): boundary only for b <= (2t - 5)/3.
Next: understand the mod-3 split (lead: comets' alpha-deficit floor(m/3), Brinkmann et al. 2012).

## Review of the period rule (research session, 2026-11-15): what is proven vs observed

- Provenance of the "b + 2 = t" exception: read off the t <= 10 data (t = 3, 5, 6, 8, 9) and written into cc6dec9
  after seeing it; pre-registered only for t = 11 (b = 9) and t = 12 (b = 10). Those two are its only fresh tests.
- Scope: verdicts were checked only up to the largest b whose trees fit in 127 vertices (about b = 36-40 depending
  on t); larger b is untested.
- a-range: every verdict looked only at a = 2b, 2b + 1, 2b + 4. "Never again" / "none" claims for all larger a are
  observations, not proofs.
- Closing it with Lemma 5.1: for each (t, b), T = the tree with A's leaves removed (v = A = hub 0); threshold
  p0 = (|V1| - 1)(|V2| + 1). Computing every a = 1..p0 proves the verdict for all a. Within 127 vertices this is
  possible for 128 of 520 (t, b) cases (t = 1: b <= 27; 2: <= 20; 3: <= 16; 4: <= 13; 5: <= 11; 6: <= 9; 7: <= 7;
  8: <= 6; 9: <= 5; 10, 11: <= 4; 12, 13: <= 3). The other 392 stay observed, flagged as such.
Lemma 5.1 proof runs (2026-11-15, `analysis/prove_a_range.py`, `notes/prove_a_range.txt`): every a = 1..p0 for all
128 reachable (t, b) cases, 8,405 trees. All 128 match the rule at every a: 61 with a boundary (alpha for a <= 2b,
deficit 1 for a >= 2b + 1, hence for all a by Lemma 5.1), 67 without (alpha for every a). These 128 verdicts hold for
ALL a (computer-assisted: Lemma 5.1 + the validated 128-bit program). The other 392 (t, b) cases (larger b for each t)
remain observed at a = 2b, 2b + 1, 2b + 4 only. One tree of the period_test3 run (t = 1..10) is still running.

## Review of the proven tier (research session, 2026-11-15)

- V1 check: threshold() takes V1 = colour class of vertex 0 = A's centre (the hub with a leaves) = the class of v. OK.
- Above 63 vertices the widened copy had been checked only against itself: 95 of the 128 "proven" (t, b) cases
  include trees with n > 63 (3,226 of 8,405 trees; 1,636 alpha, 1,590 non-alpha). Our alpha_fix never ran above 48.
  Independent checks now:
  1. All 5,082 proof-run trees with n <= 62 rerun on Brinkmann's ORIGINAL program: 0 disagreements. So the 33 cases
     entirely <= 62 vertices do not depend on the patch.
  2. alpha verdicts above 63: certified independently by finding an alpha-labelling with alpha_fix128 (MAXN 128,
     arrays only) and verifying it in Python (barrientos.alpha_check). Running (`analysis/witness_big.py`).
  3. non-alpha verdicts above 63: no independent certificate possible with our decider; only known-answer tests of
     the widened copy (T(a), deficit 1 for all a >= 2 by original program + Lemma 5.1, at n = 64..127; random
     caterpillars n = 64..127, deficit 0). Running.
- Publishing: the proof tier needs releasable code. Queued for Alex: ask Brinkmann whether his program and our
  128-bit patch may be released. Until then, the tier claims for n > 63 rest on the patch.
Independent checks, results (2026-11-15):
- alpha witnesses above 63: the general search (alpha_fix128) found none at n = 64 (24 tries; stopped). The
  block-structured split search (gblocks, block thresholds 4, 3, 2, 5) certified 651 of 1,636 alpha trees, each
  converted to an alpha-labelling and verified by barrientos.alpha_check (`notes/witness_block.txt`). It works near
  the boundary (b < a <= 2b: 117 of 124) but mostly fails in the far tail (a > 2b: 534 of 1,508): tail labellings
  are not block-structured.
- Known-answer tests of the 128-bit copy (`/data/sem-lobsters/known_answer.txt`): running; first 70 all correct.
- Proven tier, by what it rests on: 52 of 128 (t, b) cases independent of the patch (original program <= 62
  vertices + verified alpha-labellings above); 29 depend on the patch for uncertified alpha verdicts above 63;
  47 depend on the patch for non-alpha verdicts above 63. For the write-up, the proof tier is the 52 until the
  patch is released (Brinkmann's permission) or an independent certificate exists for the rest.
Known-answer tests of the 128-bit copy, final (`notes/known_answer.txt`): T(a), a = 54..117 (n = 64..127, deficit 1
known without the patch): 64 of 64 correct. Random caterpillars n = 64..127 (deficit 0): 163 of 163 that finished
correct; 37 hit the 5-minute per-tree cap (TIMEOUT, no answer). No wrong answer anywhere.
Period test t = 1..10 (`period_test3`) complete: 1,128 of 1,128 trees.

## Release permission (Brinkmann, email 2026-11-16; recorded here 2026-11-23)

Brinkmann agreed to the release of his program with our change, on two conditions: the change is commented in the
code, and a plain 64-bit build stays available (it is faster). Done 2026-11-23: `analysis/multi_alphadeficit.c` is his
program with an optional 128-bit build (`-DALPHA128`, up to 127 vertices); 64-bit is the default; every changed line
is marked "ALPHA128 change". `make` builds both bin/multi_alphadeficit and bin/multi_alphadeficit128. This replaces the
earlier local copy analysis/multi_alphadeficit128.c. So the "patch not releasable" caveat above no longer applies: the
proof tier is all 128 (t, b) cases (computer-assisted), 69 of them also checked independently of the 128-bit build.

## Conjecture 1: proof runs via Lemma 5.1 (2026-11-23, `analysis/prove_conj1.py`, `notes/prove_conj1.txt`)

For t = 1..6 and every b whose threshold tree fits in 127 vertices (b <= 28, 21, 17, 14, 12, 10 for t = 1..6), every
a = 1..p0 computed (v = A, p0 = (|V1| - 1)(|V2| + 1), V1 = class of A): 102 (t, b) pairs, 6,026 trees, 0 mismatches
with Conjecture 1. 64-bit program for n <= 63, 128-bit build above (2,138 trees, 59 alpha, 2,079 non-alpha); 38 pairs
lie entirely within 63 vertices. The tree is symmetric in A and B, so Conjecture 1 now holds (computer-assisted) whenever
min(a, b) <= 28, 21, 17, 14, 12, 10 for t = 1..6. Open: both stars above those bounds. Whole run took about 20 s.
Period rule rescored from all result files: 9,259 trees, 419 (t, b) pairs, 0 mismatches; 128 pairs proven for all a,
the other 291 tested at a = 2b, 2b + 1, 2b + 4 only.

## Correction: a fifth moving family, fid 574 (2026-11-23)

Rescoring the c <= 9 landscape (constant for all a, b >= m, >= 50 tail cells): m = 1 for 589 families, 2..8 for 41,
and five families with no small m: 126, 440 (both "m = 18" artefacts of their linear boundaries), 206, 600, and 574.
fid 574 (core [[0,5],[0,8],[1,0],[1,2],[1,3],[1,4],[5,6],[5,7]], hubs 2, 3) was missed by the earlier scan: for
b = 0, 1 (mod 3) from b = 6 the deficit has period 3 in a below a cutoff growing roughly linearly in b, then 1;
for b = 2 (mod 3) it is 0 except a = 3 and a short run of small a that lengthens with b. So "4 of 635 families
move" was wrong: 5. No exact rule yet; not checked past 62 vertices.

## Commit hashes changed (2026-11-23)

The history was rewritten before publishing (PDFs, Brinkmann's unmodified file and binaries removed), so hashes
quoted above are the pre-rewrite ones. Mapping (dates unchanged): cc6dec9 -> eedee92 (period rule as frozen),
d8d178d -> 4306a25 (pre-registered predictions), 626d01a -> bc77685 (results).
