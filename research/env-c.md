# env-c: WLGEN_C (day-count) sweep — audit-only, knob dead

## Baseline (branch start, no env, in-session `wlgen audit`)

book: strain 1.02 (exc 153.4, short 0.0) | size 0.92 (instr 9292,
longest 21, slots 1291) | rhythm 2.00 | drift 0.00 (spread 0.17,
pace -0.17) | score 0.886

(Note: task brief quoted book 0.897 / drift ~0.06; in-session default
audits at 0.886 / drift 0.00. Pace noise between runs; quality terms
strain/size/rhythm match exactly.)

## Probes (`WLGEN_C=<v> .venv/bin/wlgen audit`, book row)

| WLGEN_C | score | strain | size | rhythm | drift (spread/pace) |
|---------|-------|--------|------|--------|---------------------|
| default | 0.886 | 1.02 (exc 153.4) | 0.92 (instr 9292, longest 21, slots 1291) | 2.00 | 0.00 (0.17 / -0.17) |
| 2       | 0.887 | 1.02 (exc 153.4) | 0.92 (instr 9292, longest 21, slots 1291) | 2.00 | 0.01 (0.17 / -0.16) |
| 4       | 0.894 | 1.02 (exc 153.4) | 0.92 (instr 9292, longest 21, slots 1291) | 2.00 | 0.05 (0.17 / -0.13) |

Per-program rows (III/II/I/CMS/MS) byte-identical across all three
runs; only book-level pace/drfit wiggles (±0.05 drift, +0.001/+0.008
score — pace noise).

## Verdict

**Knob dead in the default path.** C=2 and C=4 reproduce all three
quality terms (strain, size, rhythm) exactly — no value wins, no
code changes, no follow-up. Stopped per protocol, no code spelunking.

`pytest -q`: 128 passed (no src changes).
