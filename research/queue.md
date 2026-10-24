# Idea queue (cheapest first; bases in parens)

- DONE cap-refits: REJECTED (no plan change at 300, pace tax; pin test kept).

1. hotspot-2 (stack-1): re-profile the stacked tree and attack the new
   top hotspot. ipf-stall moved the bottleneck; find where it went.
2. mindose-tol (stack-1): MIN_DOSE 6->5/7, TOL 0.2->0.15/0.25 probes.
   Likely breaks pinned tests; audit-only first, stop at first red.
3. demand-cheap (stack-1): demand path won strain 1.02->0.83 at 3x CPU.
   Cap its search (fewer refits, narrower split) and see if any strain
   win survives at neutral pace.
4. sizeweight-nudge (stack-1): tiny SIZE_WEIGHT nudges that do NOT trip
   the structural tests r2-shape hit. Small blast radius only.
5. longest-followup: depends on longest-surgical result.
6. stack-verify (orchestrator, not a subagent): verify all winner
   branches combine cleanly before any merge decision.

7. day-rebalance (stack-1): shift volume BETWEEN days (not groups) to
   hit contrast 2.75 with more turns. Scored on total book — strain may
   pay. New angle: all rhythm tries moved patterns, none moved mass.
8. feasible-trim (stack-1): new eyes on _feasible (18% of build).
   hotspot-2 ruled out float-unsafe cuts; look for algorithmic skips
   (early exit, memo keys), byte-identity gate.
