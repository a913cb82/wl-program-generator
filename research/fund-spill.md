# fund-spill

Spill the class I peak session's top-slice Fundamental lifts to the same
week's lightest co-host session.

## Target (exact)

- Peak: class I meso1/wk1/sess2 (L, vol 139), Fundamental
  `{50:1, 60:4, 70:13, 80:12, 90:7, 100:2}` — largest Fundamental dose
  at 90% in class I (tie-break over meso0/wk1/sess1 via heavier 100-zone load).
- Recipient: same week's lightest Fundamental host, meso1/wk1/sess3
  (M, vol 93), Fundamental `{60:1, 70:2, 80:3, 90:2, 100:1}`.
- Move: 2 lifts @100 (donor's whole highest-zone dose >= 90) sess2 -> sess3.
  Same weekly lifts, same zones, only the day changes. No new movements anywhere.

## Result

- Class I exc 45.0 -> 44.5; book exc 147.8 -> 147.3, strain 0.99 -> 0.98.
- Book totals identical: instructions 9289, slots 1282, longest 21, shortfall < 0.1.
- 130/130 green (129 baseline + 1 new spill test). Gate held: no session-shape
  failure, no totals movement.

## Mechanism

`spill_peak_fundamental(plan)` in `src/wlgen.py`, applied at the end of
`build_plan` for class I only. Rule-based (finds the peak by largest
Fundamental @90 dose, the recipient by lightest co-host vol), so it tracks
the plan rather than hardcoding indices. Session vols track their movements
(`sum == vol` invariant) and the week's bins are recomputed.

## Why it works / why safe

- Spilling only into sessions that already host the movement keeps every
  session's hosted set matchable (the shape tests that tripped twice before
  when a movement was added to a session never fire).
- Fundamental is BALLAST (never paired), so the move is pure count
  bookkeeping with no pair/slot side effects.
- The donor L session sat over Prilepin capacity at the top; the recipient
  M session absorbs +2 @100 without crossing it — net exc falls.
