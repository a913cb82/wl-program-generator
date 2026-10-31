# exp: unpair-heavy — thin fallback over-cap tech co-hosts in place

## What (one rule, ~10 lines, no new passes, no cross-day moves)
In `pair_fit` (`src/wlgen.py`), when a detected tech co-host pair's fit dose
exceeds `PAIR_DOSE_CAP` (40) — i.e. the dose-gate's solo-first fallback, no
free single slot — the snap now searches the full `pair_options` list and
keeps only schedules with snapped total `ac+aj <= PAIR_DOSE_CAP` (closest 6
feed the existing hill-climb; if none fit, the smallest-total option).
Test pairs (`Clean+Jerk` backbone) are untouched. Freed dose is absorbed by
the existing ballast refit in the same week; session count and hosting
decisions never change. `PAIR_DOSE_CAP` value unchanged; no new knobs.

## Why
P1 cells are co-hosted tech over the complex cap, and `_dose` counts paired
reps for BOTH members (doctrine, frozen), so a 60-dose fallback complex
scores ~2.4 vs 1.5 tolerance. The dose-gate already unpairs big tech where a
solo slot is free; this covers the fallback pairs in place, per the
tops-first spec: decide hosting dose-aware in ONE pass (no prediction, no
refit, no post-hoc surgery).

## Numbers (same box; audit path, `PYTHONPATH=src`)
- exc book: 190.3 -> 181.2 (-9.1, -4.8%)
  - III 9.0 -> 9.0, II 10.0 -> 10.0, I 35.4 -> 34.8, CMS 42.6 -> 41.9,
    MS 93.3 -> 85.5 (win lands in MS fallback pairs; III/II/I P1 untouched)
- instructions 9421 -> 9408, slots 1440 -> 1444, longest 33 (24/26/33/26/28)
- rhythm book 5.22 -> 5.16 (per-class 1.08/1.11/1.27/1.08/0.61, all <= +0.1)
- CPU (audit user+sys, this box): 5.68 -> 5.50 (-3%; brief's 2.95s was
  another box; same-box delta is within +5%)
- suite: 211 -> 212 green (1 new test), score 2.558 -> 2.345
- costs: soft 84 -> 88 (I +2, CMS +1, MS +1); ob_micro MS 0 -> 16.0
  (thinned dose re-hosted same-week; meso totals and week volumes exact)

## Pins touched (all with Takano-fidelity argument)
- `test_book_numbers_match_research`: exc/slots/instructions — the goal.
- `test_shipped_scores_clean` soft I 18->20, CMS 17->18, MS 24->25: thinned
  tech re-hosts solo; Takano renders heavy co-hosts as separate sets
  (fixtures show `pairs: {}` — no paired complexes), so solo/small sets
  ARE the Takano shape.
- `test_shipped_scores_clean` ob_micro MS 0->16.0: the 16 moved lifts,
  priced; meso-exactness holds; Takano keeps heavy complexes small, so the
  nominal shape flexes where the cap bites.
- `test_day_patterns_keep_canonical_first`: MS Prep4-2 w0 SLSLS->MSLMM, MS
  Prep2-4 w0 LSMML (new): same 5-day counts, dose-floor-forced by thinned
  targets, never a preference (the test's own framing).
- `test_week_targets_near_nominal`: 4 MS thinned-group allowances (thin down
  to MIN_DOSE floor, never grow past band — thinning only removes).
- `test_rendered_set_sizes_match_takano_centers` ClPull@90 2->3: Takano
  ground truth is 3 at I (27 triples), 4 at CMS/MS; rendered mode 3 moves
  TOWARD Takano. Roman allows pulls 2-6 at 80-99%.
- New: `test_pair_fit_thins_overcap_tech_in_place` (SnPull 30 + Snatch 30
  snaps <= 40 in the same session).

## Fidelity notes
- Cap 40 kept: both books keep heavy complexes small; Takano complex slots
  top out near 40 lifts.
- Untouched per brief: `zone_alloc`, render/session-building, quotas, taper
  chain, `close_*`, `src/wlscore.py` (ruler frozen), `runs/2026-10-24-wlgen`,
  `/tmp/wt-b`, `/tmp/wt-c`. (`tests/test_wlscore.py` pins updated under the
  pin-change clause; the scorer itself never opened.)
- Caveat: `python -m wlgen audit` without `PYTHONPATH=src` scores the
 venv's editable install (`/home/abrai/projects/wl-program-generator/src`),
  not this tree — always run audit/tests with `src` on the path here.
