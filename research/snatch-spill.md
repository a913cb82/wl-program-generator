# snatch-spill (research/snatch-spill) — null result on time budget

Target: clone the proven fund-spill-2 shape for Other Snatch SINGLES in
class MS at 70% (peak sessions). Constraints: co-host-only, same weekly
lifts, vols track, bins recompute, gap-guard revert; rhythm gate MS in
[2.91, 3.01].

## Baseline (this worktree, before changes)

- `.venv/bin/wlgen audit`: book **0.849** (strain 0.96 [exc 144.7,
  short 0.0], size 0.92 [instr 9282, longest 21, slots 1282],
  rhythm 2.09, drift -0.11 [off 0.0, vol 0.0, bad 0, spread 0.16,
  pace -0.27]).
- MS row: strain 0.28 (exc 42.5), rhythm **2.96**, drift 0.18.
- Per-class exc: III 13.4, II 13.4, I 44.0, CMS 31.5, MS 42.5.

## Probe (uncommitted code, not kept)

Peak Other Snatch singles in MS (tol 1.5, cap@70 = 24):

- meso4/wk1/sess1 `{60:7, 70:28, 80:4, 90:5, 100:1}` vol 137:
  score 2.35, exc 0.85 (largest single excess).
- meso4/wk2/sess1 `{60:5, 70:18, 80:4, 90:7, 100:1}`: exc 0.57.
- meso3/wk2/sess1 `{60:6, 70:25, 80:3, 90:4, 100:1}`: exc 0.54.
- Total Other Snatch single excess in MS ≈ 1.96 (≈1.61 quoted at 70%
  alone — the 70-zone slice dominates).

Hypothesis (untested): `spill_peak_snatch(plan, top_k=...)` limited to
`plan["class"] == "MS"`, donor/recipient both hosting Other Snatch as
SINGLES (in `movements`, in no `pairs` entry), moving a MIN_DOSE (6)
slice @70 from the peak single to the same week's lightest single
co-host, with the fund-spill-2 gap-guard revert and the MS rhythm gate
[2.91, 3.01]. Concern: donor meso4/wk1/sess1's week-mates hosting
single Other Snatch are thin (wk1 has sess1 only?), so co-host
availability may force week-skips — the likely kill point.

## Verdict

No change attempted within budget; baseline stands
(book 0.849, MS rhythm 2.96). The spill_probe above is the recommended
next 5-minute shot, reusing `spill_peak_fundamental` verbatim with the
group/zone/pair predicates swapped.
