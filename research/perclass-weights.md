# Per-class SIZE_WEIGHT probes (research/perclass-weights)

Base: research/stack-1 (`SIZE_WEIGHT = {S:1, M:2, L:3}`), branch
research/perclass-weights. Uniform moves exhausted per
research/sizeweight-nudge (all six single-step probes lose; {1,2,3} a local
optimum, closest M+1). Lead: higher classes (I/CMS/MS) carry the worst rhythm
rows, so probe one class at a time with small nudges, audit-only.
Method: in-process `wlscore.score_book()` in a fresh subprocess per
candidate, monkeypatching `wlgen.day_split` per-class (no src edits, no
`wlscore` edits, no test edits). Baseline in-harness book **0.920**
(strain 1.023, size 0.920, rhythm 2.00, drift 0.174).

## Probe table (book score; lower is better)

| probe | weights (S/M/L) | book | strain | size | rhythm | drift | verdict |
|---|---|---|---|---|---|---|---|
| base | 1 / 2 / 3 (all) | 0.920 | 1.023 | 0.920 | 2.00 | 0.174 | — |
| MS-only M+1 | MS 1 / 3 / 3 | 0.904 | 0.988 | 0.917 | 2.00 | 0.168 | moves right on audit, REJECTED (see below) |

Planned but unrun (budget): I/CMS-only M+1, MS-only M+0.5, I/CMS-only M+0.5.

## Verdict: NO-GO — reverted, no src change

MS-only M+1 moved every quality term the right way on audit
(book -0.016 via strain/excess 153.4 -> ~148.2), so it was implemented
narrowly (`SIZE_WEIGHT_BY_CLASS = {"MS": {S:1, M:3, L:3}}`, threaded through
`day_split`/`sessions`/`week_sessions`). Fence-check failed: 3 of 128 tests
red — `test_day_patterns_keep_canonical_first` (MS weeks pick LMLM over
canonical SLMS under the M/L tie), `test_spread_avoids_back_to_back_sessions`
(boundary 17 > 10 cap), `test_book_numbers_match_research` (pinned excess).
The M/L tie breaks canonical-pattern preference and regresses a spread guard,
so the book gain is not clean. Reverted; `pytest` back to 128 green.
Do not retry M/L ties per-class without a tie-break/canonical mechanism.
