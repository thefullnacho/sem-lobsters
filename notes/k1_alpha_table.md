# One-vertex connector: alpha-labelling by pendant and star sizes (2026-11-11)

Exhaustive search (`full_alpha.py 1 5`, cap 2e8 per pinned vertex). YES = alpha found and re-checked;
NO = search finished, none exists; CAP = undecided (rerun at 2e10 in `k1_capped_rerun.txt`).

| P | pendant edges (root 0) | |P| | a=4 b=4 | a=5 b=4 | a=5 b=5 | a=6 b=4 |
|---|---|---|---|---|---|---|
| 0 | single vertex | 1 | YES | YES | YES | YES |
| 1 | [(0, 1)] | 2 | NO | NO | NO | NO |
| 2 | [(0, 1), (1, 2)] | 3 | NO | NO | NO | NO |
| 3 | [(1, 0), (0, 2)] | 3 | NO | NO | NO | NO |
| 4 | [(0, 1), (0, 2), (1, 3)] | 4 | YES | YES | YES | YES |
| 5 | [(1, 2), (1, 0), (2, 3)] | 4 | YES | YES | YES | YES |
| 6 | [(0, 1), (1, 2), (1, 3)] | 4 | NO | NO | NO | NO |
| 7 | [(1, 0), (0, 2), (0, 3)] | 4 | NO | NO | NO* | NO* |
| 8 | [(0, 1), (0, 2), (1, 3), (3, 4)] | 5 | NO | NO* | NO* | NO* |
| 9 | [(1, 0), (1, 3), (0, 2), (2, 4)] | 5 | NO | YES | YES | NO* |
| 10 | [(1, 2), (1, 0), (2, 3), (3, 4)] | 5 | YES | YES | YES | YES |
| 11 | [(0, 1), (0, 2), (1, 3), (1, 4)] | 5 | YES | YES | YES | YES |
| 12 | [(1, 0), (1, 4), (0, 2), (0, 3)] | 5 | YES | YES | YES | YES |
| 13 | [(1, 2), (1, 0), (2, 3), (2, 4)] | 5 | YES | YES | YES | YES |
| 14 | [(2, 1), (2, 4), (1, 0), (1, 3)] | 5 | YES | YES | YES | YES |
| 15 | [(0, 1), (1, 2), (1, 3), (1, 4)] | 5 | NO | NO | NO* | NO* |
| 16 | [(1, 0), (0, 2), (0, 3), (0, 4)] | 5 | NO | NO* | NO* | NO* |

\* decided at cap 2e10 per pinned vertex (`notes/k1_capped_rerun.txt`). No CAP left.
