# Ratio-schedule audit: OURS vs ROMAN vs TAKANO

Src: `src/wlconfig.py` RATIOS/ratio_ok/SCHEDULES; `research/roman-mining/selection.md`, `intensity.md`, `reviews/complexes-roman.md`; `tests/fixtures/takano-*.json` vs `outputs/*.json` modal `[r1,r2]` per complex×tier (H=90+, M=80s, L=<80), all levels. Tiers = our rh/rm/rl cut-points.

## 1. Ratio tables cell-by-cell

OURS (global rule, identical for all 8 pairs): rh(90+)={(1,1)}; rm(80)={(1,1),(2,1),(1,2)}; rl(<80)=all 7 {(1,1),(2,1),(1,2),(3,1),(1,3),(3,2),(2,3)}. SCHEDULES narrows by construction (rank H≤M≤L, members non-decreasing downward).
Pairs: SnPull+Sn, SnPull+OthSn, Cl+J, OthCl+OthJ, OthCl+J, Cl+OthJ, ClPull+Cl, ClPull+OthCl.

ROMAN prescription (no per-set Pull+X ratio exists — pulls standalone p64; low-class NO pulls p61): combos only 45–80%: front-squat+push-jerk 2+2, clean+front-squat+jerk 1+2+1, beginner power-clean+push-press 1+3 (p60-61). Table 1 per-side: 2–3 @60s → 1–2 @70s → 1 @80%+. Full C&J every 7–10d, parts otherwise. Beginners: cleans=jerks 1:1. Jerk ≥ clean in every recipe; never 3 cleans + N jerks.

TAKANO modal practice [L / M / H] (sets counted): Cl+J: III [2,1]/[2,1]/[1,1], II [2,1]/[2,1]/[1,1], I [2,2]/[2,1]/[1,1], CMS [4,1]/[2,1]/[1,1], MS [3,1]/[3,1]/[1,1], MSIC [2,1]/[2,1]/[1,1]. OthCl+OthJ: symmetric [2,2]/[3,3] L-only (CMS L [3,3]x23/[2,2]x20; M=1 set; H=12×[1,1] singles exception; else ~0 above 70). OthCl+J: L [2,2]/[2,1]/[4,4]-mix, H=[1,1] always. SnPull+Sn: FIXED [3,1] at every zone L+M (MS 6+15, I 4+6, CMS 2+3), H never. ClPull+Cl: FIXED [3,1] L+M (MS 6+13). OthSn+OthSq / OthSn+Press (Tak-only): [3,3]/[4,4]/[2,3] L-only.

OURS modal [L / M / H]: Cl+J: III/II [3,3]/[2,2]-[1,1]/[1,1], I/CMS [2,3]/[2,1]/[1,1], MS [2,3]/[2,1]/[1,1]. OthCl+OthJ: III/II [3,1]/[1,1]/[1,1], I/CMS [2,1]/[1,1]+[2,1]/[1,1], MS [2,2]/[2,2]+[1,2]/[1,1]. OthCl+J: [3,2]/[1,2]/[1,1] III/II, [3,3]/[2,2]/[1,1] I/CMS/MS. SnPull+Sn: [2,3]/[1,2]/[1,1] everywhere (MS [1,3]/[1,2]/[1,1]). SnPull+OthSn (ours-only): [1,2]/[1,2]/[1,1] (MS L [1,3]x99). ClPull+OthCl: [3,1]/[2,2]/[1,1] mixed.

## 2. Cells where we contradict ROMAN (+ rendered consequence)

- ALL pairs × H=(1,1): Roman has zero complexes ≥90 (combos ≤80%, lag rules p109-110). E.g. MS `OthCl+OthJ 90/[1,1]` (79 sets); MS m2w2d5 `Cl+J …90/[1,1]x5`; MS `SnPull+OthSn 90/[1,1]` (55 sets).
- Pull+Sn / Pull+OthSn / ClPull+OthCl × ALL tiers: pulls never fused (rule 8); low-class no pulls at all. E.g. CMS m0w1d2 `SnPull+OthSn 60/[1,2]x16 incl 90/[1,1]`; CMS m0w3d4 `ClPull+OthCl 60/[3,1]`.
- Cl+J fam × L with jerk>clean or 3+3: Roman jerk≥clean, max 2–3/side only as singles. E.g. CMS m0w0d3 `Cl+J 60/[2,3]x5+70/[2,3]x2`; III m3w3d5 `Cl+J 60/[3,3] 70/[3,3] 80/[1,1] 90/[1,1]`; II m0w0d2 `OthCl+J 60/[3,2]`.
- Cl+J fam × M with any 2: Table 1 gives 1/side @80%+. E.g. CMS m0w0d3 `Cl+J 80/[2,1]` (M modal [2,1]×32 I/CMS, ×55 MS).

## 3. Cells where we contradict TAKANO's habit

- SnPull+Sn × L,M: ours snatch-heavy [2,3]/[1,2] vs Tak fixed pull-heavy [3,1]. OURS m0w0d0 `SnPull+Sn 60/[2,3] 70/[2,3]…` vs TAK m0w4d0 `SnPull+Sn 60/[3,1] 70/[3,1] 80/[3,1]x4`.
- SnPull+OthSn × all: Tak never pairs this (0 slots all levels); ours runs 10/11/29 slots I/CMS/MS with modal [1,2]/[1,3].
- Cl+J × L: ours jerk-heavy triples [2,3] (I/CMS/MS: 71/70/107 hits) vs Tak clean-heavy [2,1]/[3,1]/[4,1] everywhere. (M and H agree: both [2,1]-family → [1,1].)
- OthCl+OthJ × M,H: ours loads 50+19 (CMS), 61+18 (I), 87+79 (MS) sets ≥80; Tak quarantines to L (~0 above 70 except CMS H 12×[1,1]). E.g. MS m1w1d3 `OthCl+OthJ …80/[2,2]x2 90/[1,1]`.
- ClPull+Cl × M: ours [2,2]/[1,1] vs Tak fixed [3,1] (MS M 13/13). L agrees ([3,1] both).
- OthSn+OthSq / OthSn+Press × all: Tak staple symmetric [3,3]/[4,4] L (6/6/29 slots CMS/MS); we never emit (pairs not in PAIRS).

## 4. Ratio-narrowing-with-weight?

OURS: yes by construction (1→3→7 legal ratios; modals narrow: Cl+J [2,3]→[2,1]→[1,1]). ROMAN: yes (per-side 2–3→1–2→1; combos capped ≤80%; 1+2+1 keeps squat-2 while ends go 1+1). TAKANO: only the competition lift narrows (Cl+J L [3,1]/[2,1] → M [2,1]/[3,1] → H [1,1], all levels + MSIC). Assistance complexes do NOT narrow — they are zone-quarantined flat: Pull+Sn [3,1] identical L+M, OthCl+OthJ [3,3]/[2,2] L-only, OthSn+* L-only. Verdict: our narrowing shape matches Roman/Tak only for Cl+J; for every other pair we narrow where Takano quarantines.

## 5. Verdict: ratio cells to change (pair, tier, old → new)

1. All 7 pairs × H: (1,1) → none (delete H tier from SCHEDULES); keep Cl+J/OthCl+J [1,1] only as 7–10d test singles. Kills §2-row 1 (MS 79+55+40 H-sets) and matches Roman ≤80% + Tak quarantine.
2. SnPull+Sn, SnPull+OthSn × L,M: {(2,3),(1,2),(1,3),(3,2),(2,3)} → {(3,1)} only (forbid 2nd≥1st). Copies Tak fixed [3,1]; kills inverted OURS m0w0d0.
3. Cl+J, OthCl+J, Cl+OthJ × L: {(2,3),(1,2),(1,3),(3,3)} → {(2,1),(3,1),(2,2)}. Copies Tak clean-heavy L; kills CMS m0w0d3 / III m3w3d5; satisfies Roman jerk≥clean everywhere except kept [2,2].
4. OthCl+OthJ × M,H: {(2,1),(1,2),(1,1),(2,2)} → none (L-only pair; rl={(3,1),(2,1),(3,2),(2,2),(3,3)} kept). Copies Tak quarantine; kills MS m1w1d3-type 166 M+H sets.
5. SnPull+*, ClPull+* × all tiers, classes III/II: any → none (no Pull+X schedules below Class I). Roman p61 low-class rule; ours currently emits none here anyway — lock it so III/II stay clean.
