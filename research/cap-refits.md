# CAP refits 200 -> 300: quality-vs-pace trade (REJECTED)

## Baseline (research/cap-refits, before change)

- `.venv/bin/wlgen audit`:
- book 0.878 (strain 1.02 = exc 153.4 + short 0.0, size 0.92,
  rhythm 2.00, drift -0.04 with off 0.0, vol 0.0, bad 0,
  spread 0.17, pace -0.21).
- `pytest -q -p no:cacheprovider`: 128 passed.

## Hypothesis

Raising `CAP_REFITS` in `pair_fit` (src/wlgen.py) from 200 to 300 lets
the week-mix snap/refit search try more variants: strain/size quality
may improve while pace charges the extra search. Keep only if the total
book score falls.

## Final (CAP_REFITS = 300, after change)

- book 0.883 (strain 1.02 = exc 153.4 + short 0.0, size 0.92,
  rhythm 2.00, drift -0.01 with off 0.0, vol 0.0, bad 0,
  spread 0.17, pace -0.18).
- `pytest -q -p no:cacheprovider`: 129 passed (128 + 1 pin test).

## Result: REJECTED, reverted clean

- book 0.878 -> 0.883 (+0.005, wrong direction).
- strain/size/rhythm rows identical (exc 153.4, same per-class rows):
  the extra 100 refits changed no plan, so there was no quality gain
  to offset the pace charge (pace -0.21 -> -0.18).
- src reverted to `CAP_REFITS = 200`; pin test kept as
  `test_pair_fit_keeps_refit_cap` (129 green at revert).

## Lesson

The week-mix search already saturates by 200 refits on this stack: more
variants find nothing better, and the audit prices the extra search via
pace. Same dead-knob family as the WLGEN_C / WLGEN_T companion probes.
Future quality work must change the search (or the support), not raise
its cap.
