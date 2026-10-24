# polish-again: is wave_polish idempotent?

## Baseline (branch base, stack-1)

`wlgen audit` book row: strain 0.99 (exc 147.8, short 0.0) | size 0.92
(instr 9289, longest 21, slots 1282) | rhythm 2.09 | drift ~-0.16
| score ~0.847 (pace -0.32). `pytest`: 129 passed.

## Question

`wave_polish` cut 9 instructions in size-again. Is the polish idempotent,
i.e. does a second pass over already-polished winners find anything more?

## Probe (scratch script, full pipeline IR build)

Hooked `wave_polish` during a full `ir_with_slots(build_plan(cls))` build
over all classes (caches cleared first), then re-applied `wave_polish` to
each polished output and compared instruction counts via `scheme_cost`
with stray/warmup checked:

- unique winner inputs seen: 854
- first pass changed: 5 (instr 6195 -> 6189 at unique-scheme level;
  fewer than size-again's 8 slots because stack-1 changed the winners)
- **second pass changed: 0 / 854** (instr 6189 -> 6189, stray/warmup identical)

Unique-level fixed point implies slot-level fixed point (same pure
function over the same winner multiset per slot). No stray/warmup
regression possible: every second pass returned its input untouched.

## Verdict: NULL — do not wire in

Second pass strictly no-ops everywhere. Nothing to ship in `src/`.
Kept as regression guard: `test_wave_polish_second_pass_is_fixed_point`
(polished outputs are fixed points, complexity unchanged).

## Final

`wlgen audit` book: strain 0.99 (exc 147.8) | size 0.92 (instr 9289,
longest 21, slots 1282) | score 0.850 (pace -0.31; delta vs baseline is
pace noise, size/instrunes identical). `pytest`: 130 passed (129 + 1 new).
