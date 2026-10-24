# pair-next: non-gating levers on paired doubles (analysis only, no src change)

Baseline: book 0.851, strain 0.99 (exc 147.8, short 0.0). 124.1 (84%) is
doubling-attributable; 126.0 in 244 paired-member sessions. Top cells:
MS Other Snatch 13.7 (9.0 @70%), I Other Snatch 11.8 (7.3 @70%, 1.18/sess),
I Other Clean 10.6. Pair types: SnPull+Other Snatch (MS 6.5 / I 6.4 / CMS 4.7),
Clean+Jerk in I (5.7). Scorer frozen: `_dose` double-counts pairs,
exc = max(0, score - tol), tol classic 1.5 / strength 2.0.

## Ranked non-gating / non-support levers

| Rank | Lever | Exact cell moved | Expected exc delta | Likely killer fence |
|------|-------|------------------|--------------------|---------------------|
| 1 | Ratio schedules: force asymmetric light-tier ratio (or split legs across days) on SnPull+Other Snatch @70% | I Other Snatch @70% pairs (7.3 in 10 sess, 1.18/sess); MS Other Snatch @70% (9.0) second | ~-3 to -6 book (halving double-count in 10 sess ≈ 0.3-0.6/sess) | Pair-snap re-coupling (strain-ease #3: partner +3.2 Jerk/+4.0 Squat, paired sess 208→235); MIN_DOSE=6 collapses shrunken leg; ratio_ok legality (1:1 only ≥90%) |
| 2 | Demand-path shapes at template cost (WLGEN_RULE=demand, capped days/rhythm) | All paired @70%+80% (104.8, 71% of book) | ~-20 to -30 (strain-ease: 153→122) but pace +3.9..+4.7, 3.2× slower | Pace/CPU_BOOK=3.6 fence (known pace trap); rhythm/instr regressions eat it |
| 3 (dead) | Tolerance floor ONLY on doubled leg (+0.5 on paired-member score) | 244 paired-member sessions (126.0 exc) | Fake ~-40 to -60, book only | Frozen scorer: `_tolerance` is the independent ruler (fund-spill-3 lesson); generator-side shadow tol moves nothing on book |

## Recommended next shot (ONE)

Attack I Other Snatch @70% SnPull+Other Snatch pairs with a light-tier-only
schedule lock (e.g. forbid 1:1 below 80%, force pull-heavy 3:1/2:1 at 70%):
densest cell on the map, classic tol 1.5 is tightest, and ratio_ok is widest
below 80% so the move is legal by construction. Price: ~-3 to -5 exc if the
doubled leg halves without partner steepening. Watch the re-coupling fence:
measure Jerk/Squat partner delta and paired-session count alongside exc.
