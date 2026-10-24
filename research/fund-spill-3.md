# fund-spill-3: remove the generator's scorer import — NO-GO (filter too strict)

## Breach
`spill_peak_fundamental` (research/fund-spill-2, branch `research/fund-spill-2`)
does `from wlscore import _unjustified_gaps` and reverts any spill move that
raises the donor/recipient gap count. The generator calls the scorer to check
its own work — the scorer must stay an independent ruler. Never edited
`wlscore`.

## Prescription (from task)
Donor zeroing only shrinks its range (always safe); recipient gains at `top`
are safe iff the recipient's max used Fundamental zone is already >= `top`
(no new gap possible by construction, so no guard call needed). Keep top-k
loop, distinct donor weeks, all classes, vols track, bins recompute.

## What was tried (TDD: layering + filter tests written red first)
1. **No-stretch only** (recipient max >= top): exc 144.7 -> **145.2**
   (within the 145.5 cap) but **+1 unjustified gap** (class I,
   meso2/wk0/sess3: recipient `[0,1,3,3,2,0,3]` gains at 100 while 100 is
   empty) -> REJECTED (zero-defect gate).
2. **No-stretch + drained-band** (additionally skip when any co-host has a
   hole in `[donor_newmax, top]`): exc -> **146.8** (book: strain 1.0,
   short 0.0, instr 9283, gaps 0, illegal 0, clash 0), zero defects, green
   except the stale 144.7 golden -> REJECTED (over the 145.5 revert line).
3. **Band scoped to donor+recip only**: gaps reappear (MS) -> REJECTED.

## Why the prescription is unsound as stated
`_unjustified_gaps` is week-relative, not session-local: a covered hole
stays silent only while `week - locked < spanning`. Zeroing the donor's top
zone removes its above-side coverage for zones below it, so a *covered*
hole (in the recipient or a third session) inside the drained band can
surface — "range only shrinks" is not "always safe". The recipient-side
no-stretch rule cannot see this. A sound purely-local rule must also
forbid holes in the drained band, and that over-blocks moves the guard
proved gap-neutral (third-session holes with redundant coverage): cost
+2.1 exc total (144.7 -> 146.8), past the 145.5 line.

## Numbers
- Baseline (gap-guarded, breach state): book ~0.84, strain 0.96
  (exc 144.7, short 0.0), 132 green, zero defects.
- Sound no-import variant: book 0.9, strain 1.0 (exc 146.8, short 0.0),
  zero defects (gaps/illegal/clash all 0).
- Reverted final (this branch, I-only single spill): book ~0.844,
  strain 0.98 (exc 147.3), 130 green, zero defects.

## Verdict
**NO-GO on the gate: no layering-clean local filter holds exc <= 145.5
with zero defects. Reverted to HEAD (no src/test change); breach fix not
shipped.** The -2.6 exc of fund-spill-2 is intact on
`research/fund-spill-2` (with its guard).

## Follow-ups (not tried, over budget)
- Recover the ~0.5 stretch cost: allow `top` above the recipient range only
  when the recipient-after profile is contiguous (still local, still no
  import) — spec deviation, needs its own gate run.
- Precise flip-set band (`[max(newmax, umin+1), top)`, never blocks for
  singleton donors) instead of the `[newmax, top]` superset.
- Move the gap check out of the generator entirely (audit-time/report-time
  reversal in the CLI layer) so the shipped plan never depends on it.
