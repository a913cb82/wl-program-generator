# exp: wide-split — peel half the largest zone-cell

## Baseline (B2+D kept tree, commit 7b6d47a)
longest 13/17/13/16/14; marathons (>=14) 0/1/0/3/1; exc 187.8;
instr 9585; slots 1587; rhythm 5.20; soft 52; suite 220 green; CPU ~11.5s.

## Residue (from split-deep-1.md, re-verified post-split)
5 post-split slots still rendered >=14, each a wide (>2-zone) chunk
with no legal MIN_DOSE boundary (every contiguous-band cut strands
<6 lifts on one side) and refused by halve_counts (scoped to <=2 zones):
- II Press (0,2,2,28,2,0,0) -> 17 sets
- CMS Fundamental (0,1,4,23,0,0,0) -> 15 sets
- CMS Fundamental (0,2,3,22,4,0,0) -> 16 sets
- CMS Fundamental chunk (0,2,3,21,0,0,0) -> 14 sets (post-boundary half)
- MS Squat (0,1,2,11,0) -> 14 sets

## Landed (src/wlgen.py render seam + tests only)
New `halve_largest_cell(counts)`: peel half the largest zone-cell into
its own same-day slot; the remainder keeps every other zone. Both halves
hold >= MIN_DOSE lifts (odd cells deal parity to the legal side, so the
MS 11-cell peels 6/5 into 8/6 chunk-halves); narrow cells return None
(halve_counts owns them); sums exact. Both halves stay book-shaped: the
remainder is a contiguous band from its own base (warm-up ramp survives
in the day's first chunk) and the peel is single-zone. Wired as the last
fallback in `split_chunks` (`split_marathon or halve_counts or
halve_largest_cell`); recursion re-renders every chunk, so each split
strictly shrinks totals above the MIN_DOSE floor and the loop terminates.
No other function touched: movements matrix, quotas, hosting, taper,
movers, close_*, warm-up ramps, strip_feelers, pair path all untouched.

## Numbers (after -> before in parens)
- longest III/II/I/CMS/MS: 13/13/13/13/13 (13/17/13/16/14)
- marathons (>=14): 0/0/0/0/0 (0/1/0/3/1) — all 5 killed, none resist
- exc book 187.8 -> 187.8 exact; shortfall 0.0; rhythm 5.20 identical
- soft 52.0 exact (1/7/18/5/21 per class); spread 0.18 identical
- instr book 9585 -> 9599 (+14, extra same-day slots compress)
- slots book 1587 -> 1592 (+5, one per killed marathon)
- suite 221 green (220 + 1 new halve_largest_cell unit test)
- CPU 11.32s vs 11.49s baseline (back-to-back, within noise)

## Pins moved (both with Takano-fidelity justification)
- `test_book_numbers_match_research`: instr 9585->9599, slots 1587->1592,
  longest 17->13. Direction longest-down (book max 13, Takano slots top
  at 10) plus mechanical consequences; exc/shortfall/rhythm/soft pins exact.
- `test_split_chunks_recurses_until_clean`: the wide-chunk residue pin
  (came back whole) now asserts a 2-chunk exact clean split.
- Modes HELD (not moved): Squat-70 mode stays 2, ClPull-80 mode stays 1
  (accepted structural per B2). `test_rendered_set_sizes_match_takano_centers`
  passes untouched.

## NOT landed / no resistance
Every splittable wide cell split; no cell resisted (the tightest, MS
11-cell, deals 6/5 legally above the floor). ClPull-80 mode 1 and zone
WIDTH capping remain hosting/quota work, out of scope for this seam.
