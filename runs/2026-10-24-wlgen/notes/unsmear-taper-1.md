# exp: unsmear-taper — NEGATIVE (P3 falsified, reverted, no code change)

## What
Tried to redirect taper-topup 90+ extras from light sessions onto heavy ones
(`spread_extra` fewest-tops-first → most-tops-first, one-line sort-key flip).
Reverted: the flip moved the book-total pin the wrong way and P3's mechanism
does not reach the ruler. No src/test change shipped.

## Why
P3 (excess-anatomy): taper chain rehomes deleted 90+ into weeks 1-3 and
`spread_extra` spreads it onto 80-holding FEWEST-tops (light) sessions.
Confirmed the mechanism in code — but paired topup already favors heavy
(`pair_zones` extras allocate proportional to session units), and measurement
shows the book total does not respond to taper-chain placement at all.

## Numbers (before → after)
- Book exc: 190.3 → 190.3 (redirect) → 190.3 (topup zeroed) → 190.3
  (close_ramps no-op). Immovable via taper chain / ramp repair.
- Redirect variant: soft 84→84, short 0→0, drift 7.37→5.89, pace +2.99→+1.51,
  score 2.854→2.558 — but exact book excess 190.35x rounds to **190.4**,
  reddening `test_wlscore.py::test_book_numbers_match_research` (out of scope
  to touch). Reverted.
- Session-level probe (taper meso wks 1-3, sessions holding 90+≥4):
  MS 31 with topup vs 25 zeroed; III 2 vs 2. The smear exists at session
  level (+6 cells in MS) but does not propagate to the book ruler: offending
  book cells are structural (Squat/pull/Fundamental 90+ mass from
  `week_bin_lifts` of untapered weeks — quotas/zones, out of scope).
- Taper never deletes volume (fractions renormalize; short stays 0 even with
  topup zeroed) — it only converts 90+ placement to sub-90. Conservation
  test `test_comp2_keeps_taper_slack` passes on baseline.

## Origin check (`git show e553b6b:wlgen.py`)
Init taper deleted Snatch/CJ 90+ only, no rehoming (`take_up_slack`,
`spread_extra`, `reinforce` did not exist). Pull-100 taper + rehome chain
accreted later. Deleting the rehome today breaks in-scope conservation pins
without moving exc — not a deletion candidate after all.

## Lines deleted / pins touched
- Net code: 0 (one-line flip attempted, reverted).
- Pins touched: `test_spread_extra_favors_light_sessions` (held — doctrine
  unchanged), `test_book_numbers_match_research` (held at 190.3 after revert).
- Suite: 211 green. CPU: no code change, bar trivially holds.

## Verdict for orchestrator
P3 attribution does not replicate: taper-chain placement contributes ~0 to
book exc (three independent nulls). Exc lives in zone-count structure
(Squat/pull 90+ volumes), reachable only via quotas/bins — outside this
track's edit scope. Recommend retiring P3 / redirecting the exc hunt to
`week_bins`/quota structure, not the taper chain.
