# Autoresearch log

Book baseline (audit, main @ 28ab2ea): score 0.942
(strain 1.02, size 1.00, rhythm 2.00, drift 0.16 incl. pace -0.01).

## Round 1 (from main)

| Agent | Branch | Worktree | Direction |
|-------|--------|----------|-----------|
| pace-hunt | research/pace-hunt | ../wlg-pace-hunt | cheaper builds, same quality |
| size-cut | research/size-cut | ../wlg-size-cut | fewer instructions, same guarantees |
| strain-ease | research/strain-ease | ../wlg-strain-ease | volumes closer to tolerance |

Rules: tests stay green, output deterministic, guarantees hold.
Notes live in research/<slug>.md on each branch. Only winners merge.

## Round 1 results (verified on orchestrator machine)

| Agent | Baseline | Final | Verdict |
|-------|----------|-------|---------|
| pace-hunt (f2d3097) | 0.983 | 0.934 (pace +0.19 -> -0.05, quality identical) | MERGED |
| size-cut (a58e6e8) | 0.961 | 0.922 (size 1.00 -> 0.92, longest 25 -> 21) | MERGED |
| strain-ease (806613b) | 0.969 | 0.969, tree clean | parked, see finding below |

Merged book: 0.927 (strain 1.02, size 0.92, rhythm 2.00, drift 0.21).
Baselines differ per machine because pace prices CPU; quality terms match.

strain-ease finding (seed for round 2): 86% of excess is paired-session
doubling under the frozen scorer, fixable only via support-level host
control. Amount-shaping/peak-skip/host-spread all backfire.

Rule from now on: every explorer gets a 5-minute budget.

## Round 2 (from main @ 157e7ab, 5-min budgets, no merges to main)

| Agent | Branch | Direction |
|-------|--------|-----------|
| r2-host | research/r2-host | support-level host control for paired doubling |
| r2-hotspot | research/r2-hotspot | profile current build, cut top CPU hotspot, byte-identical output |
| r2-shape | research/r2-shape | weekly shape: day counts, peak placement, peak patterns |

## Flow notes (no rounds; always 3 running; no merges to main)

- R2: r2-host reverted clean (host bias backfires). r2-hotspot found only
  noise (pace +0.09 -> -0.04 machine wobble; kept one exactness test).
  r2-shape reverted SIZE_WEIGHT tries (broke structural tests) but left
  an untried lead: MSLMM / MSLSMM canonical patterns.
- Launched: shape-patterns (that lead), pair-freq (gate pair formation),
  size-again (next instruction cut). All from main, 5-min budgets.

- shape-patterns REJECTED (rhythm -0.09, strain +0.16; follow-up: 6-day
  only, keep trailing S). pair-freq FALSIFIED (render-level singles-first
  kills pair_fit discipline; +1.2 exc). Both notes harvested, worktrees
  cleared. Launched shape-6day + floor-retry (bounded floor retry now
  that caches are cheap) alongside size-again.

- shape-6day REJECTED (MSLSMS leaves rhythm flat, regresses elsewhere;
  reverted clean). Relaunched ipf-stall immediately (pre-prepped tree).
  Running: size-again, floor-retry, ipf-stall. Spare: support-cap tree.

- size-again WON (-9 instructions via wave-polish, 345a366, pace-neutral
  size 0.9201 -> 0.9196). floor-retry KILLED clean (floor never cuts
  strain; 15x blowup confirmed again at floor 8). Notes harvested.
- Launched support-cap (peak-day group cap, pair-free singles) and
  demand-sweep (proper demand-path attempt with pace guardrail).
  Running: ipf-stall, support-cap, demand-sweep.

- ipf-stall WON (stall-abort at iter 400-600, byte-identical, pace
  -0.04 -> -0.21, 5bac17d). Launched beam-trim (other half of CPU).
  Running: support-cap, demand-sweep, beam-trim.

- demand-sweep REJECTED (demand wins strain 1.02 -> 0.83 but 3x CPU,
  pace +3.5, score 1.55). support-cap FALSIFIED (pair-softening
  concentrates pairs off-peak, exc +11.6 + idle defects). beam-trim NULL
  (budget expired; queued BEAM 32->16 hypothesis in its notes).
- Built research/stack-1 (main + ipf-stall + size-again winners,
  test conflict resolved, 128 green, book 0.897). Exploration base
  for pace/size work; main stays untouched.
- Launched beam-narrow (queued hypothesis, stack base), longest-cut
  (attack the 21-set block), knob-scan (coordinate descent on stack).

- beam-narrow REJECTED (beams load-bearing; narrowing changes all five
  JSONs). Its stale-outputs flag checked on main: regen is
  byte-identical, no staleness — artifact of its own worktree.
- size-again notes rule out wider waves/fraction merging (would need
  scorer changes). longest-cut NULL (recon only; the three 21-set slots
  are mapped in its notes for the next attempt).
- Launched env-c / env-t (audit-only knob probes on stack) + beam-wide.

- env-t + env-c: both knobs DEAD in the default path (quality terms
  byte-identical; only pace wiggles). 5-minute audit-only probes work
  well as filler. Launched cap-refits (next live knob).
- beam-wide still running.

- beam-wide REJECTED (48 is pure pace tax; 5 fewer instructions do not
  pay for +0.05 pace). Launched beam-joint (narrower blast radius) and
  longest-surgical (attack the mapped 21-set slots). Running:
  cap-refits, beam-joint, longest-surgical.

- cap-refits REJECTED (300 changes no plan, pace tax; pin test kept).
  Launched hotspot-2 (re-profile stacked tree). Spare ready:
  mindose-tol tree. Running: beam-joint, longest-surgical, hotspot-2.

- beam-joint verdict was INVERTED (kept a +0.04 regression; lower is
  better). Verified on orchestrator box (0.952, longest 22, pace
  +0.13) and reverted on its branch. Lesson recorded in its notes.
- hotspot-2 NULL (no float-safe cut past compensated sums).
  longest-surgical NULL (repacking infeasible; recommends post-pass
  split). Launched split-20 + demand-cheap (capped demand variant).
  Running: mindose-tol, split-20, demand-cheap.

- mindose-tol: all four values REVERTED (pinned-test breakage, no
  quality signal). Launched sizeweight-nudge (last knob-scan lead).
  Running: split-20, demand-cheap, sizeweight-nudge.

- split-20 NULL with teeth: post-pass split is illegal under frozen
  cell-match, and additive counting would hold instr flat anyway.
  demand-cheap KILLED (capped demand: strain 0.73/0.79 but pace never
  neutral; demand strain win is real but unreachable).
  Launched day-rebalance (move mass, not patterns) + feasible-trim.
  Running: sizeweight-nudge, day-rebalance, feasible-trim.

- sizeweight-nudge NO-GO (all 7 uniform moves lose; {1,2,3} is a local
  optimum; closest M+1 at 1.042). Suggests per-class weights next.
- Stack verified: stack-1 outputs differ from main on 4/5 classes
  (size-again schemes), CMS identical; ipf-stall contributes no diff.
- Launched spread-trim (nobody has attacked spread 0.17 directly).
  Running: day-rebalance, feasible-trim, spread-trim.

- day-rebalance KILLED (strain cost 4.5x rhythm gain; turns-vs-peaks
  tradeoff floors 4-6-day weeks). Launched perclass-weights (non-uniform
  SIZE_WEIGHT for the worst rhythm rows). Running: feasible-trim,
  spread-trim, perclass-weights.

- perclass-weights NO-GO (MS-only M+1 right direction, 3 guards trip;
  unrun: I/CMS-only, half-steps). Harvested.
- feasible-trim HOLD (13% CPU cut, byte-identical, pace inside noise).
  spread-trim NULL with a concrete lead (free-day1 running it).
- Launched perclass-icms (unrun follow-ups). Running: free-day1,
  polish-pairs, perclass-icms.

- free-day1 REVERTED hard (book 4.809 with defects; the DAY[1] anchor
  is load-bearing — spread-trim's recommendation is dead).
- perclass-icms NO-GO unrun, but recon done (M+0.5 allowed, patch
  points found). Launched perclass-half + meso-split (untouched MACRO
  table) + order-4day (4-day reorder). Running: order-4day,
  perclass-half, meso-split.

- order-4day CANCELLED (wedged on runaway find; no notes, clean tree).
  Idea stays open for a disciplined retry.
- perclass-half SPLIT: MS-only M+0.5 audit-GO (-0.027, real strain),
  I/CMS dead. Launched perclass-impl + finish-scan (FINISH_SCAN 2->1).
  Running: meso-split, perclass-impl, finish-scan.

- meso-split NO WIN (MACRO split is a local optimum for single-meso
  ±0.02; every nudge raised strain/size). Launched quota-cap
  (untried week_quota divisor). Running: perclass-impl, finish-scan,
  quota-cap.

- quota-cap: both directions rejected (pace-only movement; //6 is the
  sweet spot). perclass-impl VERIFIED on orchestrator box (0.844) and
  STACKED: stack-1 now 0.859, 129 green (strain 0.99, pace -0.26).
- finish-scan REJECTED (not byte-identical, book loss, 2 test failures).
  Regen check on main is byte-stable — its nondeterminism flag was an
  artifact of its tree. Do not chase.
- Launched pair-ratio + taper-trim (untouched taper shape) + cap-evals
  (untested sibling). Running all three.

- pair-ratio NO WIN (ladder locally optimal in both directions).
- cap-evals verdict INVERTED (kept a +0.013 regression as "WIN").
  Re-audited: the spread is pure pace noise, quality never moves.
  Reverted on its branch. Second inverted verdict — added a rule to
  every brief: report quality terms first, pace last.
- perclass-impl stacked (stack-1 book 0.859). Launched order-4day-2
  (disciplined retry, command allowlist) + ms-rhythm (repair MS 3.00
  without losing the strain win). Running: bins-shift, order-4day-2,
  ms-rhythm.

- bins-shift NO WIN (fence both directions; probe-B strain -1.1 sits
  under noise + breaks the golden pin).
- order-4day-2 REVERTED (SMSL rhythm -0.13, strain +21.8 — clean
  quality tradeoff that loses).
- Launched exc-map (analysis-only: map the 147.8 excess to direct the
  next strain shot) + ms-rhythm recovery steer.

- ms-rhythm NO-GO (rhythm fix works 3.00->2.22 but strain 147.8->150.1;
  S-less shapes are load-bearing for the strain win).
- exc-map delivered: I 45.0/MS 43.3 top classes; 70% band holds 49% of
  excess; 84% is paired doubling. Top shot: I Other Snatch 70% pairs
  (7.3 exc, 10 sessions). Launched i70-gate + iclean-gate (cell #3) +
  polish-again (is the polish idempotent?).

- polish-again NULL with proof (second pass changes 0/6189; +1
  idempotence test, 130 green).
- noise-floor measured: identical-code score spread 0.008, pace spread
  0.03. New bar: pace delta > 0.03 (score > 0.008) counts as real.
  Quality terms bit-stable across runs. This confirms the cap-evals
  correction (0.013 was noise) and clears perclass-impl (+0.057/-0.015).
- iclean-gate NO-GO (support gating breaks session shape; clean revert).
  i70-gate killed by clock with the design preserved; relaunched as
  i70-gate-2 (implement-only) plus beam-seed (untuned seeds).

- i70-gate-2 NO-GO (same refit-clash defect even refit-aware). Gating
  family is dead: support is the shape, cannot gate without reshaping.
- beam-seed attempted nothing (budget burned on setup/read). Relaunched
  tight (beam-seed-2: edit in 60s, audit-only). Launched single-exc
  (analysis-only): the ~24 non-doubled excess is the untouched
  remainder; gating verdicts attached so it is not retried.

- clpull-2 + ms70-2 NO-GO (budgets expire before implementation even
  with inline briefs; 4 runs, zero implementation).
- Orchestrator spike: one-cell ClPull spill KILLED by construction
  (only host that week; adding a movement dwarfs the ~2 exc gain).
  Rescue: spill only into co-host sessions. Fundamental is everywhere
  -> launched fund-spill (I-class Fundamental peak->light).
- Skill updated twice: shared-notes paths go stale; briefs must be
  self-contained (paste exact targets inline).

- fund-spill WIN, VERIFIED on orchestrator box (exc 147.3, 130 green,
  diff reviewed: 58-line co-host-only post-pass, class I). STACKED:
  stack-1 book 0.847, strain 0.98. First spill success after 4
  orientation deaths — the fix was co-host-only + inline briefs.
- Launched fund-spill-2 (top-k, then other classes, rhythm-gated).

- fund-spill-3 NO-GO, reverted (no-stretch filter too strict: gaps are
  week-relative, my "range only shrinks" theory was wrong). Lesson
  recorded. The gap-guard is load-bearing for the 144.7 win.
- Launched fund-spill-4 (move the gap helper to wlconfig, the module
  both sides import; byte-identical gate) + pair-next (recon: next
  non-gating lever on the paired 84%).

- fund-spill-4 NO-GO by MY base error (stack predated fund-spill-2).
  Lesson: briefs must name the prerequisite commit and tell the agent
  to check `git log` first. Verified + STACKED fund-spill-2 myself:
  stack-1 book 0.840, strain 0.96 (exc 144.7), 132 green.
- Parallelism up (idle CPU): 3 runners + 1 hot spare. Launched
  layer-fix-2 (shared-module gap helper, correct base, byte gate) +
  sched-lock (pair-next rec: light-tier 1:1 lock, I Other Snatch 70%,
  re-coupling fenced) + snatch-spill (clone the spill for MS Other
  Snatch singles, rhythm-gated).

- layer-fix-2 PASS, VERIFIED (byte-identical exc 144.7/instr 9282/
  rhythm 2.09) and STACKED: stack-1 book 0.841, strain 0.96, 136 green.
  Generator<->scorer private coupling gone (shared wlconfig helper).
- sched-lock + snatch-spill died in recon again. New doctrine: I do
  recon (exact anchors), agents get mechanical briefs (<=2 edits).
  Relaunched sched-lock-2 (3-line global 1:1 lock below 80) +
  snatch-spill-2 (verbatim clone for MS Other Snatch, top-1).

- sched-lock-2: global 1:1 lock wins exc -13.9 but breaks MS shape
  (defect + 8 red) -> reverted. Scope is everything: relaunched
  scoped (I-only, pair-only, cls threading).
- snatch-spill-2: clone wins exc -0.3 but trips a drift defect the
  gap-guard never watches -> reverted. Relaunched with defect-first
  discovery (name the component, then guard exactly that).
- Doctrine holding: recon is mine (anchors), briefs mechanical.

- snatch-spill-4: singles filter holds zero defects but exc-neutral
  (no movable MS single). Parked MS. My recon: class I hosts Other
  Snatch singles on many sessions (both ends) -> launched
  snatch-spill-5 (I-only) + cms-snatch-spill (CMS-only), same recipe.
- sched-lock line parked (scoped lock is a no-op on this family).
