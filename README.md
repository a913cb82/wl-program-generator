# WL Program Generator

Generates a 20-week Soviet-style Olympic weightlifting macrocycle from an annual lift target, ending at a competition. It splits volume first, then intensity, then sets, and writes a styled HTML report per class. It is deterministic. It uses only the standard library.

## Run

`wlgen` writes one plan per competition class into `outputs/`.

```sh
uv sync --all-extras                 # create .venv from uv.lock (Python 3.14)
.venv/bin/wlgen                      # write all five plans
.venv/bin/pytest -q                  # run the tests
.venv/bin/pre-commit install         # enable format and type hooks
```

Classes are independent, so the five plans render in parallel by default (one
worker per class, up to the CPU count). Set `WLGEN_JOBS` to change it.
`1` renders serially.

```sh
WLGEN_JOBS=1 .venv/bin/wlgen         # single process, identical output
.venv/bin/wlgen audit                # print the scoreboard for all five plans
.venv/bin/wlgen score outputs/III.json  # score one saved plan
```

Get uv from <https://docs.astral.sh/uv/>.

Or use it as a library:

```python
from wlgen import build_plan, to_html

text = to_html(build_plan("MS"))
```

## What you get

Ten files, one HTML page plus one JSON file per competition class, III (entry) to MS (top):

| File | Class | Annual lifts |
|------|-------|-------------:|
| `outputs/III.html` | Class III | 12000 |
| `outputs/II.html` | Class II | 12000 |
| `outputs/I.html` | Class I | 15000 |
| `outputs/CMS.html` | CMS | 15000 |
| `outputs/MS.html` | MS | 18000 |

Open one in a browser. Each file is self-contained (inline CSS, no scripts).

A plan has two parts, Volumes and Training Plan. Volumes holds three tables. The first shows the whole-block total and the meso sizes. The second shows one volume column per meso with the weekly sizes. The third shows lifts per group and zone for each week. Training Plan holds one table per mesocycle. Weeks go across. Sessions and slots go down.

Each training plan slot gets one row with two columns per week. The first column names the movement. The second column shows its scheme with the zone over the reps, as a stacked fraction:

```
| | Week 1 | |
| 1 | SnPull+Snatch | 80% / 1+2 |
```

`80%/1+2` is one set of one pull plus two snatches at 80%. `70%/3*2,2` is two sets of three then one set of two at 70%. `4*(70%/3+2, 80%/2+1)` repeats a two-zone complex block four times. Sets of one omit the `*1`.

## What's in the repo

- `src/wlconfig.py` — all data and tuning.
- `src/wlgen.py` — the generator and the HTML renderer.
- `src/wlscore.py` — the program scorer and the audit.
- `tests/test_wlgen.py` — the generator test suite.
- `tests/test_wlscore.py` — the representation and scorer tests.
- `outputs/` — the five generated plans, each as HTML and JSON.
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

Each level takes a share of the level above it.

### Volume

- Volume counts lifts above 50% of the best lift in that movement. The plan covers all 12 groups.
- The block is five 4-week mesos: three prep, two comp.
- Weekly group volumes follow the class ratio table. The tool shifts a little volume between weeks (±20% per group, 10% per week) so lifts stay whole, sessions fit, and the meso sums exactly.
- A session draws from five optional slots. Combined movements such as `SnPull+Snatch` or `Clean+Jerk` share one slot. Other options split across the week, and each movement gets a minimum dose (6 lifts).

### Intensity

- The plan buckets intensity into zones at 60%, 70%, 80% and up.
- Each class has a yearly zone mix from Takano's tables.
- Prep sits below that mix, comp above it, and the gap grows with class. Higher classes ramp up across the three prep mesos too.
- The last comp week tapers: snatch and clean and jerk stay below 90%.

### Sessions and sets

- A session orders its sets like a warm-up. Zones first appear from light to heavy. Each jump up goes to the next zone in the session. Reps stay flat or drop as weight rises. A drop back down can add reps.
- Two paired movements sharing a day follow a fixed rep ratio, for example 2 pulls per snatch or 2 cleans per jerk. Lighter zones allow more ratios, and the choice narrows as weight rises. Pair volume counts toward both movements.
- The tool packs each movement's reps at a zone into as few sets as possible, then picks the cleanest legal order.

## Representation and scoring

Each plan is also saved as JSON (`outputs/<CLASS>.json`). The JSON is the intermediate representation. It holds plain data with no tuples, so any tool can read it. The HTML is rendered from the JSON itself. The scorer reads the JSON too.

`wlgen audit` builds all five classes and prints one scoreboard row per class plus the book total. The score has four parts. Lower is better.

- **Strain** — dose health. Work over the tolerance plus work under the 0.25 floor, in session units, divided by 150.
- **Size** — instructions to follow plus the longest single block.
- **Rhythm** — how far the median week is from a 2.75 contrast, plus missing turns and off-count peaks. A turn is a change of direction between days. A peak is a day heavier than its neighbors. Only moves of at least a tenth of the week's range steer the turns and the peaks.
- **Drift** — everything off plan. Group and total misses at week, block, and program scale. Illegal sets, unworkable days, gaps, idle movements, uneven spacing, and slow builds.

`score = 0.4·strain + 0.3·size + 0.1·rhythm + 0.2·drift`. A shipped plan scores zero on every defect term. Only spacing is nonzero today.

## Guarantees

- Every split sums exactly.
- Sets follow the warm-up order.
- Every paired-movement ratio stays legal, and each side's reps stay flat or fall as weight rises.
- Each session's zone profile is contiguous from its own base. A gap stands only where the week cannot cover every session spanning it.
- A session touches the week's base zone whenever the week holds enough to share.
- Every movement in a session prescribes 0 or at least 6 total reps. A combined movement counts both sides.
- Same input, same output.

## Open

1. Which volume split should the default Comp meso use?
