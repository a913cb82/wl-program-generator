# Demand-cheap: capped demand allocator (KILLED, reverted clean)

## Baseline (this worktree, stack-1)

- `.venv/bin/wlgen audit`: book **0.897** (strain 1.02, pace -0.11).
- `pytest -q -p no:cacheprovider`: 128 passed.

## Hypothesis

Demand rule (WLGEN_RULE=demand) won strain 1.02→0.83 but cost 3x CPU
(pace +3.5, net 1.55). A capped variant — same demand split, bounded
search — could keep the strain win at neutral pace.

## Attempts (both under WLGEN_RULE=demand, TDD test-first, then reverted)

1. **Floor variants at cap-driven count**: `demand_variants()` helper,
   `start = max(demand_days(...), len(sessions(vol)))`. Kills doomed
   small-n retries (demand_split squeezes vols through cap(), so they
   burn a full fit instead of continuing cheap).
   → book 1.159 (strain 0.73, pace +1.70). Pace halved, still red.
2. **Single-shot demand + template fallback**: first demand n only, then
   canonical template pattern per n (per-variant `isinstance(str)`
   dispatch for day_split vs demand_split).
   → book 0.940 (strain 0.79, size 0.94, short 1.1, pace +0.47).

## Why it dies

- Pace never reaches neutral (+3.5 → +1.7 → +0.47 vs -0.11 baseline).
  Residual cost is failed fits at feasible n plus inherent per-group
  `week_bin_lifts` work (inner is already @cache'd; targets vary weekly,
  so memoizing `week_demand` buys nothing — verified by inspection).
- Strain win always ships with regressions: size 0.92→0.94 and
  `short ~1` under-floor work in both attempts.
- Net book never beats template (0.940 vs 0.897). Two attempts, pace
  still red, no path to neutral without rebuilding the fit itself.

## Verdict: NEGATIVE, reverted clean

No src/test changes kept. Default audit after revert: book 0.897
(strain 1.02, pace -0.11); pytest 128 passed. Do not retune T/C/shape
here — sweep already showed both T directions worse and shape=alt emits
an illegal set.
