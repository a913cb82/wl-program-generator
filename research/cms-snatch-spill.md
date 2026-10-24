# research/cms-snatch-spill — REVERTED (no-op under gap-guard)

Mechanical clone of `spill_peak_fundamental` (research/fund-spill-2) to
`spill_peak_snatch` per recipe: "Fundamental" -> "Other Snatch", CMS-only
guard (`plan["class"] != "CMS"`), top_k=1 single pass, chained after the
fund-spill call in `build_plan`, wlconfig gap-guard verbatim, singles-host
filter on BOTH ends (`any("Other Snatch" in p for p in
session.get("pairs", {}))` skips donor candidates and co-host recipients).

TDD: `tests/test_snatch_spill.py` (CMS-only identity on MS plan + CMS
smoke) — red before, green after implementation.

## Result

| | book | exc | CMS rhythm | defects |
|---|---|---|---|---|
| baseline | 0.84 | 144.7 | 3.00 | 136 green |
| with spill | 0.83–0.84 | 144.7 | 3.00 | 138 green (136 + 2 new) |

exc 144.7 NOT < 144.7 → gate FAIL (strict improvement required).
CMS exc/rhythm/instr byte-identical (31.5 / 3.00 / 1829): the single
candidate move was either gap-guarded away or no eligible unpaired donor
existed — spill is a no-op on current plans.

## Verdict

REVERTED FULLY. `src/wlgen.py` restored, `tests/test_snatch_spill.py`
removed. Post-revert audit confirms baseline (exc 144.7, CMS 3.00,
136 green). No commit to src/tests; this note is the only artifact.
