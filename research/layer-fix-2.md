# layer-fix-2: gap helper moves to the shared module

## Breach
`spill_peak_fundamental` (src/wlgen.py) did `from wlscore import _unjustified_gaps`
— the generator core imported the scorer's private gap function. Week-relative
gaps, so no wlgen-local approximation can hold the guard; the import was
load-bearing and had to be moved, not removed.

## Fix (pure move, no re-tune)
- `src/wlconfig.py`: gained `_unjustified_gaps`, byte-identical logic (wlconfig
  already owns shared matching rules; no new dependency edges).
- `src/wlgen.py`: imports it from wlconfig at top level; deferred wlscore
  import deleted. Remaining `from wlscore import audit/score_json` lines are
  CLI dispatch (`main()`), not generator-core coupling.
- `src/wlscore.py`: private copy deleted; imports the shared copy instead
  (`wlscore._unjustified_gaps is wlconfig._unjustified_gaps`).
- `tests/test_layer_gap_shared.py`: 4 layering tests (shared home, scorer
  reuse, no scorer import in spill fn, semantics spot-check). TDD: failed
  4/4 before the move (red confirmed), pass after.

## Behavior
- Baseline (pre): book score ~0.84, strain 0.96 (exc 144.7), instr 9282,
  rhythm 2.09, 132 green.
- After: exc 144.7, instr 9282, rhythm 2.09 identical; 136/136 green.
- Note: drift/pace/score wobble run-to-run on the BASE commit too
  (e.g. 0.835 vs 0.933 consecutive runs) — pre-existing audit nondeterminism,
  unrelated to this move. Guarded metrics are to the digit.
- Verdict: PASS (pure move, layering restored, behavior held).
