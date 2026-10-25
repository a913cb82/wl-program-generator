"""Overlapping sine waves for program rhythm, fitted to data.

Volume and intensity targets as sums of sines over the macrocycle day.
Magnitudes come from the Soviet source tables (the repo's first commit)
and Takano's programs; phases are per plan (the generator picks the peak
day) except where the tables pin them down. A fitted amplitude near zero
means the data drops that curve; the shape stays uniform so every scale
is priced by its evidence.

Scoring uses the floors, not the full stack: a plan must contain the
waves (fitted amplitudes above the floors), not follow any single
prediction. Generation will sample the full stack later.
"""

import math

MACRO_DAYS = 140

# (period in days, amplitude, phase in days or None for per-plan, source, R^2)
VOLUME = [
    # Soviet macro shares (5 mesos): single sine, R^2 0.88.
    {"period": 140, "amplitude": 0.226, "phase": 20},
    # Takano training days (312): weak weekday wave, R^2 <= 0.10 pooled.
    # Phase is per plan (peak day chosen at generation).
    {"period": 7, "amplitude": 0.13, "phase": None},
    # Sub-weekly ripple: no global phase pools across programs,
    # so the generator fits the phase per plan around this magnitude.
    {"period": 2.5, "amplitude": 0.20, "phase": None},
]

# Intensity moves at slow scales only: Takano day fits sit near zero
# (R^2 0.06-0.10), so only the annual curve survives. His Class III
# weekly mean zones climb into a comp peak then snap down for the meet.
INTENSITY = [
    {"period": 140, "amplitude": 0.042, "phase": 15},
]

# Strength (pull, squat, fundamental) deviation from the base annual
# curves. Soviet prep/comp group ratios move barely a point
# (amplitude 0.0086, R^2 0.37): the prior holds, levels differ little.
STRENGTH_VOLUME_DEV = [
    {"period": 140, "amplitude": 0.0086, "phase": 5},
]

# Strength intensity runs about five zone points hotter than competition
# lifts through the whole program, a flat offset rather than a wave.
STRENGTH_INTENSITY_OFFSET = 5.0

# Intensity wave floor for scoring: his ex-taper programs fit annual
# amplitudes 0.028-0.041; our plans fit 0.002-0.012 with no wave at all.
# Peak placed at 0.85 of plan length (his week 7 of 8, our week 17 of 20).
INTENSITY_WAVE_FLOOR = 0.02
INTENSITY_WAVE_PEAK = 0.85


def level(day, waves):
    """Multiplier (or relative shift) at a macrocycle day: one plus the
    sum of the sines. Phases fixed to None are skipped here; the caller
    supplies them per plan."""
    total = 0.0
    for w in waves:
        if w["phase"] is None:
            continue
        total += w["amplitude"] * math.sin(
            2 * math.pi * (day - w["phase"]) / w["period"]
        )
    return 1.0 + total


def fit_amplitude(fracs, values):
    """Annual-wave amplitude of weekly values at plan-relative positions:
    least squares against a sine peaking at INTENSITY_WAVE_PEAK."""
    mean = sum(values) / len(values)
    if mean == 0:
        return 0.0
    y = [v / mean - 1 for v in values]
    x = [math.sin(2 * math.pi * (f - (INTENSITY_WAVE_PEAK - 0.25))) for f in fracs]
    return sum(a * b for a, b in zip(x, y)) / (sum(a * a for a in x) or 1e-12)
