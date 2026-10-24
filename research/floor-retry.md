# Floor-retry: per-session dose floor (bounded probe, killed)

Hypothesis: reintroduce a small per-session dose floor (`MIN_DOSE` in
`wlconfig.py`, then 6 lifts) and watch strain vs pace in the audit.
Pace prices the fit cost, so the score decides. Kill fast if pace blows up.

Baseline (this box, branch research/floor-retry): book ~0.91-0.93,
strain 1.02 (exc 153.4, short 0.0), pace ~0.0 (+/-0.1 run noise).
123 tests green.

## Probes (MIN_DOSE only, DAY template untouched)

| floor | book | strain (exc/short) | pace | verdict |
|------:|-----:|-------------------:|-----:|---------|
| 8 | 34.36 | 1.12 (167.8/0.8) | +166.77 | DEAD: fit explodes (~13x CPU), the old 15x trap reprised |
| 4 | 1.92 | 1.12 (165.6/2.0) | -0.19 | DEAD: shortfall appears, plus a defect (bad=1) |
| 5 | 0.90 | 1.08 (162.3/0.2) | ~-0.2 | DEAD (see below) |

## Why floor 5 was killed despite scoring 0.90

- The strain hypothesis is falsified in every direction: strain never
  improves (1.02 -> 1.08/1.12/1.12). Loosening the floor spreads dust
  into sub-tolerance sessions (shortfall 0.0 -> 0.2-2.0); tightening it
  concentrates peaks (exc up) and explodes fit cost.
- Floor 5's net gain (~-0.02) comes from pace (-0.2, within/measurable
  but noisy) and rhythm discreteness (1.92), while strain worsens
  (+0.06). Pace re-runs show +/-0.1 noise on this box, so half the
  "gain" is timing luck.
- Floor 5 breaks three quality guardrails: MS back-to-back sessions
  152 vs the 130 cap, a warmup-ramp violation (2 < 3 in a marginal
  zone), and the canonical-variant exception map. Rebasing guardrails
  to bless a pace-driven +0.02 while strain worsens is score-hacking,
  not training improvement.

## Lesson

The floor knob is fully fenced: up explodes pace, down strands dust
and degrades spread/ramp. Support-shaping (which sessions host which
groups), not amount floors, remains the only open direction per
strain-ease round 1. Tree left clean: src and tests at baseline,
123 green, book strain 1.02.

## Result

No improvement. Killed fast per protocol.
