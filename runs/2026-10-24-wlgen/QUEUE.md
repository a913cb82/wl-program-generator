# Queue

Live subset of IDEAS.md. Statuses: open, trying, done, dropped, parked.

| status | idea |
|---|---|
| dropped | snatch-spill-5 (neutral; Other Snatch line stopped: 4 neutral in a row) |
| dropped | cms-snatch-spill (neutral no-op) |
| dropped | I Other Clean singles spill (priced: 48 lifts/7 sess, ceiling ~2 exc, recipe 0-for-3) |
| done | host ubiquity mapped (Squat ubiquitous but exc-free; SnPull never singles) |
| dropped | pace-prof (top fns already memoized, unique args) |
| dropped | jerk-spill (only 3 singles donors, no co-hosts; family 5/5 neutral) |
| done | fund-bulk (70% Fundamental spill) |
| done | ms-timing (MS peak-week rotation) |
| done | pairvol-trim (I 70% paired-volume x0.9) |
| done | perclass-T (per-class day count) |
| done | rhythm-price (recon: price rhythm components) |
| dropped | fund-bulk-2 (interior-70 always gaps; structural no-op) |
| dropped | pairvol-trim-2 (starves sessions into drift; hypothesis dead) |
| dropped | perclass-T-2 (exc -13.7 BUT pace +0.82, book +0.2; gate was exc-only) |
| dropped | fold-thu (clash x24 as priced; kill line held) |
| dropped | lean-3 (exc +10.6, pace worsened; small-base thesis wrong) |
| dropped | lean-2 (exc +10.5, pace worsened; symmetric) |
| trying | shapediff (recon: diff demand vs template winner shapes) |

## Round exc-size-2 (2026-11-01, loop research/exc-size-2, base 8940c00)
- [trying] A-unpair-heavy: thin/unpair heavy co-hosted tech (P1 57% exc) in cover/pair_fit, no eviction. Owner: /tmp/wt-a.
- [trying] B-thin-slots: cap zones/slot + split deep doses in zone_alloc/render/quotas (105 WIDE + 25 DEEP). Owner: /tmp/wt-b.
- [trying] C-unsmear-taper: heavy-favoring taper rehome or delete taper chain (P3 18% + -110 lines). Owner: /tmp/wt-c.
- [dropped] A-unpair-heavy: exc -9.1 (MS-only) but ob_micro 0->16 + soft +4; every class score flat-or-worse, book 2.520->2.629. Fails exam gate (drift regressed). Corollary: paired-dose removal IS the exc win; bands price it. No revision (zero-sum without eviction).
- [done] B-thin-slots: KEPT. Render-only marathon split (same-day second slot, exact volumes). longest 33->24, marathons 130->44, exc exact 190.3, rhythm identical, CPU flat/down, suite 213 green. Follow-ups: strip second-half re-ramp feelers (ClPull-80 mode 3->1 vs Takano 4); recursive split for residual 40-lift upper chunks (MS 20); zone-width cap needs allocator (out of scope).
- [idea] D-flatten-80: below-MS excess P2 (solo Squat-80 piles via PHASE_PEAK prep 2.0). Untried lever after A/C ruled out.

## Round exc-size-3 (goal: exc within 10% of Takano ~129; longest ~Takano x1.1; marathons ~0; base 851fbd9: exc 190.3, longest 20/17/17/18/24, mar 2/1/10/11/20, instr 9409, slots 1537, rhythm 5.22, soft 84, CPU ~2.6, suite 213)
- [trying] D-flatten-80: flatten prep peak concentrating Squat-80 (P2) on biggest day. Owner: /tmp/wd.
- [trying] E-quarantine-90: diagnose I/CMS/MS 90+ exc cells, quarantine to heavy day (post-alloc only). Owner: /tmp/we.
- [trying] B2-split-deep: recursive split + set-split + pair-split + feeler-strip (residual longest/modes). Owner: /tmp/wb2.
- [dropped] E-quarantine-90: NEGATIVE. Perfect quarantine RAISES exc +7.3 (convex per-session penalty); perfect spreading saves -1.4. 90+ mass is quota-forced. Pin kept (convexity test), zero src diff.
- [done] D-flatten-80: KEPT. SQUAT_PREP_PEAK=-1.0 (squat-only prep counter-spread). exc -2.5 broad, soft 84->52 (fewer heavy openers), ob/iv 0, rhythm flat, CPU flat, modes/longest/fusion/share identical, 215 green.
- [done] B2-split-deep: KEPT (with D interaction healing Squat-70 2->1 back to 2=Takano). longest 24->17, marathons 44->5, exc/rhythm/soft/fusion/share exact, CPU flat, 220 green. Residue: 5 wide no-boundary marathons + ClPull-80 mode 1 (structural, quotas) + zone width (allocator).
