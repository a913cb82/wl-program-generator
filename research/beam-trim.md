# Beam trim (research/beam-trim) — null result on time budget

## Baseline (this worktree, before changes)

- `.venv/bin/wlgen audit`: book score **0.944**
  (strain 1.02, size 0.92 [instr 9301, longest 21, slots 1291],
  rhythm 2.00, drift 0.29 [off 0.0, vol 0.0, bad 0, spread 0.17, pace +0.12]).
- Per-class rows: III/II score 0.344 (pace +0.00), I 0.617 (+0.00),
  CMS 0.592 (+0.00), MS 0.544 (+0.00). All pace cost sits in the book row.
- `pytest -q -p no:cacheprovider`: **123 passed**.
- Tree clean, no src/tests changes (null result — nothing to gate on wlscore).

## Hypothesis (untested — budget expired before the experiment)

Narrow the session-order beams (`BEAM 32→16`, `BEAM_JOINT 16→8` in
`src/wlconfig.py`) and accept only byte-identical `outputs/*.json`.
Rationale: `fixed_beam` (preferred-fill path, the common case) fans out up to
32 survivors per depth step, and the joint `beam_search` fallback keeps 16;
both then rescore `FINISH_SCAN=2` survivors under the true cost
(`scheme_cost` + `compact_text`, the expensive phrase-parse). If the beams are
wider than needed, halving them cuts expansion ~2x with identical winners.
Cheaper follow-ups if narrowing is not identity-safe: `FINISH_SCAN 2→1`,
or dedupe beam states on `(caps, last_zone, last_value, seen, run_len,
cur_count)` keeping the cheapest prefix.

## Verdict

No change attempted within budget; baseline stands (book 0.944, 123 green).
The beam-narrowing hypothesis above is the recommended next 5-minute shot,
with the existing byte-identity oracle (`test_write_outputs` + rebuild diff)
as the acceptance gate.
