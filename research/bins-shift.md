# Bins-shift probe (research/bins-shift)

Baseline (stack-1): book score 0.855, strain 0.99 (exc 147.8, instr 9289, slots 1282).
Protocol: `.venv/bin/wlgen audit` + `pytest -q -p no:cacheprovider` (129). Scores via wlscore only.

Target: `BINS["MS"]["Snatch"] = [0.16, 0.63, 0.19, 0.02, 0.00]` (zones 60/70/80/90/100).
One-share ±0.01 nudges between the 70% and 80% bins, audit-only.

| Probe | MS Snatch bins | book score / strain (exc) | MS score / strain (exc) | pytest |
|---|---|---|---|---|
| baseline | [0.16, 0.63, 0.19, 0.02, 0.00] | 0.855 / 0.99 (147.8) | 0.609 / 0.29 (43.3) | 129 green |
| A: intensity up (70→80) | [0.16, 0.62, 0.20, 0.02, 0.00] | 0.859 / 0.99 (147.8) | 0.609 / 0.29 (43.2) | n/a (flat/worse, reverted) |
| B: intensity down (80→70) | [0.16, 0.64, 0.18, 0.02, 0.00] | 0.836–0.853 / 0.98 (146.7 stable) | 0.606 / 0.28 (42.1) | 128/129 — golden pin `test_book_numbers_match_research` (exc 147.8, instr 9289) red |
| C: down x2 | [0.16, 0.65, 0.17, 0.02, 0.00] | 0.855 / 0.98 (146.6) | 0.616 / 0.28 (42.1), drift off 2.0 | n/a (fence, reverted) |

Notes:
- Fence confirmed both directions: up regresses book (0.855→0.859); down-x2 collides
  (MS drift off-table 2.0, MS score 0.606→0.616, book back to 0.855). One-step optimum only.
- Probe B audit is nondeterministic in drift/pace: book score ranged 0.836–0.853 over 5 runs
  (baseline 0.847–0.855 over 2 runs) — score win within noise. Strain/excess deterministic
  and stable: exc 147.8→146.7, MS exc 43.3→42.1. Other classes bit-identical.
- Verdict: NO-WIN committed. Probe B is at best a marginal strain-only gain and breaks the
  golden book pin; per protocol (revert at first red test, src-only commits) src reverted clean.
  If the golden pin is ever rebased, B (MS Snatch 0.64/0.18) is the documented candidate.
