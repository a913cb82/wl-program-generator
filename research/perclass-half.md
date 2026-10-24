# Per-class half-step (M+0.5) weight probes (research/perclass-half)

Branch `research/perclass-half`, from stack-1 + tree wins (size-again,
ipf-stall). Follows research/perclass-icms (UNRUN rows — executed here).
Protocol: audit-only via monkeypatch (`week_sessions` stashes `cls`,
`day_split` substitutes weights for target classes); no src edits, no
`wlscore` edits, no test edits. Scores are `wlscore.audit` book totals
(lower is better).

Measured baseline in this tree: book **0.877** (stack-1's 0.897 plus
harvested size-again + ipf-stall wins — not re-baselined, taken from
the clean-tree audit at probe time).

## Probe table (book score; lower is better)

| probe | weights (S/M/L) | book | Δ vs base | verdict |
|---|---|---|---|---|
| base (all classes) | 1 / 2 / 3 | 0.877 | — | — |
| MS-only M+0.5 | MS 1 / 2.5 / 3, rest 1 / 2 / 3 | **0.850** (0.853 parallel, 0.850 serial confirm) | −0.027 | GO (audit) — implement |
| I/CMS-only M+0.5 | I,CMS 1 / 2.5 / 3, rest 1 / 2 / 3 | 3.477 | +2.600 | REJECT — catastrophic |

## Detail

- MS-only M+0.5: strain exc 153.4 → 147.8 (real, machine-independent),
  instr 9292 → 9289, pace −0.21 → −0.31, rhythm median 2.00 → 2.09
  (slightly worse). Stable across parallel + serial runs (0.853/0.850).
  Note: MS class score itself worsens (0.544 → 0.609, rhythm 2.1 → 3.0)
  while the book improves — book metric governs per protocol.
- I/CMS-only M+0.5: class I grows a `bad 1` week (drift 0.16 → 5.16,
  score 0.617 → 1.506); CMS size longest 21 → 26. The half-step tips an
  I week into violation — same fence that killed whole-step moves, hit
  from below. Do not retry I/CMS nudges without a guard for that week.
- Guard outlook for implementing MS-only M+0.5 in src: M < L stays
  strict (2.5 < 3), so no M/L tie → canonical-pattern preference
  (`test_day_patterns_keep_canonical_first`) should hold; spread cap and
  pinned-excess guards need a pytest run on the implementing branch.
  Threading `cls` into `day_split` (also called from `sessions()`
  without class context) is the invasive part — left to the
  implementation session.

## Verdict: SPLIT — MS-only M+0.5 audit-GO (book 0.877 → 0.850),
I/CMS-only M+0.5 REJECTED (book 3.477). No src change (audit-only);
tree clean, pytest 128 green.

Probe harness: `/tmp/probe_half.py` (not committed — 30-line
monkeypatch; recipe in perclass-icms.md + Detail above).
Next session: implement MS-only M+0.5 in src on a fresh branch,
pytest must stay 128 green.
