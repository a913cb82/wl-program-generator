# Feasible-trim: skip max-flow on isolated demand

## Hypothesis
`_feasible` is ~19% of build tottime (profile below). Most `False`
answers are trivial: a demand row/column with empty support can never
be saturated. Answer `False` in the key-building pass and skip the
graph build + BFS. Gate: identical booleans ⇒ byte-identical
`outputs/*.json`, only pace may move. No `sum()` touched.

## Profile (cProfile, all five `build_plan`, ~3.1 s, this worktree)

| frame | tottime | share |
|-------|---------|-------|
| `_ipf` (1537 calls) | 1.031 s | 34% — untouchable per pace-hunt/r2-hotspot |
| `_feasible` (11976 misses) | 0.583 s | 19% — target |
| `sum` (mostly `_ipf`) | 0.501 s | 16% |

## Call census (spy on raw `_feasible`, full 5-class build, 21304 calls)

- True nontrivial: 7032; False: 14272
- Of the False: **9776 isolated** (demand row/col, empty support),
  4496 structural, 0 total-mismatch. So ~46% of all calls can skip
  max-flow with zero semantic change (necessary condition: no flow
  can cross an empty-support row/col, so max-flow returns False too).

## Change (`src/wlgen.py`, `tests/test_wlgen.py`)
- `feasible()` builds the 0/1 support key in one explicit pass that
  also tracks per-row/per-column support presence; returns False
  before `_feasible` when a demand row/col has none.
- Test (TDD, fixed twice — zero-demand rows/cols with empty support
  are feasible, only *demand* rows/cols trigger): isolated cases
  return False and match the brute-force oracle.

## Result
- `pytest -q -p no:cacheprovider`: 129 passed (128 + 1 new).
- `outputs/*.json` md5-identical before/after; `git status outputs/`
  clean after audit.
- Fresh-process A/B full build: 1.75/1.79 s → 1.53/1.56 s (~13% CPU).
- Audit: baseline book **0.886** (pace -0.17) → final **0.887**
  (pace -0.16). strain 1.02 / size 0.92 (instr 9292, longest 21,
  slots 1291) / rhythm 2.00 / spread 0.17 all identical.

## Verdict: HOLD (real CPU win, pace-term gain inside machine noise)
The skip is sound and wall-clock drops ~13% on every run, with
provably identical booleans and byte-identical plans. But the audit
pace term (-0.17 → -0.16) sits inside the box's ±0.1 noise band
(r2-hotspot saw the same on identical code), so no score gain can be
claimed. Keep iff a cheaper-per-call key builder is wanted; the
remaining `_feasible` share is structural max-flow, not skippable
by necessity checks.
