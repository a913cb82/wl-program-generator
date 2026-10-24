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

9. polish-pairs (stack-1): wave-polish won on single-side sets; try the
   round-robin polish on PAIR complex orders (two-sided zone totals).
   Same strict gate: identical totals, no stray/warmup regression.

10. finish-scan (stack-1): FINISH_SCAN 2->1 (beam-trim's cheaper
    follow-up; narrowing proved load-bearing, but rescoring fewer
    survivors may be free).
11. quota-cap (stack-1): week_quota caps (targets//6) — untried knob
    shaping per-group hosting days. Audit-only nudges.
12. pair-ratio (stack-1): RATIOS/SCHEDULES tuning for pair schemes;
    size/strain lever, never probed.

13. bins-shift (stack-1): nudge weekly intensity-bin targets (BINS);
    intensity mix feeds strain directly. Audit-only, revert at red.
14. order-4day-2 (stack-1): disciplined retry of the 4-day reorder
    (forbid environment spelunking; 3 commands: audit, edit, audit).

STANDING RULE (two inverted verdicts): report quality terms first,
pace last. Pace deltas under ~0.05 are noise until replicated
back-to-back on one box. Never keep a change on pace alone.
