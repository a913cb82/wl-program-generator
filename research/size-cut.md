# size-cut: fewer instructions, shorter longest block

## Baseline (branch start, `617ce37`)

`wlgen audit` book row: strain 1.02 (exc 153.4, short 0.0) | size 1.00
(instr 9312, longest 25, slots 1291) | rhythm 2.00 | drift ~0.26
| score ~0.961. (`research/log.md` records 0.942; the gap is pace noise,
CPU seconds squared. Pace-neutral score is 0.944.)
`pytest -q -p no:cacheprovider`: 115 passed.

## What I tried

1. **Tighter set merging via the beam.** The beam ranked orders by
   `100·stray + 10·warmup + 4·complexity` with set count only as a
   tiebreak, so it shredded zones into small sets to save one phrase.
   Worst case: MS Comp 1 ClPull, 25 sets / 9 instructions, where a lone
   100% single caps every 110% set at one rep.
2. **New `capped_order` seed.** Fills each zone with the largest sets
   that fit under the last set below it (pure ascent, no drops, always
   legal or dropped). Wins only when strictly shorter than the beam's
   best, so its phrase-parse cost is paid only where it matters.
3. **`LENGTH_COST = 1` in the final rank** (`_rank`), matching the
   beam's own pruning unit of one per set. Swept 0/1/2/4: 0 keeps the
   25-set slot, 2 and 4 cost extra instructions, 1 is the sweet spot.
4. **Dead ends (verified, not shipped).**
   - `_parse` is already optimal: brute-forced the minimum
     instruction count over its grammar for all 1291 slots, zero
     mismatches. No wave-detection headroom left.
   - Gated the capped seed on `len < len(base)` after profiling showed
     unranked seed parsing cost +0.2 s CPU (pace). Build CPU is now at
     or under baseline (3.77 s vs 3.82 s).
   - Leftover 21-set slots (Fundamental/Other Snatch with tail
     drop-backs) are structural: zone totals plus the next-zone rule
     force two runs of the revisited zone, so merging tails into the
     bulk cannot drop below two groups. Zone consolidation would cut
     words but changes the training itself, so out of scope.

## Final deltas (book, pace-neutral via `score_book(..., cpu=None)`)

- instructions 9312 -> 9301 (-11)
- longest 25 -> 21 (-4)
- slots 1291 unchanged; strain, rhythm, and every drift term unchanged
- size 1.0006 -> 0.9201; score 0.9443 -> 0.9201 (-0.024)
- In-session `wlgen audit`: book score 0.961 -> 0.922 (pace +0.09 -> +0.01)
- 17 slots changed (Squat/ClPull strength ladders), all strictly shorter
- Guarantees hold: output deterministic (repeat builds byte-identical,
  `WLGEN_JOBS=1` matches parallel), audit `bad` counts all zero,
  all 118 tests green (115 baseline + 3 new).

## Winner

Price each extra set at one complexity unit in the final scheme rank
and compete a capped-ascent seed against the beam: longest 25 -> 21,
instructions -11, at zero CPU cost.
