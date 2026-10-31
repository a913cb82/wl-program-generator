# Room and laws: what remains and why small moves are exhausted

## Investigation: pull shares must NOT flip

Roman Table 11: MS prep snatch pull 8.5%, clean pull 10%; comp 5%
and 12%. Ours: 7% and 11% (his average). Flipping shares so SnPull
wins slot 2 would break conformance. SnPull losing slot 2 to ClPull
is the book-faithful outcome (comp 12 vs 5; group-1 vs group-2).

Bonus for tops-first: Roman group-1 (correlates with total: snatch,
C&J, squats, CLEAN pulls) vs group-2 (snatch pulls, presses,
bendovers, other squats — halved at MSIC, cut for records, p158-163).
Our engine treats all groups symmetrically; tops-first should not.

## The three laws (proven by spikes this track)

1. Three groups, one slot. Squat/ClPull/SnPull share slot 2 with
   book-faithful doses (27/11/7). One slot holds one movement, so
   at least one group pairs or relocates every day. Our loser is
   SnPull (smallest dose, group-2) — the least-bad loser, and
   correct per Roman. Solo heavies need a second strength slot,
   which deadlocks the refit (spiked). Only a hosting redesign
   creates room.
2. Dose per slot is forced. Week volume (annuals) over days (max 6)
   over movements (max 5 slots) sets dose per slot; contiguity sets
   the floor (one set per zone). Marathons are wide ladders with
   fat zones plus allocation-forced 1-lift feelers. No rendering
   dial reaches them (LENGTH_COST 1->4: 130->126 marathons;
   quota-2 overlap: 97->113). Only thinner doses (more room)
   shrink them.
3. Margins dominate priors. The pair_zones fit holds exact session
   and zone totals; no prior reweighting moves mass (spiky-90
   spike: blocks 17->17). Density needs zone-aware session splits.

## Considered and rejected

- Cell ceiling (cap lifts per group per day): upper bounds risk
  infeasibility (190 lifts over 5 capped days cannot fit); core
  surgery, not minimal.
- Wave-repeat cap at x3 (Takano max): touches load-bearing cached
  _parse (JSON items, HTML, complexity) and rewrites pinned
  philosophy tests, for a partial win. Tops-first dose
  concentration shortens waves automatically (halved doses render
  x3-or-less), making the cap unnecessary.
- Pull-share flip: breaks Roman conformance (see above).

## Simplification statement

No safe deletions remain: every rule (quarantine, dose gate,
(1,1)-cap, roles) is load-bearing and pinned. The simplification
payoff arrives with tops-first, which deletes reinforce,
spread_extra, and close_session (three 90+-placement repairs
become one allocation rule) and subsumes the dose gate (solo is
the default for big doses, not the fallback).

## Tops-first handoff (requirements)

1. Solo strength slots (second slot-2 capacity) with refit-aware
   hosting (paired rows frozen, solo rows movable — fix the
   disjointness properly instead of routing around it).
2. Zone-aware session splits (which sessions get 90-dose decides
   block density; totals-exact like today).
3. Group-1/group-2 selection axis (group-2 halves at MSIC; our
   symmetry over-programs assistance at the top).
4. Keep every pin green: contiguity, quarantine, (1,1)-cap, dose
   gate, flat singles, Table-11 within 1pt.
