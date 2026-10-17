# WL Program Generator

Builds a 20-week Soviet-style Olympic weightlifting macrocycle from an annual lift target. Volume is split to weeks, days, and sets. The plan uses discrete intensity zones, not averages. Output is Markdown. The tool is deterministic and uses only the Python standard library.

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

The tool writes `outputs/III.md`, `II.md`, `I.md`, `CMS.md`, and `MS.md`. Annual volume runs from 10k to 18k lifts by class. `build_plan` caches its result per class.

A session bullet gives exact sets, reps, and zone:

```
- Snatch: 3x3,2x2@70%
- Other Clean+Other Jerk: 3+2@70%, 4x(3+2@70%, 2+1@80%)
```

## Files

| File | Contents |
|------|----------|
| `wlconfig.py` | All data and tuning: ratios, templates, bins, search widths. |
| `wlgen.py` | The generator and the Markdown renderer. |
| `test_wlgen.py` | The test suite. |
| `outputs/` | The five generated plans. |

## Method

### Volume

- Count a lift only above 50% of that movement's max. Warm-up ramps, bar and technique work, and GPP do not count. The plan includes all 12 Soviet groups.
- The block is five mesos of four weeks. Each meso has a volume weight and a four-week split, taken from the source plan. See `MACRO`.
- Week group targets come from the Soviet class × phase ratio tables. See `III_II`, `I_CMS`, and `MS_R`. A meso type shifts the ratios, for example Comp adds Clean and Jerk and removes Squat.
- Each group may sit ±20% from its nominal share. The tool caps total movement at 10% of the week. Every level sums exactly.
- Sessions use one six-slot template (`DAY`). Slots cover Snatch, Clean, Jerk, Squat or pull, Other squat or Press, and Fundamental. Every slot is optional. `X|Y` alternatives split across days. A movement gets at least 6 lifts when the margins allow.
- Days are S (under 50 lifts), M (51–100), or L (over 100). The week picks the first size pattern with 3 to 6 days that fits. See `VARIANTS`.

### Intensity

- A zone is a 5-point band. Labels show the lower edge. Zones are 10 apart, and the top zone is open. Moving 1% of reps one zone changes ARI by 0.1.
- The anchor is the yearly bin tables from Takano: Class 2 (III and II), Class 1 (I), CMS, and MS. See `BINS`.
- Prep and comp shift the anchor by the class gap `g`: prep = yearly − 0.33g, comp = yearly + 0.67g. `g` comes from the sample-program gap table. See `GAP`.
- I, CMS, and MS fan across the prep mesos. III and II stay flat. See `FAN`.
- The last comp meso tapers. Its final week drops Snatch and C&J zones at 90% and above. All other groups use the yearly bins.
- Groups without their own table inherit one. "Other" groups and Press take their parent. See `BIN_GROUP`.

### Sessions and sets

- A session's zone profile is contiguous from its lowest zone to its own top.
- The first visit to each zone ascends by weight. An ascent goes only to the next heavier zone present. Reps never rise into or within a heavier zone.
- A clean and a jerk in one session use one legal ratio per zone tier. 1:1 is legal anywhere. 2:1 and 1:2 are legal below 90%. 3:1, 3:2, 1:3, and 2:3 are legal below 80%. The ratio may only narrow as the weight rises.
- A zone's count becomes sets from the preferred reps per family, largest first. Fewest sets wins, and `1` is always legal. See `REPS`.
- The tool searches the legal set orders and picks the cheapest.
- Notation: `NxR` for repeated sets, commas for runs (`4x3,2x2`), `p+q` for a clean and jerk complex, and `Nx(...)` for a repeated wave. A lone set omits the `1x`.

## Guarantees

- Every level keeps exact integer totals.
- Every session's profile is contiguous and follows the order rules.
- Every clean:jerk ratio is legal in every zone.
- The same input gives the same byte-identical output.

All tables and rules live in `wlconfig.py`.

## Open questions

1. Default Comp meso: which Soviet split (1, 3-1, 2, or 1-3)?
2. Use the week band to avoid sub-dose movements in taper and min weeks?
