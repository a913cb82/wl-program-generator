# lean-2: II-only minus-one-day-per-week — NO-GO (reverted)

## Change (reverted)
- `week_sessions` else-branch range start: `max(3, len(sessions(vol, cls)) - (1 if cls == "II" else 0))`
  (same insertion point as the perclass-T line; `cls` already threaded).
- TDD test `test_lean_two_uses_fewer_days` (II weeks <= III weeks each, ≥1 strictly
  fewer, cap respected) failed pre-change, passed post-change. Both reverted per gate.

## Audit (full book)
- Baseline: book 0.823–0.833 (timing noise in pace), strain 0.95 (exc 142.5).
- Final: book 0.889 (+0.06), strain 1.02 (exc 153.1, +10.6).
- II: strain 0.09→0.16 (exc 13.4→23.9), instr 1764→1620 (size win, as predicted),
  rhythm 1.55→3.43 (blowup), score 0.344→0.580. Pace gain never materialized at
  book level; concentrating the (small) 13.4 exc base into fewer days spiked
  per-day dose → strain + rhythm wrecked the book.
- Zero new defects, but book-gated: FAIL (book 0.889 > 0.830, exc 153.1 > 142.5).

## Verdict
NO-GO — fully reverted (`git checkout -- src/wlgen.py tests/test_wlgen.py`).
138/138 green on restored baseline. Lesson: for LEAN classes the day count is
load-bearing for strain/rhythm; day-count cuts concentrate dose faster than they
save size. Do not retry day-count cuts on II; class-III sibling probe is independent.
