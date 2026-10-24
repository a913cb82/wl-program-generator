# WL Program Generator

Generates a 20-week Soviet-style Olympic weightlifting macrocycle (one training block) from an annual lift target, ending at a competition. It splits volume first, then intensity, then sets, and writes a styled HTML report per class. Deterministic, standard library only.

## Run

`wlgen` writes one plan per competition class into `outputs/`.

```sh
uv sync --all-extras                 # create .venv from uv.lock (Python 3.14)
.venv/bin/wlgen                      # write all five plans
.venv/bin/pytest -q                  # run the tests
.venv/bin/pre-commit install         # enable format and type hooks
```

Get uv from <https://docs.astral.sh/uv/>.

Or use it as a library:

```python
from wlgen import build_plan, to_html

text = to_html(build_plan("MS"))
```

`build_plan` caches its result per class.

## What you get

Five files, one per competition class, III (entry) to MS (top):

| File | Class | Annual lifts |
|------|-------|-------------:|
| `outputs/III.html` | Class III | 12000 |
| `outputs/II.html` | Class II | 12000 |
| `outputs/I.html` | Class I | 15000 |
| `outputs/CMS.html` | CMS | 15000 |
| `outputs/MS.html` | MS | 18000 |

Open one in a browser. Each file is self-contained (inline CSS, no scripts).

A plan has two parts, Volumes and Training Plan. Volumes holds three tables: the macrocycle total (one group table plus the meso sizes), a mesocycles table (one volume column per meso, with the weekly sizes), and one week table with lifts per group and zone per microcycle. Training Plan holds one table per mesocycle: weeks go across, sessions and slots go down.

Each training plan slot gets one row with two columns per week: the movement name, then its scheme with the zone over the reps, fraction-style (a real stacked fraction with a vinculum, e.g. 80% over 1+2; repeated sets show as ×N beside the fraction):

```
| | Week 1 | |
| 1 | SnPull+Snatch | 80% / 1+2 |
```

`80%/1+2` is one set of one pull plus two snatches at 80%. `70%/3*2,2` is two sets of three then one set of two at 70%. `4*(70%/3+2, 80%/2+1)` repeats a two-zone complex block four times. Sets of one omit the `*1`.

## What's in the repo

- `src/wlconfig.py` — all data and tuning: ratios, templates, bins, search widths. The steps below name its tables.
- `src/wlgen.py` — the generator and the HTML renderer.
- `tests/test_wlgen.py` — the test suite.
- `outputs/` — the five generated plans.
- `pyproject.toml` — packaging, test, lint and type-check config.
- `uv.lock` — pinned dev dependencies.
- `.python-version` — interpreter uv uses.
- `.pre-commit-config.yaml` — format and type-check hooks.

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
- A session draws from five optional slots. Complexes such as `SnPull+Snatch` or `Clean+Jerk` share one slot. Other `X|Y` options split across the week, and each movement gets a minimum dose (6 lifts). See `DAY`.

### Intensity

- The plan buckets intensity into zones at 60%, 70%, 80% and up.
- Each class has a yearly zone mix from Takano's tables. See `BINS`.
- Prep sits below that mix, comp above it, and the gap grows with class. Higher classes ramp up across the three prep mesos too.
- The last comp week tapers: snatch and C&J stay below 90%.

### Sessions and sets

- A session orders its sets like a warm-up. Zones first appear from light to heavy. Each jump up goes to the next zone in the session. Reps stay flat or drop as weight rises. At one weight, a single may lead into work sets. A drop back down can add reps.
- Two paired movements sharing a day follow a fixed rep ratio (eg 2 pulls per snatch, 2 cleans per jerk). Lighter zones allow more ratios, and the choice narrows as weight rises. Pair volume counts toward both movements' bins.
- The tool packs each movement's reps at a zone into as few sets as possible (`70%/3*2,2`), using the zone's preferred rep counts from `REPS`. A search then picks the cleanest legal order.

## Guarantees

- Every split sums exactly.
- Sets follow the warm-up order.
- Every paired-movement ratio stays legal, and each side's reps stay flat or fall as weight rises.
- Each session's zone profile is contiguous from its own base; a gap stands only where the week cannot cover every session spanning it.
- A session touches the week's base zone, and each zone below its top the week holds in force, whenever the week holds enough to share.
- Every session slot prescribes 0 or at least 6 total reps: one
  movement's sets, or one complex counted across both sides.
- Same input, same output.

## Open

1. Which volume split should the default Comp meso use?
