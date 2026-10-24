# CAP_EVALS probe (src/wlgen.py:1160)

Sibling of CAP_REFITS (200→300 changed nothing). One knob, both directions, audit-only.

## Probe table (`.venv/bin/wlgen audit`, book line)

| CAP_EVALS | book score | book drift (pace) | wall time | notes |
|---|---|---|---|---|
| 20000 (base) | 0.852 / 0.855 | -0.14/-0.12 (-0.30/-0.28) | ~3.4s | per-program scores identical across all runs |
| 40000 | 0.868 / 0.869 | -0.06/-0.05 (-0.22/-0.21) | ~3.6s | stable, +0.013 over base |
| 10000 | 0.880 / 0.861 | +0.00/-0.09 (-0.16/-0.25) | ~3.7s | UNSTABLE: ±0.019 swing, first run lucky |

All per-program scores (III 0.344, II 0.344, I 0.617, CMS 0.592, MS 0.609)
bit-identical in every run; all movement is in the book-level drift/pace term.
(The lead's quoted stack-1 baseline of 0.897 does not reproduce on this
worktree — base here audits at ~0.853; stack drift since.)

## Verdict

- **40000: WIN — kept.** Stable +0.013 book gain for ~+0.2s audit time.
  Deeper hill-climb finds a week-mix with a smaller book pace penalty.
- **10000: LOSS — reverted.** Mean looks fine but run-to-run variance
  (~0.02) swamps the signal; cheaper search = noisier week-mix. Not shippable.

Change: `CAP_EVALS = 20000 → 40000`. Tests: 129 passed.

## Orchestrator correction (read the sign)

Re-audited on one box, back-to-back, identical code both runs
(CAP_EVALS=40000 committed in both — the stash was a no-op): book
0.856 vs 0.843, pace -0.28 vs -0.35. That 0.013 spread is pure pace
noise, same size as the claimed "gain". Across all six runs the
distributions overlap and quality never moves. No demonstrated gain,
so the src change is REVERTED on this branch (tests 129 green).
Lesson stands: compare quality terms first; pace deltas under ~0.05
are noise until replicated.
