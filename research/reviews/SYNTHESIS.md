# Fleet synthesis: 17 adversarial reviews (2026-10-31)

Readers: `research/reviews/volumes.md`, `intensity.md`, `sessions.md`,
`methodology.md`, `selection.md` (fleet 1, cross-cutting) and
`level-{III,II,I,CMS,MS}-{takano,roman}.md`, `method-{takano,roman}.md`
(fleet 2, sharded). This file adjudicates: what we fixed, where the
books disagree with each other, and what is banked architecture.

## Fixed this turn (all green, 207 tests)

1. **Invented top zones (all 5 level reviews + intensity S2/S3).**
   The comp-meso upward shift pushed mass into zone 100/110 where the
   yearly frac is zero (e.g. III Snatch m4w2: 0.04 @100 from a 0.0
   base). `shift()` now treats zero-base zones as walls: moves into
   them are skipped without spending delta, so heat pools at the
   highest allocated zone. Low-class 100% singles: gone at every
   class. Side effect, and the point: pooled heat lands on 90s, where
   we were starved (II m1/m2 classic 90+ was literally 0).
2. **Final-week pull maxima (intensity S6, MS-roman SEV-3, CMS-roman
   #4).** The taper stripped classics only; 100%+ clean pulls leaked
   into week 4 (I 1, CMS 2, MS 4) where Roman (p110) and Takano (zero
   everywhere) agree there are none. `taper()` now strips pulls ≥100;
   `taper_topup()` rehomes the slack to weeks 1–3 like classic slack
   (Roman: maxima move to week 3). Squat/fundamental 90s in week 4
   stay: both books allow ~10% remnants; we hold ~6–7%.
3. **Finding 4 MS-jerk cell (selection S1).** Was printed as 45%
   (Roman 46); actual prep 42.6%. Two small same-direction
   absolute-cell errors amplify in the ratio; rows also mixed
   whole-program and prep denominators. Corrected in
   `research/volume-intensity-levels.md` (43% prep, denominators noted).
4. **Ramp-test calibration.** The old bar demanded uniform dose
   thickness below every top — stricter than the books (Roman ramps
   taper upward; any nonzero rung renders legal sets) and our README
   guarantee ("one unbroken run"). Recalibrated to contiguity with
   the spare-gate kept. The two sessions that tripped it
   (`[6,9,2,1]` pyramids on big shock days) are textbook-shaped.

Book score 2.63 → 2.81 (+0.18): excess 219.7 → 204.3 (less
over-capacity stacking), instructions 9641 → 9505. Ship constraints
(illegal/clash/idle/gaps) hold at zero everywhere.

## Source conflicts (do NOT "fix" without picking a side)

- **80-modal vs 70-pyramid.** Takano programs 80-multis routinely
  (modal 80, CMS ClPull `[100,2]x3`); Roman's quotas want 70 > 80 >
  90+ (254/116/50) with pull 100%+ as singles. We fit Takano's
  texture, so Roman's counts read us ~1.5–2x hot in prep. Both
  positions are documented; texture follows the sample programs,
  quotas stay an open research question (external-count targets are
  the tops-first project's business).
- **Selection: textbook vs coach.** Takano's classic shares RISE with
  level (snatch 50→62%) while Roman's fall (50→40); Takano programs
  pulls (and 90% press days) for III/II against Roman's explicit
  no-pulls rule (p61). We side with Roman (zero pulls low-class,
  Table-11 mix within 0.3pp nearly everywhere). Do not fit selection
  to fixtures.
- **Annuals: our rate vs Roman's year.** Our 13k–22k annualize a
  loaded 20-week block; Roman's year totals (MS 18k) include
  deload/transition months his bands omit. The rate matches Takano
  (MS +2.5%); the year-over-year comparison overstates us. Keep the
  rate; label it honestly.
- **Low-class heaviness.** Roman prescribes a few 90s/mo at III/II
  (13/8/5 prep); Takano's blocks show ~nothing in prep and 90-only
  peaks. Our fitted top bins are near-zero low-class: prep-starved
  per Roman, faithful per Takano-prep. The wall fix feeds 90s (not
  100s) to comp mesos — the compromise both books tolerate.

## Reviewer artifacts corrected during adjudication

- "Takano rarely exceeds 80" (sessions S1) is false: his MS 90%+ is
  23%. Our 90+ dose is thin vs his, not vs a strawman.
- "Squat 60×7–8 violates Table 1" needs the zone: Takano writes
  `Squat x8` too (at 60). Our grinds are texture, not violation.
- Final-week squat 90s are within Roman's ~10% allowance, not
  violations. Only pull 100+s were (fixed).
- Intensity S2's "zone-map bug" is a hosting bug: pair sides inherit
  the classic's zone (correct — the complex is one weight), but solo
  heavy SnPull never gets hosted (see next).

## Banked: the tops-first program (unanimous across 3 method reviews)

The single biggest confirmed debt: our SnPull fit demands 59–89% of
pull volume at 90+, but 100% of it renders paired at 60–80 (ClPull
matches fit because it gets solo slots). More generally, classic 90s
render 30–50% under fit while squats render over — tops are residue
of shifted distributions, not the plan. All three method reviewers
independently prescribe the same inversion: allocate counted
90%+/100%+ lifts (and weekday roles: classic/variant/strength-day
with ceilings, shock-day pinning, lag tables, role-based taper) FIRST,
then pour volume around them. That project subsumes: solo heavy
pulls, thin-top starvation, m4w3 >35% concentration, L-day movement
counts (3–4 vs Roman's 5–8), S/L/S/L whipsaw, uniform 4.1 wave and
26% comp cut (Takano/Roman both steepen with level), and most of the
`close_*` repair stack. Evidence files are linked above; the two
`[6,9,2,1]` shock-day sessions are the motivating example (thin top
correctly placed, ramp a lift short of our old bar).

Near-term (no architecture): grade the comp cut by level, split the
III/II annual (Takano +12% II over III), Other-Squat dose at I+
(~6%, from the Fundamental bucket), III/II small top-bin 90s in prep
(a few, never 100s).
