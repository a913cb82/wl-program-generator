# Session-realism audit (adversarial, 2026-10-31)

Sources: outputs/{III,II,I,CMS,MS}.json vs tests/fixtures/takano-*.json; Roman rules = research/roman-mining/selection.md secs 95-103,133-135 (Table 1 reps/set; S<=50/M 51-100/L>100; 2-3 ex. small / 5-8 large; squat+pull near-daily; press mid/end; low-class <=5@90%/<=3@95%, 100% per 7-14d).
Metric: lifts/session = sum reps over slots (complex [a,b] counts a+b, per Roman p60-61).

## S1 — Submax/max dose per session explodes at high classes (worst)
- MS avg 7.2 sets >=90/session, max 27; III avg 1.5, max 7. Takano fixtures almost never exceed zone 80.
- CMS m4w2d3: Snatch 3x[90x1]+100x1, Other Clean 3x[90x1]+100x1, Squat 5x[90x2]+2x[90x2]..., Fundamental 90x2+3x100x1 — ~17 sets >=90 in ONE session, 100% in 3 slots same day. Low-class cap is <=5@90/session; qualified norm ~10 submax middle-class/workout (p48,57) — this doubles-triples it.
- MS m4w2d2: 23 sets >=90 (SnPull+OtherSn 14-set slot ending 90/100/110 mixes, C+J 9 sets incl 3x100x[1,1], ClPull to 110x2, Fundamental to 110x1). No taper logic; comp-month rules ban this clustering (secs 133-135).
- III stays mostly clean (singles only at 90, rare 100) — the generator's intensity model visibly detaches from class.

## S2 — Marathon slots: 14-24 sets in one movement (uncoachable)
- Roman: 10-30 lifts/workout per lift group (p48-60); Takano slots are 4-6 sets. Ours: III m2w1d2 Squat 24 sets ([50x1..90x1] warmup + 17x70/80 doubles + 90x1); CMS m2w2d1 Fundamental 24 sets; I m3w1d2 Squat 30-set region.
- CMS m0w1d2: SnPull+OtherSn 14 sets alternating 60/70x[1,2] then 80s; Fundamental 14x80x2. No coach runs 14 identical sets; Takano varies 4-5 sets then moves on.
- Root cause: large (120-148 lift) sessions keep only 3-4 movements, so each slot absorbs 30-50 lifts. Roman demands 5-8 exercises when large (p156). Takano-CMS large days have 6-7 movements; ours never exceed 4.

## S3 — Sawtooth ladders, feeler-singles, yo-yo zones
- Typical slot: III m0w3d2 Snatch [60x3,70x3,60x3,70x3,60x3,70x3,80x2x3,90x1,60x2,60x2,70x2,60x3] — climbs, collapses to 60, climbs again. Roman: monotonic ramp to top set(s), then optional back-off; power-sn->snatch handoff is 5-15 kg step (p48-52), not 60-70-60-70 oscillation.
- Feeler-single pattern: CMS m4w1d0 SnPull+Snatch [..80x[1,2],90x[1,1],60x[3,2],70x[3,2],80x[1,2],90x[1,1]] — a 90-single mid-slot, then back to 60. Same in MS m4w2d3 Squat (90x1 buried between 60x1/70x1 warmup singles and 60x5 volume). Takano repeats one zone (e.g. 5x70x4), boring but coachable.
- Warmup-to-top is continuous only because zones are quantized to 50/60/70/80/90/100/110 — no >10pp jumps exist by construction, which hides rather than solves ladder design.

## S4 — Reps/set: between Table 1 and Takano — but on the wrong side for low classes
- Table 1: classics 1 rep at 80-89%. Takano violates routinely (classic 80+ multi-rep sets: CMS 143/55 sess=2.6/sess, MS 236/83=2.8/sess, III 21/26=0.8/sess).
- Ours: III 64/71=0.9, II 99/71=1.4, I 81/89=0.9, CMS 74/89=0.8, MS 66/101=0.7 per session. So at III/II we are *worse* than Takano-III/II; at CMS/MS more conservative than Takano.
- Concrete: III m0w0d0 Snatch [60x3,70x3,80x2,60x2]; II m0w0d5 Snatch [60x2,60x2,70x2,80x1,70x2,80x2]; CMS m0w1d4 Jerk 3x80x2 + 70x3/80x2 cycling. All violate Table 1 (80%x2), matching Takano's habit — defensible for qualified, not for III/II prep where Roman caps at 90-92.5% with low reps.
- Complexes are worse and uncounted: I/CMS/MS program 80x[2,2]/[3,2] (=4-5 reps at 80%) e.g. CMS m0w3d5 Clean+Jerk 4x80x[2,2]; Roman counts rep-by-rep (140/2+2, p60-61), so these are 4-rep 80% sets — heaviest violation in the corpus.

## S5 — Session sizes: S/M/L mix present, movement counts wrong
- Sizes: III min/med/max 24/48/148; I/CMS 26/79/145; MS 26/78/150 vs Takano medians 52-80, max 103-185. Our range matches, but distribution whipsaws: III wk0 [42,125,42], MS wk0 [40,118,39,118,39] — alternating S/L/S/L, not Roman's wave (e.g. MS prep 90/60/100/110/77, p145).
- Small sessions still carry 3-4 movements (III: 26x 3-mov + 37x 4-mov; only 8x 2-mov) — Roman says 2-3 exercises if small (p156). Conversely 140+ sessions have just 3-4 movements where Roman wants 5-8.
- Single-movement days appear only at CMS/MS (CMS m3w0d1 Squat-only 48 lifts; m3w1d5 C+J-only 48) — no Roman precedent; Takano minimum is 2 movements and those are GPP-ish, not 48-lift squat marathons.

## S6 — Placement/frequency: legs do NOT train near-daily where it matters
- Roman: squats almost every workout (~20-30, to 60, split in 2 series if large, p68); pulls almost every workout, alternating sn/clean (p64); presses mid/end (p69).
- III: squat-days 3/3-4/4 per week (correct — low-class squat staple, no pulls at all: pull-days 0 — correctly follows "low-class: no pulls" p61).
- MS wk0: squat-days 2/5, pull-days 3/5; CMS wk0: squat-days 2/4. Squats are *less* than daily at the classes that need 20%-share leg volume. Takano-MS starts with Squat 45/83 sessions; ours starts SnPull+OtherSnatch 30/101, Snatch 28 — squat-first almost never (4/101).
- Presses vanish upward: III last-movement Press 29/71; Takano-CMS/MS end Press 24/55, 26/83. Ours I/CMS/MS end Fundamental 66/61/86 (opaque bucket) with whole weeks at 0 press-days (CMS wk0). "Fundamental" as a last-slot catch-all has no Roman equivalent and buries press placement auditing.
- Order is otherwise plausible (snatch/clean first, squat/fundamental last) — the one dog that didn't bark.

## Verdict
Conservative Table-1 discipline is claimed but not delivered at 80% (doubles everywhere, 4-5-rep complexes); intensity discipline collapses with class (MS 27x90+ in a day); set counts per slot (14-24) and 3-movement 140-lift days are the most visibly uncoachable artifacts. Fix order: (1) cap 90+ sets/session by class, (2) cap sets/slot + force 5-8 movements on L days, (3) enforce monotonic ladders, (4) kill 80%-doubles for III/II and 80%-complexes everywhere.
