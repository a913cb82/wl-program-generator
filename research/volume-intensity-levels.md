# How volume, intensity, and exercise selection scale with lifter level

Research question: how should a generated program differ for lifters of
different levels, at each scale — macrocycle, mesocycle, microcycle,
training session? Sources: Takano (sample programs, in JSON fixtures),
Roman "Training of the Weightlifter" (transcribed in full:
`research/roman-transcription/chunk-1..5.md`; mined extractions in
`research/roman-mining/{volumes,intensity,selection}.md`).

All cross-source numbers below use one shared bin grid per movement
family. Caveat (Finding 4): our bins are % of each movement's own max;
Roman denominates everything in % of limit snatch (snatch work) or
limit C&J (everything else). Pull/squat "90%+" therefore means
different things — comparisons are valid within classics, and need a
conversion elsewhere (≈ squat max is 125–133% of C&J, p64–65).

## Finding 1 — Takano's volume curve across levels is steeper than ours

| Program | Ours (annual) | Takano (annualized) | Delta |
| --- | --- | --- | --- |
| III | 12,000 (230/wk) | 9,230 (178/wk) | −23% |
| II | 12,000 (230/wk) | 10,383 (200/wk) | −13% |
| I | 15,000 (288/wk) | 15,877 (305/wk) | +6% |
| CMS | 15,000 (288/wk) | 18,521 (356/wk) | +23% |
| MS | 18,000 (346/wk) | 21,393 (411/wk) | +19% |
| MSIC | 18,000 (MS grid) | 26,652 (513/wk) | +48% |

Roman's monthly bands (prep/comp, p88) converted to weekly (÷4.33):
beginners 254–300/208–231; low-class 231–347/173–243; I&CMS 300–462/
219–335; MS 347–624/254–439; MSIC ≈300–577/219–404. Takano's prep-week
averages (III 208, II 227, I 357, CMS 406, MS 479, MSIC 598): classes
I and up sit inside Roman's prep bands; III/II fall *below* even the
beginner band. Our generator (230/230/288/288/346) sits at the floor
of Roman's bands at every level. Open: is Takano III/II a lighter
pre-competition block type, or does Roman's "beginner" sit below
Class III? (Roman milestones, p81: Class III at end of year 1 —
his "beginners" are first-year lifters, so Takano III should map to
his low-class band 231–347, against which 208 is still ~10% light.)

## Finding 2 — levels differ by volume AND weight, not volume alone

| | Mean zone | 90%+ share | 60-share | Modal zone |
| --- | --- | --- | --- | --- |
| Takano III → MSIC | 71.9 → 78.6 (+7) | 3.7% → 23% | 26% → 9% | 80 (~40–48% every level) |
| Ours III → MS | 72.1 → 72.5 (flat) | 8.6–10.9% (flat) | 11–17% (flat) | 70 (~38–46% every level) |

Roman confirms the direction and grades it further: high-intensity
(70%+) quotas in snatch+C&J rise with level in absolute terms (MS
middleweight 443 prep / 342 comp per month, p107; I/CMS 56kg 378/mo
last prep month, p130–137); at the very top (MSIC/WR) the 70–79%
band shrinks while 80–89% and 90%+ stabilize (p160). Heavier weight
classes do *fewer* high-intensity lifts for the same effect (p47,
p54–55) — a within-level gradient by bodyweight our model lacks.

## Finding 3 — the 90%+ gradient lives in assistance, not classics

Classic snatch+C&J lifts at 90%+ per month: Takano III 11, II 12,
I 36, CMS 38, MS 57, MSIC 80 — proportional to month size, matching
Roman Tables 2–4 almost exactly at every level (low 20/mo at
1250/mo ≈ 1.6% vs Takano III 1.4%; I/CMS 47/mo at 1650 ≈ 2.8% vs
Takano 2.7%; MS 56/mo at 2100 ≈ 2.7% vs Takano MS 57 at 2074).
The steep all-groups gradient (3.7% → 23%) is driven by pulls and
squats done heavy: Takano SnPull+ClPull at 90%+ goes 10 → 281/mo
across levels. Roman agrees structurally (pulls ~45–50% at 90–99%,
squats with 100%+ singles, both increasing with level, p63–67).

## Finding 4 — exercise selection already matches Roman; intensity does not

Classic share of each lift family, prep period (Roman Table 11,
p102/p45/p53 vs our built plans):

| Family | Roman low / I,CMS / MS | Ours III / I,CMS / MS |
| --- | --- | --- |
| Snatch | 50 / 45 / 40% | 50 / 45–44 / 39% |
| Clean | 44 / 40 / 38% | 44 / 41 / 38% |
| Jerk | 68 / 58 / 46% | 67 / 57–58 / 43% |
| Front+back squat share of month | 27 / 23 / 20% | 27 / 23 / 19% |

Nearly exact — the DAY template already encodes Roman's selection
gradient. Correction (2026-10-31 adversarial review): the MS jerk cell
was overstated at 45% (actual prep 42.6%, whole-program 42.9%); two
small same-direction absolute-cell errors amplify in the ratio, and the
table above mixed whole-program and prep denominators across rows.
Gradient direction still holds (68→58→46 vs ours 68→57–58→43) with
the last step overshooting ~3pp. Gaps: other squats vanish in our I+ plans (Roman keeps
~6% prep at I/CMS, large heavyweight volumes at MS); presses vanish
above III (Roman keeps press/bendover/other work at ~15–18%, folded
into our Fundamental bucket at 15–18% — roughly consistent in total,
different in composition).

So: selection ✓ (keep), intensity shape ✗ (fix). The `zone_alloc`
work should grade the intensity profile with level — more 90%+,
less 60%, modal mass shifting 70 → 80 — while leaving the DAY
selection template alone. Within-level, add the bodyweight
correction (heavier lifters: fewer high-intensity lifts, p45–47).

## Session and week structure (inputs to rhythm work)

- Day sizes: S ≤50, M 51–100, L >100 lifts; ≤2 large days/week for
  low-class; named 3–6 day combos (p106–107, p121). Our sessions
  match in shape but we don't model S/M/L types explicitly.
- Week variants (Table 13, p111): 1, 2, 3-1, 1-3, 2-4, 4-2 with
  fixed % splits; volume and intensity waves concur in prep, may
  contrast in comp (p131–136, p148); shock day = competition
  weekday (p110); final week 11–14% of month (p105).
- Submax/max placement: ≤35% of month's in week 3, C&J capped at
  week 2, last-lift lags 5–19 days by lift and weight (p108–110);
  final-week protocols differ by weight class (p141).
- Rest: Sunday off; 3-day rest post-competition; 90%+ repeat
  rules 2–3 days same exercise, daily if rotated (p48, p57).

## Open questions

1. Micro/meso/session scales: how do wave shape, rest days, and
   exercise mix change with level? (Partially answered above;
   session-mix gradients still open.)
2. Weekly shapes within each band: which Table 13 variant per
   level/period? (Miner data present; fitting open.)
3. MSIC anomaly: trains ~25% more than MS at similar intensity.
   Roman: MSIC does 200/150 fewer monthly lifts than MS (p88) —
   contradicts Takano MSIC's +25%! Resolve: different MSIC
   definitions, or block vs year effect?
4. Our CMS mean zone dips below our I (72.2 vs 74.2). Generator
   noise or real? Revisit after zone_alloc grading.
5. Bin denominators: convert our per-movement %s to Roman's
   limit-S/limit-C&J basis (or vice versa) before fitting zone
   tables directly. Squat norm 125–133% of C&J (p64–65) anchors
   the conversion.
