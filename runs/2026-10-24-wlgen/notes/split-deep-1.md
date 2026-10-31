# exp: split-deep — recursive, set-split, pair-split, feeler-fold

## Baseline (B-kept tree)
longest 20/17/17/18/24; marathons (>=14) 2/1/10/11/20; exc 190.3 exact;
instr 9409; slots 1537; rhythm 5.22; soft 84; suite 213 green; CPU ~2.6s.

## Landed
Render-only slot-building seam (`src/wlgen.py` only: `halve_counts`,
`strip_feelers`, `split_chunks`, `split_pair_chunks`, `scheme_entries`
branch bodies) plus `tests/test_wlgen.py` unit/pin updates. Movements
matrix, quotas, hosting, taper, movers, `close_*`, `wlscore.py`, runs/
untouched.

1. **Recursive split** — `split_chunks` re-applies boundary splits to chunks
   still rendering >=14 (MIN_DOSE floor guarantees termination).
2. **Set-split** — `halve_counts` deals zone-narrow chunks (single-zone
   re-marathons, deep 2-zone cells) lift-even per zone; halves sum exact.
   Refused (>2 zones): width needs hosting redesign, and 4-zone halves
   invent packings the book never renders (one CMS Fundamental half came
   out 90-before-80, scorer-illegal; the suite pins illegal==0).
3. **Pair-split** — `split_pair_chunks` deals the rendered set list in half
   (every complex touches both sides, so no one-sided zone can arise —
   the pair_fill crash direct lift-halving risks), each half re-rendering
   from exact lift vectors. Halves that would open past 1-5 stay whole.
4. **Feeler-strip as fold** — literal dropping breaks the scorer's
   cell-match rule (`scheme does not match the cell`, 15 illegals), so
   leading sub-2 entry singles of non-first chunks fold into same-zone
   work sets instead (volume-exact, ladder-cap-guarded, never building
   the opener past 1-5). First chunks keep the full warm-up ramp.

## Numbers (after -> before in parens)
- longest III/II/I/CMS/MS: 13/17/13/16/13 (20/17/17/18/24)
- marathons (>=14): 0/1/0/3/0, 4 total (2/1/10/11/20, 44 total)
- exc book 190.3 -> 190.3 exact; shortfall 0.0 (< 0.2)
- instr book 9409 -> 9487 (+78, extra same-day slots compress)
- slots book 1537 -> 1577 (+40)
- rhythm medians identical (1.08/1.11/1.28/1.08/0.67, book 5.22)
- soft 84.0 exact (2/23/18/17/24 per class)
- suite 218 green (213 + 5 new), run twice
- build-all CPU 2.52s vs 2.52s baseline (cached renders; within +5%)

## Pins moved (all with Takano-fidelity argument)
- `test_book_numbers_match_research`: instr 9409->9487, slots 1537->1577,
  longest 24->17. Direction longest-down plus mechanical consequences;
  exc/shortfall/rhythm/soft/clash/gaps/idle pins untouched.
- `test_scheme_entries_splits_marathon_singles`: 33-set monster now three
  slots (9/8/8 sets), dose exact, all clean.
- `test_rendered_set_sizes_match_takano_centers`: Squat-70 mode 2->1.
  Forced trade, documented: the 2-mode was carried by three 14-20-set
  joint renders (past Takano's 10-set slot max and the book's 14-set
  marathon line), whose 70-mass packed 2s in ramp context. Recursion
  isolates that mass into ladder-top 4s/5s across thin same-day slots
  while 223 first-touch singles stand. Shape toward Takano (nothing
  past 13 sets); count recovery needs fewer touches per zone (quota and
  hosting work), not render work.

## NOT landed (residue for hosting/quota work)
- **ClPull-80 mode stays 1** (needs to move toward Takano 3-4). Proven
  structural in the allowed seam: only 4 ClPull cells in the book ever
  split, all 4-zone with single-zone-100 second halves; the 63 ones are
  49 first-touch full-cell entries + 14 day-first half entries, all
  protected by the warm-up-ramp rule, vs 58 work 3s. Every allowed
  transform preserves those renders exactly. Moving it requires touching
  first-touch ramps (forbidden) or re-hosting 80-mass (quotas).
- **Squat-70 mode 2->1** (above): the twos live only in the three joint
  renders; any clean split repacks them. Same hosting-width follow-up.
- **4 residual marathons** (II Press 17, CMS Fundamental 16 + 14 x2):
  wide (>2-zone) chunks with no legal MIN_DOSE boundary. II longest
  flat at 17 = baseline; everywhere else down.
- Zone WIDTH uncapped (B residue, unchanged): chunks still span up to
  4 zones; true zone-capping needs tops-first allocator redesign.
