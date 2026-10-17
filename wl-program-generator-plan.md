# WL Program Generator — Plan v1.2

## Locked
| Decision | Value |
|----------|-------|
| Macro | Block ~6 mo, ends in comp |
| Vol | # lifts. Soviet counting: working lift if >50% of that movement's max; exclude warm-up ramps, bar/technique. GPP not counted |
| Categories | Full Soviet set (12 groups), all planned at every level |
| Intensity | % of each movement's own max (squat/pull maxes per-athlete) |
| Ratio | User input; Soviet class × phase templates |
| Taper | Ordinary mesocycle (vol + int spread across weeks) |
| Output | Markdown |

## Inputs
| Input | Values |
|-------|--------|
| Maxes | Sn, Clean, Jerk, BSq, FSq, Sn-pull, Cn-pull |
| Annual vol | 10k / 12k / 15k / 18k (full Soviet count, all groups) |
| Base ratio table | % vol per group (macro-level); sub-ratio FSq:BSq |
| Meso perturbations | per meso type ratio shift (e.g. Comp → +Clean/Jerk, −Squat) |
| Templates | 1 macro + 1 meso per type + 1 micro |
| Constraints | days/wk, comp date(s) |

## Ratio templates (Soviet class × phase, % of volume)
| Group | III–II P | III–II C | I–CMS P | I–CMS C | MS P | MS C |
|-------|---------:|---------:|--------:|--------:|-----:|-----:|
| Snatch | 10 | 10 | 9 | 9 | 8 | 8 |
| Other snatch | 10 | 10 | 11 | 12 | 12 | 13 |
| Clean | 7.5 | 7.5 | 6 | 6 | 5 | 5 |
| Other clean | 9.5 | 9.5 | 9 | 9 | 8 | 8 |
| Jerk | 7.5 | 7.5 | 7 | 7 | 6 | 6 |
| Other jerk | 3.5 | 3.5 | 5 | 6 | 7 | 8 |
| FSq+BSq | 27 | 27 | 23 | 23 | 20 | 20 |
| Other squats | 15 | 15 | — | — | — | — |
| Sn-pull | — | — | 7 | 5 | 8.5 | 5 |
| Cn-pull | — | — | 5 | 6 | 10 | 12 |
| Pressing | 10 | 10 | — | — | — | — |
| Fundamental | — | — | 18 | 17 | 15.5 | 15 |

Pulls counted from Class I up.

## Templates

### Macro templates
| Macro | Meso | Length | Rel. vol | Intensity | Example vol |
|-------|------|-------:|---------:|-----------|------------:|
| Soviet qualified year | Prep1 (4-2) | 4 wk | 0.20 | low-mid, rising | 1350 |
| | Prep2 (2-4) | 4 wk | 0.22 | mid | 1500 |
| | Prep3 (3-1) | 4 wk | 0.25 | mid-high | 1650 |
| | Comp1 (1) | 4 wk | 0.18 | high | 1200 |
| | Comp2 (2) | 4 wk | 0.15 | high, taper | 1000 |

Meso volumes = annual vol × macro weight × rel. vol. Example volumes are from the source plan for a qualified athlete.

### Meso templates
| Type | Vol split (%) |
|------|---------------|
| Prep 4-2 | 21/28/17/34 |
| Prep 3-1 | 27/18/32/23 |
| Prep 2 (i) | 20/35/27/18 |
| Prep 1-3 | 32/19/27/22 |
| Prep 2-4 | 22/33/18/27 |
| Prep 2 (ii) | 23/32/26/19 |
| Prep 1 | 31/27/23/19 |
| Comp 1 | 36/28/24/12 |
| Comp 3-1 | 29/25/35/11 |
| Comp 2 | 28/33/26/13 |
| Comp 1-3 | 32/26/29/13 |

Source gives volume splits. Intensity distribution per meso: TBD (see Open).

### Micro templates (Soviet session-size patterns)
S <50 lifts, M 51–100, L >100:
| Days/wk | Patterns |
|---------|----------|
| 3 | S L S; M L M; L S L; L M L |
| 4 | S L MS; L M LM; L M LS; L S LS; S M MS; M L MS |
| 5 | MSL MS; MSL MM; SLS LS; LSM ML; MSM MS |
| 6 | SMSMSM; MSLSMS; MLSMSM; MMSMSM; MSLSMM; SLSLSM |

### Session templates
One template for every day, in execution order. Every slot is optional and
trains exactly one movement (`X|Y` = XOR); a movement needs at least 6 lifts
when present, with no upper limit (the annual spread keeps doses sane).

| Slot | Movements (min 6 lifts) |
|------|-------------------------|
| 1 | Snatch\|Other Snatch |
| 2 | Clean\|Other Clean |
| 3 | Jerk\|Other Jerk |
| 4 | Squat\|SnPull\|ClPull |
| 5 | Other Squat\|Press |
| 6 | Fundamental |

When a session trains a clean and a jerk together, every intensity bucket uses a small ratio (1:1, 2:1, 3:1, 3:2, 1:2, 1:3, 2:3). Wider ratios are only legal at lighter weights: 3:1, 3:2, 2:3 and 1:3 below 80%, 2:1 and 1:2 below 90%, 1:1 anywhere. A session's ratio may change between buckets, but only narrow as the weight rises.

Session total should fall in the slot's S/M/L target; the scheme layer below turns every group × bin cell into exact sets×reps.

## Allocation model

### Template fields
| Object | Fields |
|--------|--------|
| Macro template | meso sequence; per meso: length, rel. vol, intensity bias, meso template ref; ratio templates (prep/comp, by class) |
| Meso template | type; weeks; weekly vol split; intensity wave (bin × week); ratio delta |
| Micro template | day slots (size, focus, groups allowed, intensity bias); size weights |
| Session template | movements with volume ranges; execution order; optional add-ons |

### Resolved plan
| Object | Holds |
|--------|-------|
| Macrocycle | vol target; mesocycles |
| Mesocycle | vol target; resolved ratios; weeks |
| Week | vol target; lifts per group; lifts per group × bin; sessions |
| Session | vol target; lifts per group × bin; schemes |

### Volume division
| From → To | Rule |
|-----------|------|
| Annual → macro | macro weights, normalized |
| Macro → meso | rel. vol, normalized |
| Meso → week | weekly vol split (%); each week may sit ±20% (min 1 lift) from its nominal group split, capped at 10% of week volume; later weeks pick up the slack, meso totals stay exact |
| Week → group | nominal ratio table (template ± meso delta), normalized to 100; banded by the rule above |
| Week → session | split by slot size weights (S/M/L), normalized; the week picks the first pattern (fewest days, table order) its sessions can host |
| Session fill | one shared template every day; each slot trains one movement (X\|Y slots are XOR); group × session table by proportional fitting with week rows and session columns both exact; a soft annual host prior picks the support (each free slot shares the week's days evenly up to the 6-lift cap, phases stagger across slots, last week's final-day movement avoids this week's first day when another is free); the 6-lift floor is soft where exact session volumes force a smaller cell |

### Intensity division
| From → To | Rule |
|-----------|------|
| Class × phase → group bins | yearly bins (below); prep = yearly − 0.33g, comp = yearly + 0.67g (g = Table 8.1 prep→comp gap); one gap per class for all groups |
| Meso | prep fan (−g, 0, +0.8g) for I/CMS/MS, flat for III/II; comp flat |
| Meso → week | flat in prep; Comp 2 week 3 peak (+g); Comp 2 week 4 taper: Sn/C&J drop all ≥90% zones, all other groups = yearly bins; Comp 1 flat |
| Week → session | flat prior 2D fit: clean+jerk co-hosted use a legal ratio per intensity tier, narrowing as weight rises; otherwise rows = week zone counts, cols = session group lifts; each session keeps its own warmup ramp (ramp-closing swaps), no upper-zone work without lower-zone work |
| Session → schemes | family/zone rep table filled exactly (fewest sets, no stray singles; 1 is a fallback); paired clean+jerk zip into complexes k*p+k*q capped by the zone reps; a beam search over the preferred fill's set order picks the cheapest legal sequence; if that fill cannot be ordered, the search may also re-split it (1 is always legal); cost = 100·below-min + 10·run + 5·rep change + 3·phrases + sets, ties by phrases, compact length, then text |

Session rules: session group totals = week group targets; a week's zone totals are the sum of its session counts; each `X|Y` slot trains one movement per session, so alternatives split across days; a session's profile is contiguous from the lowest used zone to its own top while the week has reps to spare; 3 reps per 5% zone is the preferred ramp dose, 2 or 1 acceptable. A session's first visit to each zone is in ascending weight order; an ascent goes only to the next heavier zone present, and reps never rise while the zone stays or rises. A session's zone profile is contiguous: reps at a heavier zone imply reps at every intermediate zone, and a week's integer bins are closed the same way before they are split. A session's clean:jerk ratio is legal in every zone and never widens as the weight rises; the week's clean/jerk totals flex within the week band to fit the ratio blocks.

Scheme ranges (reps per set, largest first):

| Family | 50 | 60 | 70 | 80 | 90 | 100 | 110 |
|---|---|---|---|---|---|---|---|
| Snatch / Clean / Jerk | — | 3,2 | 3,2 | 2,1 | 1 | 1 | — |
| Squat / Other Squat | 5,4,3,2 | 5,4,3,2 | 5,4,3,2 | 4,3,2 | 2,1 | — | — |
| SnPull / ClPull | — | — | 4,3,2* | 4,3,2 | 4,3,2 | 3,2 | 3,2 |
| Press / Fundamental | 5,4,3,2 | 5,4,3,2 | 5,4,3,2 | 4,3,2 | 3,2 | 1 | 1 |

\* ClPull only. A zone's exact count picks the least sets, then the least small sets; `1` is always legal. Repeated sets collapse to `NxR`, a lone set drops the `1x`, and distinct runs are comma-separated (`4x3,2x2`, `4,3`, `3`). Co-hosted clean and jerk keep the zone ratio and render as one complex per set (`5x3+1`, `3+3,2+2`); the complex size is capped by the zone's reps. Order is searched, not fixed: first visits ascend by zone, ascents never skip a present zone, reps never rise within or into a heavier zone, and repeated waves collapse to one phrase (`2x(2@80%, 1@90%, 3@70%)`).

Zone nominal = lower edge + 1; labels show the lower edge, bins are 5 wide and 10 apart; moving 1% of reps one bin = 0.1 ARI.

Yearly bins, Class 2 (III, II; Takano table 8.2–8.7):
| Group | 50% | 60% | 70% | 80% | 90% | 100% | 110% | ARI |
|-------|-------|-------|-------|-------|-------|---------|-----|-----|
| Snatch | | 9 | 51 | 29 | 11 | | | 75 |
| Clean & Jerk | | 8 | 42 | 37 | 12 | 1 | | 76 |
| Sn-pull | | | | 20 | 41 | 36 | 3 | 92 |
| Cn-pull | | | 6 | 30 | 40 | 20 | 4 | 89 |
| Squat | 13 | 28 | 27 | 30 | 2 | | | 71 |
| Fundamental | 3 | 8 | 28 | 32 | 16 | 12 | 1 | 80 |

Yearly bins, Class 1 (I; Takano table 11.3):
| Group | 50% | 60% | 70% | 80% | 90% | 100% | 110% | ARI |
|-------|-------|-------|-------|-------|-------|---------|-----|-----|
| Snatch | | 7 | 56 | 28 | 8 | 1 | | 75 |
| Clean & Jerk | | 4 | 45 | 39 | 11 | 1 | | 77 |
| Sn-pull | | | | 24 | 33 | 39 | 4 | 92 |
| Cn-pull | | | 17 | 34 | 26 | 19 | 4 | 87 |
| Squat | 14 | 27 | 21 | 35 | 3 | | | 70 |
| Fundamental | 3 | 11 | 31 | 31 | 16 | 7 | 1 | 78 |

Yearly bins, CMS (Takano table 12.3):
| Group | 50% | 60% | 70% | 80% | 90% | 100% | 110% | ARI |
|-------|-------|-------|-------|-------|-------|---------|-----|-----|
| Snatch | | 10 | 61 | 25 | 4 | | | 72 |
| Clean & Jerk | | 9 | 53 | 33 | 5 | | | 74 |
| Sn-pull | | | | 31 | 32 | 31 | 6 | 91 |
| Cn-pull | | | 23 | 36 | 23 | 13 | 5 | 84 |
| Squat | 22 | 28 | 25 | 22 | 3 | | | 68 |
| Fundamental | 5 | 11 | 40 | 26 | 10 | 6 | 2 | 79 |

Yearly bins, MS (Takano table 13.3):
| Group | 50% | 60% | 70% | 80% | 90% | 100% | 110% | ARI |
|-------|-------|-------|-------|-------|-------|---------|-----|-----|
| Snatch | | 16 | 63 | 19 | 2 | | | 71 |
| Clean & Jerk | | 11 | 55 | 31 | 3 | | | 73 |
| Sn-pull | | | | 25 | 37 | 32 | 6 | 91 |
| Cn-pull | | | 20 | 38 | 24 | 13 | 5 | 84 |
| Squat | 22 | 30 | 25 | 20 | 3 | | | 66 |
| Fundamental | 4 | 13 | 39 | 25 | 10 | 8 | 1 | 79 |

MS squat 90% is 3% (source prints 2% but the row sums to 99 and ARI 66).

Gap and prep fan (Table 8.1 classic lifts; sample-program shape):
| Class | g | Prep meso fan |
|-------|---|---------------|
| III, II | 0.5 | flat |
| I | 1.0 | −1.0, 0, +0.8 |
| CMS | 1.5 | −1.5, 0, +1.2 |
| MS | 1.9 | −1.9, 0, +1.5 |

Bin sources (source table has no separate bins for "other" groups; inherit parent):
| Group | Bin source |
|-------|-----------|
| Snatch, Other snatch | Snatch |
| Clean, Other clean, Jerk, Other jerk | C&J |
| FSq+BSq, Other squats | Squat |
| Sn-pull | Sn-pull |
| Cn-pull | Cn-pull |
| Pressing, Fundamental | Fundamental |

Intensity is planned as bins (discrete), not average %; avg % is validation only.

### Allocation utilities
| Utility | Use |
|---------|-----|
| Largest remainder | 1D splits |
| Proportional fitting (IPF) | 2D splits (groups × sessions, zones × sessions); exact margins; integer pass keeps rows and columns exact |
| Bounded round | week group targets inside the deviation band |

Deterministic: no RNG; residual ties by index order, session schemes by the scheme key.

### Validation
- Per-level sums exact; group ratios match template within rounding
- Sessions meet the week's group targets and zone bins exactly
- Each `X|Y` slot trains one movement per session (alternatives split across days)
- Every session's zone profile is contiguous; first zone visits ascend; ascents never skip a present zone; reps never rise into or within a zone
- Session doses ≥ 4 lifts, except where a week's small days leave no alternative
- Yearly bin mixture = Σ meso × week volume × bins (±0.75 ARI)
- Phase gap within ±0.6 ARI of Table 8.1
- Comp 2 taper week has no Sn/C&J ≥90% zones
- Heavy-rep counts (Table 8.1: 90-100% snatch+C&J per meso) validated, not enforced
- Every group allowed in ≥1 slot; every slot has ≥1 allowed group
- Sessions within S/M/L caps

## Pipeline
| # | Step |
|---|------|
| 1 | Volume: annual → macro → meso → week → group → session |
| 2 | Intensity: class bins → meso shift → week wave → session bias |
| 3 | Schemes per session (rep table → exact fill → clean+jerk complexes → beam-ordered sets) |
| 4 | Validate |

## Markdown output
| Section | Contents |
|---------|----------|
| Macro | dates, total vol, base ratio table |
| Meso | type, weekly vols, pattern, ratio perturbation |
| Micro | week table (day, focus, size) + lifts per group × zone + ARI |
| Session | bullets: movement, sets×reps@zone e.g. `4x3,2x2@70%, 2@80%, 3x1@90%`; co-hosted clean+jerk e.g. `5x3+1@70%` |

## Open
1. Default Comp meso: which Soviet split (1, 3-1, 2, 1-3)?
2. Use the week deviation band to avoid sub-dose movements in taper/min weeks?

## Follow-up (post-v1)
- Movement variations + aux; split "other" groups into specific movements
