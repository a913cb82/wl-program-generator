# IPF stall-abort: cut doomed burns early

## Hypothesis
~125 feasible-but-glacial IPF burns per MS build run all 1000 iterations and
return None anyway, plus ~108 slow convergers (400-800 iters). If doomed
trajectories stall (flat deviation) while convergers keep shrinking, a
no-progress abort returns the same None much earlier. Acceptance gate:
byte-identical `outputs/*.json` and unchanged quality terms in the audit
(strain/size/rhythm/instructions/longest); only pace may improve.
Every `sum()` kept exactly as-is (3.14 compensated summation flips
fit tie-breaks otherwise).

## Measurement (MS build, instrumented `_ipf`, dev sampled every 100 iters)
- 602 calls: 126 doomed (1000 iters, None), 110 slow (>=300 iters), 366 fast.
- Doomed trajectories freeze: e.g. dev `... 0.0832 -> 0.075 -> 0.075`
  (last 100 iters literally flat); per-100-iter ratios in [0.484, 0.904].
- Slow convergers plunge geometrically: `0.1468 -> 0.01 -> 0.0007 -> 0.0001`;
  per-100-iter ratios all <= 0.200 (200-iter windows: slow max 0.040,
  doomed min 0.318).
- Calibration: abort when a 200-iter window improves less than 2x
  (`dev > anchor * 0.5`), anchored at iter 200, first decision at iter 400.
  Margin: 12x below the best converger window, ~1.6x above the laziest
  doomed window (later windows only get flatter, so the abort still fires).

## Change (`src/wlgen.py`, `tests/test_wlgen.py`)
- New `_ipf_stalled(dev, anchor)`: `dev > anchor * 0.5`.
- `_ipf` check block now accumulates total deviation from the existing
  `sum()` calls (no sum touched, same `ok` semantics) and, every 200 iters,
  returns None on stall. Converging burns are untouched (their ratios are
  ~10x under the threshold).
- Tests (TDD: helper test red first): real harvested fixtures — a doomed
  (12,3) burn must still return None, a 510-iter slow converger must return
  exactly the naive-reference matrix.

## Result
- `pytest -q -p no:cacheprovider`: 123 -> 126 passed.
- Rebuilt `outputs/*.json`: md5-identical on all 5 classes.
- Audit: baseline book 0.912 (pace -0.04) -> final book **0.877**
  (pace -0.21). strain 1.02 / size 0.92 (instr 9301, longest 21, slots 1291)
  / rhythm 2.00 / off 0.0 / vol 0.0 / bad 0 / spread 0.17 all identical;
  per-class rows unchanged. Only pace moved.
- Verdict: hypothesis holds. Doomed burns abort at iter 400-600 instead of
  1000 with zero output change; the whole book-score delta is pace.
