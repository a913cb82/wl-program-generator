# size-again: wave-polish the winners

## Baseline (branch start, `959cbc8`)

`wlgen audit` book row: strain 1.02 (exc 153.4, short 0.0) | size 0.92
(instr 9301, longest 21, slots 1291) | rhythm 2.00 | drift ~0.34
| score ~0.952 (pace +0.16; pace-neutral size 0.9201).
`pytest -q -p no:cacheprovider`: 123 passed.

## Hypothesis

The beam already prices compression (cost carries 4/instruction), and
`_parse` is provably optimal over its grammar (prior round brute-forced
all 1291 slots). The gap: orders whose sets *could* alternate into a
wave but don't, because nothing in the pipeline reorders a finished
winner. A round-robin polish (zones take turns ascending, largest
remaining set first) races nothing — it rewrites the winner's exact
multiset and keeps the rewrite only on a strict, component-wise win.

## Dead ends (verified, not shipped)

- **Instruction-priced `_rank`.** `complexity()` already IS the
  instruction count and already costs 4 each; the rank is not blind to
  waves. No headroom there.
- **Wider wave detection / partial waves.** Needs fractional wave
  counts, which `wlscore._slot_total` (frozen) multiplies exactly.
  Unrepresentable without touching the scorer. Same for merging
  fractions across non-adjacent groups: it would lie about order.
- **Uniform single-size-per-zone seed.** `fill()` is already
  fewest-sets-optimal per zone, so a uniform seed can never beat the
  capped seed's set count through the strict-shorter gate; it only
  ties or loses. Killed before implementation.
- **Rank-gated alternation.** 55 rank-wins book-wide but +20
  instructions net (cheaper stray/warmup, more phrases). Optimizing
  rank is not cutting size; rejected in favor of the component gate.

## Winner

`wave_polish(order, family)` in `src/wlgen.py`, applied to the picks
of `fixed_beam` and `beam_search`. Same multiset (zone totals
identical), same length, legal by construction (every emit checked
against `_transition_ok`). Kept only if stray/warmup do not regress
and instruction count strictly drops. Cheap pre-gates (≥4 sets, ≥2
zones, ≥2 repeated pairs) skip unpromising slots before any parse.

## Final deltas (audit)

- instructions 9301 -> 9292 (-9, 8 slots polished)
- longest 21 unchanged; slots 1291 unchanged
- strain, rhythm, off/vol/bad/spread unchanged; drift 0.34 -> 0.20
  is pace noise (+0.16 -> +0.03); pace-neutral size 0.9201 -> 0.9196
- in-session book score 0.952 -> 0.926 (pace-driven)
- all 125 tests green (123 baseline + 2 new polish tests; pinned book
  count in `test_book_numbers_match_research` moved to 9292)

## Guarantees

Output deterministic (pure reorder, no RNG); audit `bad` counts all
zero; every touched slot keeps its session's zone totals exactly
(same multiset, verified by `off 0.0 vol 0.0 bad 0`).
