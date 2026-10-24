# env-t: WLGEN_T template-parameter sweep (audit-only)

Base: research/stack-1. Branch: research/env-t. No src changes.

## Probe table (book row from `wlgen audit`)

| value | book score | strain | size | rhythm | drift |
| --- | --- | --- | --- | --- | --- |
| default (no env) | 0.896 | 1.02 | 0.92 | 2.00 | 0.06 |
| WLGEN_T=4 | 0.886 | 1.02 | 0.92 | 2.00 | 0.00 |
| WLGEN_T=6 | 0.879 | 1.02 | 0.92 | 2.00 | -0.03 |

Baseline per brief: book 0.897 (strain 1.02, size 0.92, rhythm 2.00, drift ~0.06)
— default re-run confirms (0.896, same terms).

## Verdict: KNOB DEAD in the default path

Strain / size / rhythm reproduce the baseline exactly at both T=4 and T=6.
Only drift/pace wiggles (0.06 -> 0.00 -> -0.03; score -0.010 / -0.017 vs
default), which is pace noise, not a quality-term move. No value wins.
Stopped per protocol — no code spelunking.
