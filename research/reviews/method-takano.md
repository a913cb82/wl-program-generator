# Method: Takano's construction vs ours

Evidence: `tests/fixtures/takano-*.json` (6 levels), volume-intensity Finding 3.

## 1. Takano's probable construction order (argued from repetition)

Fixed first: the **weekday exercise script**. At MS, day identities repeat almost
exactly across weeks — Mon/Wed/Fri train Snatch+Clean(+Squat), Tue/Thu/Sat train
Other-Snatch+Other-Clean+Other-Squat, Saturday is pulls+squat only
(`m0w0`–`m0w2` day sets nearly identical; `Clean+Jerk` complex on every classic
day, `Other Clean+Other Jerk` / `Other Snatch+Other Squat` on variant days).
Volume waves ride on top and never repeat (MS weekly vols 579→391→505→434→567…;
day count breathes 4–6), while the alternation survives. So: **days → exercises →
zones**, not volumes → hosts → zones.

Second: **day roles fix the intensity ceiling**. Variant days cap ~70 while
classic days carry 80–90+ (MS w0; Saturday SnPull 100). Finding 3's gradient
(90%+ in pulls/squats, 10→281/mo) follows: heavies belong to strength-role slots,
and level buys more strength-role volume.

Third: **taper deletes by role, then scales down**. Final weeks shrink day count
and volume together (MS …391→326→228→187→116; CMS …320→226→216→182); classics
lose 90%+ first. Low levels scramble the script itself (III `m0w0`–`m0w3` day
identities share almost nothing) — the template is a habit strength grows into,
not a universal scaffold.

## 2. Right output, alien mechanism

- **Classic share matches** (Finding 4: Snatch 50/45/40 etc. nearly exact) — but
  ours falls out of annual ratios + the DAY slot template, while his falls out of
  counting classic-role vs variant-role days. Same totals, different cause.
- **S/M/L session shapes match** — ours from the `VARIANTS` pattern table + CAP
  search (`week_sessions` first-feasible); his from day roles (Saturday small but
  heaviest: SnPull 100 on the lightest day). Size and heaviness are decoupled in
  his build, correlated in ours.
- **Top-zone concentration** (`PHASE_PEAK` prep 2.0 gather, fitted to Takano) —
  ours gathers 90%+ onto big days via the `peak` exponent in `zone_alloc`; his
  gathers onto classic/strength-role days regardless of size. The knob reproduces
  his statistic while inverting his rule.
- **Contiguity** (`close_ramps`/`close_bins` swaps) — we repair gaps after IPF
  rounding; his sessions are ramps, so gaps never occur.

## 3. Habits our machinery cannot express (missing mechanism each)

- **Classic/variant weekday alternation.** No object in `wlconfig`/`wlgen` names a
  weekday's exercise role; `week_quota` staggers phases per slot to *avoid*
  regularity, the opposite of his script. Missing: a weekday→exercise-role table.
- **Saturday strength day.** Pulls+squat-only sessions with the week's top zone
  (SnPull 100) violate every prior we have (peak gathers top onto high-volume
  days). Missing: role-based, not size-based, zone permission.
- **Variant-day intensity cap.** Variants stay ≤70 even on big weeks — a ceiling
  attached to the exercise, not the day. Our `BINS`/`shift` grade zones per group
  globally; nothing caps an exercise on specific days. Missing: per-role ceilings.
- **Taper by day deletion.** His day count shrinks into competition (6→3); our
  `sessions()`/`demand_days()` derive day count upward from volume, so taper can
  only shrink days, never delete roles first. Missing: role-dropout ordering.
- **Level-dependent script rigidity** (III scrambles, MS repeats). Our quota/prior
  machinery uses one regularity at all levels. Missing: a level knob on adherence.

## 4. The single construction-principle change

**Fix the weekday exercise script before allocating a single lift: build
days-outward from weekday roles (classic / variant / strength), then pour
volume and zones into roles — instead of volumes-downward from annual ratios
through `spread → week_sessions → week_quota → zone_alloc`.** Everything else
(ratios, bins, GAP/FAN) becomes calibration of a script-first builder rather than
the builder itself. That one inversion reproduces his alternation, his Saturday
heavies, his role-based taper, and his level rigidity gradient — none of which
are expressible as settings on the current chain.
