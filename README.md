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
- A week table with lifts per group × zone, plus ARI.
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

### Volume

- Working volume counts lifts above 50% of your best in that movement.
- All 12 Soviet groups get planned: Snatch, Clean, Jerk, Squat, SnPull, ClPull, Press, Fundamental, plus the Other variants of the first four.
- The block is five mesos of four weeks, three prep and two comp. Each meso has a weight and a weekly split. See `MACRO`.
- Group targets come from the class ratio tables, shifted by the meso. eg the Comp meso adds clean and jerk and cuts squat. See `III_II`, `I_CMS` and `MS_R`.
- A group can drift ±20% from its share. The tool caps total drift at 10% of the week. Every split sums exactly.
- Sessions use six slots: Snatch, Clean, Jerk, Squat or pull, Other Squat or Press, and Fundamental (general strength). Each session fills the slots it needs. `X|Y` means one or the other, split across days. A movement gets at least 6 lifts when the margins allow. See `DAY`.
- Days are S (up to 50 lifts), M (51–100) or L (over 100). The week takes the first pattern with 3 to 6 days that fits its volume. See `VARIANTS`.

### Intensity

- A zone is 5 points wide (eg 70–74%) and zones sit 10 apart. The label is the lower edge. The top zone is open.
- ARI is average relative intensity. Moving 1% of reps one zone moves ARI by 0.1.
- The anchor is Takano's yearly bin tables: class 2 (III and II), class 1 (I), CMS and MS. See `BINS`.
- Prep and comp shift the anchor by the class gap `g`, the prep to comp intensity rise. Prep = yearly − 0.33g, comp = yearly + 0.67g. See `GAP`.
- I, CMS and MS fan across the prep mesos. III and II use one prep shift for all three. See `FAN`.
- The final comp meso tapers. Its last week keeps snatch and C&J below 90%. Other groups use the yearly bins.
- An "Other" variant inherits its base table. Press inherits Fundamental. See `BIN_GROUP`.

### Sessions and sets

- A session's zone profile is contiguous from its lowest zone to its top.
- First visits ascend. Each ascent goes to the next zone present. Reps hold or drop as the zone holds or rises.
- A clean and a jerk in one session get one ratio per tier:
  - 1:1 anywhere.
  - 2:1 and 1:2 below 90%.
  - 3:1, 3:2, 1:3 and 2:3 below 80%.
- The ratio narrows as weight rises.
- A zone's count becomes sets from the preferred reps per group, largest first. Fewest sets wins. 1 is always legal. See `REPS`.
- The tool searches the legal set orders and takes the cheapest.
- Notation:
  - `NxR` for repeated sets.
  - Commas for runs, eg `4x3,2x2`.
  - `p+q` for a clean and jerk complex.
  - `Nx(...)` for a repeated wave.
  - A lone set is just the rep count.

## Guarantees

- Every split sums exactly.
- Zone profiles stay contiguous.
- Every clean:jerk ratio stays legal.
- Same input, same output.

## Open

1. Which split should be the default Comp meso (1, 3-1, 2 or 1-3)?
2. Use the ±20% week band to avoid movements below 6 lifts in taper and low-volume weeks?
