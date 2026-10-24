# Support-cap: peak-day group cap with pair-free singles (FALSIFIED)

Baseline (research/support-cap @ 3604ad9, this box): book 0.983
(strain 1.02 = exc 153.4 + short 0.0, size 0.92, rhythm 2.00,
drift 0.49 incl. pace noise). 123 tests green.

## Hypothesis

Amount-shaping inside a fixed support is near zero-sum across rows
(strain-ease round 1). So reshape the support itself: the week's peak
day keeps full prior weight only for ballast (never-paired) rows —
exactly 4 groups (Squat, Other Squat, Press, Fundamental) — while every
pairable row goes soft (EPS, never 0) on the peak column. Complexes are
then forced onto smaller days, where the frozen scorer's pair-doubling
scores less excess. Implemented as `cap_peak()` in `plan_sessions`,
soft so the exact fit stays feasible.

## Result: REJECTED, reverted clean

- book 0.983 -> 4.000; exc 153.4 -> 165.0 (strain 1.02 -> 1.10)
- drift 0.49 -> 15.32 with bad=3 (starved volumes / idle defects)
- rhythm 2.00 -> 2.15; 6 test failures (back-to-back, canonical
  patterns, ramp/contiguity, both wlscore book tests)
- Tree reverted to baseline: src and tests clean, 123 green.

## Lesson

Same backfire family as peak-skip (strain-ease try #4) and r2-host:
pushing pairable groups off the peak concentrates them onto fewer
off-peak days, making bigger off-peak complexes, while rows that only
fit on the peak starve (bad defects). Support-narrowing from the prior
cannot beat the three-sided fence (MIN_DOSE concentrator,
slot-disjointness, MS back-to-back headroom 8). Peak composition
needs joint host+amount control, not prior softening.
