# Adversarial intensity audit (slots ground truth, READ-ONLY audit)

Method: figures from `slots` [zone,reps] (pairs split); zones nominal % of own max. Ours = 5x4 wks;
Takano = 8-17 wk blocks; per-week normalized. DENOMINATOR WARNING: Roman Tables 5-6 denominate pulls/squats
in % of limit SNATCH/C&J, ours/Takano in % of each movement's own max — squat/pull zone
shares are NOT comparable to Roman; classics (same-movement %) ARE.

## S1 (critical): III/II prescribe ZERO pulls
- `outputs/{III,II}.json` contain no SnPull/ClPull slot at all (0 lifts) vs Takano III 131+103,
  II 144+117 pull lifts. Not an intensity miss — a selection hole. (Finding 4's "selection
  matches" is false for pulls at low classes.)

## S2 (critical): snatch-pull catastrophically light; clean-pull OK
- SnPull mean (own-max %): ours 70.4/70.4/72.9 (I/CMS/MS) vs Takano 86.9/92.6/93.8.
  90%+ share: ours 3.5/3.0/6.5% vs Takano 58.9/88.8/86.1%. SnPull is parked at 60-80 while
  Takano lives at 80-100. ClPull by contrast matches (means 83.6-88.6 vs 80.0-89.1; 90%+
  46-70% vs 8-73%) — the bug is snatch-pull-specific (likely zone-map bug, cf. movements[]
  arrays logging all SnPull in bin0).

## S3 (major): classics too light with wrong mode at every level
- Classic (Sn/Clean/Jerk) mean: III 67.6 vs 72.0; II 68.7 vs 73.5; I 70.7 vs 75.6;
  CMS 71.1 vs 75.3; MS 72.0 vs 76.9 (ours always -2.5 to -5.0).
- Modal classic zone: ours 60/70 vs Takano 80 (II/I/CMS/MS). One full zone low.
- Classic 90%+: ours 2.9/1.4/4.4/4.6/5.6% vs Takano 7.5/5.5/9.3/8.0/12.7% (~half).
- All-lifts picture is closer (means -1.6 to -2.6; mode 80 both except our III at 60) only
  because heavy ClPulls mask weak classics. Note: slots show a 69.4->75.5 mean gradient,
  so Finding 2's "flat 72.1-72.5" understates the slope (counting-method artefact) — but the
  LEVEL is still 2-3 pts under Takano everywhere.

## S4 (major): prep->comp 90%+ surge is half Takano's amplitude
- Ours m0->m4 90%+ (all lifts): III +4.6, II +4.2, I +9.8, CMS +16.3, MS +18.9 pts.
  Takano prep->precomp: III +3.9, II +15.6, I +28.3, CMS +22.3, MS +31.6 pts.
- Takano precomp classic 90%+ hits 14.5/15.4/40.6/34.3/47.4% (III/II/I/CMS/MS); ours never
  gets near that density. Our taper shape (70+/wk peaks m2, falls m3-m4) is right; the
  top-zone amplitude is not.

## S5 (moderate): 70%+ volume EXCEEDS Roman quotas — inherited, then worsened
- Family 70+/wk, peak meso: ours III 78, II 91, I 140, CMS 148, MS 188 vs Roman quotas
  (~MS 102 prep/79 comp; I/CMS 87 last-prep/76 comp per wk). Takano also overshoots
  (MS 155, CMS 152, I 128/wk prep), so the breach is inherited — but our MS m2 (188/wk)
  runs ~30/wk hotter than Takano's average. Quota-breach is a Takano-vs-Roman dispute;
  ours escalates it at the top end.
- Composition too bottom-heavy: 70/80/90+ split ours III 67/29/4, II 62/36/2, I 54/40/6,
  CMS 56/37/7, MS 55/37/8 vs Roman I/CMS 60/28/12, MS 60/28/12 and Takano MS 44/44/11.
  Too much 70, too little 90+.

## S6 (moderate): final-week taper is backwards
- Ours: ZERO classic 90%+ in the final week at ALL classes (also zero family 90+).
  Roman prescribes ~10% remnants (I/CMS avg 22@70/10@80/2@90+); Takano keeps 0/0/3/9/9
  classic 90+ (III/II/I/CMS/MS, spread across lifts). Zero is correct only for
  heavyweights (p150-151); for I/CMS it over-tapers vs both books.
- Simultaneously ours LEAKS 100%+ ClPulls into the final week (I 1, CMS 2, MS 4 lifts)
  where Roman demands NONE in week 4 (p110) and Takano has ZERO at every class.
  Clean on classics, dirty on pulls — exactly inverted.
- m4 week-3 holds 37-39% of meso 90%+ (cap <=35%, p109); final wk keeps 6-7% vs ~10% — wrong exercise.

## Caveats
- Takano's 36-49% precomp 90%+ may be competition-week artefact — match SHAPE, not raw %.
- Ours m4w1 volume spike (MS 418, CMS/I 332) vs shock-week-on-comp-weekday rule unchecked.
