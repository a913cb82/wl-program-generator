# Beam-wide: BEAM 32 -> 48 (reverted)

Lead: beams are load-bearing; narrowing was tried separately. This spike tried
the other direction: widen the session-order beam from 32 to 48 in
`src/wlconfig.py`, hoping a wider search finds shorter schemes (size term pays
back more than the pace term charges for the extra CPU).

## Result: REVERTED — book rose

| | book | size | pace (in drift) | instr |
|---|---|---|---|---|
| baseline (BEAM 32) | 0.880 | 0.92 | -0.20 (drift -0.03) | 9292 |
| BEAM 48 | 0.890 | 0.92 | -0.15 (drift +0.02) | 9287 |

- Size: flat (instr 9292 -> 9287, -5 instructions; size term unchanged at 0.92).
  The wider beam found no meaningfully shorter orderings.
- Pace: worse (-0.20 -> -0.15). The extra search CPU was charged with no payback.
- Net: book 0.880 -> 0.890 (+0.010). Change reverted; `src/wlconfig.py` back at
  BEAM 32.
- `tests/test_wlscore.py::test_book_numbers_match_research` failed under BEAM 48
  (pins baseline instr count) and passes again after revert; 128 green.

## Verdict

Widening the beam to 48 is a pure pace tax with no size payback on the book —
beam width 32 already exhausts the ordering gains. Keep 32; do not widen.
