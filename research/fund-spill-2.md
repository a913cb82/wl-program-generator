# fund-spill-2: generalize the peak-Fundamental co-host spill

Proven base (research/fund-spill, stack-1): class-I-only post-pass at end of
`build_plan` moves the single global peak Fundamental top-slice (highest zone
>= 90) to the same week's lightest co-host session. Result: exc 147.8 -> 147.3,
zero defects, 130 green. Co-host-only (no new movements) is load-bearing.

## Step 1: top-k loop (KEEP)

Loop the spill over the top 3 peak sessions: recompute the best after each
move, never reuse a donor week twice.

- Raw top-3 (no guard): exc 147.3 -> 146.9, but +1 unjustified zone gap
  (meso4/wk0 recipient side) -> REJECTED as-is (defect gate).
- With gap guard (tentative move reverted + week skipped if
  `_unjustified_gaps` rises on donor/recipient): exc 147.3 -> 146.8
  (I exc 44.5 -> 44.0), zero defects, green. KEEP.
- k=2 alone: exc unchanged at 147.3 (second pick nets ~0) -> no reason to stop
  at 2; the guard makes 3 safe.

## Step 2: other classes (KEEP, all classes)

- MS-only next: MS exc 43.3 -> 42.5 (-0.8, ~half the single-excess pool as
  predicted). MS rhythm 3.00 -> 2.96 (delta 0.04 <= 0.05 kill limit).
  Book 146.8 -> 146.0, zero defects. KEEP.
- All classes (CMS/II/III too): CMS exc 32.8 -> 31.5 (-1.3), CMS rhythm
  3.09 -> 3.00, longest 21 -> 20. II/III unchanged (13.4, no peak to spill).
  MS rhythm steady at 2.96. Book 146.0 -> 144.7, zero defects. KEEP.

## Final

- Baseline: book ~0.844, strain 0.98 (exc 147.3), 130 green.
- Final: book 0.841 (pace noise +/-0.01), strain 0.96 (exc 144.7, short 0.0),
  132 green (130 + 2 new spill pins). Total: exc -2.6 (~5x the proven win).
- Per-class exc: I 44.5 -> 44.0, MS 43.3 -> 42.5, CMS 32.8 -> 31.5.
- MS rhythm 2.96 (within 0.05 of 3.00 base). No new movements anywhere;
  weekly zone totals unchanged by construction; vols track movements.

## Change

- `spill_peak_fundamental(plan, top_k=3)` in `src/wlgen.py`: top-k loop over
  all classes + gap-guard revert (deferred `wlscore` import; scorer never
  imports the generator, so no cycle). Applied at end of `build_plan`.
- Pins: `test_fund_spill_top3_uses_distinct_weeks_and_keeps_shape`,
  `test_fund_spill_adds_no_unjustified_gaps`; golden exc 144.7 / instr 9282.
