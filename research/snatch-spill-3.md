# snatch-spill-3 (research/snatch-spill-3) — guarded clone, exc-neutral, REVERTED

Target: guard the verbatim Other Snatch spill clone (research/snatch-spill,
reverted: exc -0.3 but MS drift 0.18 -> 5.18, bad 0 -> 1) against its known
defect and keep iff exc < 144.7 with zero defects.

## Baseline (this worktree, before changes)

- `.venv/bin/wlgen audit`: book **0.84** (strain 0.96 [exc 144.7,
  short 0.0], size 0.92, rhythm 2.09, drift ~-0.2 [bad 0]).
- MS row: strain 0.28 (exc 42.5), rhythm **2.96**, drift 0.18
  (off 0.0 vol 0.0 bad 0 spread 0.18 pace +0.00).
- `pytest -q -p no:cacheprovider`: **136 green**.

## Discovery (one audit of the re-applied verbatim clone, top_k=1, MS-only)

- Drift detail line:
  `MS drift 5.18 (off 0.0 vol 0.0 bad 1 spread 0.18 pace +0.00)`.
- Raw breakdown: **illegal 1**, clash 0, gaps 0, idle 0, idle_meso 0.
- **Defect component: illegal.** The recipient (meso4/wk1/sess2) hosts
  Other Snatch inside pair `('SnPull', 'Other Snatch')`; the added slice
  breaks the paired slot scheme:
  `SnPull+Other Snatch: scheme does not match the cell`. The clone's
  cohost filter (`"Other Snatch" not in s.get("pairs", {})`) compared a
  group name against tuple keys, so it never excluded paired hosts —
  the recipe's SINGLES-only rule was silently void.

## Implementation (reverted)

`spill_peak_snatch(plan, top_k=1)`, MS-only, chained after the fund
spill, with two guards and nothing else:

1. MIN_DOSE guard (prescribed for illegal): revert any move raising
   `count_dose_violations([donor, recip])` (donor keeps < 6 reps).
2. Singles-only fix (the actual defect): skip donors/cohosts pairing
   Other Snatch, tested against pair-tuple membership.
3. Kept the fund-spill-2 gap-guard revert.

TDD: 4 tests (non-MS identity, stranded-donor skip, paired-cohost
skip, no new dose violations) — red before, green after.

## Final book (guarded clone, before revert)

- book strain 0.96 (exc **144.7**, short 0.0), MS exc 42.5,
  MS rhythm **2.96** (in [2.91, 3.01]), MS drift 0.18 (bad 0).
- 140 green (136 + 4 new), zero defects.
- The guarded pass moves exactly one exc-neutral rep (meso4/wk1/sess4
  -> sess1 @100); the peak-week full-slice move is correctly skipped
  (paired recipient / gap revert), so exc never drops below 144.7.

## Verdict

**REVERTED src+tests fully** — the guard holds zero defects and rhythm,
but cannot hold exc below 144.7 (144.7, exc-neutral). Baseline restored
(136 green, book exc 144.7, MS rhythm 2.96, bad 0).

Lesson: for Other Snatch the only peak-week cohosts pair the group, so
a singles-only spill has no exc-positive move; the -0.3 came entirely
from the illegal paired move. Next shot would need a pair-aware spill
(re-render the recipient's paired slot scheme), not a slice guard.
