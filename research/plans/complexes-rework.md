# Plan: complexes, Takano-first with Roman guardrails

Source reviews: `research/reviews/complexes-*.md` (+SYNTHESIS).
Design constraint from the fleet: ratios couple to totals (member
lifts = ratio x ref-units), ceilings strand fitted mass without solo
hosts, set caps need spill slots. So the plan changes ALLOCATION
ORDER and PERMISSION, not set-packing: one role flag, one legality
condition, no new stages.

## Principle (adjudicated)

Takano-first (he is the fitted source; his practice is measured),
Roman-bounded (his caps and shapes veto, his program doesn't rule:
full Roman compliance — no Pull+X ever, C+J every 7–10d — deletes
37–45% of complex volume with nowhere for the mass to go; that is a
different program, not a tune).

## The three rules

**Rule 1 — Pair roles replace global tiers.** Every pair is `test` or
`tech`, one `PAIR_ROLE` dict:
- test: Clean+Jerk, Other Clean+Jerk (Takano peaks both: precomp
  C+J 47/88 sets ≥90, OthCl+J 24/34 ≥90, all [1,1]).
- tech: everything else (OthCl+OthJ, Pull+Sn, ClPull+Cl, new
  OthSn+OthSq, OthSn+Press).
Tech pairs: zones ≤80 (variant–variant ≤70), fixed shapes
([3,1] pull+x; symmetric variant pairs), few sets. Test pairs:
full ramp, H=[1,1], peak-week flat blocks (Rule 3).

**Rule 2 — No heavy tech (one legality condition, the forcing
function).** A pair instance is legal only if test, or its share
holds no 90+ units. Tier info (`week_units` H/M/L, already
computed) flows one step earlier into cover/pair_fit; nothing else
moves. Orphaned 90s MUST render solo — so solo heavy-pull slots and
classic singles emerge by necessity, which is exactly the missing
structure behind the SnPull evaporation (fit 59–89% @90+, rendered
3–5%). No new hosting code: the constraint creates the structure.
Small L-zone tech doses shrink the 12–18-set marathons structurally
(no set cap needed). Feasibility gate below watches slot capacity.

**Rule 3 — Peak blocks (narrow rendering exemption, cited).**
Pre-comp peak week: test-pair 90-dose renders as flat N×[90,[1,1]]
single-zone slots mirroring the Snatch ladder (Takano MSIC
m1w2d0/m1w2d4). Contiguity exemption for peak-week test tops only —
a book practice (his peak slots ARE single-zone), not scaffolding.
Implement rendering-side in pair_fill; do not touch close_ramps.

## Pair-by-pair disposition

| Pair | Disposition | Reason |
|---|---|---|
| Clean+Jerk | test, L clean-heavy | Takano L [2,1]/[3,1]/[4,1]; Roman jerk-heavy dissent noted, Takano-first |
| Other Clean+Jerk | test-shadow, H [1,1] only | Takano precomp peaks it; light-day role |
| Clean+Other Jerk | REMOVE | neither book; tiny dose migrates solo |
| OthCl+OthJ | tech, L(+[1,1]-only M), no H | Takano quarantine (L symmetric [2,2]/[3,3]; CMS 12×[1,1] exception kept exactly) |
| SnPull+Snatch | tech, L/M fixed [3,1] | Takano staple verbatim |
| SnPull+OthSn | REMOVE (prototype; fallback tech-light) | Takano 0 slots, Roman never-fused; 13.6% MS dose must absorb solo — feasibility gate decides |
| ClPull+OthCl | REMOVE | same, tiny dose |
| ClPull+Clean | tech, L/M fixed [3,1] | Takano staple, rare |
| + OthSn+OthSq | ADD tech, symmetric L-only | Takano light-day leader ([3,3]/[4,4] @60-70, ~5 sets); one COMPLEX_SLOTS line |
| + OthSn+Press | ADD tech, symmetric L-only | same mechanism, same shape |
| Roman-only triples | NOT added | 1+2+1/1+3 need leg machinery; Takano doesn't do them |

## Rollout (simplest first, TDD, worktree; full suite green each step)

1. Remove the two dead pairs (Cl+OthJ, ClPull+OthCl). Measure strand
   rate + pins. (Expectation: absorbed solo, pins steady.)
2. Role flag + tech H-quarantine in pair legality. Measure:
   feasibility (zero infeasible weeks), variant-H sets (= 0 target),
   solo SnPull 90-share (up toward fit), book score.
3. Test-pair L clean-heavy preference (investigate pair_options
   tie-break first; ordered options per role if tie-broken by order).
   Measure modes vs Takano centers.
4. Add the two variant tech pairs (config + slot + ref + role).
   Measure light-day shape.
5. Peak flat-90 blocks (pair_fill exemption). Measure: C+J
   flat-90 blocks present pre-comp; taper unchanged.
6. Recalibrate once: ratios move mass between members, so re-verify
   Table-11 selection shares + annuals, adjust quotas, re-pin,
   regenerate outputs.

## Gates (stop/adjust if red)

- Feasibility: no `ValueError` weeks; `count_dose_violations` ≤ HEAD.
- Shape: complex share 14–30%; variant-H sets 0; solo SnPull exists;
  C+J flat-90 blocks pre-comp; modes within Takano ±1.
- Pins: book score must not regress for texture reasons; every pin
  move re-measured with book citation (wall-fix procedure §28).

## Non-goals

Roman-only triples, full-C+J rarity, AM/PM splits, Table-1-as-law,
per-side rep monotonicity beyond current law — all previously
adjudicated (fleet reviews / WORKLOG §27c).
