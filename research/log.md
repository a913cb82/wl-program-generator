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
