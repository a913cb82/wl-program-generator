# Per-class day counts (perclass-T) — UNEXECUTED, budget expired

Discovery only; no probe was implemented. Working tree left clean.

## Discovery

- Weekly day count derives in `week_sessions` (src/wlgen.py):
  - `DAY_RULE=templates` (default): start day `n = len(sessions(vol, cls))`,
    first cap-feasible pattern in `VARIANTS[n..6]` wins.
  - `DAY_RULE=demand`: start day `n = demand_days(demand, vol)`
    (`ceil(total/DAY_T)`, cap, max 6).
- `cls` is already threaded into `week_sessions` and `sessions`
  (MS-only `SIZE_WEIGHT_MS` half step), so a per-class day delta is a
  small change: offset the range start by class, e.g.
  `start = max(3, base + DAY_DELTA.get(cls, 0))` with `{"MS": -1}`.
- Baseline re-measured on research/perclass-T: book exc 144.7,
  score 0.840, 136/136 pytest green.

## Verdict

Neither probe ran (5-minute budget exhausted during discovery plus
baseline audit). Hypothesis for a retry: MS carries the largest
per-class exc (42.5); one fewer MS day concentrates its volume into
fewer, heavier sessions — likely worse, not better. The I+1-day probe
(spreading I's 44.0 exc over more days) looks the more promising
direction, but global T=6 evidence (3-day median collapse) warns that
extra days can strand light-day doses.

## Probe 1 (executed): class I +1 day/week — KEEP

- Change (`src/wlgen.py`): `DAY_DELTA = {"I": 1}`; both `week_sessions`
  range starts offset by `DAY_DELTA.get(cls, 0)` (capped at 6). MS/others
  untouched. TDD: `tests/test_perclass_days.py` (RED first, then GREEN).
- Audit: book exc 144.7 -> **131.0** (I 44.0 -> 30.3; MS 42.5, CMS 31.5,
  II/III 13.4 unchanged). short/bad/off all 0, no ValueError, no
  infeasible weeks. 138/138 pytest green (2 new + 3 stale goldens updated:
  canonical-pattern exceptions for I, fund-spill recip sess3->sess4 with
  identical doses/bins, book golden numbers).
- Caveat: book drift pace +0.00 -> +0.82, score 0.839 -> 1.046 (I rhythm
  3.09 -> 3.06, size 0.52 -> 0.54). exc gate rules, so KEEP, but drift is
  the next thing to watch.
- Verdict: KEEP (commit 7afe1a6). Gate exc < 142.5 ✓, zero defects ✓,
  138 green ✓.
