"""Tests for the fitted wave model. Magnitudes are pinned to the fits
in /tmp/fit_waves.py and /tmp/fit_days.py; refit if the data changes."""

import math

from wlwaves import (
    INTENSITY,
    INTENSITY_WAVE_FLOOR,
    INTENSITY_WAVE_PEAK,
    STRENGTH_INTENSITY_OFFSET,
    STRENGTH_VOLUME_DEV,
    VOLUME,
    fit_amplitude,
    level,
)


def test_annual_volume_magnitude_matches_soviet_fit():
    assert VOLUME[0]["period"] == 140
    assert abs(VOLUME[0]["amplitude"] - 0.226) < 0.01


def test_level_averages_one_over_full_periods():
    waves = [w for w in VOLUME if w["phase"] is not None]
    total = sum(level(d, waves) for d in range(140)) / 140
    assert abs(total - 1.0) < 0.01


def test_level_skips_per_plan_phases():
    waves = [{"period": 7, "amplitude": 0.13, "phase": None}]
    assert level(0, waves) == 1.0


def test_fit_amplitude_recovers_known_wave():
    fracs = [(i + 0.5) / 20 for i in range(19)]
    peak = INTENSITY_WAVE_PEAK
    vals = [
        72 * (1 + 0.03 * math.sin(2 * math.pi * (f - (peak - 0.25)))) for f in fracs
    ]
    assert abs(fit_amplitude(fracs, vals) - 0.03) < 0.005


def test_fit_amplitude_near_zero_for_flat_weeks():
    fracs = [(i + 0.5) / 20 for i in range(19)]
    assert abs(fit_amplitude(fracs, [72.0] * 19)) < 0.005


def test_intensity_floor_sits_below_his_wave():
    # his ex-taper programs fit 0.028-0.041; our plans fit 0.002-0.012
    assert INTENSITY_WAVE_FLOOR == 0.02


def test_strength_deviation_is_tiny():
    assert abs(STRENGTH_VOLUME_DEV[0]["amplitude"] - 0.0086) < 0.002
    assert STRENGTH_INTENSITY_OFFSET == 5.0
    assert len(INTENSITY) == 1  # slow scales only; fast curves fit ~0
