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

## 8 — scorer upgraded, stack rebased (2026-10-24)
- commit: 5bc35c5 (main), stack-1 merged
- score: exc 142.5 flat, drift +69.8 (14 bin gaps x5), 140 green
- best: exc 142.5, gaps 14 (I 12, MS 2)
- verdict: keep (bin gaps are true comp holes: 90 with no 80)
- what changed: _bin_gaps at 3 levels; rep-memory tried and dropped (815 flags vs ladder design)
- what you learned: widening ladders are intentional (c51d889); the scorer must not defect them
- next: fill the 14 comp holes (generator work, strain-neutral?)

## 9 — Takano-calibrated scorer, stack rebased (2026-10-24)
- commit: 7f5e254 (main), stack-1 merged green (145)
- score: exc 142.5 flat; drift prices 75 hard openers + 14 bin gaps
- best: exc 142.5, gaps 14, hard openers 75 (all Squat@50% x6-10)
- verdict: keep (opener rule Takano-unanimous; climb relaxation deletes a false ban)
- what changed: _step_ok frees climb rises, pair guard is flip-only, opener>5 defect
- what learned: ruler banned Takano's own ramps; unpeaked-rise parked (550 us vs 1 Takano)
- next: narrow Squat openers (generator), fill 14 bin holes

## 10 — Softness pass + week gaps dropped (2026-10-24)
- commits: 56138fe (soft), 719ad13 (week gaps), stack-1 green (146)
- score: exc 142.5 flat; drift 81.9 -> 21.9; bad 2 (both meso-level, Takano-dirty)
- verdict: keep both (Takano-measured, simpler scorer)
- what changed: opener defect -> soft degree x0.05; week _bin_gaps call deleted
- what learned: Takano weeks hole bridges 44/57; mesos/macros 0 holes; his rhythm 5.4 vs our 2.09
- next: narrow Squat openers (soft 240), fill 2 I meso holes, rhythm ideal question

## 11 — 7-day wave rhythm with real weekdays (2026-10-24)
- score: exc 153.4 flat; rhythm 2.00 -> 2.45 (his weeks score 0.07)
- verdict: ship (separation validates: his 0.07 vs ours 2.45)
- what changed: sessions carry weekday (his modal layouts), rhythm = contrast vs per-count ideal + missing turns, multi-peak free
- what learned: his contrast grows with day count (1.6/2.3/2.3/2.4); Monday peaks 86%; Sunday never trains
- next: close the contrast gap (ours 3.0 vs his 1.6-2.4)

## 12 — Weekdays are plan data (2026-10-24)
- verdict: keep (modal table deleted; even Mon-Sat spread; JSON carries days)
- what learned: same vols in Mon-Fri vs spread score identically (0.081) -
  the wave prices order and contrast, not the calendar. His Mon/Tue
  back-to-back heavies (69->110) support no adjacency penalty.
- next: adjacency pricing only as new theory with his-data support

## 13 — Rhythm as a floor, not a shape (2026-10-24)
- verdict: keep (his median 0.00, ours 0.00; only flat weeks pay)
- what changed: per-count ideals deleted; 7-day movement vs 0.3 floor + sparse turns
- what learned: 7-vector turns punish his 5-day run-descents; sparse turns do not.
  Floor 0.3 sits below his flattest week (0.42), above a flat block (0.17).
- next: rhythm is a guardrail now; steering moves to strain/size/drift

## 14 — JSON is class plus sessions (2026-10-24)
- verdict: keep (HTML byte-identical, all pins hold, file halved)
- what changed: to_ir strips to sessions; from_ir rebuilds rich; _parse moved to wlir
- what learned: paired-collapse in movements is not recoverable from slots,
  so movements and pairs stay in the file; the @cache on _parse is load-bearing
- next: scorer reads class ground truth tables (done: nominals from CLASSES)

## 15 — Truth-priced nominals kill invisible hacks (2026-10-26)
- verdict: reverted ms-timing rotation on the stack (exc 142.5 -> 144.7)
- what learned: the rotation only won because nominals followed stored vols.
  Against ground truth tables it prices +1342 drift. Timing shifts belong
  in the tables, not in generator code.
- next: table-driven timing experiments replace code rotation hacks

## 16 — Intensity wave joins the scorer (2026-10-26)
- verdict: keep (his ex-taper A 0.028-0.041, ours 0.002-0.012, floor 0.02)
- what changed: rhythm gains fitted-amplitude shortfall; wlwaves.py ships
- what learned: weekly volume sines fit nothing (R2<=0.1); alternation depth
  hits his own weeks at zero; T=2 sine is singular on integers.
  The floor beats waves for presence; waves score intensity shape.
- next: volume waves wait for generation; taper shape unpriced

## 17 — Zeros out of rhythm (2026-10-26)
- verdict: keep (rest as gaps, not zeros)
- what changed: movement floor now per training day (0.10, his min 0.113);
  new rest-before-heavy median price (his plan medians +0.4..+0.6, ours -0.45)
- what learned: movement scales with rest days (3-day 2.0 vs 6-day 0.9),
  so the old floor priced schedule; load curves smooth away shape (our
  weeks fit sines better than his); dose x preceding-gap median splits
  +0.77 vs -0.45 with his odd weeks rescued by the median; T=2 sine is
  singular on integer days
- next: CMS/MS program parse for level-vs-program diff curves

## 18 — Taper slack stays home; days gain character (2026-10-26)
- verdict: keep (meso conservation exact: III +5/+5, MS +6/+7)
- what changed: taper_topup hands week-4 90s to weeks 1-3 of Comp 2
  (m-level for pairs preserves tier ratios; per-session reinforce for
  singles); zone_alloc peak 0.8 fits his 1.12x top concentration
- what learned: fixing taper semantics first (raw vs shifted cost a
  test each); pair splits quantize single 90s away (ratio rounding);
  m-column edits after ra/rb are dead code; build_plan cache poisons
  counterfactual tests (use __wrapped__); integer topups go
  winner-take-all across channels
- next: exc 160.9 (+5%: 3.9 required slack + 3.6 honest heavy days)

## 19 — Phase-keyed spread: prep gathers, comp spreads (2026-10-30)
- verdict: keep (book 5.560 -> 5.426; I prep 1.154 vs his 1.16, comp 1.023 vs his 0.98)
- what changed: PHASE_PEAK prep 2.0 / comp -0.3 threads into unpaired
  (zone_alloc) and paired (pair_zones) priors; close_session fills lone-top
  gaps at 90+ from the session's own top; close_week fills week holes from
  unpaired tops (paired render vectors untouched)
- what learned: priors move zone_alloc-level concentration 1.02 -> 1.24
  but final bins plateau near 1.13 (repairs dominate); machinery has a
  natural 1.1 floor so comp needs a negative peak to reach 0.98; thin
  spreading strands lone 100s (session gaps) that only an own-top cascade
  fixes; +0.17 shortfall is the priced cost of starved thin tops
- next: Narrow Squat openers (soft driver); fill 2 I meso holes

## 20 — Taper topup spreads onto light days (2026-10-30)
- verdict: keep (comp III 0.980 -> 0.972, II -> 0.972, I 1.023 -> 0.994;
  book 5.426 -> 5.418, instr -1, all else pinned)
- what changed: spread_extra deals 80-holders fewest-tops-first (was
  90-holders first); paired path untouched (its units-proportional split
  is concentration-neutral, take_up_slack's 90-vs-100 pick never moves
  the >=90 metric)
- what learned: topup runs Comp2 only so the fix touches comp alone;
  extras are 1-3 lifts, so the lever fades in big weeks (CMS comp 1.052,
  MS comp 1.143 unmoved) where his programs give no ground truth anyway;
  remaining comp concentration lives in repair demotion (guarantee
  change, not attempted)
- next: Narrow Squat openers (soft driver); fill 2 I meso holes
