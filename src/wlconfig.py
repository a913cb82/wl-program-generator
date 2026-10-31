"""Tunable data and rules for the WL program generator."""

import os as _os
from functools import cache
from typing import Any, Dict

GROUPS = [
    "Snatch",
    "Other Snatch",
    "Clean",
    "Other Clean",
    "Jerk",
    "Other Jerk",
    "Squat",
    "Other Squat",
    "SnPull",
    "ClPull",
    "Press",
    "Fundamental",
]

MACRO = [
    ("Prep 4-2", "prep", [21, 28, 17, 34], 0.20),
    ("Prep 2-4", "prep", [22, 33, 18, 27], 0.22),
    ("Prep 3-1", "prep", [27, 18, 32, 23], 0.25),
    ("Comp 1", "comp", [36, 28, 24, 12], 0.18),
    ("Comp 2", "comp", [28, 33, 26, 13], 0.15),
]

# Session-size patterns per day count, first Soviet variant first (plan table).
VARIANTS = {
    3: ["SLS", "MLM", "LSL", "LML"],
    4: ["SLMS", "LMLM", "LMLS", "LSLS", "SMMS", "MLMS"],
    5: ["MSLMS", "MSLMM", "SLSLS", "LSMML", "MSMMS"],
    6: ["SMSMSM", "MSLSMS", "MLSMSM", "MMSMSM", "MSLSMM", "SLSLSM"],
}
PATTERNS = {n: patterns[0] for n, patterns in VARIANTS.items()}
SIZE_WEIGHT = {"S": 1, "M": 2, "L": 3}
CAP = 150  # max lifts in one day

# How a week is cut into days. "templates" walks the Soviet shape table;
# "demand" computes the day count from the week's Prilepin demand and cuts
# the volumes by a heavy/light rhythm instead.
DAY_RULE = _os.environ.get("WLGEN_RULE", "templates")
# Tuned on the real book: five session-equivalents of Prilepin score per day
# is the sweet spot. Lower starves the light days (4 was infeasible), higher
# concentrates the week (6 gave a three-day median and a 4.13 worst dose).
DAY_T = float(_os.environ.get("WLGEN_T", "5"))
# Heavy days run three times the light ones, every other day.
DAY_C = float(_os.environ.get("WLGEN_C", "3"))  # 0 means scale with the week
DAY_CMAX = float(_os.environ.get("WLGEN_CMAX", "3"))
# "peak" gives the week one peak with mid-size shoulders; "alt" gives every
# other day a peak. Tuned: one peak keeps contrast three for 20% less
# over-capacity work than alternating peaks, which concentrate twice as much.
DAY_SHAPE = _os.environ.get("WLGEN_SHAPE", "peak")
# 1 keeps the old rule of one group per day per slot; more lets groups share.
DAY_QUOTA = float(_os.environ.get("WLGEN_QUOTA", "1"))

TOL = 0.2  # a microcycle's group targets may sit +/- this far from the nominal split
CAP_DEV = 0.1  # ... and its total deviation may not exceed this share of volume
MIN_DOSE = 6  # a session trains a movement only if it has at least this many lifts

# preferred reps per set (largest first) by lift family and zone lower bound;
# 1 is always a legal fallback
REPS = {
    "Snatch": {60: (3, 2), 70: (3, 2), 80: (2, 1), 90: (1,), 100: (1,)},
    "CJ": {60: (3, 2), 70: (3, 2), 80: (2, 1), 90: (1,), 100: (1,)},
    "Squat": {
        # The light zones run the full rep range. A zone total then fits in
        # one or two even sets, so the ascent carries a single rep count
        # instead of leaving a 2 or 3 behind that caps every zone above it.
        50: tuple(range(12, 2, -1)),
        60: tuple(range(8, 1, -1)),
        70: (5, 4, 3, 2),
        80: (4, 3, 2),
        90: (2, 1),
    },
    "SnPull": {80: (4, 3, 2), 90: (4, 3, 2), 100: (3, 2), 110: (3, 2)},
    "ClPull": {
        70: (4, 3, 2),
        80: (4, 3, 2),
        90: (4, 3, 2),
        100: (3, 2),
        110: (3, 2),
    },
    "Fund": {
        50: tuple(range(12, 2, -1)),
        60: tuple(range(8, 1, -1)),
        70: (5, 4, 3, 2),
        80: (4, 3, 2),
        90: (3, 2),
        100: (1,),
        110: (1,),
    },
}

BEAM = 32  # session-order beam width
BEAM_JOINT = 16  # fallback width when the preferred fill cannot be ordered
FINISH_SCAN = 2  # survivors rescored under the true cost (waves compress)
STRAY_COST = 100
# Prilepin's chart: the most reps a single session spends at each intensity
# before it is past the top of his range. Flat outside the anchors.
PRILEPIN_CAPACITY = {60: 30, 70: 24, 80: 20, 90: 10, 100: 4}
# One session's worth of capacity is free. The classic lifts the chart was
# built from then climb at the hard rate above 1.5; squats, pulls and
# fundamentals are exempt from its calibration and get until 2.0.
PRILEPIN_CLASSIC = ("Snatch", "CJ")
PRILEPIN_SOFT_AT = {"classic": 1.5, "strength": 2.0}
PRILEPIN_SOFT = 4
PRILEPIN_HARD = 20
WARMUP_COST = 10
COMPLEXITY_COST = 4
# One more set to read and follow in a slot. The beam already spends one
# unit of pruning guide per set while it searches; the final choice prices
# the same unit, so a shorter order wins when it costs little extra.
LENGTH_COST = 1

# Soviet class tables: % volume per group (prep/comp)
III_II = {
    "prep": [10, 10, 7.5, 9.5, 7.5, 3.5, 27, 15, 0, 0, 10, 0],
    "comp": [10, 10, 7.5, 9.5, 7.5, 3.5, 27, 15, 0, 0, 10, 0],
}
I_CMS = {
    "prep": [9, 11, 6, 9, 7, 5, 23, 0, 7, 5, 0, 18],
    "comp": [9, 12, 6, 9, 7, 6, 23, 0, 5, 6, 0, 17],
}
MS_R = {
    "prep": [8, 12, 5, 8, 6, 7, 20, 0, 8.5, 10, 0, 15.5],
    "comp": [8, 13, 5, 8, 6, 8, 20, 0, 5, 12, 0, 15],
}

# Yearly lifts per class: 12 prep weeks at the prep band midpoint plus 8
# comp weeks at the comp band midpoint (Roman p88: low 1250/900,
# I&CMS 1650/1200, MS 2100/1500 lifts/month). Ratios 1 : 1.33 : 1.67.
CLASSES: Dict[str, Any] = {
    "III": {"annual": 13000, "macro": MACRO, "ratios": III_II},
    "II": {"annual": 13000, "macro": MACRO, "ratios": III_II},
    "I": {"annual": 17500, "macro": MACRO, "ratios": I_CMS},
    "CMS": {"annual": 17500, "macro": MACRO, "ratios": I_CMS},
    "MS": {"annual": 22000, "macro": MACRO, "ratios": MS_R},
}

# Intensity bins: measured annual zone shares from the Takano sample
# programs (fixtures takano-{III,II,I,CMS,MS}.json, classic and assistance
# lifts pooled by bin type). Direction checked against Roman Tables 2-6:
# modal mass moves 70 toward 80, 90%+ grows, 60% shrinks with level.
# Keyed per class; III and II get their own tables, not one shared table.
BINS = {
    "III": {
        "Snatch": [0.49, 0.32, 0.15, 0.04, 0.0],
        "CJ": [0.45, 0.35, 0.16, 0.04, 0.0],
        "Squat": [0.04, 0.24, 0.34, 0.35, 0.03],
        "SnPull": [0.91, 0.09, 0.0, 0.0],
        "ClPull": [0.08, 0.84, 0.08, 0.0, 0.0],
        "Fund": [0.04, 0.09, 0.24, 0.63, 0.0, 0.0, 0.0],
    },
    "II": {
        "Snatch": [0.36, 0.36, 0.26, 0.02, 0.0],
        "CJ": [0.4, 0.36, 0.21, 0.03, 0.0],
        "Squat": [0.02, 0.23, 0.32, 0.37, 0.06],
        "SnPull": [0.78, 0.22, 0.0, 0.0],
        "ClPull": [0.0, 0.85, 0.15, 0.0, 0.0],
        "Fund": [0.0, 0.05, 0.05, 0.81, 0.09, 0.0, 0.0],
    },
    "I": {
        "Snatch": [0.27, 0.33, 0.33, 0.07, 0.0],
        "CJ": [0.26, 0.34, 0.32, 0.08, 0.0],
        "Squat": [0.01, 0.19, 0.23, 0.51, 0.06],
        "SnPull": [0.41, 0.43, 0.16, 0.0],
        "ClPull": [0.04, 0.42, 0.45, 0.09, 0.0],
        "Fund": [0.0, 0.2, 0.23, 0.53, 0.04, 0.0, 0.0],
    },
    "CMS": {
        "Snatch": [0.24, 0.37, 0.33, 0.06, 0.0],
        "CJ": [0.23, 0.36, 0.34, 0.07, 0.0],
        "Squat": [0.02, 0.2, 0.26, 0.44, 0.08],
        "SnPull": [0.11, 0.49, 0.4, 0.0],
        "ClPull": [0.02, 0.41, 0.36, 0.21, 0.0],
        "Fund": [0.0, 0.09, 0.13, 0.62, 0.16, 0.0, 0.0],
    },
    "MS": {
        "Snatch": [0.19, 0.34, 0.39, 0.08, 0.0],
        "CJ": [0.2, 0.36, 0.34, 0.1, 0.0],
        "Squat": [0.01, 0.15, 0.18, 0.58, 0.08],
        "SnPull": [0.14, 0.34, 0.49, 0.03],
        "ClPull": [0.03, 0.24, 0.51, 0.22, 0.0],
        "Fund": [0.0, 0.09, 0.2, 0.57, 0.11, 0.03, 0.0],
    },
}
BIN_CLASS = {"III": "III", "II": "II", "I": "I", "CMS": "CMS", "MS": "MS"}
BIN_ZONES = {
    "Snatch": [60, 70, 80, 90, 100],
    "CJ": [60, 70, 80, 90, 100],
    "Squat": [50, 60, 70, 80, 90],
    "SnPull": [80, 90, 100, 110],
    "ClPull": [70, 80, 90, 100, 110],
    "Fund": [50, 60, 70, 80, 90, 100, 110],
}
BIN_GROUP = {
    "Snatch": "Snatch",
    "Other Snatch": "Snatch",
    "Clean": "CJ",
    "Other Clean": "CJ",
    "Jerk": "CJ",
    "Other Jerk": "CJ",
    "Squat": "Squat",
    "Other Squat": "Squat",
    "SnPull": "SnPull",
    "ClPull": "ClPull",
    "Press": "Fund",
    "Fundamental": "Fund",
}
# prep -> comp ARI gap (Takano table 8.1, classic lifts); one gap for all groups
GAP = {"III": 0.5, "II": 0.5, "I": 1.0, "CMS": 1.5, "MS": 1.9}
# classes whose sample programs ramp intensity across the prep mesocycles
FAN = {"I", "CMS", "MS"}

# One session template: (alternatives, min reps, max reps, optional). Every
# slot may be empty; the annual spread decides what each session trains.
# Alternatives holding a "+" are complexes: both groups train together in
# one slot and their session volumes must keep a legal clean-and-jerk style
# ratio (see RATIOS below). Singles sharing a slot split across the week.
DAY = [
    (["Snatch", "Other Snatch", "SnPull+Snatch", "SnPull+Other Snatch"], 6, None, True),
    (
        [
            "Clean",
            "Other Clean",
            "Jerk",
            "Other Jerk",
            "Clean+Jerk",
            "Other Clean+Other Jerk",
            "Other Clean+Jerk",
            "Clean+Other Jerk",
            "ClPull+Clean",
            "ClPull+Other Clean",
        ],
        6,
        None,
        True,
    ),
    (["Squat", "SnPull", "ClPull"], 6, None, True),
    (["Other Squat", "Press"], 6, None, True),
    (["Fundamental"], 6, None, True),
]


def token_parts(token):
    """Groups trained by one slot alternative (one for singles, two for A+X)."""
    return tuple(token.split("+"))


def slot_singles(slot):
    return [t for t in slot[0] if "+" not in t]


# groups never in a complex (the refit only ever moves these)
BALLAST = ("Squat", "Other Squat", "Press", "Fundamental")
# allowed A+X complexes: session volumes of both members must keep a legal
# ratio (RATIOS) at every shared zone, widening only as weight drops.
# Canonical display order is pull/classic first ("SnPull+Snatch").
PAIRS = [
    ("SnPull", "Snatch"),
    ("SnPull", "Other Snatch"),
    ("Clean", "Jerk"),
    ("Other Clean", "Other Jerk"),
    ("Other Clean", "Jerk"),
    ("Clean", "Other Jerk"),
    ("ClPull", "Clean"),
    ("ClPull", "Other Clean"),
]
# reference member per pair for intensity tiers and zone labels: the classic
# lift (or jerk) limits the complex, so paired pulls count at classic zones.
PAIR_REF = {
    ("SnPull", "Snatch"): "Snatch",
    ("SnPull", "Other Snatch"): "Other Snatch",
    ("Clean", "Jerk"): "Clean",
    ("Other Clean", "Other Jerk"): "Other Clean",
    ("Other Clean", "Jerk"): "Jerk",
    ("Clean", "Other Jerk"): "Clean",
    ("ClPull", "Clean"): "Clean",
    ("ClPull", "Other Clean"): "Other Clean",
}
PAIRED_GROUPS = {g for p in PAIRS for g in p}
# allowed clean:jerk ratios when both are trained in one session
RATIOS = ((1, 1), (2, 1), (3, 1), (3, 2), (1, 2), (1, 3), (2, 3))


def ratio_ok(p, q, zlo):
    """Legal rep ratio at a zone: 3:2/2:3 (and wider) below 80%, 2:1/1:2
    below 90%, 1:1 anywhere."""
    if p == q == 1:
        return True
    if zlo >= 90:
        return False
    if zlo >= 80:
        return (p, q) in ((2, 1), (1, 2))
    return True


def allowed_ratios(zlo):
    return tuple(r for r in RATIOS if ratio_ok(*r, zlo))


def ratio_rank(p, q):
    if (p, q) == (1, 1):
        return 0
    if (p, q) in ((2, 1), (1, 2)):
        return 1
    if (p, q) in ((3, 2), (2, 3)):
        return 2
    return 3


SCHEDULES = tuple(
    (heavy, mid, light)
    for heavy in allowed_ratios(90)
    for mid in allowed_ratios(80)
    for light in allowed_ratios(70)
    if ratio_rank(*mid) >= ratio_rank(*heavy)
    and ratio_rank(*light) >= ratio_rank(*mid)
    # Neither member's share may grow with weight: a flip such as
    # light (1, 2) -> mid (2, 1) would force one side's per-set reps up
    # on the way up (e.g. 1+2@70% -> 2+1@80%).
    and heavy[0] <= mid[0] <= light[0]
    and heavy[1] <= mid[1] <= light[1]
)


PAIR_SET = {frozenset(p) for p in PAIRS}
PAIR_BY_SET = {frozenset(p): p for p in PAIRS}


def _slot_tables():
    singles: dict = {}
    complexes: dict = {}
    for si, slot in enumerate(DAY):
        for tok in slot[0]:
            parts = token_parts(tok)
            if len(parts) == 1:
                singles.setdefault(parts[0], set()).add(si)
            else:
                complexes.setdefault(frozenset(parts), set()).add(si)
    return singles, complexes


SINGLE_SLOTS, COMPLEX_SLOTS = _slot_tables()


@cache
def is_matchable(groups):
    """True when every hosted group can take a template slot, with listed
    A+X complexes sharing one slot.

    Co-hosted pairs need not render jointly: unpaired groups keep their own
    sets (separate bullets), so overlapping triples only need distinct-slot
    sharing here. Designated pairs are chosen later by detect_pairs."""
    groups = set(groups)
    if not groups:
        return True
    if any(g not in SINGLE_SLOTS and all(g not in p for p in PAIR_SET) for g in groups):
        return False

    def rec(remaining, used):
        if not remaining:
            return True
        g = next(iter(remaining))
        rest = set(remaining)
        rest.discard(g)
        for si in SINGLE_SLOTS.get(g, ()):
            if si not in used and rec(rest, used | {si}):
                return True
        for h in list(rest):
            key = frozenset((g, h))
            if key not in PAIR_SET:
                continue
            for si in COMPLEX_SLOTS.get(key, ()):
                if si not in used:
                    rest2 = set(rest)
                    rest2.discard(h)
                    if rec(rest2, used | {si}):
                        return True
        return False

    return rec(groups, set())


def slot_match(groups):
    """True when every group can take a distinct template slot (listed
    complexes may share one)."""
    groups = set(groups)
    return is_matchable(frozenset(groups))


# free slots carry the annual spread; the Clean/Jerk slot is shaped by the
# pair rule instead (its singles still host via the fit, but with no quota)
FREE_SLOTS = (DAY[0], DAY[2], DAY[3], DAY[4])
EPS = 0.01  # soft weight for a non-target host day
BOUNDARY = 0.001  # even softer: first day after a group trained last week

# weekday names for rendering. Sunday rests; sessions spread Mon-Sat.
WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

# week table columns
DISPLAY_ZONES = [50, 60, 70, 80, 90, 100, 110]
