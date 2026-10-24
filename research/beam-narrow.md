# Beam narrow (research/beam-narrow) — REJECTED, null result

## Baseline (this worktree, before changes)

- `.venv/bin/wlgen audit`: book score **0.881**
  (strain 1.02, size 0.92 [instr 9292, longest 21, slots 1291],
  rhythm 2.00, drift -0.02 [off 0.0, vol 0.0, bad 0, spread 0.17, pace -0.19]).
- Per-class rows: III/II score 0.344 (pace +0.00), I 0.617 (+0.00),
  CMS 0.592 (+0.00), MS 0.544 (+0.00). All pace cost sits in the book row.
- `pytest -q -p no:cacheprovider`: **128 passed**.
- Note: prior notes quote 0.944 (beam-trim.md) and 0.897/-0.11 (task brief);
  neither reproduces on this worktree — 0.881 / -0.19 is the measured baseline.

## Hypothesis (tested, FAILED)

Narrow the session-order beams (`BEAM 32→16`, `BEAM_JOINT 16→8` in
`src/wlconfig.py`), accepting only byte-identical `outputs/*.json`.

## Method

TDD: added `test_narrow_session_order_beams` asserting the halved widths
(red), applied the config change (green), then ran a full `.venv/bin/wlgen`
and diffed `outputs/*.json` narrowed-vs-baseline (both freshly generated).

## Result — REJECTED

All five class JSONs differ between narrowed and baseline beams
(`CMS I II III MS.json` all differ), so the beams are load-bearing:
halving them changes session orders and the gate fails. Change reverted;
no quality comparison needed once identity fails.

Side observation (uninvestigated): regenerating `outputs/` from unmodified
baseline code also differs from the committed `outputs/*.json` for
I/II/III/MS (CMS identical) — committed outputs look stale relative to
stack-1 code, or generation is nondeterministic across runs. Worth one
check before trusting `git diff outputs/` as an oracle: run `wlgen` twice
on identical code and diff.

## Follow-ups (untested)

Cheaper shots from beam-trim.md, still open: `FINISH_SCAN 2→1`, or dedupe
beam states on `(caps, last_zone, last_value, seen, run_len, cur_count)`
keeping the cheapest prefix. Fix/settle the outputs oracle first.

## Verdict

No src/tests change kept (null result — nothing to gate on wlscore).
Baseline stands: book 0.881, pace -0.19, 128 green.
