# Adversarial review: OURS Class III vs Roman low-class (III–II)

Verdict: group mix + month volumes are near-clones of Roman's worked Class III 75kg example; failures are all intensity-ceiling / reps-per-set / density, worst at the end (meso 4).
OURS parsed from `outputs/III.json` slots (`[zone,reps]`; `+` slots split `[clean,jerk]`). Roman refs: volumes/intensity/selection briefs (pp. cited therein).

## PASS (exact matches — do not "fix")
- Month volumes: m0 997 / m1 1097 / m2 1247 / m3 897 / m4 748 lifts vs Roman low-class prep 1000–1500, comp 750–1050 (plan 1250/900). m4 is 2 lifts under the comp floor — trivial.
- Group mix m2 (1247): snatch 250 (20.0%), clean 218 (17.5%), jerk 135 (10.8%), front/back sq 332 (26.6%), other sq 187 (15.0%), press 125 (10.0%) — vs Table 11: 20 / 17 / 11 / 27 / 15 / 10%. m3 identical (20.1/17.3/11.1/26.6/14.9/9.9%).
- Classic shares m2: snatch 125/250 = 50% (Roman 50%), clean 94/218 = 43% (44%), jerk 91/135 = 67% (68%). m3 same (50/43/67%).
- NO pulls anywhere (37×4-slot, 26×3-slot sessions checked) — correct per p61 (low-class: no pulls; power variants suffice).
- Press = 10.0% every meso; ≤2 large (>100) sessions/week everywhere (exactly 1/week).

## FAIL (severity-ranked)
1. **SEVERE — 100% zone in Class III prep/volume block (cap 90–95% snatch / 90–92.5% C&J, p121).** m4w2d0 `Snatch [60,2],[70,1],[60,2],[70,2],[80,1],[90,1],[100,1]`; same day `Other Snatch …[90,1],[100,1]`; m4w2d5 `Clean+Jerk …[90,[1,1]],[100,[1,1]]` (i.e. clean AND jerk at 100% together). Roman: 100% 1–2 sets once per 7–10d snatch / 10–14d C&J, never as prep capstone; 90% ≤5 / 95% ≤3 per session. A double at 100% C&J is a qualified-lifter pattern, not III.
2. **MAJOR — squat reps/set exceed Table 1 / p68 (45–85%: 2–6; middle 1–4).** m2w1d2 `Squat [60,8],[60,2],[70,2]×6,[80,2]×9…` (60%×8); m2w0d2 `Squat …[60,7],[70,5]…`; m0w3d2 `Squat …[60,7],[70,3]×4…`. Light/middle III should be 1–3/1–4 per set; 7–8×60% is GPP-style volume Roman reserves for 6–10× other-squat types only.
3. **MODERATE — 90%+ timing: no post-comp exclusion week.** Roman Table 15: 0× 90%+ in wk1 after comp; 90%+ concentrated wk2–3. OURS puts `[90,1]` singles in m1w2d0 Snatch, m1w1d0 Other Snatch, m1w3d3 `Other Clean+Jerk [90,[1,1]]` — i.e. scattered ~1/week from m0w1d5 (`Clean [90,1]`) onward with no deload gap. Frequency (~1 single/session) is within ≤5@90%, but placement ignores the wk1 rule.
4. **MODERATE — session density extremes.** Largest: m4w1d2 148 lifts (`Other Snatch 25 + Clean/Jerk-pair 33 + Squat 65 + Other Squat 25`), m0w3d2/m2w0d2 145, vs Roman shock Mon 130 / Fri 135 (p121) — 10–13 lifts over the exemplar with 4 movements (Roman: 5–8 exercises for large sessions). Smallest: m4w3d2 24, m3w3d0/…5 31 lifts — under S=50 norm (p106), i.e. wasted travel days, not active-restoration 40–50.
5. **MINOR — press-before-max-C&J adjacency.** Presses correctly sit last slot (middle/end, p70), e.g. m1w0d2 `… Squat 56 + Press 24`. But m4w1d0 `Snatch …[90,1],[90,1] + Press 26 ([90,1],[80,4],[80,3])` pairs a 90% press day immediately before m4w1d2's 90%-snatch/squat peak — Roman: "never heavy press day before submax/max C&J" (p70).
6. **MINOR — full classic C&J cadence.** Roman: complete C&J every 7–10d (p55–56). OURS does classic `Clean+Jerk` only 5× total (m3w3d5, m4w0d5, m4w1d5, m4w2d5 + one `Clean+Jerk` split) — technically within cadence but back-loaded; first 3 mesos run almost entirely on split `Other Clean+Jerk` pairs (e.g. m0w0d2 `[60,[3,2]]×4…[80,[1,2]]`).

Fix priority: strip all 100% slots in III (cap at [90,1]×≤3 / [95,1]×≤1); clamp squat 60–70% sets to ≤4–6 (split 7–8s into two series per p68); re-add a zero-90% week after each volume peak.
