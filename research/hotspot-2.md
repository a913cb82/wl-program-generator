# Hotspot-2: profile the stacked build (caches + IPF stall-abort)

## Method
`python -m cProfile -s tottime` over `build_plan` for all five classes
(III, II, I, CMS, MS). Stack includes shared max-flow/zone caches,
memoized helpers (pace-hunt), wave-polish (size-again), and the IPF
stall-abort (ipf-stall). Total: ~3.18 s, ~11.16 M calls.

## Profile table (by internal/tottime)

| Function | tottime | share | cumtime | ncalls |
|----------|---------|-------|---------|--------|
| `_ipf` (wlgen.py:248) | 1.048 s | ~33% | 1.520 s | 1537 |
| `_feasible` (wlgen.py:302) | 0.579 s | ~18% | 0.801 s | 11976 |
| `sum` (builtin, mostly from `_ipf`) | 0.517 s | ~16% | 0.587 s | ~4.45 M |
| `list.append` | 0.139 s | ~4% | — | ~2.30 M |
| `feasible:296 <genexpr>` | 0.119 s | ~4% | 0.182 s | 270458 |
| `len` | 0.099 s | ~3% | — | ~2.07 M |

By cumtime the chain is `build_plan > week_sessions > plan_sessions >
fit_session > resolve_slots > rec > ipf > _ipf`; `_ipf` is the top
self-time hotspot even after the stall-abort.

## Verdict: REVERT CLEAN (no cut)
- The NEW top hotspot is **`_ipf` itself at ~33% of total self time**
  (1.048 s / 3.18 s). The stall-abort already removed the doomed-burn
  tail; what remains is the dense Python iteration loop of converging
  burns, whose body cost is dominated by `sum()` calls (~4.45 M calls).
- No safe cut inside the 5-minute budget: prior work proved every
  `sum()` must stay exactly as-is (3.14 compensated summation flips fit
  tie-breaks) and `_ipf`'s float sequence is the byte-identity gate.
  Any rewrite (numpy, manual loops, reduced iterations) risks output
  drift with no time to validate the identity oracle + audit.
- Tree left clean: no src/tests changes. `pytest`: 128 passed.
- Baseline book 0.906 (strain 1.02, size 0.92, rhythm 2.00, pace -0.07,
  this machine) = final book 0.906. Nothing moved, as required.
- Lead for next round: `_feasible` BFS at ~18% (11,976 calls) is the
  largest non-`sum` block; micro-opts there (adjacency layout, queue
  discipline) keep float semantics out of the blast radius.
