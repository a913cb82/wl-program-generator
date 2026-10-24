# finish-scan: FINISH_SCAN 2→1 probe (REJECTED)

## Question
Beam-trim showed BEAM narrowing is load-bearing. Is FINISH_SCAN=2 (survivors
rescored under the true cost) needed, or does FINISH_SCAN=1 give identical
output for less CPU?

## Method
`.venv/bin/wlgen audit` + `pytest -q -p no:cacheprovider` before/after;
`wlgen build` + `git diff outputs/` byte-identity check; wlscore audit numbers only.

## Baseline (measured, FINISH_SCAN=2, 128 green)
- book **0.931**, pace **+0.06** (strain 1.02 / size 0.92 / rhythm 2.00 / drift 0.23)
- NOTE: lead brief said baseline book 0.897 / pace −0.11 — not what this
  worktree measures. The FINISH_SCAN=1 result below (0.898/−0.11) matches the
  brief's "baseline" almost exactly; flagging in case numbers got crossed.

## Result FINISH_SCAN=1 (REJECTED)
- NOT byte-identical: all 10 outputs/* files changed.
- book **0.931 → 0.898** (strain/size/rhythm unchanged; drift 0.23→0.06 but
  score down). Per-scheme scores identical (0.344/0.344/0.617/0.592/0.544);
  loss comes from book-level instr growth 9292→9313.
- 2 test failures: `test_beam_prefers_separated_rep_change`,
  `test_book_numbers_match_research` (pins 9292, got 9313).
- Verdict: keep FINISH_SCAN=2. Reverted; tree clean, 128 green.

## Side observation
Fresh `wlgen build` with identical src is NOT byte-stable vs committed
outputs (ordering-only diffs, e.g. I.json byte ~23246 `[60,4],[60,4],[70,3]…`
vs `[60,4],[70,3],[80,3],[60,4]…`; audit numbers identical, tests green).
Likely set-iteration nondeterminism across runs. Byte-identity checks on
outputs/ should therefore compare two fresh builds, not build-vs-HEAD.
Committed outputs restored via `git checkout -- outputs/`.
