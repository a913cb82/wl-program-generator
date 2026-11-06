# Track A — Takano AM/PM sessions + MSIC→IMS rename + IMS meso repair

Branch `research/takano-sessions`, base `1daed42`. Ground-truth rebuild:
exactness over cleverness; every number below is measured, not estimated.

## 0. Rename MSIC → IMS (scripted, living files only)

- `MSIC` was our chunk-3 working name for the Ch.14 program. The book
  name is International Master of Sport → program key `IMS`.
- Map: `MSIC` → `IMS` in `src/takano.py` (TITLE `"Takano IMS"`, job tuple,
  `"IMS"→"MS"` grid mapping), `tests/test_takano.py`,
  `tests/fixtures/takano-MSIC.json` → `takano-IMS.json`,
  `outputs/takano-MSIC.html` → `takano-IMS.html`.
- NOT touched: `runs/` history logs, `research/` history docs
  (still say MSIC; they describe past work).
- Suite green after rename, before any functional change (27/27 takano).

## 1. Marker rule (parser: `runs/2026-10-24-wlgen/takano_parse.py`)

- `/tmp/takano.txt` carries 239 standalone `AM`/`PM` lines (`A M` = AM).
  The old parser dropped them, merging each split day into one session.
- Rule: a marker records `(len(day_ex), half)` on the open day; days are
  post-split into blocks at marker indices, each block labeled by its
  preceding marker.
  - No markers → one block, half `null` (whole-day; all of III/II/I/CMS).
  - One marker (`AM@0` / `PM@0`) → one session with that half
    (e.g. MS week-1 Saturday = single `PM` session).
  - `AM@0 … PM@k` → two sessions `AM` + `PM`.
  - Leading unmarked block ahead of a mid-day `PM` (exactly one day:
    IMS week-1 Wednesday, 156 reps, `PM` after exercise 3) → labeled `AM`
    (implicit morning; the book splits >100-rep days breakfast/afternoon).
- Measured marker shapes (parsed days): 72× `[AM, PM]`, 83+61× `[AM]`,
  13+1× `[PM]`, 1× relabeled `[AM, PM]`; zero odd patterns, zero
  `(PM, AM)` days, `AM` always at index 0.
- Also fixed the parser `sys.path` to `/tmp/wta/src` (was the old
  `/home/abrai/projects/wl-program-generator/src`).

## 2. IMS meso-label repair (same file)

- `meso_pat` now `Week \d+\s*[—\-:]*\s*\((.*?)[Mm]esocycle(?:\s*(\d+))?\)`:
  - `Week 1 (Preparation mesocycle 1)` → label `Preparation 1`
    (was `?`: the trailing `1` broke the old pattern). Phase → prep.
  - `Week 5—(Preparation Mesocycle)` (em-dash, found by inspecting all
    IMS headers) → `Preparation` (was `?`).
- Remaining `?` labels: exactly one, CMS week 9 `(Pre-competition
  Macrocycle)` — pre-existing, out of scope (inherits prep as before).
- IMS precomp headers are all plain `Pre-Competition/Pre-competition
  Mesocycle` and already parsed; no change needed there.

## 3. Converter (`src/takano.py`)

- `build_session(ex_list, day, half=None)`; session dict gains `half`
  (`null` / `"AM"` / `"PM"`).
- `build_program` builds one session per non-empty block; both halves
  share the day's weekday. (`wi += 1` stays per-week — caught and fixed
  an indent slip that would have numbered per-day.)
- `main()`: asserts `(meso, week, day, half)` unique; injects `half`
  into each `to_ir` session in order (fixtures carry halves today;
  `wlir.to_ir`/`_restore_sessions` persistence is Track B's side).
- `split_programs` unchanged: III(8w) II(9w) I(12w) CMS(12w) MS(17w)
  IMS(17w).

## 4. Session counts before → after

| class | days (before) | sessions (after) | delta = split days |
|---|---|---|---|
| III | 26 | 26 | 0 (no markers) |
| II | 29 | 29 | 0 |
| I | 50 | 50 | 0 |
| CMS | 55 | 55 | 0 |
| MS | 83 | 117 | +34 |
| IMS (ex-MSIC) | 95 | 133 | +37 split + 1 implicit-AM |
| total | 338 | 410 | +72 |

- MS week 1: 6 days → 9 sessions
  `(0,AM),(0,PM),(1,AM),(2,AM),(2,PM),(3,AM),(4,AM),(4,PM),(5,PM)` —
  pinned in `test_ms_week_one_is_nine_half_sessions`.
- Fixture halves: MS 61 AM / 47 PM / 9 null; IMS 94 AM / 38 PM / 1 null
  (nulls are small single-session days, e.g. IMS (m1,w4,Thu)).

## 5. Tally audit (halves sum to days; dose untouched)

- Line audit over 1545 tally lines, old vs new prog JSON: **10 overs,
  58 B/C chain breaks — bit-identical lists** (all pre-existing
  source-side: tally typos, Good-Morning convention, truncations).
- Split-boundary check (72 split days, B-chain run across AM→PM):
  7 breaks, **all mid-block (never the boundary line)**, all in the
  baseline-58 set. Splits introduce zero new discontinuities.
- Dose check: per-`(meso,week,day)` movement totals AND per-day slot
  seqs old-vs-new identical for MS and IMS (whole-day ≡ AM+PM).
- Spot: MS (m0,w0,d0) AM 52 + PM 96 = 148 = day plan.

## 6. Score-pin moves (deliberate, dose-identical)

`illegal`/`soft`/`idle` unchanged everywhere (dose preserved).
`clash` is per-session `slot_match` over more sessions; `gaps` is
per-session `_unjustified_gaps` (narrower halves, fewer holes):

| class | illegal | clash | idle | gaps | soft |
|---|---|---|---|---|---|
| MS | 109 = | 38 → **44** | 9 = | 3 → **0** | 36.0 = |
| IMS | 126 = | 52 → **55** | 10 = | 2 → **0** | 45.0 = |

- MS's 3 gap sessions (day0 vol148, day4 vol115, day3 vol106) and IMS's
  2 (m0w1d4 vol104 → AM52+PM52; m0w5d4 vol129 → AM57+PM72) all split
  into halves with no unjustified holes.
- `tests/test_wlscore.py` needs no change: it has no Takano
  session-count pins (book pins exc 187.8 / longest 13 / rhythm 5.20
  untouched — suite green).
- New tests (7): whole-day default, half carry, block split with
  dose-sum, PM-only day, MS-w1 nine sessions, IMS-w1-Wed implicit AM,
  key-uniqueness + halves-sum-to-days over all six fixtures.

## 7. Out of scope (not parsed)

- `Sample 20-Week Training Program`, txt line 7698 (APPENDIX): explicitly
  excluded; the parser's APPENDIX gate still stops before it.

## 8. IR contract for Track B (fixture JSON already conforms)

- Session = `{"meso","week","day","half","movements","pairs","slots",…}`;
  `half` ∈ {null, "AM", "PM"}; null = whole-day.
- `(meso,week,day,half)` unique (asserted at build; tested per fixture).
- Needed in `wlir.py` (not mine): `to_ir` persists `half`;
  `_restore_sessions` restores it (default null); `from_ir` keeps the
  `(meso,week)` week grouping (halves are siblings; verified safe —
  volumes roll up from slots, `_week_rhythm` sums halves per day).
- Needed in `wlgen.py` `to_html` (not mine): same-day halves currently
  render as two same-day tables; requested: day header with AM/PM
  sub-headers. `outputs/takano-{MS,IMS}.html` regenerated with current
  renderer in the meantime.

## Files changed

`runs/2026-10-24-wlgen/takano_parse.py`, `src/takano.py`,
`tests/test_takano.py`, `tests/fixtures/takano_prog.json`,
`tests/fixtures/takano-{III,II,I,CMS,MS}.json` (half:null added),
`tests/fixtures/takano-MSIC.json` → `takano-IMS.json`,
`outputs/takano-MS.html` (split sessions), `takano-MSIC.html` →
`takano-IMS.html`; III/II/I/CMS html byte-identical (renderer input
unchanged: `from_ir` drops halves until Track B persists them),
`README.md` (session/half terms).
Gate: 228 passed (221 + 7 new).

---

# NOTES: day-not-session (research/takano-sessions, Track B)

## Every assumption found + fix

1. **IR had no half.** Sessions were keyed (meso,week,day); a Takano AM/PM
   day would collide. Fix (`src/wlir.py`): session dict gains `half`
   (null/AM/PM); unique key (meso,week,day,half). `to_ir` writes it,
   `_restore_sessions` restores it, docstrings updated. Whole-day plans
   round-trip with `half: null`.
2. **Generator stamped day only** (`_assign_weekdays`). Fix (`src/wlgen.py`):
   stamps `half: None`; docstrings on `day_split`/`plan_sessions`/
   `demand_days`/`_assign_weekdays` now say one whole-day session per day.
   No volume logic changed (our programs keep 1 session/day).
3. **Scorer priced doses per session** (`_score_items` exc/shortfall loop).
   Fix (`src/wlscore.py`): new `_day_doses` merges halves sharing a weekday
   (movement vectors sum zone-wise; shared pairs sum per side), and the
   excess/shortfall loop prices merged days.
4. **Rhythm counted sessions** (`_week_rhythm`: `trained` = sessions with
   volume; turn order over sessions; `_week_rest_corr` per session with
   zero intra-day gaps for halves). Fix: all three aggregate by day first
   (volumes/day summed, `trained` = days with volume, turns over day vols,
   rest corr over day vols). Day arithmetic unchanged for whole-day plans.
5. **Session-level metrics deliberately still count sessions**: slot loop
   (instructions/longest/slots/soft/illegal), clash check, idle/spread
   indices, `_unjustified_gaps`. Slots belong to sessions, not days.
6. **README** terminology: session vs day, dose, tolerance, IR key, turns.

## Exc-granularity numbers + recommendation

- Current fixtures (Takano + ours) all hold 1 session/day, so both
  granularities agree exactly (e.g. MS Takano 80.2/80.2, ours 93.1/93.1).
- Synthetic split (MS week-0 day into even AM/PM halves): session-granular
  exc 0.72 -> 0.00 (convex kink at tolerance forgives each half), shortfall
  0.000 -> 0.042. Splitting halves would LOWER Takano exc vs our whole-day
  plans: an asymmetric comparison.
- **Recommendation (judgment call for orchestrator)**: scorer prices dose
  health (excess AND shortfall, two sides of one coin) at DAY granularity;
  volumes already sum so they are granularity-free. Implemented. Session-
  granular reporting added as unit pins (`test_exc_ignores_day_split`
  asserts the removed asymmetry explicitly). To revert: price `_dose` per
  session again in `_score_items` (delete `_day_doses` use); tests to update.

## Gate

`.venv/bin/python -m pytest tests/ -q -p no:cacheprovider`: 231 passed
(221 baseline + 10 new: 3 wlir half round-trip, 5 wlscore day-granularity,
2 wlgen whole-day pins). Slot-level pins (longest/modes/exc-per-day/
volumes: excess 187.8, instructions 9599, slots 1592, longest 13) UNMOVED.
Session-count pins: no pinned session totals exist; new tests pin halves
merge to whole-day values.
