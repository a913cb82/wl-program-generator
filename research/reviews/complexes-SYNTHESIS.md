# Complexes: how our approach differs (fleet synthesis, 2026-10-31)

Evidence: `reviews/complexes-{inventory,roman,takano,codepath,ratios}.md`.
JSONs measured directly; code path read, not changed.

## The one-sentence verdict

**We use complexes as the volume engine (MS 45% of lifts, [2,3]
triples, 7–18 sets, spread 60–90, opening sessions); Takano uses
Clean+Jerk as the competition test ([2,1]→[1,1], 5–7 sets, mid-session
after Snatch) and quarantines every other complex to light 60–70
technique work.** We train *through* the complex; he trains *up to* it.
Roman goes further: full C+J every 7–10d in parts otherwise, pulls
never fused, combos ≤80%.

## Role inventory (measured)

- Ours complex share: 19% (III/II) → 37% (I/CMS) → 45% (MS).
  Takano: 14–30% (MSIC 25%).
- Ours-only pairs (slots MS): Pull+OthSnatch 29, Pull+Snatch 19,
  ClPull+OthClean 2, Clean+OthJerk 0–2. Takano never programs these.
- Takano-only pairs: OthSnatch+OthSquat ([3,3]/[4,4] L-only, 6 slots
  CMS/MS), OthSnatch+Press. We never emit them (not in PAIRS; no
  shared DAY slot either — template surgery, banked).
- Heaviest agreed violation: variant complexes under 90%+ load —
  MS OthCl+OthJ 79 sets, Pull+OthSn 55 sets at 90. Takano takes no
  variant complex above 70–80 (one CMS 12×[1,1] exception); Roman
  takes no complex above 80%, period.
- C+J modal L: ours jerk-heavy [2,3] (107 MS hits) vs Takano
  clean-heavy [2,1]/[3,1]/[4,1] everywhere. Pull+Sn modal: ours
  snatch-heavy [2,3]/[1,2] vs Takano fixed pull-heavy [3,1].
  Position: our complexes open sessions (slot 0); his C+J sits
  mid-session after the Snatch ladder it mirrors.
- Peaking: Takano peaks THROUGH complexes (flat 6–9×[90,[1,1]]
  blocks, meso-1 C+J 47/88 ≥90). Ours sprinkles 90s in ramps
  (MS C+J 40/207) and tapers by dropping sets.

## Why nothing changed today (read before proposing a patch)

1. **Ratios couple to totals.** Member lifts = ratio × fixed ref-units,
   so a ratio change is a volume change: banning (3,3) in CJ-family
   (~49 low-zone sets) would silently uncalibrate the annuals. Ratios
   are calibration, not patches.
2. **Every cell but one is a book-conflict.** Roman's "never 3
   cleans" vs Takano's staple [3,1]; Roman's jerk-heavy recipes vs
   Takano's clean-heavy L; Takano's 90-[1,1] blocks vs Roman's ≤80%
   cap. The single both-books-agree cell — no (3,3) with classic
   members — needs per-pair tiers; SCHEDULES/allowed_ratios are
   global, and per-pair plumbing for 49 low-zone sets is
   scaffolding, not modeling.
3. **Ceilings strand fitted mass.** Quarantining Pull+X or variants
   below 80/90 deletes the only host the fitted 90-pull-mass has
   (solo heavy slots don't exist) — it would evaporate through
   repairs instead. Ceilings require the tops-first allocator that
   creates solo slots in the same move.
4. **Set-count caps need spill destinations.** Capping complexes at
   9 sets without L-day movement slots just repacks the same dose
   into bigger sets. The 12–18-set marathons die when large days
   host 5–8 movements (banked L-day work), not before.

## Banked calibration (for the tops-first project)

Exact cell changes from `complexes-ratios.md` §5, preserved verbatim
for the rewrite (per-pair H/M/L tiers; Pull+X → [3,1]-only;
CJ-family L → clean-heavy; OthCl+OthJ → L-only; III/II locked out
of Pull+X): implement together with role-scripted allocation —
counted 90+ tops (incl. solo heavy pulls at pull-%) first, weekday
roles (classic/variant/strength) with ceilings, flat-90 C+J peak
blocks mirroring the Snatch ladder, variant complexes leading light
days at 60–70. The code-path review (`complexes-codepath.md` §3–4)
names the same single change from the machinery side.
