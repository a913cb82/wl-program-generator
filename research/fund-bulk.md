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

## fund-bulk attempt + revert (2026-10-24)

Stack realigned first: cherry-picked ms-timing (9dd8fe7) onto this branch
(f6ff790) — baseline is now book exc 142.5, 138 green, as instructed.

Implemented `spill_peak_bulk` per recipe (clone of
`spill_peak_fundamental`, donor = max Fundamental dose at 70%, whole
70-zone dose to same week's lightest co-host; top_k=3, distinct weeks,
gap-guard revert, vols track, bins recompute; chained after fund spill).
Pair-grep verification: no pair key contains 'Fundamental' (singles-only,
no filter needed). TDD: structural tests failed red (no `spill_peak_bulk`),
then implemented.

Result: total no-op — touched weeks [] for I, MS, CMS. Every whole-dose
move empties the donor's interior 70 zone while the week still covers it
(e.g. class I donor 13 lifts 70 -> gap 0 -> 1), so the wlconfig gap guard
reverts all candidates. The specified move is structurally unplayable:
unlike the fund top-slice (edge zone), emptying spanned 70 always opens a
donor gap. exc would hold 142.5, never < gate.

Verdict: REVERTED FULLY per gate. src/wlgen.py and tests/test_wlgen.py
restored byte-identical (git status clean vs f6ff790). Post-revert:
`wlgen audit` book exc 142.5, `pytest` 138 passed, zero defects.
Lesson: any future bulk/70 spill must leave the donor's 70 zone populated
(partial dose) or pair the move with a gap-filling companion — whole-dose
emptying of an interior zone cannot pass the guard.
