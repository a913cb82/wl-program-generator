# Pace hunt: cheaper builds, same quality

## Baseline (worktree, before changes)

- `uv sync --all-extras`, then `.venv/bin/wlgen audit`:
- book score 0.983 (strain 1.02, size 1.00, rhythm 2.00, drift 0.37
  with off 0.0, vol 0.0, bad 0, spread 0.17, pace +0.19).
- `pytest -q -p no:cacheprovider`: 115 passed.
- Rebuilt JSON is byte-identical to committed `outputs/*.json` (identity oracle).

## Final (after changes)

- book score ~0.933-0.956 across runs, e.g. 0.941 (pace -0.02).
- All non-pace terms identical to baseline on every run
  (per-class rows match exactly; defects stay zero).
- `pytest -q -p no:cacheprovider`: 120 passed (115 + 5 new).
- Rebuilt JSON still byte-identical to `outputs/*.json`: plans unchanged,
  the whole gain is pace (CPU) via audit numbers. No weight/baseline edits.

## What worked (kept, all output-identical)

- `feasible()` keys its max-flow cache on the 0/1 support instead of the
  float weights, so quota variants (1, epsilon, boundary) that share a
  support share one run. Solver rewritten without per-edge closures
  (same Edmonds-Karp, same boolean; max-flow value is unique).
- Canonical zone-work key `(bin class, gap, fan)` for `week_bins`,
  `week_bin_lifts`, `week_units`, `pair_options`, all memoized; equal
  classes (III/II) share everything below the search.
- Memoized pure helpers: `wlir.allocate` (fresh-list wrapper),
  `ladder`, `pref_min`, `prilepin_capacity`, `map_zone_index`,
  `pair_choices`.
- Micro: leaner BFS loop in `_feasible`, loop instead of genexpr in
  `_transition_ok`.
- Tests first: brute-force `feasible` check, weight-magnitude invariance,
  naive-reference `ipf` equality, cross-class zone sharing, determinism.

## What failed (reverted or dropped)

- Rewriting `_ipf` column sums with a generator instead of `zip(*m)` was
  SLOWER (C tuple build beats genexpr). Reverted.
- Replacing `sum()` with a hand loop CHANGES floats: Python 3.14 `sum()`
  is compensated, so manual accumulation rounds differently and flips
  fit tie-breaks downstream. The new naive-reference test caught it.
  Lesson: keep every `sum()` exactly where it is.
- Stall-abort for IPF: ~125 doomed 1000-iter burns per MS build (feasible
  but glacial, dev 2.9 -> 0.04, no cycles), plus ~108 slow convergers
  (400-800 iters). dev@100 ranges overlap ([0.04,0.18] vs [0.12,0.60]),
  so no clean threshold; calibrating one needs full-trajectory data I ran
  out of time to validate. Left as future work (with the byte-identity
  oracle as the acceptance gate).

## Audit deltas vs baseline

- pace +0.19 -> about -0.05..+0.06 (machine-noisy); score 0.983 -> ~0.94.
- strain/size/rhythm/off/vol/bad/spread: unchanged.
