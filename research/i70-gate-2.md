# i70-gate-2: ban SnPull+Other Snatch in class I, refit-aware — KILLED (NO-GO)

Lead (from research/i70-gate): densest excess cell I / Other Snatch / 70%
pairs, 7.3 exc in 10 sessions. Gate: ban the SnPull+Other Snatch complex in
class I (pair-free single hosting, amounts untouched).

## Attempt (reverted clean)

- `wlconfig.GATED_PAIRS_BY_CLASS = {"I": (frozenset(("SnPull","Other Snatch")),)}`
- `cover_session(hosted, banned=())` skips banned pair edges;
  `detect_pairs(..., banned=())` passes through;
  `pair_fit` looks up the ban by `cls`.
- Refit-aware (iclean-gate lesson applied): gated co-hosts treated as
  slot-designated in the refit — they block only their shared complex slot
  (slot 0), not both single slots (slots 0+2) — via `gated_occ` merged into
  the BALLAST blocking computation.
- TDD test (red confirmed: `GATED_PAIRS_BY_CLASS` ImportError, then green).

## Result: NO-GO, reverted clean

- Same failure mode as the sibling cell (research/iclean-gate): class I
  **Comp 2 wk0 falls back SLS → MLM** (`test_day_patterns_keep_canonical_first`:
  `assert 'MLM' == 'SLS'`), plus a `test_session_profiles_keep_a_ramp`
  warmup-block defect. The refit-aware unpairing was not sufficient — the
  gated sessions' unsnapped volumes still break the canonical-size refit.
- Per lead instruction (kill fast on idle/clash defects), reverted
  `src/wlconfig.py`, `src/wlgen.py`, `tests/test_wlgen.py` to stack-1.
- 129 tests green after revert.

## Baseline = final (stack-1, this box)

- book 0.853, strain 0.99 (exc 147.8, short 0.0)
- per-class exc: I 45.0, MS 43.3, CMS 32.8, III 13.4, II 13.4
- tests: 129 green (`pytest -q -p no:cacheprovider`)

## Lesson

Pair bans are not free even when refit-aware: skipping detection leaves
gated co-hosts at as-fit (frozen, unsnapped) volumes, and the snap
hill-climb + slot refit still strands under canonical sizes. Both sibling
gates (iclean, i70) now die the identical SLS→MLM death in class I Comp 2
wk0 — the week is brittle to any pairing change. Future work should price
the 70% doubling at the scorer/zone level, not at hosting.

## Verdict

NO-GO. Lead spent; do not retry hosting-level pair bans in class I.
