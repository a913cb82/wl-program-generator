# Worklog

One entry per round. Never edit an old entry.

## 0 — setup (2026-10-24)
- commit: 215004c (stack-1)
- score: exc 144.7, 136 green
- best: exc 144.7
- verdict: keep
- what changed: run folder, EXAM, STRATEGY, IDEAS, QUEUE, PROGRESS seeded
- what learned: noise floor 0.008 score / 0.03 pace, 6 repeats one box
- next: snatch-spill-5, cms-snatch-spill (blind-gate protocol starts after they land)

## 1 — Other Snatch spill line stopped (2026-10-24)
- commit: 215004c (stack-1, unchanged)
- score: exc 144.7 (no move, 3 rounds)
- best: exc 144.7
- verdict: drop the line (4 neutral/dropped in a row: MS/I/CMS)
- what changed: singles-host filter holds zero defects but finds no exc-positive move
- what you learned: singles pools are dose-balanced; only Fundamental (dense peaks) spills
- next: pace-prof; I Other Clean priced out (ceiling ~2)

## 2 — pace-prof null (2026-10-24)
- commit: 215004c (unchanged)
- score: exc 144.7, pace -0.33 -> -0.31 (noise)
- best: exc 144.7
- verdict: drop (top self-time fns memoized with unique args; nothing safe to cut)
- what changed: nothing (2 memo probes reverted)
- what you learned: audit CPU is all unique-arg calls; pace floor is structural
- next: jerk-spill, then stop the loop if neutral (5th miss in a row)

## 3 — jerk-spill neutral, LOOP STOPS (2026-10-24)
- commit: 215004c (unchanged)
- score: exc 144.7 flat, I rhythm 3.09 flat, zero defects
- best: exc 144.7
- verdict: drop; stop the loop (queue empty of open ideas + 5 neutral rounds in a row)
- what changed: nothing (clean no-op, reverted)
- what you learned: spill family exhausted 5/5 on non-Fundamental; singles pools are dose-balanced
- next: restart only on a bold new design (3-try budget): paired-84%% needs a new mechanism

## 4 — loop reopens BOLD x5 (2026-10-24)
- commit: 215004c (unchanged)
- score: exc 144.7
- best: exc 144.7
- verdict: trying (stop lifted: 5 fresh lines, box idle)
- what changed: 5 parallel probes (bulk spill, MS timing, pair-volume trim, per-class T, rhythm pricing)
- what you learned: compute was idle; fill the share
- next: harvest any, stack winners

## 5 — ms-timing stacked, 4 relaunches (2026-10-24)
- commit: ff3692c (stack-1)
- score: exc 142.5, 138 green
- best: exc 142.5
- verdict: keep (verified: MS 40.3, rhythm 2.91, 2-line change)
- what changed: MS week-vol rotation; harvested 5 notes
- what you learned: discovery must be priced into the budget or done by me
- next: fund-bulk-2, pairvol-trim-2, perclass-T-2, fold-thu

## 6 — perclass-T rejected on book, gate fixed (2026-10-24)
- commit: ff3692c (stack-1, unchanged)
- score: exc 131.0 claimed but book 0.839->1.046 (pace +0.82)
- best: exc 142.5
- verdict: reject (book regressed; my exc-only gate was the bug)
- what changed: EXAM gains a book-gate rule; exc-only gates banned
- what you learned: more days = more CPU, structurally; strain gains can't repay pace at 0.2 vs 0.4 weights unless 4x
- next: lean-3, lean-2 (inverse bet on lean classes, book-gated)

## 7 — day-count line dead both directions (2026-10-24)
- commit: ff3692c (stack-1, unchanged)
- score: exc 142.5 flat (both probes 153.1, reverted)
- best: exc 142.5
- verdict: drop the line (I+1 pace-killed; III/II-1 strain+pace loss)
- what changed: book-gate held (both failed all four conditions)
- what you learned: concentrating lean weeks spikes strain AND pace; the thesis inverted
- next: shapediff recon (borrowable demand features, not transplants)
