# Demand sweep: demand-driven day rule (WLGEN_RULE=demand)

## Baseline (worktree, before changes)

- `.venv/bin/wlgen audit`: book 0.915 (strain 1.02, size 0.92,
  rhythm 2.00, drift 0.15 incl. pace -0.03). Quality terms match the
  0.927 book quoted in the brief; the score gap is machine pace noise.
- `pytest -q -p no:cacheprovider`: 123 passed.
- Tree clean; no src edits were made in this sweep (env-only probes).

## Hypothesis (one shot)

The parked demand path (day count from Prilepin demand via `DAY_T`,
heavy/light rhythm via `DAY_C`/`DAY_SHAPE`) could beat fixed Soviet
day templates on strain without costing pace — iff tuning T/c/shape
finds a point with equal-or-better quality at equal CPU.

## Result: REJECTED, reverted clean (no src changes to revert)

| Config | Book | Strain / Size / Rhythm | Drift (pace) | Verdict |
|--------|------|------------------------|--------------|---------|
| template baseline | 0.915 | 1.02 / 0.92 / 2.00 | 0.15 (-0.03) | — |
| demand default (T=5, c=3, peak) | 1.55 | 0.83 / 0.93 / 2.00 | 3.7 (+3.5) | strain wins (-0.19), pace kills (+3.5) |
| demand T=8 | 4.46 | 1.69 / 0.97 / 1.92 | 16.5 (+11.3, bad 1 illegal set) | catastrophic |
| demand SHAPE=alt | 2.55 | 1.24 / 0.87 / 2.00 | 7.9 (+2.8, bad 1) | size wins, illegal set + pace kill |
| demand T=3 | — | (no book row; run produced no audit line) | — | infeasible-or-worse, not pursued |

Default demand strain 0.83 beats template 1.02, but it also adds
`short 1.4` under-floor work, regresses size 0.92 -> 0.93, and —
fatally — triples build CPU (MS 0.82s -> 2.73s single-process;
book pace -0.03 -> +3.5). Net score 0.915 -> ~1.55.

## Why it is slow (profile, MS, demand default)

- 35 `plan_sessions` calls for 20 weeks: `demand_days` picks n +-1
  vs the cap-driven template count, so ~15 variant retries burn full
  `fit_session`/IPF searches before falling through to a feasible n.
- Plus 240 uncached `week_bin_lifts` calls inside `week_demand`
  that the template path never pays.

## What would be needed (not attempted; budget out)

- Lower-bound the variant loop at `max(demand_days(...),
  len(sessions(vol)))` to skip doomed small-n retries, and memoize
  `week_demand` per (cls, mi, wi). That buys pace parity at best;
  the strain win (-0.08 book points) is too small to justify keeping
  a second day-rule path alive. Kill it fast per the pace guard —
  same death as the floor retry.
- Do NOT tune further along T (both directions worse) or shape=alt
  (emits an illegal set, `bad 1`).

## Final

- `pytest -q -p no:cacheprovider`: 123 passed (unchanged).
- No src/test changes. Tree clean except this note.
