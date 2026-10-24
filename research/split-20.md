# Split-20 (research/split-20)

## Baseline (live audit, this worktree)
- `.venv/bin/wlgen audit`: book **0.932**, instr **9292**, longest **21**, slots 1291.
- `pytest -q -p no:cacheprovider`: **128 passed**.
- (Lead brief cited 0.897; live reads 0.932. longest-surgical's 0.885 also stale —
  book drifts per machine via the pace term; quality terms match.)

## Audit: the len>20 map (unchanged from longest-surgical)
- 4 slots at 21 sets: I Prep 3-1 wk0 sess2 + wk2 sess3 (Fundamental),
  CMS Prep 3-1 wk0 sess2 (Fundamental), MS Comp 2 wk1 sess1 (Other Snatch).
- Longest-surgical showed order-preserving repack is infeasible
  (`_transition_ok` flat-or-fall + ladder caps) and recommended a post-pass
  split: one long slot -> two same-movement slots, longest 21 -> ~11,
  claimed "score-free except +1 group phrase in instr".

## Finding: the split is illegal — scorer checks every entry vs its cell
- `wlscore._entry_problems`, single-group case:
  `if _slot_total(items) != sum(session["movements"].get(g, []))`
  -> `"{text}: scheme does not match the cell"`.
- Each split half prescribes half the reps, but each half is checked
  independently against the FULL cell. Both halves always fail; 4 splits
  would add +8 `illegal` to drift `bad`. Same for paired halves
  (checked against the summed pair cell).
- Halves under different movement names fail harder (cell lookup misses).
- Moving dose across sessions/groups would keep cells matched but changes
  the program itself (strain, gaps, hosting) — not a post-pass, out of budget.
- Side note: even if legal, `_count` is additive over items, so instr
  would at best hold flat; only the longest/25 term would pay.

## Verdict
No code change — the recommended shot is infeasible under the frozen
scorer (which must not be edited). One regression test added docs the
blocker. Tree left with tests + this note only.

## Final
- audit after: book **0.932**, longest **21** (unchanged).
- pytest: **129 passed** (128 + 1 split-20 probe).

## Test
- `tests/test_split20.py::test_post_pass_split_halves_rejected_by_cell_match`:
  takes a live len>20 single slot, splits its seq at the middle,
  asserts both halves trip "does not match the cell".
