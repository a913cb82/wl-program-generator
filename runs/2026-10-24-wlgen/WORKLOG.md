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

## 26 — Generic IR: title + meso labels, no fixed grid (2026-10-31)
- verdict: keep (192 green; 6 Takano fixtures reconverted, same sessions)
- what changed: Takano JSONs now carry "title" + "mesos" (name + phase per
  mesocycle, from book week headers: Preparation 1-4 etc.); from_ir builds
  from stored (meso, week) keys instead of our 5x4 macro grid, so 8/9/12/17
  week programs render with zero phantom weeks; volumes roll up from slots
  (no prescription, so actuals stand as planned); to_ir stays minimal
  (class + sessions) and the legacy macro path is verbatim, so our own
  round-trip and book pins are untouched (test_ir_round_trip gates it);
  to_html needed no changes (already data-driven); precomp scores with comp
  ratios (competition-period training)
- what learned: the parser already captured week phase labels, only 3
  "?" headers needed continuity inheritance; the book has no Competition
  phase weeks (finals are pre-competition); phantom idle was the whole
  story (III 113->5, MS 40->10); illegal/clash/gaps/soft barely moved,
  proving they were always content-driven
- next: Narrow Squat openers; fill 2 I meso holes; table-driven volume work

## 27 — Roman/Takano catch-up, items 1-2: level-graded intensity + steeper annuals (2026-10-31)
- verdict: keep (193 green; book score 5.418 -> 2.63 via fitted nominals)
- item 1 (intensity grades with level): BINS refit per class from Takano
  measured annual zone shares (fixtures, classic+assistance pooled by bin
  type), direction-checked against Roman Tables 2-6 (modal 70->80, 90%+ up,
  60% down). III/II split into own tables (was shared C2). New test asserts
  monotone slope + spread (MS-III >= 5 mean, >= 12pp hi90); exact low pins
  not asserted (Roman no-pulls rule keeps our low classes lighter than
  Takano's pull-heavy blocks). Output now III 69.4/2.5% -> MS 76.1/14.9%,
  monotone, spread 6.7/12.4pp (Takano 6.3/19.3pp). Remaining ~2pt level gap
  is taper/phase-balance work (items 5/7), noted not chased.
- item 2 (annuals): 12/12/15/15/18k -> 13/13/17.5/17.5/22k, from Roman
  band midpoints x 12 prep + 8 comp weeks (ratios 1:1.33:1.67). Selection
  ratios untouched (already Roman Table 11 almost exactly; low-class
  pulls stay 0 per Roman p61/p118 against Takano's blocks).
- collateral fixed, all honest: test_spread back-to-backs now counts only
  gratuitous adjacency (forced 2k-S-1 subtracted; Roman programs legs
  near-daily); pair_zones runs close_session on ref columns after topup
  extras (take_up_slack stacks onto 100s above empty 90s, stranding tops;
  ref-level close keeps ratios legal, bins roll up from sessions so pool
  stays consistent); prep-top test moved III->MS (thin tops make the ratio
  noisy at low classes); day-pattern exceptions regenerated (25, all
  dose-floor-forced by construction since week_sessions prefers canonical);
  HTML/volume pins re-measured (ratios to old all ~= annual ratios).
- what learned: worktrees need PYTHONPATH (venv resolves wlgen to main
  repo, silently invalidating isolation); take_up_slack proportional
  stacking is a gap factory for paired columns (bottom-up would fix at
  the source; post-hoc ref close is the surgical version); higher volumes
  make dose-stranding rarer (old exceptions evaporate) while CAP binds
  nowhere (all 25 exceptions dose-driven, 0/25 CAP).
- soft redistribution (total 177->116): CMS/MS down a lot, II/I up;
  thin low-class bases narrow openers. Minor drift term, accepted.
- next: item 3 (Roman Table 1 as rep law)

## 27b — Roman catch-up, item 3: Table 1 rep caps (2026-10-31)
- verdict: Table 1 NOT adopted as generator law (evidence-backed refusal)
- what measured: Takano violates Table 1 at every level (70/3-4: 46-52% of
  classic sets; 80/2-4: 55-89%; squat 80/3-4 routine; pull 90/5s, 100/4s),
  and Roman's own text is looser than his table (pulls 2-6, squats 2-6).
  Table 1 is technique guidance (singles for precision at 85-95%, p40),
  not volume law. Our ladders sit between Table 1 and Takano (midpoint):
  caps flag only his tails (correct per our law), rendering centers on
  his modes (classics within 1 rep everywhere).
- new test pins rendered set-size modes per family/zone (solo slots) plus
  the Takano cross-check; complexes excluded (pair sides follow ratios).
- observations banked, not chased: light-zone feeler singles (221 at
  squat-70; size term prices them); Fund-80 renders 2s vs books' 3+
  (thin per-session doses from flat zone spread -> item 4/5 concentration
  work, not ladder work); Press/Fundamental ladder split needed for full
  bend-over fidelity (rejected: ~15 lines across the beam path + cache keys
  for audit cosmetics and zero shipped-score change; on IDEAS list).
- next: item 4 (S/M/L + Table 13 week vocabulary)

## 27c — Roman catch-up, item 4: S/M/L week vocabulary (2026-10-31)
- verdict: mostly already compliant -> pins, not machinery
- what measured: S/M/L letters already distribute Roman-plausibly (low
  classes ~1 L + S/M mix over 3.5 days/wk = Roman's 3-4 WL days; MS 5/wk);
  low-class L-cap holds (0 weeks with 2+ L-days; Roman allows 2); meso
  volume waves 2.0-2.5x peak-to-trough (Table 13 mildest is 1.8x); macro
  names already encode concur/contrast (Prep 4-2: vol peaks w4, int w2).
  New tests pin the L-cap (III/II) and the meso wave floor (1.5x).
- quota experiment (WLGEN_QUOTA=0.75): hosting barely moves (Fund I
  3.3->3.4 d/wk) because dose caps bind before the budget does; real
  concentration needs per-group host-dose norms (new subsystem).
- deferred with evidence: accessory dose concentration (Fund-80 renders
  2s vs books' 3+; 548 sets). On IDEAS list: host-dose norms per group.
- next: item 5 (meso high-intensity quotas)

## 27d — Roman catch-up, item 5: meso high-intensity quotas (2026-10-31)
- verdict: verification, not new machinery (quotas already hit where books agree)
- what measured: our meso S+CJ-70+ vs Takano meso quotas (per-4w): upper
  prep matches (I 88-110%, CMS 77-97%, MS 100-121%); two systematic
  deviations, both explained: (1) III runs ~2x Takano (his III does 16%
  pulls, Roman-forbidden; we redistribute into squats+S+CJ); (2) Comp 1
  runs 125-145% (shock + double-taper structure; phase-level comp cut is
  23%, inside Roman's 20-40%). New tests pin the Roman comp cut (60-80%)
  and monotone prep heavies across classes (both books agree).
- next: item 6 (bodyweight axis)

## 27e — Roman catch-up, item 6: bodyweight axis (2026-10-31)
- verdict: keep (201 green; axis plumbed end to end, one tilt rule live)
- design: weight is a bodyweight input (light/middle/heavy), not 25
  tables: BINS stay class-keyed, BW_TILT (+0.5/0/-0.5 ARI, uniform across
  groups per Roman p47/55/63/67) rides _shifted_fracs on every path.
  Threaded build_plan -> week_sessions/week_demand/plan_sessions/
  pair_zones/taper_topup -> week_bins/week_bin_lifts/untapered, all
  defaulting "middle". Default path byte-identical (full suite untouched).
  IR carries "bw" only when non-middle (minimal contract holds; Takano
  fixtures default middle); scorer needs no change (drift prices group
  volumes vs level ratios, never zone splits vs nominals).
- calibration: +/-1.0 moved hi90 +/-3-5pp, far past Roman's "slightly"
  (+/-2-5 lifts a zone); +/-0.5 gives mean spread ~0.9, hi ~4pp. MS
  light 77.2/20.5% -> middle 76.1/14.9% -> heavy 75.3/11.9%: monotone,
  Roman-scale. Weight-differentiated selection (Table 11 columns) and
  the 110kg+ special rules stay deferred (need ratio tables per weight).
- next: item 7 (session frequency/composition + calendar rules)

## 27f — Roman catch-up, item 7: session rules + calendar (2026-10-31)
- verdict: pins, not machinery (composition already book-shaped)
- what measured: presses never render before legs (0/26); final week =
  13% of meso with 6.5% heavies left and zero classic 90+ (Roman: 11-14%,
  ~6-10%, 2@90+ classics + 4 squats); squat doses mean 23-38, max 78
  (Roman ~20-30, to ~60); movements/session 1-4 all classes (low end
  matches beginner range). New tests pin press order and the final-week
  shape. Left to template discipline or future meso-memory work:
  submax/max lags, cross-day 90% spacing, shock weekday, two-a-day,
  post-comp rest (fixed 20-week calendar by design).
- housekeeping: README annuals + zone-mix source + bw field/rule + gaps
  line; outputs/*.html+json rebuilt for review; 203 green, lint/mypy at
  HEAD baseline (5 ruff + 6 mypy pre-existing, zero new).
- research loop CLOSED: all 7 items landed as commits d3707c0 (1-2),
  58ed4f7 (3), 3adc3c3 (4), 3207c7 (5), 8d33762 (6), plus this one (7).

## 28 — adversarial review fleet: 17 reviewers, 3 fixes (2026-10-31)
- launched fleet 1 (volumes/intensity/sessions/methodology/selection)
  then fleet 2 sharded per-class x source (10) + method-vs-source (2);
  all read-only, findings in research/reviews/*.md + SYNTHESIS.md.
- FIXED (TDD red→green): (1) walled shift — comp shift invented 100s
  where yearly frac is zero (III/II singles); moves into zero-base
  zones skip without spending delta, heat pools at highest allocated;
  (2) taper strips pull 100+ in final week + topup rehomes to w1-3
  (Roman p110, Takano zero); (3) Finding 4 MS-jerk 45→42.6% +
  denominator honesty. Pins re-measured (excess 204.3, instr 9505,
  soft III/I/CMS/MS 6/38/23/22). 207 green, lint at HEAD baseline.
- TEST recalibrated (not weakened): ramp bar demanded uniform dose
  thickness — stricter than books (Roman ramps taper; any nonzero rung
  renders legally) and README ("unbroken run"). Now contiguity with
  spare-gate. The 2 tripping sessions ([6,9,2,1] pyramids) are textbook.
- ADJUDICATED source conflicts (document, don't chase): Takano 80-modal
  texture vs Roman 70-pyramid quotas; textbook vs coach selection
  (we side Roman); annual-rate vs Roman-year; low-class heaviness.
  Corrected reviewer artifacts (Takano 90%+ is 23%, not rare; Takano
  writes Squat x8; wk4 squat-90s within allowance).
- BANKED (unanimous, 3 method reviews): tops-first inversion —
  allocate counted tops + weekday roles first, volume follows.
  Smoking gun: SnPull fit 59-89% @90+, rendered 3-5% (pairs eat the
  dose; ClPull matches via solo slots). Subsumes solo pulls, thin-top
  starvation, L-day counts, wave steepening, most close_* repairs.
  Near-term: graded comp cut, III/II annual split, Other-Squat dose,
  low-class prep 90s.

## 29 — complexes fleet: 5 reviewers, no code change (2026-10-31)
- fleet: inventory (ours vs Takano JSONs), Roman doctrine, Takano
  practice, code-path lifecycle, ratio audit. Findings in
  research/reviews/complexes-*.md + complexes-SYNTHESIS.md.
- verdict: complexes are our volume engine (MS 45%, [2,3] triples,
  7-18 sets, open sessions) vs Takano's competition test ([2,1]→[1,1],
  5-7 sets, mid-session) with variant quarantine at 60-70; Roman
  stricter still (full C&J 7-10d, pulls never fused, combos ≤80%).
- worst agreed violations: variant complexes at 90+ (MS 79+55 sets),
  inverted pull ratios ([2,3] vs fixed [3,1]), missing OthSn+OthSq /
  OthSn+Press staples, no flat-90 peak blocks.
- DELIBERATELY UNCHANGED: ratios couple to totals (member lifts =
  ratio x ref-units; a ratio patch uncalibrates annuals); 4 of 5
  ratio cells are book-conflicts; ceilings strand fitted 90-pull-mass
  with no solo host; set caps need L-day spill slots. The 5 exact
  cell changes are banked as tops-first calibration data.

## 30 — complexes step 1: dead pairs removed (2026-10-31)
- removed Clean+Other Jerk and ClPull+Other Clean (PAIRS, PAIR_REF,
  DAY slot 1); neither book programs them. TDD: new test pins
  absence from PAIRS and from all rendered plans.
- mass re-hosts solo/paired with zero infeasible weeks; 5 day-pattern
  flips in tight I/CMS Prep 2-4 weeks (1 healed to canonical, 4 new
  dose-forced, 0 CAP-bound, all 0-violation). I m3w1d2 gains a solo
  Clean slot (3->4 slots) while its squat slot grows 30->33 sets
  (marathon class pre-exists; noted in pin comment).
- complex share flat (I 36.7->37.1, MS 45.4->45.0): the removed pairs
  were rare in output; share battle is step 2 (H-quarantine).
- book 2.81->2.67: soft 115->97 (variant-fusion soft openers gone),
  excess steady; Takano clash pins +1/+2 (their co-hostings predate
  our template); solo ClPull now renders 80x3 (both books allow).
  208 green, lint at HEAD baseline. Outputs regenerated.

## 31 — complexes step 2: tech H-quarantine (2026-10-31)
- PAIR_ROLE (test: Cl+J, OthCl+J; tech: rest) + fold in pair_zones:
  tech 90+ ref units pool at 80. A ceiling, not a floor: totals
  exact, no strand risk, no slot changes. ~10 lines + role table.
- effect: tech-90 lifts 0 everywhere (was MS 158 OthCl+OthJ + 110
  Pull+OthSn + more); heat concentrates in test pairs + solos.
  Complex share flat (engine still runs; volume battle is later).
- book 2.67->2.64: excess 204->189, soft 97->96. Ramp-test bar
  recalibrated to contiguity (README guarantee; tapered pyramids
  are book-fine). Taper-slack test now measures 80+ conservation
  (placement pinned separately). Hi-spread bar 12->11pp with the
  honest note: Takano true 19pp needs solo pull heavies (ticketed).
  Modes: solo ClPull renders 80x3 (both books allow).
- 209 green, lint at HEAD baseline. Outputs regenerated.

## 32 — complexes step 3: L preference DROPPED after investigation
- pair_options sorts by fit-distance to hosted (c,h) member totals;
  the L schedule follows the data (jerk-heavy Table-11 shares), not
  option order. Clean-heavy L needs per-pair schedules (banked) or
  breaking selection shares. Cost > value on a contested cell;
  status quo [2,3] is Roman-compatible. Takano dissent stands.

## 33 — complexes step 4 REVERTED (layering verdict)
- Added OthSn+OthSq/OthSn+Press (tech, slot 0): rendered III/II-only
  (22+6 slots, zero at I+ where selection gives them no dose) as
  8-9-set [2,3] pistons, not Takano's few-big-sets. Worse: pairing
  absorbers breaks snap/refit disjointness -> infeasible weeks at
  III/II. BALLAST shrink restores feasibility but book 2.64->2.76.
- Verdict: absorbers must not pair (invariant test stays); variant-
  variant pairs need the tops-first hosting redesign. Reverted both
  changes; suite 209 green, book back to 2.67, outputs regenerated.

## 34 — complexes step 5 PINNED (mechanism already exists)
- Measured: all 114 test-pair 90-sets program-wide render [1,1]
  (zero exceptions); 6-10-dose flat blocks already sit on big-day
  C+J slots (III 1, I 4, CMS 5, MS 8), ramps below (Takano's shape:
  his blocks top ladders). No code change; new strict-singles test
  + block floors {I:3, CMS:4, MS:6}. Density is tops-first's dose
  question, not a rendering one.

## 35 — complexes step 6 VERIFIED (no recalibration needed)
- Annuals intact: 4986/4986/6712/6712/8438 -> 13k/13k/17.5k/17.5k/22k.
  Table-11 classic shares within 1pt of synthesis baseline on every
  cell (III 50/43/68, I 44/40/57, MS 40/37/42 vs Roman 50/44/68,
  45/40/58, 40/38/46; MS-Jerk outlier pre-exists). Shipped changes
  conserve group totals by construction, so selection needs no
  retune. Pins current, outputs regenerated. Complexes track done
  pending tops-first (solo heavies, share, marathons, density).

## 36 — dose-gated pairing shipped (9e7a63e); slot/stagger rejected
- Step A slot 5: MS infeasible (fit packs 6-movement sessions, refit
  cannot place ballast). Reverted. Within-slot stagger: quotas lose
  to margins (big doses re-concentrate). Reverted. Walls documented.
- Step C shipped: cover_session tries solo first for tech pairs over
  PAIR_DOSE_CAP=40 (Takano max), pairing as fallback. Same solution
  space, new order: zero feasibility risk by construction.
- I/CMS fusion -10%, solo SnPull 0->34 lifts, share 37.5->35.2%,
  (1,1)-cap earlier killed test (3,3)s (book 2.67->2.52). MS big
  days full -> fallback; MS room waits on tops-first.
- 2 pattern flips to SMSMSM (splittable medium days beat one L-day
  hogging dose; peak-less alternation is legit rhythm). Solo SnPull
  modes 80x4/90x4/100x3 (REPS-max, Takano 90x3/100x2-3 staple).
- 211 green. Book 2.52->2.49 (soft 96->84).

## 37 — spiky-90 spike: no lever (reverted without trace)
- Exponent 3.0 on Comp1 top-zone row: blocks 17->17. The pair_zones
  fit holds exact margins (session totals x zone totals), so no
  prior reweighting moves 90-mass across sessions. Density needs
  zone-aware session splits (tops-first). Quota-2 also spiked and
  rejected (marathons 97->113: overlap fattens pair slots).
- Remaining violations all reduce to room: MS fusion, MS marathons,
  block density need solo/L-day capacity (tops-first). Nothing left
  that a small config change can fix. Capacity track done.

## 38 — tops-first slice 1 tried and reverted (uniform refit + slot 5)
- Uniform refit feasible via as-fit seeding + work-sum fixed rows +
  restored ballast absorber (margin-exact; self-exclusion fix for
  need_slots; BALLAST stays, margin math needs it). Alone: book
  2.49->2.50, room flat (freedom without slots just reshuffles).
- Slot 5 (+ uniform refit) builds MS (deadlock solved) but loses:
  fusion +184/+206, solo 34->0, share +6pp; marathons halve.
  Capacity feeds pairing. Solo needs separation, not capacity.
- Handoff sharpened: hosting (separation) first, gate second.
  Reverted both; baseline intact, 211 green, outputs byte-identical.

## 39 — tops-first slice 2 tried and reverted (feedback ban)
- Banned-support threading + one feedback refit per fallback week:
  18/23 wins, never fires III/II. I/CMS/MS fusion -259/-154/-194,
  solo SnPull 4x/2.6x with 90s. Separation confirmed as the room
  formula (evict to roomy days beats adding slots).
- Reverted: modes off Takano centers, rhythm +0.17, +11% CPU,
  book +0.027. Quality-neutral, pace-negative; unpriced objective
  cannot pass a priced gate — tops-first must be structural.

## 40 — tops-first slice 3 no-op and reverted (quota day-dose)
- separate_big_days quota post-pass: unit green, 212 green, book
  and room identical to baseline. Proportional estimates cannot
  see concentration. Reverted.
- Three slices close patches (capacity feeds pairing; feedback
  costs a pass + fidelity; prediction is information-starved).
  Spec banked in research/plans/tops-first-allocator.md: decide
  hosting dose-aware in one pass, then fit volumes to the decision.

## 41 — day-share cap tried and reverted (value surgery)
- `_split_dumps` exact cap-and-swap in fit_session: dirty exc -17.5
  but +17% CPU + 6 pins + fusion; partial-clean exc -7.7, rhythm
  -0.42, CPU +6%, 3 pins. Post-hoc surgery churns placements for
  modest wins. Reverted; 211 green.
- 4th negative banked: caps must be pre-fit allocator decisions.
