# exp: quarantine-90 — NEGATIVE (do not quarantine; smear is load-balancing)

## Idea
Kill P3 excess by quarantining 90+ to ONE heavy day per week.

## Verdict: NEGATIVE — the premise is backwards. No src change. One pin test added.

A perfect quarantine (every within-week 90+ lift piled onto the week's
heaviest session, week bins and session vols kept exact) makes book exc
**worse**: **+7.3** (I +0.30 / CMS +1.86 / MS +5.12), gaps/soft/drift
unchanged. Perfect pro-rata spreading saves only **−1.4**. Current
placement is already near-optimal; the 90+ mass is quota-set and out of
scope. Concentration is priced, smear is rewarded — quarantine is the
wrong direction.

## Diagnosis (read first, per brief)

- `runs/2026-10-24-wlgen/notes/unsmear-taper-1.md`: track C proved the
  taper chain (taper_topup/takeup/spread_extra/close_ramps) does not reach
  the book ruler (three independent nulls). Untouched here.
- `research/plans/tops-first-allocator.md`: concentration emerges from
  fit exactness; decide hosting pre-fit, never repair post-hoc.
- Takano fixtures (`tests/fixtures/takano-{CMS,MS}.json`): his 90s live on
  big-day C+J flat blocks topping ladders; his pulls/squats train heavy.
- Roman (`research/roman-mining/intensity.md`): pulls at 90–100%+ are
  Group-1 strength work (p64: 95%/3x8, 15–30 pulls/workout); 90% over one
  day or 2–3 days running in small doses (p48); no 100%+ classics in
  week 4 — our week-4 shape already complies (see §27f).

## Enumeration (built plans, this tree)

Sessions with 90+ ≥ 4 lifts: **I 44 / CMS 98 / MS 128**
(session_dose view, i.e. paired work counted on both members — the
double-count itself creates ~12 extra 90+≥4 cells in CMS vs the raw
movements view). Light-day cells (< week-mean vol): I 10/44, CMS 28/86,
MS 44/120. By group the mass is pulls + squats: MS ClPull 56 cells,
Squat 22, Fundamental 15; I ClPull 25, Squat 12.

## Mechanism trace (which mover placed it)

None of the post-alloc movers **create** 90+ mass — week totals are fixed
upstream by `week_bin_lifts` ← meso quotas, and every mover below only
redistributes within exact totals:

- `zone_alloc` (peak 2.0 prep / −0.3 comp): prior-weighted split of fixed
  counts. Prep peak already concentrates tops on big days — i.e. the
  tree already quarantines *toward* heavy, and the ruler prices it.
- `pair_zones` base floor + flat prior + peak: fixed ref-unit totals split
  over paired sessions so every complex keeps its warmup ramp; tech
  H-quarantine already folds tech 90→80 (step 1, exc 204→189).
- `pair_fit` snap: snaps co-hosted pairs to small ratios; week targets
  flex only inside the tolerance band. Does not mint 90+.
- `reinforce` / `spread_extra` / `take_up_slack`: move 90+ between
  sessions of one week at fixed totals (track C: ruler-blind).

The penalty is convex per session (`prilepin_score` reps/capacity summed,
`prilepin_excess` 0 below 1.0, soft rate 4 to 1.5/2.0, hard rate 20 past
it; paired work counted on **both** members via `session_dose`). Convex
penalty ⇒ spreading a fixed dose over sessions minimizes exc,
concentrating maximizes it. That is the whole story.

## Causal numbers (black-box `wlscore`, week bins + vols exact)

| variant | I | CMS | MS | book |
|---|---|---|---|---|
| baseline exc | 35.36 | 42.63 | 93.34 | 190.3 |
| perfect quarantine (all 90+ → heavy day) | +0.30 | +1.86 | +5.12 | **+7.3** |
| perfect pro-rata spread | −0.02 | −0.40 | −0.98 | −1.4 |

Spread floor ≈ baseline ⇒ remaining 90+ exc is quota-forced.

## Which quota forces it (out of scope to touch)

MS week-level 90+ mass from `week_bin_lifts` (quota-set): **2034 lifts**,
of which ClPull 642 + SnPull 529 = **58% pulls**, Squat 196, Fundamental
153. Roman prescribes exactly this (heavy pulls/squats = strength work);
Takano programs it. Reaching it requires quota/bin changes — forbidden
on this track. Comp density is not theforcer at session level: the mass
sits in ordinary prep/comp weeks, not just peak weeks.

## Lines changed / pins

- src: 0 (deliberately).
- tests: +1 (`test_spreading_90_never_raises_session_penalty` pins the
  convexity so no future track re-tries concentration).
- No pin failures; taper-conservation pins untouched.

## Recommendation

Retire quarantine-90. If 90+ exc must fall, the only in-scope handle is
pre-fit hosting (tops-first allocator: decide heavy-day hosting before
fit so dose never strands where capacity is thin) — or quota/bin work
owned by another track.
