# Day-rebalance: shift mass BETWEEN days (killed)

Hypothesis: every rhythm attempt moved day PATTERNS and failed; none moved MASS.
Stretch each week's day volumes about the mean to a peak/light contrast of exactly
2.75 (order-preserving, week total and per-group weekly volume fixed — lifts move
across days only). TDD test `test_stretch_vols_hits_contrast_keeps_total_and_order`
(red, then green). Hooked into `day_split` (templates path): stretch after allocate+cap,
re-cap so no day exceeds CAP.

Baseline (stack-1, reverted tree): book 0.902, rhythm 2.00, strain 1.02
(audit jitters run to run: 0.887–0.905 seen; drift/pace nondeterministic).

- Attempt 1 (full stretch, mix=1.0): book 2.177, rhythm 1.24, strain 1.88.
  Rhythm −0.76 (×0.1 = −0.076) vs strain +0.86 (×0.4 = +0.344). Strain cost ~4.5×
  rhythm gain; drift also blew up (I drift 5.21, one bad week). MS rhythm got WORSE
  (2.10 → 4.51): heavier peaks trip CAP in `sessions()` day-count choice, pushing
  big weeks into 6-day shapes whose missing-turn/away-peak floor (~2–3) exceeds
  anything the contrast fix saves.
- Attempt 2 (half stretch, mix=0.5): book 1.317, rhythm 2.81, strain 1.88.
  Rhythm worse than baseline AND strain still doubled. No dose-response — killed.

Verdict: KILL. Contrast is not the binding constraint; the turns-vs-peaks tradeoff
(single peak → missing turns; alternating → extra peaks) floors 4–6-day weeks at
~1–3 regardless of amplitude, and concentrating mass raises Prilepin excess faster
than amplitude falls. Reverted src+tests (128 green); no code kept.

Lesson: rhythm total = amplitude + missing-turns + |peaks−1| — any shape fix must
reduce missing+away jointly, not amplitude alone. Next: try fewer days per week
(lower the n−3 single-peak floor) rather than reshaping mass within the week.
