# Noise floor: `wlgen audit` repeatability (identical code, 6x back-to-back)

Branch: research/noise-floor (based on research/stack-1). No src changes.

## Book line per run

| run | strain | size (instr/longest/slots) | rhythm | drift (spread/pace) | score |
|-----|--------|----------------------------|--------|---------------------|-------|
| 1 | 0.99 | 0.92 (9289/21/1282) | 2.09 | -0.16 (0.16/-0.33) | 0.846 |
| 2 | 0.99 | 0.92 (9289/21/1282) | 2.09 | -0.18 (0.16/-0.34) | 0.843 |
| 3 | 0.99 | 0.92 (9289/21/1282) | 2.09 | -0.17 (0.16/-0.34) | 0.844 |
| 4 | 0.99 | 0.92 (9289/21/1282) | 2.09 | -0.16 (0.16/-0.33) | 0.846 |
| 5 | 0.99 | 0.92 (9289/21/1282) | 2.09 | -0.14 (0.16/-0.31) | 0.851 |
| 6 | 0.99 | 0.92 (9289/21/1282) | 2.09 | -0.16 (0.16/-0.32) | 0.848 |

Sub-book lines (III/II/I/CMS/MS) were bit-identical across all 6 runs
(e.g. III strain 0.09 size 0.41 rhythm 1.55 drift 0.14 pace +0.00 score 0.344).

## Spread

- Score range: 0.843–0.851 → spread **0.008**
- Pace range: -0.34–-0.31 → spread **0.03**
- Drift range: -0.18–-0.14 → spread 0.04 (driven by pace; spread term fixed at 0.16)
- Quality terms stable: **yes** — strain, size, instr count, rhythm, rhythm-weeks
  identical every run. Only pace/drift/score move.

## Measured noise bar

Old guess: "pace deltas under ~0.05 are noise."
Measured: identical-code runs differ by up to **0.03 in pace** (0.008 in score).

**New rule: a future verdict must clear pace delta > 0.03 (score delta > 0.008)
to count as a real change.** Keep 0.05 as a conservative ceiling if desired,
but 0.03 is the measured floor.
