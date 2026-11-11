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
