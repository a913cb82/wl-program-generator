# Fold Thursday -> Wednesday: NO-GO (reverted)

## Shot
Post-pass `fold_thursday` at end of `build_plan` (same style as
`spill_peak_fundamental`): for each 4-session week shaped
`v1 > v2 > v0 >= v3` (middle two heaviest, last lightest — the
median-band `[45,133,89,44]`-type; 7 III + 7 II + 1 I + 3 CMS + 6 MS
weeks match), merge Thursday's whole dose into Wednesday (all groups,
vols track), drop the zeroed Thursday, recompute bins. One rule, all
classes. TDD: `tests/test_fold_thu.py` (move + totals + bins; skip
non-matching) passed 2/2 against the implementation.

## Result (`.venv/bin/wlgen audit`) — REVERTED
- book: exc 142.5 -> 137.6, strain 0.95 -> 0.92, rhythm 2.09 -> 2.00
  (gain 0.09), **drift -0.16 -> +119.78 (bad 0 -> 24)**,
  score 0.832 -> 24.8
- MS rhythm **worsened** 2.91 -> 3.78 (`[45,134,111,44]` ->
  `[45,134,155]`: hi/lo 3.44, amplitude 2.78)
- III/II rhythm 1.55 -> 1.52 only; I/CMS medians unchanged

## Kill mechanism
Exactly one new defect per folded week (7+7+1+3+6 = 24): `clash`
(III: 0 -> 7). Merging Thursday's groups into Wednesday builds a
day-mix with no matching slot (`slot_match(hosted)` fails), +~5 drift
per clash. The pricing note's 2.09 -> ~0.82 assumed the zero Thursday
merely drops out; the scorer instead counts a clash per folded week,
and MS weeks get a bigger endpoint peak, not a smaller one.

## Gate: NO-GO, reverted
- Kill line gates (exc 137.6 < 150; strain delta -0.03 < 2x0.09 gain)
  pass on paper, but drift explodes 120 points and score 30x —
  unwinnable trade, MS rhythm regresses.
- Tree restored byte-identical (`git checkout src/wlgen.py`, drop
  probe tests); audit back to exc 142.5 / score 0.832. No wlscore
  change. Lesson: day-removal moves must be slot-match-checked per
  week, not just vol-checked.
