"""Layering guard: the zone-gap helper lives in wlconfig (shared)."""

import wlconfig
import wlscore


def test_gap_helper_lives_in_shared_config():
    assert callable(getattr(wlconfig, "_unjustified_gaps", None))


def test_scorer_reuses_shared_gap_helper():
    assert wlscore._unjustified_gaps is wlconfig._unjustified_gaps


def test_shared_helper_matches_scorer_semantics():
    session = {"movements": {"A": [0, 5, 0, 7, 0]}, "pairs": {}}
    sessions = [session]
    week_bins = {"A": [0, 1, 1, 1, 0]}
    assert wlconfig._unjustified_gaps(session, sessions, week_bins) == 1
