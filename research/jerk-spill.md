# Jerk-spill: Jerk peak spill, class I only (REVERTED)

Mechanical clone of `spill_peak_fundamental` (research/fund-spill-2) to
`spill_peak_jerk`, per the recipe: "Fundamental" -> "Jerk" throughout,
`if plan["class"] != "I": return plan` gate, top_k=1 single pass, chained
after the fund-spill call in `build_plan`
(`spill_peak_jerk(spill_peak_fundamental(plan))`), wlconfig gap-guard
verbatim, singles-host filter on both ends (skip any session with
`any("Jerk" in p for p in session.get("pairs", {}))` as donor or
recipient). Pairs keys are tuples like `('Other Clean','Jerk')`, so
tuple-membership is exact-element: verified
`'Jerk' in ('Other Jerk',)` is False — the "Other Jerk" substring is
safe and never matched.

WHY: I Jerk singles total 90 lifts with peak sessions ~29 — the last
untested singles pool of size. Sibling spills went neutral 4 times; this
was the final probe of the family.

## Result: REVERTED (gate fail — clean no-op)

- exc 144.7 -> 144.7 (gate required strictly < 144.7). No movement.
- I rhythm 3.09 -> 3.09 (within [3.04, 3.14], OK).
- Scorer defects: zero (bad 0 all classes, gap-guard held).
- Zero new test defects: full suite with the change 138 passed
  (136 baseline + 2 new jerk-spill tests, both passing).
- The spill fired zero times: jerk-touched sessions 0 (fund-only vs
  fund+jerk diff on class I).

Cause (diagnosed, not guessed): of 23 class-I Jerk lifts at >=90, 13
are paired-hosted (filtered) and 10 singles-hosted across only 3
eligible donor sessions (m2w0s3: 4 lifts, m1w1s3: 3, m3w0s3: 3) — and
each of those weeks has zero eligible singles-hosted Jerk co-hosts, so
every candidate exhausts the cohost check and the top-1 loop terminates
empty. The gap-guard never even engaged.

## Revert

Fully reverted: `src/wlgen.py` restored, `tests/test_jerk_spill.py`
removed. Tree clean; baseline confirmed after revert:
book strain 0.96 (exc 144.7), I rhythm 3.09, 136 green.

Note: book drift/score wobbles ±0.01 run-to-run (pace term) with the
tree clean (0.831/0.839/0.840 observed); exc/instr/rhythm/defects are
stable. Not related.

Family verdict: 5/5 spill probes neutral (4 siblings + this). The
singles-pool spill family is exhausted — no further clones warranted.
