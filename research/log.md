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
