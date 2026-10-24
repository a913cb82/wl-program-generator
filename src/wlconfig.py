"""Tunable data and rules for the WL program generator."""

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

TOL = 0.2  # a microcycle's group targets may sit +/- this far from the nominal split
CAP_DEV = 0.1  # ... and its total deviation may not exceed this share of volume
MIN_DOSE = 6  # a session trains a movement only if it has at least this many lifts

# preferred reps per set (largest first) by lift family and zone lower bound;
# 1 is always a legal fallback
REPS = {
    "Snatch": {60: (3, 2), 70: (3, 2), 80: (2, 1), 90: (1,), 100: (1,)},
    "CJ": {60: (3, 2), 70: (3, 2), 80: (2, 1), 90: (1,), 100: (1,)},
    "Squat": {
        50: (5, 4, 3, 2),
        60: (5, 4, 3, 2),
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
        50: (5, 4, 3, 2),
        60: (5, 4, 3, 2),
        70: (5, 4, 3, 2),
        80: (4, 3, 2),
        90: (3, 2),
        100: (1,),
        110: (1,),
    },
}

BEAM = 32  # session-order beam width
BEAM_JOINT = 16  # fallback width when the preferred fill cannot be ordered
REP_CHANGE = 5  # soft cost of changing reps within one zone run

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

CLASSES: Dict[str, Any] = {
    "III": {"annual": 12000, "macro": MACRO, "ratios": III_II},
    "II": {"annual": 12000, "macro": MACRO, "ratios": III_II},
    "I": {"annual": 15000, "macro": MACRO, "ratios": I_CMS},
    "CMS": {"annual": 15000, "macro": MACRO, "ratios": I_CMS},
    "MS": {"annual": 18000, "macro": MACRO, "ratios": MS_R},
}

# Intensity bins: yearly share of each group's reps per zone (Takano ch. 8,
# Medvedyev; III/II use the Class 2 table). Bins are 5 points wide and 10 apart
# and labels show the lower edge; the top zone is open. "Other" groups and
# Press inherit their parent table.
BIN_ZONES = {
    "Snatch": [60, 70, 80, 90, 100],
    "CJ": [60, 70, 80, 90, 100],
    "Squat": [50, 60, 70, 80, 90],
    "SnPull": [80, 90, 100, 110],
    "ClPull": [70, 80, 90, 100, 110],
    "Fund": [50, 60, 70, 80, 90, 100, 110],
}
BINS = {
    "C2": {
        "Snatch": [0.09, 0.51, 0.29, 0.11, 0.00],
        "CJ": [0.08, 0.42, 0.37, 0.12, 0.01],
        "SnPull": [0.20, 0.41, 0.36, 0.03],
        "ClPull": [0.06, 0.30, 0.40, 0.20, 0.04],
        "Squat": [0.13, 0.28, 0.27, 0.30, 0.02],
        "Fund": [0.03, 0.08, 0.28, 0.32, 0.16, 0.12, 0.01],
    },
    "C1": {
        "Snatch": [0.07, 0.56, 0.28, 0.08, 0.01],
        "CJ": [0.04, 0.45, 0.39, 0.11, 0.01],
        "SnPull": [0.24, 0.33, 0.39, 0.04],
        "ClPull": [0.17, 0.34, 0.26, 0.19, 0.04],
        "Squat": [0.14, 0.27, 0.21, 0.35, 0.03],
        "Fund": [0.03, 0.11, 0.31, 0.31, 0.16, 0.07, 0.01],
    },
    "CMS": {
        "Snatch": [0.10, 0.61, 0.25, 0.04, 0.00],
        "CJ": [0.09, 0.53, 0.33, 0.05, 0.00],
        "SnPull": [0.31, 0.32, 0.31, 0.06],
        "ClPull": [0.23, 0.36, 0.23, 0.13, 0.05],
        "Squat": [0.22, 0.28, 0.25, 0.22, 0.03],
        "Fund": [0.05, 0.11, 0.40, 0.26, 0.10, 0.06, 0.02],
    },
    "MS": {
        "Snatch": [0.16, 0.63, 0.19, 0.02, 0.00],
        "CJ": [0.11, 0.55, 0.31, 0.03, 0.00],
        "SnPull": [0.25, 0.37, 0.32, 0.06],
        "ClPull": [0.20, 0.38, 0.24, 0.13, 0.05],
        "Squat": [
            0.22,
            0.30,
            0.25,
            0.20,
            0.03,
        ],  # source prints 2% at 90% but sums 99 and ARI 66
        "Fund": [0.04, 0.13, 0.39, 0.25, 0.10, 0.08, 0.01],
    },
}
BIN_CLASS = {"III": "C2", "II": "C2", "I": "C1", "CMS": "CMS", "MS": "MS"}
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


# free slots carry the annual spread; the Clean/Jerk slot is shaped by the
# pair rule instead (its singles still host via the fit, but with no quota)
FREE_SLOTS = (DAY[0], DAY[2], DAY[3], DAY[4])
EPS = 0.01  # soft weight for a non-target host day
BOUNDARY = 0.001  # even softer: first day after a group trained last week

# week table columns
DISPLAY_ZONES = [50, 60, 70, 80, 90, 100, 110]
