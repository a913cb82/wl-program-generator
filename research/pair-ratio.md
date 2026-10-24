# Pair-ratio probe (research/pair-ratio)

Lead: RATIOS/SCHEDULES (allowed clean:jerk-style rep ratios per zone band) were never
probed. Pair schemes feed size (instructions) and strain (doubled doses) directly.
Baseline (stack-1 worktree): book **0.893** (strain 1.02 / size 0.92 / rhythm 2.00 /
drift 0.04). Lead cites 0.897; same worktree audits 0.893 — noise-level delta.

Bands (ratio_ok): heavy (>=90) = {1:1}; mid (80-89) = {1:1, 2:1, 1:2};
light (<80) = all 7 RATIOS. SCHEDULES = heavy x mid x light, monotonic widening.

Audit-only nudges, each reverted immediately after audit:

| Probe | Nudge | Book score | Terms (strain/size/drift) | Verdict |
|---|---|---|---|---|
| A | light drops 3:1/1:3 | 0.904 | 1.02 / 0.94 / 0.07 | worse — revert |
| B | light drops 3:1/1:3 + 3:2/2:3 | 1.985 | 1.23 / 0.93 / 5.05 (bad 1) | much worse — revert |
| C | heavy allows 2:1/1:2 | 0.905 | 1.02 / 0.92 / 0.10 | worse — revert |
| D | mid allows 3:2/2:3 | 12.911 | 1.01 / 0.92 / 60.15 (bad 12) | catastrophic — revert |
| E | mid forced to 1:1 only | 1.957 | 1.15 / 0.93 / 5.10 (bad 1) | much worse — revert |
| F | light drops 3:2/2:3, keeps 3:1/1:3 | 1.991 | 1.24 / 0.93 / 5.06 (bad 1) | much worse — revert |

Reads:
- Narrowing light (A/B/F) never pays: strain flat-to-up, and any cut past the
  3:1/1:3 pair strands bad cells (drift bad >= 1) — the snap has nowhere to go.
- Widening mid/heavy (C/D) never pays: extra freedom is unused (C: identical
  strain/size, drift up) or actively breaks cell match (D: 12 bad cells).
- Current ladder (1:1 / 2:1 / wide-only-light) looks Pareto-locally optimal:
  every single-band nudge in either direction holds or hurts.

Verdict: **no win — src unchanged** (audit-only, tree clean, 128 green).
Next if revisited: pair *frequency*/placement (which sessions host pairs), not
ratios — the ratio ladder itself is not the constraint.
