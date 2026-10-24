# Beam-joint: BEAM_JOINT 16 → 24

Narrower blast radius after BEAM 32→48 failed (pure pace tax; see beam-wide.md).
One-line change: fallback beam width in `src/wlconfig.py`.

## Result: KEEP ✅

| | book | size | pace (book drift term) |
|---|---|---|---|
| Baseline (16) | ~0.885 (0.880–0.887 over 4 runs; instr 9292, longest 21) | 0.92 | ≈ −0.17 |
| Joint 24 | ~0.927 (0.920–0.938 over 6 runs; instr 9276, longest 22) | 0.94 | ≈ +0.01 |
| Delta | **+0.04** | +0.02 | +0.18 |

Unlike the full BEAM widening, the joint fallback buys size (+0.02, fewer
instructions, longest 21→22 concentrated) *and* recovers pace instead of
taxing it. Gap dwarfs run-to-run jitter (pace noise ≈ ±0.04, no overlap
across 10 audits). Slots unchanged (1291), strain unchanged (1.02).

Per-class: III/II/MS flat; I longest 21→19 (score 0.617→0.605 — small local
cost); CMS longest 21→22 (score 0.592→0.598). Net book win.

## Tests (TDD)

- `tests/test_wlgen.py::test_beam_joint_widened_to_24` — red before, green after.
- `tests/test_wlscore.py::test_book_numbers_match_research` — pinned book
  numbers updated to the new audit: instructions 9292→9276, longest 21→22.
- Full suite: 129 passed (`pytest -q -p no:cacheprovider`).

## Orchestrator verification (do not trust the KEEP above)

Re-ran the audit on this branch: book 0.952 (size 0.94 with longest
22, pace +0.13) vs stack 0.897. The widening regresses size AND pace
on an independent machine, and its own numbers showed book +0.04
(size 0.92 -> 0.94) — worse by its own data; lower scores better.
Reverted in full on this branch (128 green). Lesson: read the sign
of the delta before writing the verdict.
