# Pace-prof: audit profile + memoization probes (all reverted)

## Profile (`python -m cProfile -o /tmp/audit.prof .venv/bin/wlgen audit`, 5.96 s, 19.1 M calls)

Top 10 by cumulative time (all orchestration / already-`@cache` leaves):

| fn | cum s |
|---|---|
| wlscore.audit | 5.94 |
| _plan_for | 5.70 |
| ir_with_slots | 3.02 |
| session_slots | 3.01 |
| scheme_entries | 2.98 |
| build_plan | 2.69 |
| week_sessions | 2.66 |
| plan_sessions | 2.66 |
| best_scheme | 2.48 |
| beam_search | 2.07 |

Top 3 by SELF time:

| # | fn | self s | calls (total/miss) | memoized? |
|---|---|---|---|---|
| 1 | `_ipf` | 0.752 | 1477 / 1477 (no hits — every margin set unique) | yes (`@cache`, never hits) |
| 2 | `_guide` | 0.517 | 294923 / 82670 (212 k hits) | yes |
| 3 | `_feasible` | 0.516 | 10804 / 10804 (all unique supports) | yes (support-keyed) |

Top SELF-time NOT memoized: `fixed_beam` (0.190 s, 859 calls, cum 0.862),
inner `key` closures (0.154 + 0.072 s, sort keys — evaluated once per
element, no redundancy), `_transition_ok` (0.143 s, 398 k calls).

## Baseline (reverted tree)

- `audit`: book score 0.837, pace **-0.33**, exc 144.7, instr 9282, rhythm 2.09.
- `pytest -q -p no:cacheprovider`: **136 passed**.
- Repeat audit on clean tree: pace -0.31 (machine noise ≈ ±0.02).

## Probes (TDD: failing `cache_info` test first, then `@cache`, then audit + pytest)

| probe | quality bit-identical? | pace (2 runs) | Δ vs -0.33 | verdict |
|---|---|---|---|---|
| `@cache _transition_ok` (398 k calls; all sites pass frozenset/tuple — pure) | yes (144.7/9282/2.09) | -0.33 | 0.00 | REVERT — body already cheaper than hash |
| `@cache fixed_beam` (types tuple + family — pure, no RNG) | yes (144.7/9282/2.09) | -0.32, -0.34 | ≈0.00 | REVERT — 859 calls nearly all unique, no sharing |

## Why nothing kept

- The profile's top-3 self-time functions are all already memoized; the two
  remaining hotspots have no cross-class sharing (`_ipf`/`_feasible` miss on
  every call, `fixed_beam` args unique), so caching only adds hash overhead.
- Call-site pruning candidates (`fit` → `feasible`/`ipf`, `prune_doses` loop)
  change winner math — out of scope for pace work (never changes winners).
- `_ipf` check-interval thinning would shift the early-exit iteration and its
  floats → tie-break risk. Not attempted.
- Gate was > 0.03 pace gain with identical quality; best probe Δ = 0.00.
  Tree left clean, no commit.
