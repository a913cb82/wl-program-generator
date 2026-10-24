# Taper trim probe (research/taper-trim)

HEAD baseline (`37767da`): `wlgen audit` book score **0.843**,
strain **0.99** (exc 147.8). Suite: **129 passed**.
(Note: lead's stack-1 figures book 0.897 / strain 1.02 predate the
perclass-impl commits on this worktree; HEAD is the effective baseline.)

## Probe table

| # | Nudge (audit-only) | Fence tests | Result |
|---|--------------------|-------------|--------|
| 0 | Baseline (no change) | — | book 0.843, strain 0.99 (exc 147.8), 129 green |
| A | Extend taper 1 wk earlier, Snatch only (Comp-2 W3) | `test_comp2_peaks_then_tapers` (peak>base>taper) | NOT RUN — timebox expired; by inspection peak==taper ⇒ red |
| B | Extend taper 1 wk earlier, one family (Comp-1 W4) | `test_only_comp2_tapers` | NOT RUN — timebox expired; by inspection red |
| C | Lift taper cap 90→95, CJ family | `test_taper_drops_classic_heavy_bins` (z≥90 must be 0) | NOT RUN — timebox expired; by inspection red |

## Verdict

**No-change.** All three candidate nudges collide head-on with the
intensity-mix fence tests (A breaks peak>base>taper, B breaks
only-Comp-2-tapers, C breaks the z≥90-zero assertion), so each is
expected red on the fence before quality terms even matter. No src
change applied; tree left clean. A future probe with remaining budget
could confirm A/B/C red empirically, or look off the fenced path
(e.g. taper shape for pulls/squats — also currently fenced by
`test_taper_drops_classic_heavy_bins` for squats).
