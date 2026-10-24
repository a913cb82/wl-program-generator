# Meso-split probe (research/meso-split)

MACRO meso-share table (prep/comp volume split, sums to 1.00):
Prep 4-2 0.20 / Prep 2-4 0.22 / Prep 3-1 0.25 / Comp 1 0.18 / Comp 2 0.15.

Baseline (stack-1, measured this session, `wlgen audit`): book
strain 1.02 / size 0.92 / rhythm 2.00, score ~0.886-0.894
(noise +/-0.004 across runs; lower score = better: 0.4*strain+0.3*size+0.1*rhythm+0.2*drift).

Protocol: one meso +/-0.02, others rescaled proportionally to sum 1.00,
audit-only, revert each nudge. Structural meso/weeks tests untouched.

| probe | nudge | book score | terms (strain/size/rhythm/drift) | verdict |
|---|---|---|---|---|
| P0 | Prep 4-2 +0.02 | 0.960 | 1.10/0.95/2.17/0.10 | revert (worse) |
| P1 | Prep 2-4 +0.02 | 0.976 | 1.04/0.95/2.14/0.31 | revert (worse) |
| P2 | Prep 3-1 +0.02 | 0.999 | 1.06/0.93/2.10/0.43 | revert (worse) |
| P3 | Comp 1 +0.02 | 0.961 | 1.10/0.97/2.11/0.10 | revert (worse) |
| P4 | Comp 2 +0.02 | 1.050 | 1.09/0.99/2.14/0.51 | revert (worse) |
| M0 | Prep 4-2 -0.02 | 2.211 | 1.25/0.96/2.00/6.12 (bad 1) | revert (much worse) |
| M3 | Comp 1 -0.02 | 1.099 | 1.14/0.96/1.96/0.80 | revert (worse) |

Verdict: NO WIN. Every +0.02 nudge raises strain/size and the score
(+0.07 to +0.16 over baseline, far outside noise); both -0.02 nudges are
worse still (M0 blows drift to 6.12 with a bad-dose flag). The stack-1
MACRO split sits at a local optimum for +/-0.02 single-meso moves.
No src change kept; tree reverted clean; pytest 128 green.
