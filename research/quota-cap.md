# quota-cap: week_quota per-group hosting-day divisor probe (6 -> 5, 7)

## Hypothesis
`week_quota` caps each group's hosted days at `targets[g] // MIN_DOSE`
(src/wlgen.py). Loosening (//5, more hosting days) or tightening (//7,
fewer) could improve spread/pace without touching amounts. Small blast
radius by construction: caps only gate hosting, amounts untouched.

## Experiment (audit-only nudges, one at a time, reverted after each)
- Baseline (this worktree): book 0.909
  (strain 1.02, size 0.92, rhythm 2.00, drift 0.12), 128 green.
  (Lead's stack-1 reference: 0.897; drift reflects stack changes since.)

| nudge | book | strain | size | rhythm | drift | verdict |
|-------|------|--------|------|--------|-------|---------|
| baseline (//6) | 0.909 | 1.02 | 0.92 | 2.00 | 0.12 | — |
| //5 (looser caps) | 0.903 | 1.02 | 0.92 | 2.00 | 0.09 | REJECT: -0.006, revert |
| //7 (tighter caps) | 0.890 | 1.02 | 0.92 | 2.00 | 0.02 | REJECT: -0.019, revert |

Class scores flat in both nudges (III/II 0.344, I 0.617, CMS 0.592,
MS 0.544); all movement is the book drift/pace term. Per-class rhythm
medians unchanged (1.55 / 3.09 / 2.10).

## Verdict: REJECTED both directions, reverted clean
Neither divisor moves strain/size/rhythm; both lower the book score via
the drift term (pace -0.05 -> -0.09 at //5, -0.15 at //7). The //6 cap
sits at the sweet spot: looser hosting spreads groups onto days the
prior then has to pull back from, tighter hosting starves the spread
the fit wants. No src change kept; `git diff` on src/ clean, 128 green
after revert.
