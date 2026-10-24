# Per-class I/CMS weight probes (research/perclass-icms)

Base: research/stack-1 (`SIZE_WEIGHT = {S:1, M:2, L:3}`), branch
research/perclass-icms. Baseline (stack-1): book **0.897**.
Follows research/perclass-weights (in wl-program-generator worktree):
MS-only M+1 moved audit the right way (book 0.920 -> 0.904 in that
harness) but broke 3 guards on implementation — canonical-pattern
preference (`test_day_patterns_keep_canonical_first`, M/L tie picks LMLM
over SLMS), spread cap (`test_spread_avoids_back_to_back_sessions`),
pinned excess (`test_book_numbers_match_research`). Reverted there.

## Harness check (code read, no run — budget expired)

- `allocate()` (`src/wlir.py:26`) does `total * w / sum(weights)` float
  math, memoized on the weight tuple: **fractional weights (M+0.5)
  are allowed**, no fight needed.
- Patch points for audit-only per-class probes: wrap
  `wlgen.week_sessions` (has `cls`) to stash the current class, wrap
  `wlgen.day_split` (no `cls`) to substitute
  `{S:1, M:3, L:3}` / `{S:1, M:2.5, L:3}` when the stashed class is in
  the target group. No src edits, no `wlscore` edits, no test edits.
- Classes: III, II, I, CMS, MS.

## Probe table (book score; lower is better)

| probe | weights (S/M/L) | book | verdict |
|---|---|---|---|
| base | 1 / 2 / 3 (all) | 0.897 | — (stack-1 baseline, not re-run) |
| I/CMS-only M+1 | I,CMS 1 / 3 / 3 | — | UNRUN (budget) |
| MS-only M+0.5 | MS 1 / 2.5 / 3 | — | UNRUN (budget) |
| I/CMS-only M+0.5 | I,CMS 1 / 2.5 / 3 | — | UNRUN (budget) |

## Verdict: NO-GO (unrun) — no src change, tree clean

Budget expired during harness recon; no probe was executed, so no
conclusion for or against I/CMS-only M+1 or half-step nudges. Next
session: run the three UNRUN rows one class-group at a time via the
patch points above, fresh subprocess per candidate, `pytest` stays
128 green. Standing warning from perclass-weights: any M/L tie
per-class breaks canonical-pattern preference — prefer M+0.5 rows
first, as they keep M < L strict.
