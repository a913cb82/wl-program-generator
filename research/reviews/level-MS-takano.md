# MS adversarial review: OURS vs TAKANO (MS), MSIC as top-end context

Scope: `outputs/MS.json` vs `tests/fixtures/takano-MS.json` (+`takano-MSIC.json`).
Unit = program-week (meso,week): OURS 20 wks / 101 sess; TAKANO-MS 17 wks / 83 sess; MSIC 17 wks / 95 sess.
Pair slots `A+B @pct [ra,rb]` split ra→A, rb→B. Reps are the comparator; sets in parentheses.

## Severity-ranked findings (worst first)

1. **Missing groups: zero Press, zero Other-Squat.** Takano-MS has Press 700 reps (10.0%) and Other-Squat 627 (9.0%); MSIC grows Press +311 to 1011. OURS has 0 and 0 — ~19% of Takano's program has no counterpart.
2. **Fundamental 2.8× overweight.** OURS 1307 reps (15.5%) vs Takano-MS 467 (6.7%). Single largest share distortion; MSIC keeps it at 6.2%.
3. **Squat overweight, classic lifts underweight.** OURS Squat 1644 (19.5%) vs 893 (12.8%). Clean 421 (5.0%) vs 645 (9.2%); Snatch 690 (8.2%) vs 732 (10.5%). OURS back-fills legs + fundamentals instead of Press/Other-Squat.
4. **Top-end (90%+) undercooked; mid-zone heavy.** 90%+: OURS 1258 (14.9%) vs Takano-MS 1609 (23.0%); MSIC holds 20.6% with 80–89% at 47.5%. OURS parks in 70–79%: 2631 (31.2%) vs 1591 (22.7%).
5. **Reps habit: singles/doubles addiction.** Per-set totals: OURS 1-rep 21.6% + 2-rep 32.5% = 54.1% of sets; Takano-MS 8.5% + 29.6% = 38.1%, with 4-rep sets 27.6% vs OURS 15.7%. E.g. OURS med sess (m3/w3/d0, 78 reps): `Other Snatch [60,1],[70,1],[80,1],[70,2],[80,2],[90,1]`.
6. **Sessions denser but narrower.** Sets/session OURS 31.9 vs 27.6, but slots/session 3.52 (max 4) vs 4.70 (max 7). OURS crams ~9.1 sets/slot vs Takano ~5.9. Takano max sess (m0/w8/d0, 155 reps) runs 7 slots incl. `SnPull [90,5]×4`, `Press [80,4]×5`; OURS max (m2/w2/d5, 150 reps) is 4 slots, e.g. `ClPull [70,1],[80,1],[90,1],[80,3],[90,3],[90,3],[100,3],[110,1]`.
7. **Only-on-one-side slots.** OURS-only: `SnPull+Other Snatch`, `ClPull+Other Clean`, `Clean+Other Jerk`. Takano-only: standalone `Press`, `SnPull`, `Other Squat`, `Jerk`, `Other Jerk`, `Other Snatch+Press`, `Other Snatch+Other Squat`, `ClPull+Clean`.
8. **Totals match only after normalizing.** Absolute: OURS 8438 reps / 3218 sets vs Takano-MS 6994 / 2290 (+20.6% reps). Per prog-week: 421.9 vs 411.4 (+2.5%); sets/wk 160.9 vs 134.7 (+19.5% — smaller sets). Sess/wk 5.05 vs 4.88. MSIC context: 512.5 reps/wk (+24.6% vs MS); carriers of the extra are Press +311, Squat +275, Jerk +261, Clean +182, SnPull +178 — i.e. the top end OURS is missing/soft on.

## Verdict
OURS-MS is a squat+fundamental program with Takano's volume rate but without its Press/Other-Squat spine, top-end exposure, or 4-rep base habit. Fix order: add Press + Other-Squat → cut Fundamental share toward ~7% → move ~8pp of volume from 70–79% into 90%+ → rebalance set sizes toward 3s/4s.
