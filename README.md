# WL Program Generator

Generates a 20-week Soviet-style Olympic weightlifting macrocycle from an annual lift target, ending at a competition. It splits volume first, then intensity, then sets, and writes a styled HTML report per class. It is deterministic. It uses only the standard library.

## Words used in this file

- Volume is a count of lifts. Only lifts above 50% of the best lift count.
- Intensity is a percentage of the best lift. A zone is an intensity bucket, for example 70%.
- A group is one of the 12 movement groups in the plan, for example snatch or squat.
- Prep is the preparation phase, which builds volume. Comp is the competition phase, which peaks for the contest.
- A macrocycle is the full program of 20 weeks. It holds five mesocycles of four weeks. Each mesocycle holds four microcycles of one week. Each microcycle holds training sessions.
- A session is one training day. It holds up to five slots. Each slot holds one movement or one combined movement.
- A combined movement trains two movements in one slot, for example clean and jerk.
- A set is one group of reps. A rep is one lift. A scheme is the written set plan for one slot. A dose is the lifts prescribed for one movement in one session.
- Median means the middle value.
- Instructions are the items the athlete must read and follow.
- A taper is a planned easy week with lighter loads.
- Prilepin's chart is a published table that links intensity to recommended reps. A session unit is one full session of work under that chart. Tolerance is the largest healthy dose for one movement in one session. The floor is the smallest useful dose.
- Contrast is the biggest training day divided by the smallest training day in one week. Range is the biggest day minus the smallest day.
- A planned amount is the lifts a week should contain for one movement. A band is the allowed range around a planned amount, 20 percent up or down.
- A base zone is the lightest zone the week uses.
- A gap is a missing intensity step inside one session, one week, one mesocycle, or the program. An illegal set breaks a training rule. A clash puts together movements that cannot share a day. Idle describes a movement that should train in a week but trains zero days.
- Spacing is how evenly training spreads across days and weeks.
- Defects are the drift items below.
- Pace is the build cost in the score. It is the square of the book's CPU seconds over 3.6, minus one. Halving the build is minus three quarters. Zero-cost builds score minus one, so speed can never buy more than one point.

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

A plan has two parts, Volumes and Training Plan. Volumes holds three tables. The first shows the whole-program total and the mesocycle sizes. The second shows one volume column per mesocycle with the weekly sizes. The third shows lifts per group and zone for each week. Training Plan holds one table per mesocycle. Weeks go across. Sessions and slots go down.

Each training plan slot gets one row with two columns per week. The first column names the movement. The second column shows its scheme with the zone over the reps, as a stacked fraction:

```
| | Week 1 | |
| 1 | SnPull+Snatch | 80% / 1+2 |
```

`80%/1+2` is one set of one pull plus two snatches at 80%. `70%/3*2,2` is two sets of three then one set of two at 70%. `4*(70%/3+2, 80%/2+1)` repeats a two-zone complex block four times.

## What's in the repo

- `src/wlconfig.py` — all data and tuning.
- `src/wlir.py` — the intermediate representation both sides share.
- `src/wlgen.py` — the generator and the HTML renderer.
- `src/wlscore.py` — two functions: `generate_json` writes the JSON files, `score_json` reads one back and returns the score.
- `tests/test_wlgen.py` — the generator test suite.
- `tests/test_wlscore.py` — the representation and scorer tests.
- `outputs/` — the five generated plans, each as HTML and JSON.
- `pyproject.toml` — packaging, test, lint and type-check config.
- `uv.lock` — pinned dev dependencies.
- `.python-version` — interpreter uv uses.
- `.pre-commit-config.yaml` — format and type-check hooks.

## How it plans

Each level takes a share of the level above it.

### Volume

- Volume counts lifts above 50% of the best lift in that movement. The plan covers all 12 groups.
- The block is five 4-week mesocycles: three prep and two comp.
- Weekly group volumes follow fixed class shares. The tool shifts a little volume between weeks: 20 percent per group and 10 percent per week at most, so lifts stay whole, sessions fit, and the mesocycle sums exactly.
- A session draws from five optional slots. Combined movements such as `SnPull+Snatch` or `Clean+Jerk` share one slot. Other options split across the week, and each movement gets a minimum dose (6 lifts).

### Intensity

- The plan buckets intensity into zones at 60%, 70%, 80% and up.
- Each class has a yearly zone mix from Takano's tables.
- Prep sits below that mix, comp above it, and the gap grows with class. Higher classes rise in intensity across the three prep mesocycles too.
- The last comp week tapers: snatch and clean and jerk stay below 90%.

### Sessions and sets

- A session orders its sets like a warm-up. Zones first appear from light to heavy. Each jump up goes to the next zone in the session. Reps stay flat or drop as weight rises. A drop back down can add reps.
- A combined movement follows a fixed rep ratio, for example 2 pulls per snatch or 2 cleans per jerk. Lighter zones allow more ratios, and the choice narrows as weight rises. It counts toward both movements.
- The tool packs each movement's reps at a zone into as few sets as possible, then picks the cleanest legal order.

## Representation and scoring

Each plan is also saved as JSON (`outputs/<CLASS>.json`). The JSON is the intermediate representation. It holds plain data using only basic types, so any tool can read it. Each session lists its slots: the movement, the atom scheme, and the parsed items. The HTML is rendered from the JSON itself. Two functions use it. `generate_json` writes the files. `score_json` reads one back and returns the score. Scoring never imports the generator, so any JSON in the same shape scores the same.

`wlgen audit` builds all five classes and prints one scoreboard row per class plus the book total. The score has four parts. Lower is better.

- **Strain** — dose health. Work over the tolerance plus work under the 0.25 floor, in session units, divided by 150.
- **Size** — instructions to follow plus the longest single slot.
- **Rhythm** — how far the median week is from a 2.75 contrast, plus missing turns and peaks away from one. A turn is a change of direction between days. A peak is a day heavier than its neighbors. Only moves of at least a tenth of the week's range steer the turns and the peaks.
- **Drift** — everything off plan. Group and total misses at week, mesocycle, and program scale. Group misses count only beyond the band. Total misses count in full. Illegal sets, clashes, gaps, idle movements, warmup softness, uneven spacing, and pace.

The divisors (150, 9300, 25, 0.25) scale each part to about 1.0 on today's plans. `score = 0.4·strain + 0.3·size + 0.1·rhythm + 0.2·drift`. A shipped plan scores zero on illegal sets, clashes, and idle movements. Warmup softness and bin gaps are nonzero in current plans. The generator must narrow the openers and fill or drop the holed zones.

## Guarantees

- Every split sums exactly.
- Sets follow the warm-up order.
- Every combined-movement ratio stays legal, and each side's reps stay flat or fall as weight rises.
- Each session's zones form one unbroken run from the session's lightest zone. A gap stands only where too few lifts remain to cover every session that needs that zone.
- A session touches the week's base zone whenever the week holds enough to share.
- Every movement in a session prescribes 0 or at least 6 total reps. A combined movement counts both sides.
- Same input, same output.

## Open

1. Which volume split should the default Comp mesocycle use?
