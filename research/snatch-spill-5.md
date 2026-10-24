# Snatch-spill-5: Other Snatch peak spill, class I only (REVERTED)

Mechanical clone of `spill_peak_fundamental` (research/fund-spill-2) to
`spill_peak_snatch`, per the MS-precedent recipe: "Fundamental" ->
"Other Snatch" throughout, `if plan["class"] != "I": return plan` gate,
top_k=1 single pass, chained after the fund-spill call in `build_plan`,
wlconfig gap-guard verbatim, singles-host filter on both ends
(skip any session with `any("Other Snatch" in p for p in
session.get("pairs", {}))` as donor or recipient).

## Result: REVERTED (gate fail)

- exc 144.7 -> 144.7 (gate required strictly < 144.7). No movement.
- I rhythm 3.09 -> 3.09 (within [3.04, 3.14], OK).
- Scorer defects: zero (bad 0 all classes, gap-guard held).
- BUT one new test defect: `test_book_numbers_match_research` fails
  (book instr 9282 -> 9281; book score 0.830 -> 0.834/0.838).
  Gate requires zero new defects -> FAIL.
- Full suite with the change: 137 passed, 1 failed
  (138 collected incl. 2 new snatch-spill tests, both passing).

The single snatch spill fired (I instr 1899 -> 1898) but moved no
excess: the top Other Snatch peak slice sits where no lighter,
singles-free co-host exists in-week, or the gap-guard reverts.
Class I's extra singles-hosting sessions did not convert.

## Revert

Fully reverted: `src/wlgen.py` restored, `tests/test_snatch_spill_5.py`
removed. Tree clean; baseline confirmed after revert:
book strain 0.96 (exc 144.7), I rhythm 3.09, 136 green.

Note: book drift/score wobbles ±0.01 run-to-run (pace term) with the
tree clean; exc/instr/rhythm/defects are stable. Not related.
