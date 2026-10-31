# Complexes code-path review (wlgen.py + wlconfig.py, READ-ONLY)

## 1. Lifecycle of a complex (allocation → pairing → zoning → rendering)
1. **Allocate:** annual → meso `spread()` → week nominals; `week_sessions` picks first feasible S/M/L variant (`VARIANTS`, `CAP`); `fit_session` IPF group×session matrix under slot-matchability (`resolve_slots`/`cover_session`) + `prune_doses` (`MIN_DOSE`=6).
2. **Pair:** `detect_pairs` finds co-hosted listed pairs sharing one complex slot; `pair_fit` hill-climbs each instance to a legal tier schedule (`pair_options` over `SCHEDULES`, ≤6 cands each), freezes pairable rows, refits only `BALLAST` (squat-family) rows; week targets flex to the snap.
3. **Zone:** `pair_zones` pools each ref-family's units (`week_units` tiers H≥90/M=80/L<80 from `week_bin_lifts` on the **ref** member), splits over paired sessions (flat prior + base floor + `close_ramps`), adds taper `pair_topup` via `take_up_slack`, `close_session` at ref level. Each ref-zone unit × tier ratio (rh/rm/rl) → member bins via `map_zone_index` (clamp out-of-range to edge bin). Rounding drift absorbed by free ballast cells; `consolidate_doses` 4-cycles the rest.
4. **Render:** per-session ref vectors (`refdata`) → `pair_choices` beam search with `pair_fill` rep caps (tightest side wins, per-side reps flat-or-falling upward); `session_dose` counts paired work against **both** members.

## 2. Baked-in assumptions vs the books
- **A+X shares one complex slot; one movement per slot** (`COMPLEX_SLOTS`, `cover_session`). SHARED: Takano runs `Clean+Jerk` on every classic day, variant pairs on variant days (method-takano §1); Roman orders combos as units (p156).
- **Ref member limits the complex; zones/labels/tiers follow ref** (`PAIR_REF`, `week_units`, `pair_choices`). SHARED: "the complex is one weight" (SYNTHESIS adjudication); Roman intensity = ÷ limit snatch / limit C&J (roman-mining/intensity.md).
- **Legs split by fixed per-tier ratio, narrowing with weight** (`ratio_ok`: 1:1 only ≥90; `SCHEDULES` monotone). MOSTLY SHARED: Takano complexes are [1,1]/[2,1]/[2,2] (level-III-takano); but ours snaps every session to exactly one schedule — book ladders vary within a session.
- **Both legs count toward both members' bins/doses** (`session_dose` double-count; `actual`). SHARED-ish: Roman counts combos rep-by-rep (`140/2+2`, p60-61; sessions.md notes ours undercount-equivalent at 80%). Ours double-counts volume both sides, inflating totals.
- **Out-of-range ref zones clamp to member edge bin** (`map_zone_index`). ALIEN: a 60%-classic pull becomes an 80%-pull-bin rep; Roman gives pulls their own % scale with min ≈60% (p61–63) and best-technique 90–95%.
- **Pairs exempt from MIN_DOSE; ballast pays rounding drift** (`count_dose_violations` skips paired; `plan_sessions` absorb loop). ALIEN: no book min-dose; Roman does 10–30 lifts/workout in snatch+variants (selection.md).
- **SnPull exists only glued inside `SnPull+Snatch`** (no solo heavy-pull host; ClPull gets solo slots). ALIEN, confirmed: "100% of SnPull renders paired at 60–80" while fit demands 59–89% at 90+ (SYNTHESIS banked §); CMS OURS-only complexes vs Takano standalone `SnPull`/`Press`/`Jerk` (level-CMS/MS-takano S7).

## 3. Three most book-alien mechanisms
1. **No solo heavy pulls.** Fit wants 90%+ SnPull; renderer can only place pulls at classic-bar 60–80 inside pairs. A coach would prescribe standalone pulls at pull-% (Roman p63–64: 2–6 reps @80–99%).
2. **Classic-weight pulls counted as pull-bin volume.** Pull reps lift the classic's bar yet fill the pull distribution's top via clamping — one weight, two books, neither correct.
3. **Snap-then-ballast week surgery.** `pair_fit` hill-climb (20k evals) + `close_ramps` inter-day swaps + drift absorption by squats: volume decides intensity and squats pay for complex rounding. Roman fits volume to placed heavy lifts, backwards from comp date (method-roman §4).

## 4. Highest-payoff single change
**Tops-first, role-scripted complexes:** allocate counted 90%+/100%+ lifts — including solo heavy-pull slots at pull-% — FIRST, with weekday roles (classic/variant/strength, per method-takano §3 + SYNTHESIS banked program), then pour volume around them. Subsumes solo-pull hosting, thin-top starvation, and most of the `close_*` repair stack.
