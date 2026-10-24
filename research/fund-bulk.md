# fund-bulk: spill the Fundamental 70% band (NOT APPLIED — budget)

Plan: copy `spill_peak_fundamental` (src/wlgen.py) to `spill_peak_bulk`
with one target change — donor = session with the largest Fundamental
dose at 70% (index 2 of [50,60,70,80,90,100,110]), move its whole 70-zone
dose to the same week's lightest co-host. Keep top_k=3 loop, distinct
donor weeks, gap-guard revert, vols track, bins recompute. Chain after
the fund spill in `build_plan`. Verified: no pair key contains
'Fundamental' (PAIRS grep empty, `any(... PAIR_SET)` False), so the
singles-host filter is unnecessary.

Baseline (research/stack-1): book 0.839, strain 0.96 (exc 144.7),
136 green.

Gate (keep iff exc < 144.7, zero new defects, 136 green) never evaluated:
5-minute budget expired during baseline/audit phase. No src/test change
made; tree left clean. Next session: add failing pin test, implement
`spill_peak_bulk`, chain in `build_plan`, update `_unspilled_plan`
helper to bypass both spills, audit + pytest, keep-or-revert per gate.
