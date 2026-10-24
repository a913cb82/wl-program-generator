# ClPull spill: peak sess2 110%-zone pulls -> light sess0 (NOT IMPLEMENTED — budget exhausted)

Target (from research/single-exc.md): MS ClPull 110%-zone pulls on sess2 peak days.
Worst session meso3/wk1/sess2 dose {70:8, 80:16, 90:10, 100:1, 110:7} exc 2.13;
spill the 7x110% pulls to sess0 with ~1.9 headroom. Move SAME weekly lifts
across days within the week — no complex removed or gated, no amounts changed.

## Result: no change shipped

- 5-minute budget exhausted in exploration (codebase orientation only:
  `session_prior` / `day_split` / `demand_split` / `plan_sessions` located,
  no edits made).
- Working tree left clean; no src/tests changes to commit.
- Baseline re-verified this session: `wlgen audit` book 0.847, strain 0.99
  (exc 147.8); `pytest -q -p no:cacheprovider`: 129 passed.

## Verdict: UNTRIED

The shot is still open and well-scoped: host-day split of MS ClPull 110%
(5-7 lifts) off sess2 onto light sess0 host within the same week, totals
identical. Next attempt should go straight to `plan_sessions` /
post-plan rehost logic with a session-shape guard (SLS->MLM fallback =
known defect; kill fast if shape tests trip) and totals assertion.
