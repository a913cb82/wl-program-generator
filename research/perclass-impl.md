# perclass-impl: MS-only M+0.5 day-split weights — GO

## Change
- `wlconfig.SIZE_WEIGHT_MS = {S:1, M:2.5, L:3}`; `day_split(vol, pattern, cls=None)`
  and `sessions(vol, cls=None)` thread `cls` through; `week_sessions` passes its
  `cls` to both. Non-MS classes use the shared table bit-for-bit (new test pins
  `sessions(300, cls) == sessions(300)` for III/II/I/CMS).
- M<L stays strict (2.5<3): variant table order and canonical preference untouched.
- 9 MS weeks leave canonical sizes (dose floor under new splits); exceptions updated
  in `test_day_patterns_keep_canonical_first`. No other class changed pattern.

## Audit (full book)
- Baseline: book 0.905, strain 1.02 (exc 153.4, short 0.0), pace −0.08.
- Final: book 0.848 (−0.057), strain 0.99 (exc 147.8, short 0.0), pace −0.32.
- MS: strain 0.33→0.29 (exc 48.9→43.3), instr 2033→2030; rhythm 2.10→3.00
  (accepted tradeoff — book wins via strain + pace, as predicted).
- Zero structural defects (illegal/clash/gaps/idle/ob_micro/iv_micro all 0).
- Tests: 129/129 green (128 existing + `test_day_split_ms_half_step`).

## Verdict
GO — harvest. I/CMS nudges stay dead; do not generalize the half-step.
