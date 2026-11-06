# Sessions/week vs weekly volume: ours vs Takano vs Roman

READ-ONLY investigation. Scripts ran in /tmp (no repo edits). Branch state: `research/takano-sessions`
HEAD ~ `5c459c5 log: row alignment done`. Counts from JSON `movements` vectors
(sum of all reps in a session = session volume). "Session" = one row in
`sessions[]`; "day" = distinct `day` within (meso,week). Takano MS/MSIC rows
carry half AM/PM/null; all other fixtures and all outputs/* have half=null
(= 1 session/day).

## 1. OUR programs (outputs/*.json)

All half=null, so sessions == days, never any AM/PM split.

| class | total sess | weeks | sess/wk (avg) | wk vol (avg) | per-sess (avg) | wk range | per-sess range (weekly min/max) |
|---|---|---|---|---|---|---|---|
| III | 71 | 20 | 3.55 | 249 | 70 | 97–399 | 32–148 |
| II | 71 | 20 | 3.55 | 249 | 70 | 97–399 | 32–148 |
| CMS | 89 | 20 | 4.45 | 336 | 75 | 131–537 | 26–145 |
| I | 89 | 20 | 4.45 | 336 | 75 | 131–537 | 26–145 |
| MS | 101 | 20 | 5.05 | 422 | 84 | 165–675 | 33–150 |

Notes:
- III and II are byte-identical programs; CMS and I are byte-identical. Only 3 distinct programs.
- Sessions/wk is 3–6 by construction (taper 3, peak 6). No week has >6 sessions.
- Per-session volume scales WITH weekly volume: MS peak week (675/6) averages
  112/session with a 150-rep day; MS wk m0w3 (574/6) averages 96/session.
  The generator adds days (3→6) but never splits a day, so big weeks make big
  sessions (~110–150 reps), not more sessions.

## 2. TAKANO fixtures (tests/fixtures/takano-*.json)

Lower classes: no doubles at all (all half=null) — sessions == days.

| fixture | weeks | sess/wk | wk vol avg (range) | per-sess avg |
|---|---|---|---|---|
| takano-III | 8 | 3.25 (3–4) | 178 (91–288) | 55 |
| takano-II | 9 | 3.22 (3–4) | 200 (118–291) | 62 |
| takano-I | 12 | 4.17 (3–5) | 305 (129–428) | 73 |
| takano-CMS | 12 | 4.58 (3–6) | 356 (182–505) | 78 |
| takano-MS | 17 | 6.88 (3–10) | 411 (116–593) | 60 |
| takano-MSIC | 17 | 7.82 (3–9) | 513 (154–715) | 66 |

Doubles (AM+PM same day) exist ONLY in MS and MSIC:
- takano-MS: every prep week (m0) has 2–4 double-days out of 4–6 training days
  (e.g. m0w0: 6 days -> 9 sessions at 579; m0w8: 6 days -> 10 sessions at 593;
  m0w1: 4 days -> 6 sessions at 391). Comp taper weeks shed doubles
  (m1w2: 4 days/5 sess; m1w3: 4 days/4 sess; m1w4: 3/3). Per-session stays
  flat 56–66 reps while weekly volume moves 388–593: volume rises via
  session COUNT, not session size.
- takano-MSIC: same pattern, one notch up — 6 training days nearly every prep
  week, 2–3 double-days -> 8–9 sessions (m0w0: 6 days -> 9 sess at 715;
  m0w4: 9 sess at 708; m0w8: 9 sess at 712). Per-session 60–79.
- Pattern by class AND by volume: III/II/I/CMS Takano never double (max 5–6
  single sessions/wk, per-sess up to ~90 at peak weeks). MS/MSIC double
  whenever the day plan exceeds ~100 lifts (same >100 rule as Roman), i.e.
  routinely at 400–700 reps/wk, and drop the second session first when
  tapering.

## 3. ROMAN (research/roman-mining + roman-transcription)

Month volumes (lifts/mo) and standard weekly rhythm. Roman counts a "workout"
= one session; a day with >100 lifts is split into morning + evening = 2 sessions.

| level | year | prep mo | comp mo | WL sessions/wk | wk vol (typical/max) | lifts/session |
|---|---|---|---|---|---|---|
| Beginner | 10,000 | 1,100–1,300 | 900–1,000 | 3 (+1 GPP); Jan 1+2 GPP; Jun–Jul 1+2 GPP | ~275–325 / 364 (Oct wk3) | ~110 (first 4 mo), ~90 prep / ~75 comp |
| Low-class III–II | ~12,000 | 1,000–1,500 (ex 1,250) | 750–1,050 (ex 900) | 5 days (Mon/Tue/Wed/Fri/Sat; Sun rest); wk2 shock Mon130/Tue40/Wed95/Fri135/Sat50 | ~250–450 (variant 20/35/27/18%) | snatch/C&J 10–30; squats 20–30 (max ~60, split in 2 series); press 6–30 |
| Class I / CMS | 15,000 | 1,300–2,000 (avg 1,650) | 950–1,450 (avg 1,200) | 4–5 days (ex: 80/110/90/56; max wk 85/50/105/90/66) | ~330–410 / 609 (wk2 of 2,100-mo example is MS; I/CMS max wk ~528 of 1,650) | same per-exercise norms; wk ≤2 large (>100) workouts for low-class; days >100 split |
| MS | 18,000 | 1,500–2,700 (avg 2,100) | 1,100–1,900 (avg 1,500) | 5–6 days; days >100 lifts split -> up to ~9 sessions/wk (ex m0w4: Mon130/Tue60/Wed140/Thu40/Fri120/Sat80 = 6 days, 9 sessions at 570) | ~440–610 / up to ~690 (33% of 2,100) | ~200 lifts/day prep (2 sessions), ~180 comp; morning +10 prep / +15 comp over evening |
| MSIC | ~18,000 minus (prep −200, comp −150/mo) | ~1,300–2,500 | ~950–1,750 | 5–6 days, same two-a-day machinery; group-2 volume halved (stage 3) | slightly below MS | same; records set while cutting total + group-2 volume |
| 110+kg MS | — | 2,300 | 1,600 | 5–6 days + doubles | ~530–760/wk | reps/set pushed to 6 fundamental / 10 local; obligatory slow/static work |

Other Roman norms used above:
- Workout size classes (p106): Small ≤50, Moderate 51–100, Large 100+ lifts.
  "The more workouts there are in a week, the larger the volume of the week's
  loading" (p106–p107). Year-to-year growth lever #2 is explicitly "more
  workouts at same lifts/session" (p80).
- Morning/evening organization (p145–146): prep — snatch mainly AM, C&J 2:1 AM,
  most 70%+ AM; squats (incl. 100%+) ~2:1 PM; snatch pulls AM, clean pulls PM;
  presses AM+PM, good mornings/hyperextensions AM. Comp — snatch ~2:1 AM,
  70%+ uniform AM/PM, squats ~even (maxes slightly PM).
- 'Two series' rule (three places): power-snatch 25–30 lifts done "in 2 series"
  (start+end or middle+end); squats "divided into two series when a large
  number" (p68); and the day-level rule — "desirable to do two workouts when
  more than 100 lifts planned for one workout", ~200 lifts/day prep / 180 comp
  (chunk-5 p145).

## 4. COMPARISON at matched weekly volumes

| weekly vol | Takano | Ours | Roman prescribes |
|---|---|---|---|
| ~200/wk (III–II) | 3–4 sess, ~55–62/sess (no doubles) | 3–4 sess, ~57–85/sess | 3 (beginner, ~90–110/sess) to 5 days (low-class ex, ~40–135 mixed S/L) |
| ~300–360/wk (I/CMS) | 4–5 sess, ~73–78/sess (no doubles) | 4–5 sess (CMS/I), ~66–81/sess | 4–5 days, S/M/L mix, no routine doubles yet |
| ~400/wk (MS) | 6–7 sess, ~62–66/sess (2 double-days; e.g. tMS m0w1: 4 days->6 sess, 391; m0w6: 4->6, 395) | 5 sess, ~76–85/sess (ours m1w0: 5/408; m2w1: 5/380; m3w1: 5/425) | 5 days, heaviest days split AM/PM |
| ~570–590/wk (MS peak) | 9–10 sess over 6 days, ~59–64/sess (tMS m0w0: 6->9, 579; m0w8: 6->10, 593) | 6 sess, ~95/sess (ours m2w0: 6/569); worst 6 sess, 112/sess (m2w2: 6/675, max day 150) | 6 days -> 9 sessions at 570 (MS 90kg m0w4: 130/60/140/40/120/80, >100-lift days doubled) |
| ~700/wk (MSIC peak) | 9 sess over 6 days, ~79/sess (tMSIC m0w0: 715; m0w8: 712) | (we have no MSIC; our max is 675 in 6) | 110+kg MS prep mo 2,300 -> ~530–760/wk via 6 days + doubles |

The lever finding:
- Our generator scales volume two ways only: more days (3->6) and bigger
  sessions (up to 150 reps/day). It never splits a day. So at 400 reps/wk we
  train 5 sessions where Takano trains 6–7 and Roman 5 days with the heavy
  ones doubled; at ~570–590/wk we train 6 sessions of ~95+ where Takano trains
  9–10 sessions of ~60 and Roman trains 6 days / 9 sessions (~200/day split
  AM/PM, morning +10).
- Takano adds SESSIONS (doubles) as volume rises, holding per-session volume
  flat (~60); days stay at 4–6. Roman's rulebook says the same thing from the
  other side: cap the single workout (~100 lifts -> split; ~20–30 squats,
  split in two series past ~60), add a second workout, keep ~200 lifts/day.
- Gap quantified: at ~400 reps/wk Takano-MS trains ~6.5 sessions vs our 5
  (+30% more sessions, each ~20 reps smaller); at ~580/wk Takano trains 9–10
  vs our 6 (+50–65% more sessions, each ~35 reps smaller). Roman's MS peak
  week is literally 6 days -> 9 sessions at 570 — the exact shape our MS
  program renders as 6 single sessions.
- Concrete consequence (already visible in outputs): our MS m2w2 packs 675
  reps into 6 sessions with a 150-rep day; no Takano week exceeds ~106/session
  (MSIC) and no Roman single workout is planned past ~100 without a split.
