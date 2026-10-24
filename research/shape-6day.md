# shape-6day: strain-neutral 6-day canonical try

## Hypothesis
Reordering day patterns to MSLMM/MSLSMM cut rhythm 2.00 -> 1.91 but the
trailing M doubled closing-week volume (strain regression). Trying the
strain-neutral variant: keep the trailing S, change ONLY the 6-day
canonical from SMSMSM to MSLSMS (same letters as MSLSMM, light close,
M open for a one-peak shape).

## Experiment (TDD: red test first, one-line change in VARIANTS[6])
- Baseline: book 0.926 (strain 1.02, size 0.92, rhythm 2.00), 123 green.
- With MSLSMS canonical: book 1.017 (strain 1.04, size 0.99, rhythm
  2.00, drift pace +0.35), 3 tests failed (sessions_cap,
  day_patterns_keep_canonical_first, book_numbers_match_research).

## Verdict: REJECTED, reverted clean
Rhythm flat at 2.00 while strain (1.02 -> 1.04), size (0.92 -> 0.99),
and pace (+0.03 -> +0.35) all regressed. The canonical pattern drives
dose feasibility, not just shape: day_split under MSLSMS re-plans
sessions into cap/slot violations elsewhere. Pattern order is load-
bearing for the planner; shape gains need a planner-aware route, not a
table reorder.

Tree reverted; 123 green; audit back at strain 1.02 / size 0.92 /
rhythm 2.00 (book 0.948 here, delta is pace machine wobble).
