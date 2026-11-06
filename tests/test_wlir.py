"""from_ir/to_ir accept any program shape, not just our 5x4 macro.

A stored "mesos" list (name + phase per mesocycle) drives the rebuild:
weeks come from the sessions themselves, never from a fixed grid.
Without it, from_ir keeps the legacy class-macro behavior verbatim.
"""

import sys

sys.path.insert(0, "src")

from wlgen import build_plan, ir_with_slots
from wlir import from_ir, to_ir


def _session(meso, week, day, lifts=6):
    sets = lifts // 3
    return {
        "meso": meso,
        "week": week,
        "day": day,
        "movements": {"Squat": [0, 0, 0, lifts, 0]},
        "pairs": {},
        "slots": [{"movement": "Squat", "seq": [[80, 3]] * sets}],
    }


def test_from_ir_uses_stored_meso_shape():
    ir = {
        "class": "III",
        "title": "Takano Class III",
        "mesos": [
            {"name": "Preparation 1-3", "phase": "prep"},
            {"name": "Pre-competition 4-8", "phase": "precomp"},
        ],
        "sessions": [
            _session(0, 0, 0),
            _session(0, 1, 0),
            _session(0, 2, 0),
            _session(1, 0, 0),
            _session(1, 1, 0),
            _session(1, 2, 0),
            _session(1, 3, 0),
            _session(1, 4, 0),
        ],
    }
    plan = from_ir(ir)
    assert [len(m["weeks"]) for m in plan["mesos"]] == [3, 5]
    assert [m["name"] for m in plan["mesos"]] == [
        "Preparation 1-3",
        "Pre-competition 4-8",
    ]
    assert [m["phase"] for m in plan["mesos"]] == ["prep", "precomp"]
    assert plan["macro"] == "Takano Class III"


def test_from_ir_derives_volumes_from_sessions():
    ir = {
        "class": "III",
        "title": "Takano Class III",
        "mesos": [{"name": "Preparation 1-2", "phase": "prep"}],
        "sessions": [_session(0, 0, 0, lifts=6), _session(0, 1, 0, lifts=12)],
    }
    plan = from_ir(ir)
    assert plan["mesos"][0]["weeks"][0]["vol"] == 6
    assert plan["mesos"][0]["weeks"][1]["vol"] == 12
    assert plan["mesos"][0]["vol"] == 18
    assert plan["annual"] == 18


def test_from_ir_without_metadata_keeps_macro_shape():
    ir = {"class": "III", "sessions": [_session(0, 0, 0)]}
    plan = from_ir(ir)
    assert [len(m["weeks"]) for m in plan["mesos"]] == [4, 4, 4, 4, 4]
    assert plan["macro"] == "Soviet year (III)"


def test_to_ir_stays_minimal():
    plan = {
        "class": "III",
        "macro": "Soviet year (III)",
        "mesos": [
            {
                "name": "Prep 1",
                "phase": "prep",
                "vol": 100,
                "weeks": [
                    {
                        "vol": 100,
                        "sessions": [
                            {
                                "day": 0,
                                "movements": {"Squat": [0, 0, 0, 6, 0]},
                                "pairs": {},
                                "slots": [
                                    {
                                        "movement": "Squat",
                                        "seq": [(80, 3), (80, 3)],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    }
    ir = to_ir(plan)
    assert set(ir.keys()) == {"class", "sessions"}
    back = from_ir(ir)
    assert [len(m["weeks"]) for m in back["mesos"]] == [4, 4, 4, 4, 4]
    assert back["macro"] == "Soviet year (III)"


def test_ir_carries_non_middle_bodyweight():
    plan = ir_with_slots(build_plan("MS", "heavy"))
    ir = to_ir(plan)
    assert ir["bw"] == "heavy"
    assert from_ir(ir)["bw"] == "heavy"
    assert from_ir(ir) == {**plan, "mesos": from_ir(ir)["mesos"]}
    middle = to_ir(ir_with_slots(build_plan("MS")))
    assert "bw" not in middle
    assert from_ir(middle)["bw"] == "middle"


def _half_session(meso, week, day, half, lifts=6):
    s = _session(meso, week, day, lifts)
    s["half"] = half
    return s


def json_round(ir):
    import json

    return json.loads(json.dumps(ir))


def test_half_round_trip_preserves_am_pm():
    ir = {
        "class": "III",
        "title": "Takano Class III",
        "mesos": [{"name": "Week", "phase": "prep"}],
        "sessions": [
            _half_session(0, 0, 0, "AM"),
            _half_session(0, 0, 0, "PM"),
            _half_session(0, 0, 2, None),
        ],
    }
    back = to_ir(from_ir(ir))
    assert [(s["day"], s["half"]) for s in back["sessions"]] == [
        (0, "AM"),
        (0, "PM"),
        (2, None),
    ]
    assert json_round(back) == back


def test_half_defaults_to_null():
    ir = {"class": "III", "sessions": [_session(0, 0, 0)]}
    assert to_ir(from_ir(ir))["sessions"][0]["half"] is None


def test_day_sums_halves():
    ir = {
        "class": "III",
        "mesos": [{"name": "Week", "phase": "prep"}],
        "sessions": [
            _half_session(0, 0, 0, "AM", lifts=6),
            _half_session(0, 0, 0, "PM", lifts=12),
        ],
    }
    plan = from_ir(ir)
    week = plan["mesos"][0]["weeks"][0]
    assert week["vol"] == 18
    assert len(week["sessions"]) == 2
