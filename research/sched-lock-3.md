# sched-lock-3: Class-I-only 1:1 light lock on SnPull+Other Snatch — REVERTED

## Hypothesis
The global 1:1-light lock won exc −13.9 but broke MS shape (reverted).
Scoping it to CLASS I ONLY + the SnPull/Other-Snatch pair family might keep
the win without the MS damage.

## Discovery
- `PAIR_REF[("SnPull", "Other Snatch")] == "Other Snatch"` (`src/wlconfig.py:272`).
- `_pair_options_keyed(c, h, binkey, gap, fan, mi, wi, ref)` had no `cls`;
  caller `pair_options(c, h, cls, mi, wi, ref)` drops `cls` via `_canon(cls)`.

## Change (tried, then fully reverted)
- Threaded `cls` into `_pair_options_keyed` (cache key extended).
- In the `for rh, rm, rl in SCHEDULES` loop:
  `if cls == "I" and ref == "Other Snatch" and rl == (1, 1): continue`.
- TDD: `tests/test_sched_lock3.py` — red before (Class I Other-Snatch
  options contained `rl == (1,1)`), green after; control cases (MS keeps
  1:1, Class I + Clean ref keeps 1:1) green throughout. Removed on revert.

## Result (gate: keep iff exc < 144.7, zero new defects, 136 green)
- Baseline: book 0.838, strain 0.96 (exc 144.7), 136 green.
- With lock: book 0.834, strain 0.96 (exc **144.7** — unchanged), per-class
  exc identical (III 13.4 / II 13.4 / I 44.0 / CMS 31.5 / MS 42.5),
  short 0.0, bad 0. Target cell (I) exc 44.0, no partner movement.
- exc did not fall below 144.7 → **REVERTED FULLY**. Tree clean, 136 green.

## Note
Book drift/pace/score jitters ±0.003 between identical-code runs
(0.838 → 0.832 on reverted code); per-class exc is rock-stable. Gate on exc.

## Lesson
Class I SnPull+Other-Snatch sessions never (or only irrelevantly) take the
1:1-light schedule — the scoped skip is a no-op. The −13.9 global win came
from elsewhere; do not retry ratio locks on this pair family.
