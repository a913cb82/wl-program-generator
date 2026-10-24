# knob-scan: coordinate-descent over small generator knobs (5-min budget)

## Baseline (branch `research/knob-scan` @ `1a5d929`, this box)

- `wlgen audit` book row: strain 1.02 (exc 153.4, short 0.0) | size 0.92
  (instr 9292, longest 21, slots 1291) | rhythm 2.00 | drift 0.00
  (off 0.0 vol 0.0 bad 0 spread 0.17 pace -0.17) | **score 0.886**.
  (Stack-1 reference cites 0.897; difference is pace noise on this box.)
- `pytest -q -p no:cacheprovider`: **128 passed**.

## Protocol (per brief)

Single-knob nudges in `src/wlconfig.py` (SIZE_WEIGHT splits, BEAM widths,
CAP_EVALS/CAP_REFITS, DAY_C, tolerances); keep only if book delta < 0
AND all 128 tests green AND output deterministic. No touching
`src/wlscore.py` (weights/baselines/thresholds are the ruler).
Tier tolerances (TOL_CLASSIC/TOL_STRENGTH in `wlscore.py`) skipped per
brief: prior sweeps found them byte-identical across 9 combos — cited
from research notes, not re-proved here.

## Result: no knobs tried — budget expired before first nudge

The 5-minute budget was consumed by baseline establishment (one full
`wlgen audit` + one full `pytest` run + research-log triage). No
single-knob nudge was applied, so there are no deltas to report and no
`src/` changes to commit. Tree reverted clean (verified: `git status`
empty at wrap-up).

## Table of knobs tried

| Knob | Values planned | Book delta | Tests | Deterministic | Verdict |
|------|---------------|------------|-------|---------------|---------|
| (none — budget expired) | — | — | — | — | not attempted |

## Queued leads for the next sweep (untested, cheapest first)

1. `WLGEN_C=2` / `=4` (DAY_C via env, no code change; audit-only probe).
2. `WLGEN_T=4` / `=6` (DAY_T via env, same).
3. `BEAM 32->48` (wider beam; expect pace cost, possible size win).
4. `BEAM_JOINT 16->24` (fallback width; narrow blast radius).
5. `CAP_REFITS 200->300` in `wlgen.py` (note: lives outside `wlconfig.py`).
6. `MIN_DOSE 6->5/7`, `TOL 0.2->0.15/0.25` (likely break pinned tests; try last).
7. SIZE_WEIGHT splits (r2-shape already showed structural-test breakage; try last).
