# Capacity and dose: minimal fixes for the remaining violations

## Diagnosis (one line each)

- Pull fusion: slot 2 holds one of Squat/SnPull/ClPull. Squat and
  ClPull outrank SnPull, so SnPull never trains solo. All its dose
  pairs.
- Marathons: 3-4 movements per session with big doses. Each slot
  holds 30-45 lifts, which renders as 10-20 sets.
- Thin blocks: pair_zones splits 90-dose over paired sessions with
  a flat prior. Every session gets some, none gets a block.
- (3,3): symmetric big doses render symmetric sets. Thinner doses
  should shrink them without a direct rule.
- Missing OthSn pairs: stay banked. Pairing absorbers breaks the
  snap/refit layering (step 4 verdict stands).

## Steps (spike-gated, smallest first)

### A. Sixth slot: pull overflow (config only)

Add slot 5 `[SnPull, ClPull]`, optional, to DAY. No new pairing
(the disjointness invariant holds). cover_session and
resolve_slots consume it only where dose needs it.

Spike: build all classes, measure solo-SnPull lifts, marathon
count, complex share, feasibility.
Gate: zero infeasible weeks, book not worse, solo SnPull > 0.
Rollback: delete the slot line.

### B. Pull-day quotas (config only)

Retune DAY_QUOTA so SnPull heavy days differ from Snatch heavy
days (Roman alternating pull days). Light pull dose may still
co-host and pair small (Takano texture); heavy dose lands solo.

Spike: measure solo-SnPull 90+ lifts and Pull+Sn fusion volume.
Gate: fusion down, solo heavies up, no infeasible weeks.

### C. Dose-gated pairing (one conditional)

In cover_session, skip the pair branch when the combined hosted
dose exceeds a cap taken from Takano (his complex slots top out
near 35 lifts). Small tech pairs keep pairing (both books fine);
big doses go solo (both books demand it).

This unifies three rules under one axis (dose size): heavy
variants, heavy fusion, and marathon complexes all become solo
work. The zone quarantine stays (proven, different axis).

Gate: complex share down toward 14-30%, marathons down, book not
worse. Rollback: delete the conditional.

### D. Spiky 90s in peak weeks (one conditional)

In pair_zones, replace the flat session prior with a spiky one
for the top zone in peak weeks (Comp1 late weeks): most 90-dose
to 1-2 big-day sessions. Contiguity holds (absence is not a gap);
the base floor still seeds warmups.

Spike: count C+J slots with 90-dose >= 6.
Gate: density up, no new gaps, modes stable. Rollback: delete
the conditional.

### E. Residuals (measure first, rule only if needed)

- (3,3): expect emergent drop after A-C (thinner symmetric
  doses). Direct rep-cap only if sets remain.
- Missing pairs: stay banked for the hosting redesign.
- [2,3] L: no action (Roman-compatible, step 3 verdict stands).

### F. Re-pin and regenerate

Update modes, pins, soft, book numbers with comments. Regenerate
outputs/*.json + HTML. WORKLOG entry per step. Commit per step.

## Why this simplifies

No new passes, no new tables, no allocator rewrite. Two config
changes (slot, quotas) plus two conditionals (dose gate, spiky
prior): about 20 lines added, zero deleted. The alternative
tops-first rewrite (+500 lines) is avoided; if it ever happens,
it subsumes reinforce, spread_extra, and close_session (all three
place 90+ mass — one allocation rule replaces three repairs).

## Non-goals

- Per-pair tiers, rep caps, ratio tables (banked machinery).
- New meso shapes, calendar mechanics, bodyweight axis.
- Touching pair_fit climb, beam, or any repair function.
