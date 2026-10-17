# WL Program Generator

Generates a 20-week Soviet-style Olympic weightlifting macrocycle (one training block) from an annual lift target, ending at a competition. It splits volume first, then intensity, then sets, and writes Markdown. Deterministic, standard library only.

## Run

`wlgen` writes one plan per competition class into `outputs/`.

```sh
uv sync --all-extras                 # create .venv from uv.lock
.venv/bin/wlgen                      # write all five plans
.venv/bin/pytest -q                  # run the tests
.venv/bin/pre-commit install         # enable format and type hooks
```

Without uv, run `python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'`.

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

- `src/wlconfig.py` — all data and tuning: ratios, templates, bins, search widths. The steps below name its tables.
- `src/wlgen.py` — the generator and the Markdown renderer.
- `tests/test_wlgen.py` — the test suite.
- `outputs/` — the five generated plans.
- `pyproject.toml` — packaging, test, lint and type-check config.
- `uv.lock` — pinned dev dependencies.
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
- A session draws from six optional slots, one movement each. `X|Y` options split across the week, and each movement gets a minimum dose (6 lifts). See `DAY`.

### Intensity

- The plan buckets intensity into zones at 60%, 70%, 80% and up.
- Each class has a yearly zone mix from Takano's tables. See `BINS`.
- Prep sits below that mix, comp above it, and the gap grows with class. Higher classes ramp up across the three prep mesos too.
- The last comp week tapers: snatch and C&J stay below 90%.

### Sessions and sets

- A session orders its sets like a warm-up. Zones first appear from light to heavy. Each jump up goes to the next zone in the session. Reps stay flat or drop as weight rises. A drop back down can add reps.
- A clean and jerk sharing a day follow a fixed rep ratio (eg 2 cleans per jerk). Lighter zones allow more ratios, and the choice narrows as weight rises.
- The tool packs each movement's reps at a zone into as few sets as possible (`3x3,2x2@70%`), using the zone's preferred rep counts from `REPS`. A search then picks the cleanest legal order.

## Guarantees

- Every split sums exactly.
- Sets follow the warm-up order.
- Every clean:jerk ratio stays legal.
- Same input, same output.

## Open

1. Which volume split should the default Comp meso use?
2. Use the ±20% week band to avoid movements below 6 lifts in taper and low-volume weeks?
