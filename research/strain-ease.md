# Strain-ease: volumes closer to tolerance (round 1)

Baseline (main @ 617ce37, this box): book score ~0.96-0.98
(strain 1.02 = exc 153.4 + short 0.0, size 1.00, rhythm 2.00,
drift ~0.2-0.3 incl. pace noise). All 115 tests green.

## Where the strain lives

- Shortfall is 0 everywhere. All strain is over-tolerance work.
- 86% of excess (131.6 of 153.4) sits in paired (complex) sessions:
  the scorer counts a paired member's lifts twice (once via
  `movements`, once via the `pairs` vector), so a 34-lift complex
  side scores as ~68 lifts. The scorer is frozen, so this doubling
  is the environment, not a bug to fix here.
- Worst cells: classic-family complexes (Other Snatch, Other Clean,
  Jerk, Clean) crammed into peak days, e.g. 34+14 in a 124-lift day.
- Perfect within-week balancing would only save ~18 exc (153 -> 136):
  doubled totals are too big for the tolerance budget. Only fewer
  lifts per paired session (more hosts) or fewer complexes help.
- All pairs are slot-structural (6 groups, 5 slots), so complexes
  cannot simply be unpicked.

## Tried (all reverted, nothing beat baseline)

1. `WLGEN_QUOTA` 1.5/2/3: strain barely moves; adds defects
   (bad=1 on I/MS) and breaks up weeks. Dead.
2. `WLGEN_RULE=demand`: exc 153 -> 122, but pace +3.9..+4.7
   (3.2x slower: `_ipf`/`feasible` search explodes with up to 6-day
   weeks). The known pace trap. Dead.
3. Row-differential amount shaping (classic rows weight days
   inversely by volume, strength rows absorb peaks): helps "Other *"
   groups (MS Other Snatch -7.1) but pair-snap re-coupling steepens
   partners (Jerk +3.2, Squat +4.0); also flips variant selection
   (extra paired sessions 208 -> 235). Book exc 153.4 -> 146.2 but
   pace/rhythm regressions eat it. Reverted.
4. Peak-day skip (small groups banned from the max-vol day):
   /2 threshold strands the peak to 2 giant strength singles
   (Fundamental 62 -> exc 2.3, worse); /3 still net worse plus a
   defect. The optimum (~4 mid groups on peaks) needs support-level
   control the quota/fit pipeline does not offer cleanly. Reverted.

## Lesson for next round

Everything honest funnels into host count (which sessions host
which groups), but that is fenced on three sides: MIN_DOSE=6
collapses light-day dust (concentrator), slot-disjointness spreads
hosts everywhere, and MS back-to-back headroom is 8 (122/130).
Amount-shaping inside a fixed support is near zero-sum across rows.
A future attempt should reshape the support itself (peak-day group
cap with pair-free singles), not the amounts.

## Result

No improvement. Tree left clean: src and tests at baseline,
115 green, book strain 1.02 (exc 153.4, short 0.0).
