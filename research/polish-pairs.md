# polish-pairs: null result (budget over)

## Baseline (branch `research/polish-pairs`, stack-1 + size-again)

`wlgen audit` book row: strain 1.02 (exc 153.4) | size 0.92
(instr 9292, longest 21, slots 1291) | rhythm 2.00
| score ~0.883 (pace -0.18; pace noise vs the 0.897 quoted at stack-1).
`pytest -q -p no:cacheprovider`: 128 passed.

## Finding: pairs are already polished — premise void

`wave_polish` is applied inside BOTH `fixed_beam` (return path) and
`beam_search` (return path) in `src/wlgen.py`, with no single/pair
branching. `best_pair_scheme` routes through exactly those two
functions, and `scheme_entries` sends every stored/detected pair
(SnPull+Snatch, Clean+Jerk) through `best_pair_scheme`. So pair
complexes were never excluded from the polish; the "never polished"
lead was wrong. There is no separate two-sided path to add the
round-robin to — it already runs there under the same strict gate
(strict instruction cut, identical zone totals, no stray/warmup
regression).

## Probe (inconclusive, time-box hit)

A monkeypatch-count probe around `W.wave_polish` during `build_plan`
recorded zero calls — expected in hindsight, since schemes render in
`session_slots`/`scheme_entries` at audit time, not in plan build.
No follow-up probe was run; budget expired before testing whether the
existing polish ever *fires* on pair orders (gate preconditions:
>=4 sets, >=2 zones, >=2 repeated pairs).

## Verdict: NULL — no change, no rewrite

No source or test changes. If pairs never alternate into waves it is
because the shared gate rejects them (transition legality via
`_transition_ok` on tuple atoms, or no strict instruction cut), not
because the reorder never runs. Any future attempt should instrument
`wave_polish` hit rates by order kind (single vs pair) during a full
audit render — that is the 5-minute experiment this session failed
to run.

Final: book score ~0.883 (pace noise), size 0.92 (instr 9292),
128 green. Unchanged from baseline.
