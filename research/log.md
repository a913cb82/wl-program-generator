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
