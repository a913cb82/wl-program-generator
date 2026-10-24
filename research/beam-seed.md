# beam-seed: tune beam search start orders (audit-only)

Budget expired before variants could run. No code changed; this note
records the stack-1 baseline so a follow-up can probe seed variations.

Baseline (`wlgen audit`, 129 tests green):
strain 0.99 (exc 147.8, short 0.0) | size 0.92 (instr 9289) |
rhythm 2.09 | drift -0.17 (spread 0.16) | pace -0.34 | score 0.844.

## Probe table

| variant | strain | size | rhythm | drift | pace | score | verdict |
|---|---|---|---|---|---|---|---|
| baseline (stack-1, unmodified) | 0.99 | 0.92 | 2.09 | -0.17 | -0.34 | 0.844 | baseline |
| (no variants attempted — budget over) | — | — | — | — | — | — | — |

## Planned probes (not run)

- Swap seed order (waved first vs flat first).
- Fewer seeds (flat only) / more seeds (extra capped-first variant).
- Bar per brief: pace delta > 0.03 (score > 0.008) counts as real;
  quality terms must stay bit-identical (same winners).

Verdict: NO-CHANGE (audit-only baseline recorded, tree untouched).
