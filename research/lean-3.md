# lean-3: one fewer day per week for CLASS III — REJECTED, reverted clean

## Hypothesis
Inverse of the I+1-day result (exc −13.7 won but pace +0.82 killed the book):
for a LEAN class (III, exc 13.4) one FEWER day per week should win twice —
fewer sessions = less build CPU (pace gain) + fewer instructions (size gain) —
while the strain risk stays small (concentrating a 13.4-exc base).

## Change (reverted)
- `wlgen.week_start_days(vol, cls) = max(3, len(sessions(vol, cls)) - (1 if cls == "III" else 0))`,
  threaded at the `week_sessions` range start (same insertion point as the
  perclass-T line, `cls` already threaded). Templates path only (`DAY_RULE=templates` active).
- 3-day floor kept: `VARIANTS` has no 2-day patterns.
- TDD: `tests/test_lean3.py` (start-day pin, floor pin, plan-uses-fewer-sessions pin) — red before, green after.

## Audit (full book)
- Baseline: book 0.832, strain 0.95 (exc 142.5), pace −0.32.
- Final: book 0.889 (+0.057), strain 1.02 (exc 153.1, +10.6), pace −0.21 (+0.11 — worse, not better).
- III concentration spiked strain far beyond the "small base" thesis; pace regressed too.
- Tests: 138 passed + 3 failed (`test_day_patterns_keep_canonical_first`,
  `test_session_profiles_keep_a_ramp`, `test_book_numbers_match_research`) —
  pattern drift plus new structural fallout, not just number pins.

## Verdict
REJECTED — reverted fully (`src/wlgen.py` restored, `tests/test_lean3.py` deleted).
Post-revert: book 0.832 (exc 142.5), 138/138 green, tree clean.
Gate needed book < 0.830 AND exc ≤ 142.5 AND zero new defects AND 138 green — failed on all four.
Lesson: III weeks sit at the dose floor already — fewer days concentrates dose faster
than it saves instructions/CPU. Do not retry day-count cuts on lean classes.
