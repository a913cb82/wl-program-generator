# Spread trim (research/spread-trim) — null result on time budget

## Baseline (this worktree, before changes)

- `.venv/bin/wlgen audit`: book score **0.896**
  (strain 1.02, size 0.92 [instr 9292, longest 21, slots 1291],
  rhythm 2.00, drift 0.06 [off 0.0, vol 0.0, bad 0, spread 0.17, pace -0.12]).
- `pytest -q -p no:cacheprovider`: **128 passed**.
- Tree clean, no src/tests changes (null result).

## Diagnosis (measured, untested fix)

- Spread is 100% meso (weekly-share unevenness 0.1745); micro (day-gap) is
  exactly 0.0 (num 0.0 / den 433). The quota placer already spaces days
  evenly; the fit never breaks within-week evenness.
- Worst meso swings (MS): SnPull 2/6→6/6, Other Clean 2/4→5/6,
  Other Jerk 1/6→5/6. The Clean/Jerk slot (DAY[1]) is excluded from
  FREE_SLOTS, so CJ groups host purely fit-driven with no quota anchor.
- Structural floor: single-host groups (Clean, Jerk: 1 day every week)
  score share 1/n, and n varies 3↔6 with week volume, so ~0.08–0.17 of
  meso range per such group is unfixable from hosting alone (day counts
  are rhythm territory).
- Rejected without trial: hardening EPS (0.01→0.001) — EPS only orders
  options in `resolve_slots`; anything legal stays legal, so magnitude
  barely changes outcomes. The wander comes from exact-margin feasibility
  + MIN_DOSE strand repair overriding quota order, not from weak weights.

## Hypothesis for next shot (untested)

Add DAY[1] to FREE_SLOTS so Clean/Jerk groups get quota days + soft prior.
Same feasible set (all weights stay >0), so no crash risk; quota still
guarantees ≥1 day (idle guardrail intact). Risk: quota's distinct-day
preference discourages Clean+Jerk same-day pairing → watch size/strain.
TDD: `week_quota` covers Clean/Jerk (red today), then audit must show
meso spread down with strain/size/rhythm/pace flat for a net win
(spread weight 0.2 → full 0.17 kill is only -0.034 book).

## Verdict

No change attempted within budget; baseline stands (book 0.896, 128 green).
