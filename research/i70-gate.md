# I70-gate: ban SnPull+Other Snatch complex in class I (budget-expired, unattempted)

Baseline (stack-1, this box): book 0.861
(strain 0.99 = exc 147.8 + short 0.0, size 0.92, rhythm 2.09,
drift -0.09 incl. pace -0.25). 129 tests green.

## Lead (unchanged, for next runner)

Densest excess cell: I / Other Snatch / 70% pairs, 7.3 exc in 10 sessions.
Gate: ban the SnPull+Other Snatch complex in class I only.

## Planned gate (not implemented — budget expired before edit)

Support-level, pair-free single hosting (no amount shaping):

- `wlconfig.py`: add class-gated ban, e.g.
  `PAIR_GATE = {frozenset(("SnPull", "Other Snatch")): {"I"}}`.
- `cover_session(hosted, banned=())`: skip banned pair edges, so co-hosted
  SnPull + Other Snatch keep separate single slots (slot 2 / slot 0).
- `detect_pairs(..., banned=())`: pass through.
- `pair_fit(..., cls, ...)`: look up banned pairs by cls, pass to detect_pairs.
- No render/`wlir` change needed: banned pairs never enter the pairs dict,
  so scorer `_dose` (frozen) stops double-counting them.

Why this shape and not alternatives:

- Fit/hosting untouched: {SnPull, Other Snatch} co-hosting stays matchable
  as two singles, so no feasibility/strand risk; no extra host day needed.
- Zone-scoped (70%-only) gating rejected: pairs snap/render per session,
  zones split inside — 70%-only would need zone_alloc/pair_zones surgery.
  Class-I-wide ban of this one complex kills the 70% doubling (plus smaller
  spillover at other zones); price via audit.
- pair-freq warning applies in miniature: banned sessions keep as-fit
  (frozen, unsnapped) volumes, so net = -doubling + snap drift. Kill fast
  if strain does not move or idle/clash defects appear.

## Verdict

KILLED by clock — no src/tests change, tree clean. Lead preserved above.
