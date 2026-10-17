# WL Program Generator

Builds a 20-week Soviet-style Olympic weightlifting macrocycle (one training block) from an annual lift target. Volume is split to weeks, days, and sets. The plan uses discrete intensity zones. Output is Markdown. The tool is deterministic and uses only the Python standard library.

## Run

```sh
python3 -m venv .venv
.venv/bin/pip install pytest ruff
.venv/bin/python wlgen.py            # write one plan per class to outputs/
.venv/bin/pytest -q                  # run the tests
.venv/bin/ruff format . && .venv/bin/ruff check .
```

Or import it:

```python
from wlgen import build_plan, to_markdown

text = to_markdown(build_plan("MS"))
```

The tool writes one plan per competition class: `outputs/III.md`, `II.md`, `I.md`, `CMS.md`, and `MS.md`. Class III is the entry level and MS the top level. Annual volume runs from 10k to 18k lifts by class. `build_plan` caches its result per class.

A session bullet gives exact sets, reps, and zone:

```
- Snatch: 3x3,2x2@70%
- Other Clean+Other Jerk: 3+2@70%, 4x(3+2@70%, 2+1@80%)
```

## Files

| File | Contents |
|------|----------|
| `wlconfig.py` | All data and tuning: ratios, templates, bins, search widths. Method steps name its tables. |
| `wlgen.py` | The generator and the Markdown renderer. |
| `test_wlgen.py` | The test suite. |
| `outputs/` | The five generated plans. |

## Method

The exact tables live in `wlconfig.py`. Each step below names its table.

### Volume

- Working volume counts lifts above 50% of the athlete's best in that movement.
- The plan covers all 12 Soviet groups. The list is Snatch, Clean, Jerk, Squat, SnPull, ClPull, Press, Fundamental, and the Other variants of Snatch, Clean, Jerk, and Squat.
- The block is five mesocycles (mesos) of four weeks: three prep and two comp. Each meso has a volume weight and a four-week split, taken from the source plan. See `MACRO`.
- Week group targets come from the Soviet ratio tables for the class and meso phase (prep or comp). See `III_II`, `I_CMS`, and `MS_R`. A meso type shifts the ratios. For example, the Comp (competition) meso adds Clean and Jerk and removes Squat.
- Each group may sit ±20% from its nominal share. The tool caps total movement at 10% of the week. Every split sums exactly.
- Sessions use one six-slot template (`DAY`). Slots cover Snatch, Clean, Jerk, Squat or pull, Other Squat or Press, and Fundamental (general strength). Each session fills a subset of the slots. `X|Y` alternatives split across days. A movement gets at least 6 lifts when the margins allow.
- Day sizes are S (up to 50 lifts), M (51 to 100), and L (over 100). The week uses the first pattern with 3 to 6 days whose day-size targets fit its volume. See `VARIANTS`.

### Intensity

- A zone covers five percentage points, for example 70% to 74%. Labels show the lower edge, and zone labels are 10 apart. The top zone is open. Moving 1% of reps one zone changes ARI (average relative intensity) by 0.1.
- The anchor is the yearly bin tables from Takano's Soviet programming tables: Class 2 (III and II), Class 1 (I), CMS, and MS. See `BINS`.
- Prep and comp shift the anchor by the class gap `g`. `g` is the intensity rise from prep to comp. Prep = yearly − 0.33g and comp = yearly + 0.67g. The sample-program gap table gives `g`. See `GAP`.
- I, CMS, and MS fan across the prep mesos. III and II use the same prep shift in all three prep mesos. See `FAN`.
- The last comp meso tapers. Its final week keeps Snatch and C&J (clean and jerk) below 90%. Other groups use the yearly bins.
- Each "Other" variant shares the bin table of its base movement. Press shares the Fundamental table. See `BIN_GROUP`.

### Sessions and sets

- A session's zone profile is contiguous from its lowest zone to its own top.
- The first visit to each zone ascends by weight. Each ascent goes to the next heavier zone present. Reps stay equal or fall when the zone stays or rises.
- A clean and a jerk in one session use one legal ratio per zone tier. 1:1 is legal anywhere. 2:1 and 1:2 are legal below 90%. 3:1, 3:2, 1:3, and 2:3 are legal below 80%. The plan narrows the ratio as the weight rises.
- A zone's count becomes sets from the preferred reps per movement group, largest first. Fewest sets wins, with `1` as the fallback. See `REPS`.
- The tool searches the legal set orders and picks the cheapest one (fewest below-target sets, then the shortest text).
- Notation: `NxR` for repeated sets, commas for runs (`4x3,2x2`), `p+q` for a clean and jerk complex, and `Nx(...)` for a repeated wave. A lone set renders as the rep count alone.

## Guarantees

- Every split keeps exact integer totals: meso, week, group, and zone counts.
- Every session's profile is contiguous and follows the order rules.
- Every clean:jerk ratio is legal in every zone.
- The same input gives the same byte-identical output.

All tables and rules live in `wlconfig.py`.

## Open questions

1. Which Soviet split should be the default Comp meso (1, 3-1, 2, or 1-3)?
2. Use the ±20% week band to avoid movements below 6 lifts in taper and low-volume weeks?
