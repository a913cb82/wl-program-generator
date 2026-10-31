# Methodology review: our construction vs Roman / Takano

## 1. Template + quota + repair: scaffolding, not a model
Our pipeline is annual ratios → `spread` → IPF `fit` against a `session_prior`
weight matrix → `close_*` repairs. The "model of a workout" is a 5-slot
abstract DAY template plus slot-matchability. Roman's model of a workout is
physiological grammar: speed → strength → endurance, power-snatch before
snatch, pulls middle/end, squats split in two series, warmup required on
structural change (selection §§3–4). Takano's is the same grammar instantiated.
What they'd recognize: CLASSES shares (near-exact, volume-intensity Finding 4),
S/M/L day sizes, VARIANTS shapes, Sunday off, final-week taper, pulls only
from I up. What they'd find alien: fitting sessions by matrix balancing with
epsilon-quota weights; MIN_DOSE=6 as a hard integer constraint that drives the
whole repair stack; the PHASE_PEAK/GAP `shift()` of entire distributions by ARI
points — books never move mass by average-intensity arithmetic, they add or
remove counted 70%+/90%+/100%+ lifts on named days.

## 2. Repairs hide bad fits
Layering is unsound: fitters guarantee exact margins on a deliberately wrong
prior, repairs restore plausibility while keeping margins exact, so tests pass
and the prior never improves. Exhibit A: `close_ramps`. `zone_alloc` starts
from a flat prior giving *every* session a share of *every* zone (each "carries
its own warmup ramp"), which mathematically guarantees interior gaps; then
`close_ramps` swaps reps between sessions until profiles are contiguous. A
principled allocator would deal contiguous blocks (one ramp per session, heavy
day gets the top) up front — the flat prior is the modeling error, the repair
is the cover. Same pattern in `consolidate_doses`/`repair_week_doses` (4-cycle
swaps hide that the fit cannot jointly satisfy MIN_DOSE + slot constraints)
and `close_session` (drops a lone 100+ onto 90 to fix what `take_up_slack`
stacked).

## 3. Genuine vs resemblance
- Vol+intensity concur: genuine in one direction only (prep ARI below yearly
  bins, comp above via GAP/FAN). Deliberate *contrast* weeks (Roman's signature
  move: max-volume week takes minimum high-intensity, e.g. I-56kg mo2
  pp131–136) is unrepresentable — our shift is a function of meso index, not
  of the week's volume.
- Table 13 variant selection by prior month: resemblance. Our MACRO splits are
  hardcoded per meso; Roman selects the 4-week shape from the *previous* month's
  size (after large month use 2/3-1/2-4/4-2, p106). We have the shapes, not the
  rule.
- Shock-day placement: absent. Roman pins shock to competition weekday (p110)
  and caps submax/max shares per week (≤35% wk3, C&J capped wk2, last-lift lags
  5–19d). We spread 90%+ by `peak` exponent and `_spread_days` even spacing.
- AM/PM splits: absent. Roman's two-a-day grammar (snatch AM / squat PM,
  pulls split, p145–146) has no counterpart — we plan ≤6 single sessions.
- Rest-day grammar: resemblance. We keep Sunday off and S/M/L contrast but
  place days evenly; Roman's S-R-L-R strings encode recovery (90% repeat
  2–3d, rotated daily), ours encodes arithmetic (`prev_last` avoidance only).

## 4. Single biggest debt
Plan high-intensity lifts first, base second. Today tops are residue of
shifting whole distributions; in the books tops are the plan (weekly 70%+/90%+
quotas per p107, shock-day pinning, last-lift lags, taper transfer to weeks
1–3) and everything else fills around them. Allocating counted tops to named
sessions first would obsolete `zone_alloc`'s flat prior, PHASE_PEAK, most of
`close_ramps`/`close_session`/`spread_extra`, and the taper-topup loop in one
move — it is the missing model the repair stack is scaffolding around.
