# iclean-gate: ban ClPull+Other Clean IN CLASS I — KILLED (NO-GO)

Lead: exc-map cell #3 — I Other Clean, 10.6 excess in 17 sessions (0.63/sess).
Shot: support-level host control — gate the ClPull+Other Clean complex in
class I via `GATED_PAIRS_BY_CLASS` + `cls` threaded through
`cover_session`/`detect_pairs`/`pair_fit` (pair-free single hosting, amounts
untouched). Sibling gates I Other Snatch 70% in parallel (different cell).

## Result: NO-GO, reverted clean

- Gate implemented + TDD test (red confirmed, then green).
- Defect on first full run: class I **Comp 2 wk0 falls back SLS → MLM**
  (canonical-pattern test fails). The unpaired co-host blocks the BALLAST
  refit (`pair_fit` returns None under canonical sizes → `week_sessions`
  takes the next variant). Textbook idle/clash defect from the gate.
- Per lead instruction (kill fast on idle/clash defects), reverted
  `src/wlgen.py`, `src/wlconfig.py`, `tests/test_wlgen.py` to stack-1.
- Book-instruction count moved 9289 → 9287 under the gate (effect real,
  but shape-breaking). No audit kept (killed before scoring).

## Baseline (stack-1, this box, reverted = final)

- book ~0.86 (0.857), strain 0.99 (exc 147.8, short 0.0)
- per-class exc: I 45.0, MS 43.3, CMS 32.8, III 13.4, II 13.4
- tests: 129 green (`pytest -q -p no:cacheprovider`)

## Lesson

Pair bans are not free: the `pair_fit` refit assumes detected pairs snap
and freeze; an undesignated-but-hosted pairable member over-blocks BALLAST
singles in the slot refit. A future retry would need refit-aware unpairing
(treat gated co-hosts as slot-designated), not just detection-skipping.
