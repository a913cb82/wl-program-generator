# free-day1: quota anchor for the Clean/Jerk slot — REVERTED

Lead: spread is 100% meso; worst swings are Clean/Jerk groups with no quota
anchor because DAY[1] is excluded from FREE_SLOTS. One shot: add DAY[1] to
FREE_SLOTS, TDD via week_quota covering Clean/Jerk.

Note: research/spread-trim.md (cited diagnosis) does not exist in this tree;
worked from the brief directly.

## Change tried (reverted)

- `src/wlconfig.py`: `FREE_SLOTS = (DAY[0], DAY[2], DAY[3], DAY[4])` →
  `(DAY[0], DAY[1], DAY[2], DAY[3], DAY[4])`, comment updated.
- TDD: added `test_week_quota_covers_clean_jerk` — failed red with KeyError
  before the fix (quota skipped DAY[1]), green after; reverted with the src
  change per protocol.

## Result (revert condition hit)

Baseline audit: book 0.890 (strain 1.02, size 0.92, rhythm 2.00,
drift 0.02 incl. spread 0.17, bad 0). pytest 128 green.

With DAY[1] anchored: book **4.809** (drift 19.74, bad 4, spread 0.16 —
flat), 7 test failures:

- `test_shipped_scores_clean`: gaps defect (class I gaps=1; MS bad 2)
- `test_spread_avoids_back_to_back_sessions`: boundary carryover 12 > 10
- `test_day_patterns_keep_canonical_first`, two session-profile tests,
  `test_book_numbers_match_research` — all regressed.

## Verdict: REVERTED, anchor exists for a reason

Forcing Clean/Jerk onto quota days fights the pair rule that shapes the
joint hosts: sessions collapse into gapped/clashing layouts instead of
spreading. Spread never moved (0.17 → 0.16); all damage is quality/defect
terms. Tree reverted clean; no follow-up on this axis.
