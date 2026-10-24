# Longest surgical (research/longest-surgical)

## Baseline (live audit, this worktree)
- `.venv/bin/wlgen audit`: book **0.885**, instr **9292**, longest **21**, slots 1291.
- `pytest -q -p no:cacheprovider`: **128 passed**.
- (Lead brief cited 0.897; live reads 0.885. Map in longest-cut.md also stale, see below.)

## Re-map: the 21s moved (4 slots, not 3)
- I, Prep 3-1, wk0, sess2 (L130), Fundamental: 21 sets, ends …[110,1]x2,[80,3],[70,1].
- I, Prep 3-1, wk2, sess3 (M102), Fundamental: 21 sets, ends …[100,1],[110,1]x2.
- CMS, Prep 3-1, wk0, sess2 (L130), Fundamental: 21 sets, ends …[110,1]x3,[60,2],[70,1].
- MS, Comp 2 (mesos[4]), wk1, sess1 (L146), Other Snatch: 21 sets,
  `[60,3],[70,3]x8,[70,2],[80,2],[70,2],[80,2],[90,1]x5,[100,1],[60,2]x2`.
- Live 20s (untouched): I wk0 sess1 slot3 (20), CMS wk2 sess3 slot2 + wk1 sess1 slot0 (20).

## Key finding: packing cannot take longest below 21
- Fund ladder (70:(5,4,3,2), 80:(4,3,2), 90:(3,2)) looks packable, but
  `_transition_ok` forces reps flat-or-fall on every climb AND within a zone.
  E.g. I-slot climbs [60,3]->[70,…] so all 70s are ≤3, last 70 ≤2 forces all
  80s ≤2, and 80-total 11 cannot fill from {2} (needs a 1, not ladder-legal).
  Order-preserving repack to fewer sets is infeasible under exact zone totals.
- MS slot is already zone-minimal: Snatch ladder caps 70 at 3, 90 at 1, so
  60:7->3 sets, 70:28->10, 80:4->2, 90:5->5, 100:1->1 = 21. Irreducible.
- Only a **split** (one slot -> two same-movement slots at a drop boundary)
  cuts longest here: same set multiset (zone totals exact, legality preserved
  as subsequences), longest 21->~11 per split slot. wlscore `size` ignores
  `slots` count, so splits are score-free except +1 group phrase in instr.

## Verdict
No code change — recon consumed the budget (map was stale: 4x21 + new
locations + legality analysis). Tree left clean. Recommended next shot: TDD a
post-pass split of slots with len>20 in `session_slots` (`src/wlgen.py:2759`),
cut at the drop nearest the middle; assert same zone totals, legal halves,
max len<=11, illegal==0; expect longest 21->20 (three 20s remain — extend the
rule to >=20 for 21->18/19 if blast radius allows).

## Final
- audit after: book **0.885**, longest **21** (unchanged).
- pytest: **128 passed**.
