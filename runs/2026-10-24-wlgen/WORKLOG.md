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

## 21 — Takano programs saved in our JSON format (2026-10-30)
- verdict: keep (fixtures render + score; all 177 green, mypy/ruff clean)
- what changed: src/takano.py converts the parsed PDF dump
  (tests/fixtures/takano_prog.json) to tests/fixtures/takano-{III,II,I}.json
  in our schema; map table auditable in-repo; zones floored to grid;
  X zones inferred by reps; single+pair coexistence accounted in scorer
  (no-op for our plans: 160 untouched green)
- what learned: his "&" is per-side for complexes ([2,1]) but consecutive
  sets for singles; OCR needs paren-aware splitting + %N repair; max work
  becomes 90-singles; his illegals under our rules are all genuine (84
  oversize assistance sets, 19 wide C&J ratios in I); clash/idle on his
  files are grid artifacts, illegal/gaps/soft are signal
- next: Narrow Squat openers (soft driver); fill 2 I meso holes

## 22 — Reviewer-found converter bugs fixed (2026-10-30)
- verdict: keep (4 agents: III/II/I/source; converter now matches
  independent reimplementation on all 1177 I exercises, 0 mismatches)
- what changed: wave regex no longer spans missing-comma gaps
  ([^()]*); absurd reps >10 drop loudly (kills the 302-phantom);
  trailing stray tokens strip instead of wiping the group; %/, and
  missing-% repair with log; ": " removed before name match
  ("Snatch: Extension:" -> SnPull, backed by 13 identical shapes);
  unbalanced-open chunks repeat the whole chunk (tally-arbitrated
  9 sets, not 5); space-split respects paren depth
- what learned: tallies arbitrate ambiguous parses (first number =
  exercise lifts: 18 confirmed the wave-x3 reading); reviewers'
  stale expectations need re-reading after a fix (their 302-accept
  and literal-Snatch both differ by design now); source dump itself
  is incomplete (~150 lines + 70 tails missing upstream of the
  converter: dropped MS W7, mis-attached II W9, 52 max lines)
- next: upstream source recovery (PDF-parse gaps); Narrow Squat
  openers; fill 2 I meso holes

## 23 — I key split into I/CMS/MS/MSIC; visual screenshot review (2026-10-30)
- verdict: keep (6 fixtures, 183 green; 3 visual agents PASS, 0 conversion errors)
- what changed: split_programs cuts the lumped I key at week-n restarts
  (I 12w, CMS 12w, MS 17w, MSIC 17w); MSIC rides the MS grid + program key;
  review renderer bypasses the 20-week grid so all weeks screenshot
- what learned: visual review caught one systematic scratch-renderer bug
  (Lifts column shows day-aggregates on duplicate-name rows; schemes +
  fixture correct, cosmetic only); tallies arbitrate ambiguous parses;
  mid-audit fixture churn is survivable when agents capture evidence early
- next: upstream source recovery (dropped MS W7, mis-attached W9, 52 max
  lines); Narrow Squat openers; fill 2 I meso holes

## 24 — Upstream source recovery: all five loss classes fixed (2026-10-30)
- verdict: keep (183 green; 6 fixtures reconverted; tally audit clean)
- what changed: rewrote the PDF-dump parser (runs/2026-10-24-wlgen/takano_parse.py):
  tolerant week/day headers (parens, reps, missing dashes, bare rest days
  with continuity + lookahead guards against volume-table prose), week-9
  split for Class II, wrap-continuation joining, slashless max lines kept,
  Sunday/rest empties skipped; converter: max-attempt reading, triple map
  entries, unclosed-paren + max03 handling
- what learned: max-N are attempt labels not counts, proved by tallies
  (Snatch 15 = 6 work-up + 9, C&J 30 = 12 + 18; work-up singles unknowable,
  counted 0); recovered MS W7 is tally-exact (ours == tally sums, day plans
  stale: 380 vs 395); full tally audit over 1530 lines: 10 overs all
  source-side (7 tally typos on unambiguous text, 1 Good-Morning tally
  convention, 2 repeat-count disagreements, text followed throughout);
  recovered-week B/C chains hold except source typos; triples fully counted
  (pair legs + single, pair stays outside our pair table by design);
  CJ/Snatch grids are deliberately coarse 10-point bins (85 floors to 80)
- next: Narrow Squat openers; fill 2 I meso holes; table-driven volume work

## 25 — Visual audits found 3 dropped-line classes; all fixed (2026-10-31)
- verdict: keep (186 green; 7 fixtures reconverted; tally audit clean)
- what changed: four visual agents audited every txt line vs fixture rows
  vs renders (III PASS 107/107, II found Day 40 missing, I found D10/wraps,
  CMS-MS found 6 semicolon lines + colon-less line, MSIC FAIL only on 1
  scheme question + 5 stale headers from mid-audit churn). Three new
  separator classes fixed in the PDF-dump parser (runs/.../takano_parse.py):
  no space after "N)" (Day 40, C1 W1 D4, 7 MSIC lines, CMS D81), semicolon
  separators (III D39, 5 CMS lines), colon-less known-name lines (MS W2
  D13 halting deadlift); APPENDIX gate stops the 444-line author log from
  matching the loosened pattern. Converter fix in src/takano.py: semicolon
  normalizes to colon before name matching. 10 recovered lines land in 10
  sessions (II +1 session Day 40); each verified by exact slot-seq match
  against its txt scheme
- what learned: each pin move traces to a real source line, never to
  converter drift (I clash +1: C1 W1 D4 Push Press completes a 7-movement
  day no template covers; CMS illegal +1: Good Morning (X/5)4 exceeds our
  Fundamental cap; MS clash +1: halting deadlift adds ClPull; CMS gaps
  3->2 and idle 86->84: added lifts fill holes; III idle 114->113 likewise).
  MSIC Day 3 #6 (75%/4)5 -> 80 is correct: SnPull ladder starts at 80,
  "below-grid folds to base" (agent assumed a 70 rung that does not exist).
  Fresh screenshots are viewport-capped at 12000px but every page is
  shorter, so all weeks are visible; screenshot bytes are deterministic per
  HTML. Pre-existing lint debt unchanged (5 ruff + 4 mypy on HEAD)
- next: Narrow Squat openers; fill 2 I meso holes; table-driven volume work
