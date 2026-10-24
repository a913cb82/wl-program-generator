# Pair-volume trim @ 70% tier (Class I) — discovery only

Budget expired before implementation. No `src/` change made; tree left clean.

## Call chain found (90s discovery)

`week_sessions` (wlgen.py:977)
→ `plan_sessions` → `pair_fit` (wlgen.py:1122) → `snap()` uses
→ `pair_options(c, h, cls, mi, wi, ref)` (wlgen.py:1056)
→ `_pair_options_keyed` (wlgen.py:1043)
→ `_week_units_keyed(binkey, gap, fan, mi, wi, t, ref)` (wlgen.py:1025)
returns `(heavy, mid, light)` = units with ref-zone `>= 90`, `== 80`, `< 80`.

The **70%-tier = `light`** (all ref zones `< 80`: 70/60/50 labels).
Session pair counts: `ac = rh[0]*heavy + rm[0]*mid + rl[0]*light`
(`SCHEDULES` = legal `(heavy, mid, light)` ratio triples, wlconfig.py:313;
light ratios are the widest, `allowed_ratios(70)`).
Then `pair_zones` (wlgen.py:1328) splits each tier's units across paired sessions.

## Planned trim (not applied)

In `_pair_options_keyed`, for Class I only (`binkey == "C1"`, since
`_canon("I") = ("C1", GAP["I"], ...)` and `BIN_CLASS = {"I": "C1", ...}`):
`light = max(MIN_DOSE, floor(light*0.9 + 0.5))` before the `SCHEDULES` loop.
Singles path (`week_bin_lifts`) untouched. Volume trim, recipe stays legal
(same ratio triples, just fewer light-tier unit blocks).

Open question: flooring *units* at `MIN_DOSE=6` inflates small-`t` options;
floor likely belongs on the resulting per-session `ac`/`aj` instead.

## Baseline (pre-change, confirmed)

- book ~0.84, strain 0.96 (exc 144.7), 136 green (`pytest`: 136 passed).
- Per-class exc: III 13.4 / II 13.4 / I 44.0 / CMS 31.5 / MS 42.5.

## Verdict

**REVERT (no-op)** — discovery only, nothing to keep or revert.
Next session: implement the trim above with a TDD test, then apply the
fence (partner-group excess delta ≤ half target fall; paired-session count
must not rise) and gate (exc < 144.7, zero new defects, 136 green).

---

## Attempt 2026-10-24: 0.9x C1 light-tier trim in `_pair_options_keyed` — REVERTED

Change (reverted): in `_pair_options_keyed` (wlgen.py:1043), `binkey` is the
class key (`_canon("I") = ("C1", ...)`). Added
`use_light = round(light * 0.9) if binkey == "C1" else light` for the
`SCHEDULES` loop, with per-schedule fallback to untrimmed `light` when the
trimmed `ac`/`aj` would strand a slot at `0 < v < MIN_DOSE` (6). Singles
path untouched. TDD test (`tests/test_pairvol_trim.py`, since removed) went
red pre-change, green post-change.

Result (gate FAIL → fully reverted):
- book exc 144.7 → 161.3 (+16.6); target class I exc 44.0 → 60.6 (+16.6).
- New defects: class I drift off 20.0 (was 0.0), longest 21 → 23 slots,
  rhythm 3.09 → 3.00 with a collapsed 0.3 week; partners III/II/CMS/MS flat.
- pytest 136 passed → 134 passed + 5 failed (day-patterns-canonical-first,
  week-targets-near-nominal, fund-spill-top-slice, shipped-scores-clean,
  book-numbers-match).
- Re-coupling fence moot (target rose, no fall to halve); paired-session
  count not separately tallied once the gate failed outright.

Verdict: **REVERT** — tree restored to HEAD, baseline re-confirmed
(exc 144.7, 136 green). Hypothesis dead: trimming light-tier units at the
pair-options stage starves Class I sessions instead of trimming volume
(pair-fit snaps to near targets, so smaller unit blocks force off-plan
drift rather than less volume).
