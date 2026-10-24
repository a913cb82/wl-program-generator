# snatch-spill-4 (research/snatch-spill-4) — singles-only retry, exc-neutral, REVERTED

Target: retry the Other Snatch spill with the exact singles-host filter and keep
iff exc < 144.7 with zero defects.

## Root cause (known)

The last clone moved an Other Snatch single onto sess2, which hosts Other Snatch
INSIDE pair ('SnPull', 'Other Snatch') -> illegal "scheme does not match the
cell". Paired sessions cannot receive singles.

## Pair-key shape (verified with one print before coding)

`session["pairs"]` keys are **tuples**, e.g. `('SnPull', 'Snatch')`,
`('Other Clean', 'Other Jerk')`. So the filter is membership-in-tuple:
`any("Other Snatch" in p for p in session.get("pairs", {}))`, applied to both
donor choice and recipient co-host choice.

## Baseline (this worktree, before changes)

- `.venv/bin/wlgen audit`: book **~0.84** (strain 0.96 [exc 144.7, short 0.0],
  size 0.92, rhythm 2.09, drift ~-0.2 [bad 0]).
- MS row: strain 0.28 (exc 42.5), rhythm **2.96**, drift 0.18 (bad 0).
- `pytest -q -p no:cacheprovider`: **136 green**.

## Implementation (reverted)

`spill_peak_snatch(plan, top_k=1)`, MS-only (`plan["class"] != "MS"` -> identity),
chained after the fund spill
(`build_plan` returns `spill_peak_snatch(spill_peak_fundamental(plan), top_k=1)`).
Verbatim clone of `spill_peak_fundamental` for group "Other Snatch" (same
top-slice key, same wlconfig `_unjustified_gaps` before/after revert), plus the
singles-host filter on both ends: skip donors and co-hosts where Other Snatch
appears in `pairs`.

TDD: 4 tests (non-MS identity, paired-cohost skip, paired-donor skip, singles
move succeeds) — red before (AttributeError), green after.

## Final book (filtered clone, before revert)

- book strain 0.96 (exc **144.7**, short 0.0), MS exc 42.5,
  MS rhythm **2.96** (in [2.91, 3.01]), MS drift 0.18 (bad 0).
- 140 green (136 + 4 new), zero defects.
- Exc-neutral: the filter correctly blocks the illegal paired move, but no
  exc-positive singles-only move exists, so exc never drops below 144.7.

## Verdict

**REVERTED src+tests fully** — zero defects and rhythm hold, but exc == 144.7
(not < 144.7). Baseline restored (136 green, book exc 144.7, MS rhythm 2.96,
bad 0). Nothing committed (tree clean at HEAD).
