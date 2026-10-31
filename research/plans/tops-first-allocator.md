# Tops-first allocator (design spike)

## Problem
Heavy tech pairs must train apart (dose over the complex cap), but the
fit packs them together: heaviest-first supports plus exact margins
concentrate dose. Three slices mapped the walls:

## What the slices proved (all reverted, all banked)
1. Capacity feeds pairing (slice 1): an extra slot builds MS but
   fusion +184/+206, solo 34->0. Cover prefers pairs; room must be
   different DAYS (separation), not more slots.
2. Feedback separates at a pass + fidelity cost (slice 2): banning
   heavy co-hosted tech and refitting wins 18/23, fusion -259/-194,
   solo 4x with 90s. Reverted: +11% CPU, modes off Takano centers,
   rhythm +0.17. Dose-awareness costs a pass; eviction reshapes
   set sizes.
3. Pre-fit has no concentration signal (slice 3): 252 tech
   co-hostings measured; weeklies (138-small vs 54-big), quota
   overlap (0-1 both), and proportional day-dose (dilutes; fires
   only at MS extremes) all fail to predict bigs. Concentration
   emerges from fit exactness. Prediction is impossible.

## Spec (from the negatives)
- Decide hosting dose-aware in ONE pass (no prediction, no refit).
- Keep small texture (spare small co-hosting, as the dose gate does).
- Design set sizes (never evict placed dose).
- Hold book + CPU; MS big days are over-constrained (the allocator
  must also control day counts, not just hosting).
- Information-theoretic point: stop predicting concentration;
  DECIDE hosting (tops-first), then fit volumes to the decision.

## Sketch (not approved)
Replace support search with explicit assignment: per group, split
weekly dose over days proportional to day volume (day-dose tops);
forbid tech co-hosting where both tops exceed shares of the cap;
fit volumes to the decided hosting (IPF on fixed support, as the
refit already does with frozen cells). Quotas become the decision,
not the suggestion. Open: exact cap-share rule, day-count control,
fidelity guard for set sizes.
