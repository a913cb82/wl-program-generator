# exp: flatten-80 — squat prep peak 2.0 → -1.0 counter-spread

## What
`SQUAT_PREP_PEAK = -1.0` in `src/wlgen.py`: `phase_peak(cls, mi, group)`
returns a mild counter-spread prior for group `"Squat"` in prep mesos;
every other group keeps the global prep peak 2.0, comp keeps -0.3, and the
pair path (`pair_zones`) keeps the global peak (pairs never carry solo
squat dose). One knob, prep-only, squat-only.

## Why (P2 anatomy, WORKLOG §41 + Takano + Roman)
- Squat's weekly 80-share (.32-.37) under the prep peak dumped 20-50
  lifts at 80 onto the biggest-volume day (baseline maxima per class:
  III 23 / II 23 / I 34 / CMS 26 / MS 50) vs Prilepin cap 20 at 80.
- Takano spreads 80s evenly (precomp 0.98) and maxes at 10/11/16 per
  session; Roman (p68) prescribes ~20-30 squats/workout, up to ~60 in
  two series — a 50-pile breaks both books.
- Prior reweighting is otherwise a known dead end (WORKLOG §37: exponent
  3.0 moves nothing against exact margins). It works here only directionally:
  the pile weeks are margin-tight (e.g. MS week: 77 lifts at 80 over two
  hosting days, floor 31), so the counter-spread prior deals the 80-row
  back toward even ([27,50] → [31,46] on pile-like margins) instead of
  stacking it. Unit-pinned in `test_squat_prep_peak_counterspread`.
- What it cannot do (floors bind): week 80-totals exceed cap × hosting
  days (77 lifts over 2 days ⇒ somebody holds ≥31). The residual needs
  hosting/quota redesign (tops-first allocator) — out of scope for this
  track's edit surface.

## Numbers (before → after; audit run with PYTHONPATH=/tmp/wd/src — see env note)
- exc book 190.3 → 187.8 (-2.5); per class III 9.0→8.9 / II 10.0→9.3 /
  I 35.4→34.7 / CMS 42.6→41.9 / MS 93.3→93.1. Max solo Squat@80:
  III 23→22, MS 50→46 (I 34 / CMS 26 maxima sit in comp mesos, untouched
  by design — comp -0.3 frozen).
- rhythm book 5.22 → 5.20 (per class 1.06/1.11/1.28/1.08/0.67 — none worse).
- drift 5.4x → 4.19 with ob/vol 0.0 everywhere (month/zone totals
  bit-identical — fit margins exact, meso quotas intact) and soft
  84 → 52 (II 23→7, CMS 17→5, III 2→1, MS 24→21: fewer soft shape
  violations pooled on the big day).
- size: instructions 9409 → 9519, slots 1537 → 1550, longest 24 → 24.
  Each hosting day renders its own 80 ladder at ladder-max (Takano-modal
  4s) sizes instead of one marathon day; rendered set-size modes are
  UNCHANGED (`test_rendered_set_sizes_match_takano_centers` passes
  unmodified — Squat-70 mode stays 2, one rep under Takano's 3).
- MS prep top-concentration median 1.129 (test bounds 1.06–1.26) — prep
  heavy/light separation survives for the tested group.
- build-all CPU 2.50s vs 2.55s baseline (within +5%); suite 214 green
  (213 + 1 new), run as `PYTHONPATH=/tmp/wd/src .venv/bin/python -m
  pytest tests/ -q -p no:cacheprovider`.

## Pins touched (2, both with Takano/Roman argument above)
- `test_book_numbers_match_research`: exc 190.3→187.8, instructions
  9409→9519, slots 1537→1550 (mechanical consequence of spreading 80s
  over more days; longest 24 and shortfall <0.2 untouched).
- `test_shipped_scores_clean`: soft map III 2→1, II 23→7, CMS 17→5,
  MS 24→21 (fewer big-day shape violations; ob/iv/illegal/clash/gaps/idle
  pins all untouched).
- Rejected direction: peak ≤ -2 breaks `test_rendered_set_sizes_match_
  takano_centers` (Squat-70 mode 2→1, two reps under Takano's 3 —
  feeler-singles texture) for only ~1 more exc. -1.0 is the fidelity
  edge: all rendering pins hold.

## Env note (for the orchestrator, not the gate)
`/tmp/wd/.venv` symlinks to another tree's venv whose `.pth` puts THAT
tree's `src` on `sys.path`. Bare `.venv/bin/python -m wlgen audit` in
/tmp/wd therefore scores the OTHER tree (I confirmed: identical 190.3
across all knob values until PYTHONPATH was set). All numbers above use
`PYTHONPATH=/tmp/wd/src`. `pytest tests/` likewise needs it in this
shell (214 green was measured that way).
