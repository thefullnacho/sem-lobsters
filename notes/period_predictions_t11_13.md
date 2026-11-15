# Pre-registered predictions, t = 11, 12, 13 (written 2026-11-14, before any of these trees were run)

Rule as committed in cc6dec9. Boundary = alpha at a = 2b, deficit 1 at a = 2b + 1 and a = 2b + 4. No boundary =
alpha at all three.
- t != 1 (mod 3): boundary iff t does not divide b and t does not divide b + 2; exception: the first b with
  b + 2 = t still has the boundary.
- t = 1 (mod 3): last b with a boundary is (2t - 5)/3 (t = 4, 7, 10 -> 1, 3, 5); none after.

| t | b | prediction | why |
|---|---|---|---|
| 12 | 4, 16, 28 | boundary | b = 4 (mod 12): 12 | b(b+2) but 12 divides neither b nor b + 2 (separates the two rules) |
| 12 | 6, 18, 30 | boundary | b = 6 (mod 12): same separation |
| 12 | 12, 24 | none | 12 | b |
| 12 | 10 | boundary | first b with b + 2 = 12 (exception) |
| 12 | 22 | none | 12 | b + 2, not the first |
| 12 | 5, 13 | boundary | control |
| 11 | 9 | boundary | first b with b + 2 = 11 (exception) |
| 11 | 11, 22 | none | 11 | b |
| 11 | 20, 31 | none | 11 | b + 2 |
| 11 | 13, 15 | boundary | control |
| 13 | 1..7 | boundary | t = 1 (mod 3), b <= (2*13 - 5)/3 = 7 |
| 13 | 8, 9, 15, 25 | none | b >= 8 |
