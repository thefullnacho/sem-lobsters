# sem-lobsters

Computer experiments on alpha-labellings and super edge-magic labellings of two-hub trees (lobsters and their
relatives): two stars joined through a short connector, with small trees hung on it.

Main results so far (details, provenance and caveats in `notes/first-look.md`):

- **T(a):** stars with a and 4 leaves joined through one vertex x, plus a path x-r-c-s hung on x, has alpha-deficit
  exactly 1 for every a >= 2 (exhaustive search for a = 2..21 by two independent programs, then Lemma 5.1 of
  Brinkmann, Crevals, Melot, Rylands, Steffen, DMTCS 14(1) (2012) 159-174).
- **Two-hub landscape:** every core tree with at most 9 vertices, both hubs carrying leaves, n <= 62: 635 families,
  maximum alpha-deficit 1; 4 families have a boundary that moves with the size of the other star.
- **A period rule** for one of those families (t leaves on one core vertex): pre-registered and held-out predictions
  all correct; proved for every a in 128 (t, b) cases (Lemma 5.1 plus exhaustive computation).
- **Conjecture 1** (two stars through one vertex with a t-leaf star hung on it): deficit 0 iff min(a, b) <= t, else 1.
  4,213 trees, t = 1..6, no exceptions.

## Layout

- `analysis/`: search and analysis scripts (Python, C). `alpha_fix.c` is our exhaustive alpha-labelling search.
- `analysis/multi_alphadeficit.c`: Gunnar Brinkmann's alpha-deficit program, released here with his permission,
  with one change: an optional 128-bit build for trees up to 127 vertices. 64-bit is the default; every changed line
  is marked `ALPHA128 change`.
- `notes/`: the research log (`first-look.md`) and the raw output of every run it cites.
- `data/`: tree shape tables from the super edge-magic search at n = 23, 24, 25.

## Build

    make                                  # bin/multi_alphadeficit (<= 63 vertices) and bin/multi_alphadeficit128
    gcc -O3 -o analysis/alpha_fix analysis/alpha_fix.c

Input is multicode (`analysis/to_multicode.py`). Scripts expect to be run from `analysis/`.

## License

MIT (see `LICENSE`), except `analysis/multi_alphadeficit.c`, which is Gunnar Brinkmann's program, distributed
here with his permission and not under the MIT license.
