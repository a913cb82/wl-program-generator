# sched-lock (I SnPull+Other Snatch light-tier ratio lock) — NOT LANDED (budget)

Lead: densest excess cell I Other Snatch @70% pairs, ~7.3 exc / 10 sessions.
Planned move: forbid 1:1 SnPull:Snatch ratio below 80% for CLASS I ONLY,
SnPull+Other Snatch pair only (force pull-heavy 2:1/3:1 at 70%).

Status: 5-min budget expired during recon/baseline. No src/tests change.
Reverted outputs/ noise; tree clean apart from this note.

Baseline (book): score ~0.84, strain 0.96 (exc 144.7), 132 green (pytest).
Target-cell/partner/pair-count fence not measured — needs next session.
Fence on revert: partner-group exc rise > half target-cell fall, or paired
sessions grow → revert.

Next: TDD test on SCHEDULES/allowed_ratios scoping (I-only, pair-only,
light-tier-only), then audit target vs partner cells before/after.

## II trial (global 1:1-forbid below 80%) — REVERTED
Edit: `ratio_ok`: `if p == q == 1: return True` → `return zlo >= 80`
(applied to EVERY pair, all classes — broader than the I-only plan in §I).
Result: book exc 144.7 → 130.8 (strain 0.96 → 0.87, score 0.84 → 1.84).
REVERTED: drift `bad` 0 → 1 (MS + book; illegal/clash/gaps/idle composite —
new defect) and pytest 124 passed / 8 failed (< 132 green).
Failures: test_beam_cj_ratios_legal, test_day_patterns_keep_canonical_first,
test_session_profiles_keep_a_ramp, test_session_profiles_are_contiguous,
test_fund_spill_moves_peak_top_slice_to_lightest_cohost,
test_fund_spill_adds_no_unjustified_gaps, test_shipped_scores_clean,
test_book_numbers_match_research.
Re-coupling fence: paired-session count (sessions with `pairs` non-empty,
all classes) 208 → 201 (MS 65 → 58, total sessions 89 → 87); per-group
SnPull prilepin excess via session_dose ≈ 0.0 both sides (metric too coarse —
partner excess lives in the joint session score, not the partner bins).
Lesson: the exc win concentrates in MS but breaks MS schedule shape
(canonical day patterns + session-profile contiguity) and trips the drift
defect; global scope too blunt. Next: I-only + SnPull/Other-Snatch-only
scoping per §I plan, with paired-session count as the revert fence.
Tree reverted (`git checkout -- src outputs`); no src commit.
