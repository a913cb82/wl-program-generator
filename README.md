# WL Program Generator

Generates a 20-week Soviet-style Olympic weightlifting macrocycle (one training block) from an annual lift target. The block ends at a competition. Volume gets split first, then intensity, then sets. Output is Markdown. The runtime is the Python standard library, and the same input always gives the same plan.

## Run

`python wlgen.py` writes one plan per competition class into `outputs/`.

```sh
python3 -m venv .venv
.venv/bin/pip install pytest ruff
.venv/bin/python wlgen.py            # write all five plans
.venv/bin/pytest -q                  # run the tests
.venv/bin/ruff format . && .venv/bin/ruff check .
```

Or use it as a library:

```python
from wlgen import build_plan, to_markdown

text = to_markdown(build_plan("MS"))
```

`build_plan` caches its result per class.

## What you get

Five files, one per competition class, III (entry) to MS (top):

| File | Class | Annual lifts |
|------|-------|-------------:|
| `outputs/III.md` | Class III | 12000 |
| `outputs/II.md` | Class II | 12000 |
| `outputs/I.md` | Class I | 15000 |
| `outputs/CMS.md` | CMS | 15000 |
| `outputs/MS.md` | MS | 18000 |

A plan has four parts:

- The macrocycle total.
- A group table per meso, with the weekly sizes.
- A week table with lifts per group and zone.
- One bullet list per session.

Session bullets give exact sets, reps and zone:

```
- Snatch: 3x3,2x2@70%
- Other Clean+Other Jerk: 3+2@70%, 4x(3+2@70%, 2+1@80%)
```

`3x3,2x2@70%` is three sets of three and two sets of two in the 70% zone. `3+2` is a clean and jerk complex. `4x(...)` is a repeated wave.

## What's in the repo

- `wlconfig.py` — all data and tuning: ratios, templates, bins, search widths. The steps below name its tables.
- `wlgen.py` — the generator and the Markdown renderer.
- `test_wlgen.py` — the test suite.
- `outputs/` — the five generated plans.

## How it plans

The plan nests four levels:

- Macrocycle — the whole 20-week block.
- Mesocycle — 5 per block, 4 weeks each: 3 prep, 2 comp.
- Microcycle — 1 week.
- Session — 1 training day.

Each level takes a share of the level above it. `wlconfig.py` holds those shares: macro weights, meso weekly splits, class group ratios and weekly intensity bins.

### Volume

- Volume counts lifts above 50% of your best in that movement. The plan covers all 12 Soviet groups.
- The block is five 4-week mesos: three prep, two comp. `MACRO` holds the meso weights and weekly splits.
- Weekly group volumes follow the class ratio table. The tool shifts a little volume between weeks (±20% per group, 10% per week) so lifts stay whole, sessions fit, and the meso sums exactly. See `III_II`, `I_CMS` and `MS_R`.
- A session draws from six optional slots, one movement each. `X|Y` options split across the week, and each movement gets a minimum dose (6 lifts). See `DAY`.

### Intensity

- The plan buckets intensity into zones, labeled by the lower edge: 60%, 70%, 80% and so on.
- The yearly anchor comes from Takano's bin tables per class. See `BINS`.
- Prep work sits below the anchor, comp work above it, with a class-dependent gap. The higher classes also ramp up across the three prep mesos.
- The final comp meso tapers. Its last week keeps snatch and C&J below 90%.

### Sessions and sets

- A session orders its sets like a warm-up. Zones first appear from light to heavy, and each jump up goes to the next zone the session uses. As weight rises, reps stay flat or drop. A drop back down can add reps again.
- When a clean and a jerk share a day, they train in a fixed rep ratio (eg 2 cleans per jerk). Lighter zones allow more ratios, and the choice narrows as weight rises.
- The tool packs each movement's reps at a zone into as few sets as possible (`3x3,2x2@70%`), using that zone's preferred rep counts from `REPS`. A search then picks the cleanest legal order.

## Guarantees

- Every split sums exactly.
- Sets follow the warm-up order.
- Every clean:jerk ratio stays legal.
- Same input, same output.

## Open

1. Which volume split should the default Comp meso use?
2. Use the ±20% week band to avoid movements below 6 lifts in taper and low-volume weeks?
