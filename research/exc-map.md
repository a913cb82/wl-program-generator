# Exc-map: where the 147.8 lives (stack-1 baseline, research/exc-map)

Baseline (this box): book 0.851, strain 0.99 (exc 147.8, short 0.0).
Method: read-only scripts vs built plans (`build_plan` + `wlscore`
internals `_dose`/`_session_score`/`_tolerance` for reading only;
scorer untouched). Zone shares split each session-group excess
proportionally to `n/capacity(z)`.

## Per-class excess (sums to 147.8)

| Class | Exc | Share |
|-------|-----|-------|
| I | 45.0 | 30% |
| MS | 43.3 | 29% |
| CMS | 32.8 | 22% |
| III | 13.4 | 9% |
| II | 13.4 | 9% |

I+CMS+MS = 121.1 (82%). III/II are thin and spread; ignore.

## Per-group excess (book)

| Group | Exc | Share |
|-------|-----|-------|
| Other Clean | 37.5 | 25% |
| Other Snatch | 34.4 | 23% |
| Jerk | 26.2 | 18% |
| Clean | 12.5 | 8% |
| Other Jerk | 9.4 | 6% |
| Snatch | 6.6 | 4% |
| ClPull | 6.5 | 4% |
| Squat | 6.5 | 4% |
| Fundamental | 5.0 | 3% |
| SnPull | 3.2 | 2% |

Classic-family complexes (Other Clean / Other Snatch / Jerk / Clean)
= 110.6 (75%).

## Per-zone-band excess (proportional share)

| Zone | Exc | Share |
|------|-----|-------|
| 70% | 71.8 | 49% |
| 80% | 33.0 | 22% |
| 90% | 14.7 | 10% |
| 100% | 13.3 | 9% |
| 60% | 10.7 | 7% |
| 110% | 3.4 | 2% |
| 50% | 1.0 | 1% |

70% + 80% = 104.8 (71%). The excess is mid-zone volume, not peaks.

## Paired-doubling vs singles

- Paired-member sessions: 126.0 (85%) in 244 sessions.
- Single-host sessions: 21.8 (15%) in 66 sessions.
- Doubling-attributable (exc minus movements-only exc): 124.1 (84%).

Confirms strain-ease: the excess IS the frozen double-count.

## Top 5 cells (class x group)

| # | Cell | Exc | Sessions | Avg/sess |
|---|------|-----|----------|----------|
| 1 | MS Other Snatch | 13.7 | 15 | 0.91 |
| 2 | I Other Snatch | 11.8 | 10 | 1.18 |
| 3 | I Other Clean | 10.6 | 17 | 0.63 |
| 4 | CMS Other Snatch | 8.8 | 9 | 0.98 |
| 5 | I Jerk | 8.2 | 14 | 0.59 |

Top zone sub-cells: MS Other Snatch @70% = 9.0; I Other Snatch @70% = 7.3;
CMS Other Snatch @70% = 5.4. Top pair types: SnPull+Other Snatch in
MS (6.5) / I (6.4) / CMS (4.7), Clean+Jerk in I (5.7).

## Recommended next shot (ONE)

**Attack: I Other Snatch 70% pairs — 7.3 excess in 10 sessions
(11.8 total in cell, avg 1.18/sess, densest cell on the map).**

Hypothesis: force pair-free single hosting for Other Snatch 70%-zone
volume in class I (support-level host control: ban/gate the
SnPull+Other Snatch complex at 70% or spill it to an extra host
session), instead of amount-shaping inside the fixed support
(known zero-sum per strain-ease). Halving the double-count in just
these 10 sessions prices ~5-7 exc off the book — the highest
exc-per-session surface found.
