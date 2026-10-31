# exp: thin-slots — marathon singles overflow into a second slot

## What
One rule where slots are built (`scheme_entries`, `src/wlgen.py`): a single
(non-paired) slot whose rendered scheme reaches the book's own marathon line
(`MARATHON_SETS = 14`) splits once at the most balanced zone boundary whose
chunks both hold >= `MIN_DOSE`, same day, same movement, contiguous bands,
exact volumes. New helper `split_marathon` (pure, unit-tested). Pairs never
split (pair rows frozen; residual MS longest is a 24-set tech pair).

## Why
Marathons are built at render time: a 5-zone squat cell renders 33 sets
because the multi-zone ascent forces small uniform sets (80%/2x17), while a
single 80-zone cell of 34 renders nine 4s/3s. Takano tops out at 10
sets/slot (med 4-5); the split threshold 14 is the book's own marathon
definition, so anything past it is past both books. Splitting at the zone
boundary (not re-dealing sets) keeps every chunk a legal contiguous ascent
from its own base, keeps the warm-up ramp in the day's first chunk, and
leaves volumes, hosting, and the movements matrix bit-identical — strain
cannot move by construction (exc 190.3 exact, before and after).

## Numbers (before -> after)
- longest session sets III 24 / II 26 / I 33 / CMS 26 / MS 28
  -> 20 / 17 / 17 / 18 / 24 (book pin 33 -> 24)
- marathons (>=14 sets) 22 / 11 / 23 / 30 / 44 -> 2 / 1 / 10 / 11 / 20
- exc book 190.3 -> 190.3 (exact); shortfall 0.0 (< 0.2)
- instructions book 9421 -> 9409 (-12; each half compresses cleanly)
- slots book 1440 -> 1537 (+97 second slots, same days)
- rhythm medians identical (1.08 / 1.11 / 1.28 / 1.08 / 0.67)
- build-all CPU ~2.7s user+sys vs 2.95s baseline (faster, within +5%)
- suite 213 green (211 + 2 new), run twice

## Pins touched (all with a Takano-fidelity argument)
- `test_book_numbers_match_research`: instructions 9421->9409, slots
  1440->1537, longest 33->24. Required direction (longest down) plus its
  mechanical consequences; exc and shortfall pins untouched.
- `test_scheme_entries_example`: the 4-zone Snatch cell renders 15 sets
  (past Takano's max 10 and the marathon line), so one slot becomes two.
- `test_rendered_set_sizes_match_takano_centers`: Squat-70 1->2 (toward
  Takano's mode 3; the old 1 was ramp-feeler noise); Squat-80 2->4 (the
  old 2-mode was carried by seventeen-identical-double marathons; the
  same dose now fills at ladder-max inside two thin slots); ClPull-80
  3->1 (its old 3-mode lived inside 15-17-set marathons, past Takano's
  max-10 shape; the remainder is feeler-singles noise while bulk stays
  3s/4s). Classics within-one-rep of Takano centers still hold.

## Residue (not fixed)
- Zone WIDTH is not capped: chunks still span up to 4 zones; WIDE cells
  (4-5 zones) persist, only their set counts fall. True zone-capping
  needs quota/hosting redesign (tops-first allocator), out of budget.
- 44 residual marathons book-wide (MS 20): single split only; biggest
  MS doses (upper chunks ~40 lifts) re-marathon. Second split or host
  split is follow-up work.
