# WL Program Generator

This tool builds a Soviet-style Olympic weightlifting program. It reads your maxes, your annual volume, and your training days. It writes a macrocycle that ends at a competition. The output is Markdown.

## Files

| File | Contents |
|------|----------|
| `wlconfig.py` | Data and rules. It holds ratios, templates, and intensity bins. |
| `wlgen.py` | The generator and the Markdown renderer. |
| `test_wlgen.py` | The test suite. It checks the hard rules. |
| `outputs/` | Five generated plans: `III.md`, `II.md`, `I.md`, `CMS.md`, `MS.md`. |

## Quick start

Use Python 3.12 or later.

```sh
python3 -m venv .venv
.venv/bin/pip install pytest ruff
.venv/bin/python wlgen.py            # write all five plans
.venv/bin/pytest -q                  # run the tests
.venv/bin/ruff format . && .venv/bin/ruff check .
```

The runtime uses the Python standard library only.

## Locked decisions

| Decision | Value |
|----------|-------|
| Macro | One block of about 6 months. The block ends in a competition. |
| Volume | A count of lifts. Soviet counting: a working lift is more than 50% of that movement's max. Warm-up ramps and bar or technique work do not count. GPP does not count. |
| Categories | The full Soviet set of 12 groups. Every level plans all groups. |
| Intensity | Percent of each movement's own max. Squat and pull maxes are per athlete. |
| Ratio | User input plus Soviet class × phase templates. |
| Taper | An ordinary mesocycle. Volume and intensity spread across the weeks. |
| Output | Markdown. |

## Inputs

| Input | Values |
|-------|--------|
| Maxes | Sn, Clean, Jerk, BSq, FSq, Sn-pull, Cn-pull |
| Annual volume | 10k, 12k, 15k, or 18k lifts. This is the full Soviet count across all groups. |
| Base ratio table | Percent of volume per group at macro level. The sub-ratio is FSq:BSq. |
| Meso perturbations | Ratio shift per meso type. Example: Comp adds Clean and Jerk and removes Squat. |
| Templates | One macro, one meso per type, and one micro. |
| Constraints | Days per week and competition dates. |

## Ratio templates

Soviet class × phase, percent of volume:

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

Count pulls from Class I up.

## Templates

### Macro templates

| Macro | Meso | Length | Rel. volume | Intensity | Example volume |
|-------|------|-------:|------------:|-----------|---------------:|
| Soviet qualified year | Prep1 (4-2) | 4 wk | 0.20 | low-mid, rising | 1350 |
| | Prep2 (2-4) | 4 wk | 0.22 | mid | 1500 |
| | Prep3 (3-1) | 4 wk | 0.25 | mid-high | 1650 |
| | Comp1 (1) | 4 wk | 0.18 | high | 1200 |
| | Comp2 (2) | 4 wk | 0.15 | high, taper | 1000 |

Meso volume = annual volume × macro weight × relative volume. The example volumes come from the source plan for a qualified athlete.

### Meso templates

| Type | Volume split (%) |
|------|------------------|
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

The source gives volume splits. Intensity distribution per meso is TBD. See Open.

### Micro templates

Soviet session sizes: S is under 50 lifts, M is 51–100, L is over 100.

| Days/wk | Patterns |
|---------|----------|
| 3 | S L S<br>M L M<br>L S L<br>L M L |
| 4 | S L MS<br>L M LM<br>L M LS<br>L S LS<br>S M MS<br>M L MS |
| 5 | MSL MS<br>MSL MM<br>SLS LS<br>LSM ML<br>MSM MS |
| 6 | SMSMSM<br>MSLSMS<br>MLSMSM<br>MMSMSM<br>MSLSMM<br>SLSLSM |

### Session templates

One template for every day, in execution order. Every slot is optional and trains exactly one movement. `X|Y` means XOR. A movement needs at least 6 lifts when present. There is no upper limit. The annual spread keeps doses sane.

| Slot | Movements (min 6 lifts) |
|------|-------------------------|
| 1 | Snatch\|Other Snatch |
| 2 | Clean\|Other Clean |
| 3 | Jerk\|Other Jerk |
| 4 | Squat\|SnPull\|ClPull |
| 5 | Other Squat\|Press |
| 6 | Fundamental |

When a session trains a clean and a jerk together, every intensity bucket uses a small ratio (1:1, 2:1, 3:1, 3:2, 1:2, 1:3, 2:3). Wider ratios are legal only at lighter weights. 3:1, 3:2, 2:3, and 1:3 are legal below 80%. 2:1 and 1:2 are legal below 90%. 1:1 is legal at any weight. A session's ratio may change between buckets. The ratio may only narrow as the weight rises.

The session total should fall in the slot's S/M/L target. The scheme layer below turns every group × bin cell into exact sets × reps.

## Allocation model

### Template fields

| Object | Fields |
|--------|--------|
| Macro template | Meso sequence. Per meso: length, relative volume, intensity bias, meso template ref, and ratio templates (prep or comp, by class). |
| Meso template | Type, weeks, weekly volume split, intensity wave (bin × week), and ratio delta. |
| Micro template | Day slots (size, focus, groups allowed, intensity bias) and size weights. |
| Session template | Movements with volume ranges, execution order, and optional add-ons. |

### Resolved plan

| Object | Holds |
|--------|-------|
| Macrocycle | Volume target and mesocycles. |
| Mesocycle | Volume target, resolved ratios, and weeks. |
| Week | Volume target, lifts per group, lifts per group × bin, and sessions. |
| Session | Volume target, lifts per group × bin, and schemes. |

### Volume division

| From → To | Rule |
|-----------|------|
| Annual → macro | Macro weights, normalized. |
| Macro → meso | Relative volume, normalized. |
| Meso → week | Weekly volume split (%). Each week may sit ±20% (min 1 lift) from its nominal group split. The cap is 10% of week volume. Later weeks absorb the remainder. Meso totals stay exact. |
| Week → group | Nominal ratio table (template ± meso delta), normalized to 100, banded by the rule above. |
| Week → session | Split by slot size weights (S/M/L), normalized. The week picks the first pattern (fewest days, table order) that its sessions can host. |
| Session fill | One shared template every day. Each slot trains one movement. `X\|Y` slots are XOR. A group × session table uses proportional fitting with exact week rows and exact session columns. A soft annual host prior picks the support. Each free slot shares the week's days evenly up to the 6-lift cap. Phases stagger across slots. The last week's final-day movement avoids this week's first day when another is free. The 6-lift floor is soft where exact session volumes force a smaller cell. |

### Intensity division

| From → To | Rule |
|-----------|------|
| Class × phase → group bins | Yearly bins below. Prep = yearly − 0.33g. Comp = yearly + 0.67g. g = Table 8.1 prep→comp gap. One gap per class for all groups. |
| Meso | Prep fan (−g, 0, +0.8g) for I, CMS, and MS. Flat for III and II. Comp is flat. |
| Meso → week | Flat in prep. Comp 2 week 3 peak (+g). Comp 2 week 4 taper: Sn and C&J drop all ≥90% zones, and all other groups use yearly bins. Comp 1 is flat. |
| Week → session | Flat prior 2D fit. Co-hosted clean and jerk use a legal ratio per intensity tier, narrowing as weight rises. Otherwise rows are week zone counts and columns are session group lifts. Each session keeps its own warm-up ramp (ramp-closing swaps). No upper-zone work without lower-zone work. |
| Session → schemes | Family/zone rep table filled exactly (fewest sets, no stray singles, 1 is a fallback). Paired clean and jerk combine into complexes k·p + k·q capped by the zone reps. A beam search over the preferred fill's set order picks the cheapest legal sequence. If that fill cannot be ordered, the search may also re-split it (1 is always legal). Cost = 100·below-min + 10·run + 5·rep change + 3·phrases + sets. Ties break by phrases, then compact length, then text. |

### Session rules

- Session group totals equal the week group targets.
- A week's zone totals equal the sum of its session counts.
- Each `X|Y` slot trains one movement per session. Alternatives split across days.
- A session's profile is contiguous from the lowest used zone to its own top while the week has reps to spare.
- A session's first visit to each zone is in ascending weight order.
- An ascent goes only to the next heavier zone present. Downward moves may skip.
- Reps never rise while the zone stays or rises.
- A session's clean:jerk ratio is legal in every zone. The ratio never widens as the weight rises.
- The week's clean and jerk totals flex inside the week band to fit the ratio blocks.
- 3 reps per 5% zone is the preferred ramp dose. 2 or 1 is acceptable.

### Scheme rep ranges

Reps per set, largest first:

| Family | 50 | 60 | 70 | 80 | 90 | 100 | 110 |
|--------|---|---|---|---|---|---|-----|
| Snatch / Clean / Jerk | — | 3,2 | 3,2 | 2,1 | 1 | 1 | — |
| Squat / Other Squat | 5,4,3,2 | 5,4,3,2 | 5,4,3,2 | 4,3,2 | 2,1 | — | — |
| SnPull / ClPull | — | — | 4,3,2\* | 4,3,2 | 4,3,2 | 3,2 | 3,2 |
| Press / Fundamental | 5,4,3,2 | 5,4,3,2 | 5,4,3,2 | 4,3,2 | 3,2 | 1 | 1 |

\* ClPull only.

A zone's exact count picks the least sets, then the least small sets. `1` is always legal.

### Notation

- Repeated sets collapse to `NxR`. A lone set omits the `1x`.
- Distinct runs use commas: `4x3,2x2`, `4,3`, `3`.
- Co-hosted clean and jerk keep the zone ratio and render as one complex per set: `5x3+1`, `3+3,2+2`. The zone's reps cap the complex size.
- The search decides the order rather than a fixed menu. First visits ascend by zone. Ascents never skip a present zone. Reps never rise within or into a heavier zone. Repeated waves collapse to one phrase: `2x(2@80%, 1@90%, 3@70%)`.

### Zone model

- Zone nominal = lower edge + 1.
- Labels show the lower edge. Bins are 5 wide and 10 apart.
- Moving 1% of reps one bin equals 0.1 ARI.

### Yearly bins

Class 2 (III and II). Takano table 8.2–8.7:

| Group | 50% | 60% | 70% | 80% | 90% | 100% | 110% | ARI |
|-------|-----|-----|-----|-----|-----|------|------|-----|
| Snatch | | 9 | 51 | 29 | 11 | | | 75 |
| Clean & Jerk | | 8 | 42 | 37 | 12 | 1 | | 76 |
| Sn-pull | | | | 20 | 41 | 36 | 3 | 92 |
| Cn-pull | | | 6 | 30 | 40 | 20 | 4 | 89 |
| Squat | 13 | 28 | 27 | 30 | 2 | | | 71 |
| Fundamental | 3 | 8 | 28 | 32 | 16 | 12 | 1 | 80 |

Class 1 (I). Takano table 11.3:

| Group | 50% | 60% | 70% | 80% | 90% | 100% | 110% | ARI |
|-------|-----|-----|-----|-----|-----|------|------|-----|
| Snatch | | 7 | 56 | 28 | 8 | 1 | | 75 |
| Clean & Jerk | | 4 | 45 | 39 | 11 | 1 | | 77 |
| Sn-pull | | | | 24 | 33 | 39 | 4 | 92 |
| Cn-pull | | | 17 | 34 | 26 | 19 | 4 | 87 |
| Squat | 14 | 27 | 21 | 35 | 3 | | | 70 |
| Fundamental | 3 | 11 | 31 | 31 | 16 | 7 | 1 | 78 |

CMS (Takano table 12.3):

| Group | 50% | 60% | 70% | 80% | 90% | 100% | 110% | ARI |
|-------|-----|-----|-----|-----|-----|------|------|-----|
| Snatch | | 10 | 61 | 25 | 4 | | | 72 |
| Clean & Jerk | | 9 | 53 | 33 | 5 | | | 74 |
| Sn-pull | | | | 31 | 32 | 31 | 6 | 91 |
| Cn-pull | | | 23 | 36 | 23 | 13 | 5 | 84 |
| Squat | 22 | 28 | 25 | 22 | 3 | | | 68 |
| Fundamental | 5 | 11 | 40 | 26 | 10 | 6 | 2 | 79 |

MS (Takano table 13.3):

| Group | 50% | 60% | 70% | 80% | 90% | 100% | 110% | ARI |
|-------|-----|-----|-----|-----|-----|------|------|-----|
| Snatch | | 16 | 63 | 19 | 2 | | | 71 |
| Clean & Jerk | | 11 | 55 | 31 | 3 | | | 73 |
| Sn-pull | | | | 25 | 37 | 32 | 6 | 91 |
| Cn-pull | | | 20 | 38 | 24 | 13 | 5 | 84 |
| Squat | 22 | 30 | 25 | 20 | 3 | | | 66 |
| Fundamental | 4 | 13 | 39 | 25 | 10 | 8 | 1 | 79 |

MS squat 90% is 3%. The source prints 2%, but the row sums to 99 and the ARI is 66.

### Gap and prep fan

Table 8.1 classic lifts. Sample-program shape:

| Class | g | Prep meso fan |
|-------|---|---------------|
| III, II | 0.5 | flat |
| I | 1.0 | −1.0, 0, +0.8 |
| CMS | 1.5 | −1.5, 0, +1.2 |
| MS | 1.9 | −1.9, 0, +1.5 |

### Bin sources

The source table has no separate bins for "other" groups. They inherit from the parent:

| Group | Bin source |
|-------|------------|
| Snatch, Other snatch | Snatch |
| Clean, Other clean, Jerk, Other jerk | C&J |
| FSq+BSq, Other squats | Squat |
| Sn-pull | Sn-pull |
| Cn-pull | Cn-pull |
| Pressing, Fundamental | Fundamental |

The plan uses discrete intensity bins, not an average percent. Average percent is for checks only.

### Allocation utilities

| Utility | Use |
|---------|-----|
| Largest remainder | 1D splits |
| Proportional fitting (IPF) | 2D splits (groups × sessions, zones × sessions). Margins are exact. The integer pass keeps rows and columns exact. |
| Bounded round | Week group targets inside the deviation band |

### Determinism

The generator uses no RNG. Residual ties break by index order. Session schemes break by the scheme key.

### Validation

- Per-level sums are exact. Group ratios match the template within rounding.
- Sessions meet the week's group targets and zone bins exactly.
- Each `X|Y` slot trains one movement per session. Alternatives split across days.
- Every session's zone profile is contiguous. First zone visits ascend. Ascents never skip a present zone. Reps never rise into or within a zone.
- Session doses are at least 4 lifts, except where a week's small days leave no alternative.
- The yearly bin mixture equals Σ meso × week volume × bins (±0.75 ARI).
- The phase gap is within ±0.6 ARI of Table 8.1.
- The Comp 2 taper week has no Sn or C&J ≥90% zones.
- The generator checks heavy-rep counts (Table 8.1: 90–100% snatch and C&J per meso). It does not enforce them.
- At least one slot allows every group. Every slot allows at least one group.
- Sessions stay inside the S/M/L caps.

## Pipeline

| # | Step |
|---|------|
| 1 | Volume: annual → macro → meso → week → group → session |
| 2 | Intensity: class bins → meso shift → week wave → session bias |
| 3 | Schemes per session (rep table → exact fill → clean and jerk complexes → beam-ordered sets) |
| 4 | Check the plan against the hard rules |

## Markdown output

| Section | Contents |
|---------|----------|
| Macro | Dates, total volume, and base ratio table. |
| Meso | Type, weekly volumes, pattern, and ratio perturbation. |
| Micro | Week table (day, focus, size), lifts per group × zone, and ARI. |
| Session | Bullets: movement, sets × reps @ zone, for example `4x3,2x2@70%, 2@80%, 3x1@90%`. Co-hosted clean and jerk: `5x3+1@70%`. |

## Open

1. Default Comp meso: which Soviet split (1, 3-1, 2, or 1-3)?
2. Use the week deviation band to avoid sub-dose movements in taper and min weeks?

## Follow-up (post-v1)

- Add movement variations and assistance work.
- Split the "other" groups into specific movements.
