# Longest cut (research/longest-cut)

## Baseline
- `.venv/bin/wlgen audit`: book score **0.907**, instr **9301**, longest **21**, slots 1291.
- `pytest -q -p no:cacheprovider`: **123 passed**.
- (Lead's brief cited 0.927 / 9312→9292; live audit in this worktree reads 0.907 / 9301. Treat the audit output above as baseline.)

## Hypothesis (one shot)
The 21-set maxima are single-movement slots whose zone totals are split into
many minimum-size sets. Repacking runs of the same zone into the largest
ladder-legal sets — keeping zone totals, zone visit order, and session vols
identical — should cut `longest` with the smallest blast radius (no change
to the general scheme/beam machinery).

## Where the 21s live (from outputs/*.json)
- **I, Prep 3-1, week 0, session 2 (L, vol 130), Fundamental**: zone totals
  `[1,4,12,11,6,1,2]`, 21-set seq, ends `…[110,1],[110,1],[80,3],[70,1]`.
- **CMS, Prep 3-1, week 0, session 2 (L, vol 130), Fundamental**: zone totals
  `[2,4,15,9,3,1,3]`, 21-set seq, ends `…[110,1]×3,[60,2],[70,1]`.
- **MS, Comp 2, week 1, session 1 (L, vol 146), Other Snatch**: 21-set seq
  starting `[60,3],[70,3]×8,…` (already uses one `wave ×2` mid-slot).

## Why packing works here (not attempted — budget over)
- Fund ladder allows 70:(5,4,3,2), 80:(4,3,2), 90:(3,2); e.g. the I-slot's
  70-zone (12 reps in 7 sets: 1+5×2+1) packs to 5+4+2+1 (4 sets), 80-zone
  (11 in 5 sets) to 4+4+3 (3 sets), 90-zone (6 in 3×2) to 3+3 (2 sets):
  21 → ~16 with identical zone totals and identical zone order.
- Climb rule (`_transition_ok`: reps must not rise on a climb) favors packing
  lower zones ≥ upper zones, which this direction satisfies; drops/waves stay free.
- Instructions (`_count`: groups + ×N suffixes) fall when groups merge, so the
  size term `(instr/9300 + longest/25)/2` improves on both halves; slot count
  is untouched (no split), so no `slots`/clash side effects.
- Hook point: a post-pass over `session_slots` output in `ir_with_slots`
  (src/wlgen.py:2710), applied only to slots with `len(seq) > 20`, merging
  same-zone runs via the movement family's `REPS` ladder. Test first:
  reproduce the 21 (assert max `len(seq)`), then assert same per-zone rep
  totals, same zone order, `len(seq) ≤ 16`, and `illegal == 0` under wlscore.

## Verdict
No code change made — budget expired before a TDD cycle could be completed
safely. Tree left clean; general scheme machinery untouched.

## Final
- audit after: book **0.907**, longest **21** (unchanged).
- pytest: **123 passed**.
