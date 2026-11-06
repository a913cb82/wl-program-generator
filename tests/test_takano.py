"""Takano programs in our JSON format: exercise map, zone floor,
X-zone inference and scheme parsing. Every non-obvious decision from
the mapping review is pinned here."""

from takano import (
    EXERCISE_MAP,
    _week_phase,
    build_session,
    floor_zone,
    infer_x_zone,
    parse_scheme,
    split_complex,
)


def test_map_covers_every_raw_name():
    from wlconfig import GROUPS

    valid = set(GROUPS) | {"drop"}
    for raw, mapped in EXERCISE_MAP.items():
        assert isinstance(raw, str) and raw, raw
        if mapped == "drop":
            continue
        kind = mapped[0]
        assert kind in ("single", "pair", "triple"), (raw, mapped)
        for g in mapped[1]:
            assert g in valid, (raw, mapped)


def test_map_complexes_are_pairs():
    assert EXERCISE_MAP["Clean & Jerk"] == ("pair", ("Clean", "Jerk"))
    assert EXERCISE_MAP["Power Clean & Power Jerk"] == (
        "pair",
        ("Other Clean", "Other Jerk"),
    )
    assert EXERCISE_MAP["Power Clean & Jerk"] == ("pair", ("Other Clean", "Jerk"))
    assert EXERCISE_MAP["Snatch High Pull & Snatch"] == ("pair", ("SnPull", "Snatch"))
    assert EXERCISE_MAP["Clean High Pull & Clean"] == ("pair", ("ClPull", "Clean"))
    assert EXERCISE_MAP["Power Clean & Front Squat & Jerk"] == (
        "triple",
        ("Other Clean", "Other Squat", "Jerk"),
    )


def test_map_review_decisions():
    # extension == pull
    assert EXERCISE_MAP["Clean Extension"] == ("single", ("ClPull",))
    assert EXERCISE_MAP["Snatch Extension"] == ("single", ("SnPull",))
    # behind the neck / rack
    assert EXERCISE_MAP["Behind the Neck Power Jerk"] == ("single", ("Other Jerk",))
    assert EXERCISE_MAP["Jerk off Rack"] == ("single", ("Jerk",))
    assert EXERCISE_MAP["Behind the Neck Push Press"] == ("single", ("Press",))
    # power jerk
    assert EXERCISE_MAP["Power Jerk"] == ("single", ("Other Jerk",))
    # squat variants incl. jumping
    assert EXERCISE_MAP["Overhead Squat"] == ("single", ("Other Squat",))
    assert EXERCISE_MAP["Jumping Back Squat"] == ("single", ("Other Squat",))
    # press bucket incl. bench
    assert EXERCISE_MAP["Push Press"] == ("single", ("Press",))
    assert EXERCISE_MAP["Bench Press"] == ("single", ("Press",))
    # hinge bucket
    assert EXERCISE_MAP["Good Morning"] == ("single", ("Fundamental",))
    assert EXERCISE_MAP["Romanian Deadlift"] == ("single", ("Fundamental",))
    # lunges drop
    assert EXERCISE_MAP["Lunge"] == "drop"


def test_floor_zone_rounds_down():
    assert floor_zone(65, [60, 70, 80, 90, 100]) == 60
    assert floor_zone(75, [60, 70, 80, 90, 100]) == 70
    assert floor_zone(85, [60, 70, 80, 90, 100]) == 80
    assert floor_zone(95, [60, 70, 80, 90, 100]) == 90
    assert floor_zone(105, [60, 70, 80, 90, 100]) == 100
    assert floor_zone(110, [50, 60, 70, 80, 90, 100, 110]) == 110
    assert floor_zone(50, [60, 70, 80, 90, 100]) == 60
    assert floor_zone(95, [50, 60, 70, 80, 90]) == 90


def test_infer_x_zone_by_reps():
    assert infer_x_zone(8) == 75
    assert infer_x_zone(7) == 75
    assert infer_x_zone(6) == 80
    assert infer_x_zone(4) == 85
    assert infer_x_zone(3) == 85
    assert infer_x_zone(2) == 90
    assert infer_x_zone(1) == 90


def test_parse_single_sets():
    assert parse_scheme("50%/3, 60%/3, (70%/2)2", False) == [
        (50, 3),
        (60, 3),
        (70, 2),
        (70, 2),
    ]


def test_parse_single_plus_is_consecutive_sets():
    assert parse_scheme("60%/2+1", False) == [(60, 2), (60, 1)]
    assert parse_scheme("60%/3+3", False) == [(60, 3), (60, 3)]


def test_parse_complex_plus_is_per_side():
    assert parse_scheme("60%/2+1", True) == [(60, [2, 1])]
    assert parse_scheme("(80%/2+1)2", True) == [(80, [2, 1]), (80, [2, 1])]


def test_parse_x_zone_uses_rep_inference():
    assert parse_scheme("(X/4)4", False) == [(85, 4)] * 4
    assert parse_scheme("(X/7)2", False) == [(75, 7)] * 2


def test_parse_strips_tallies_and_strays():
    assert parse_scheme("50%/3, 60%/3, 65%/2, (70%/2)2   13:13:13", False) == [
        (50, 3),
        (60, 3),
        (65, 2),
        (70, 2),
        (70, 2),
    ]
    assert parse_scheme("(75%/3)2  18:18::87", False) == [(75, 3)] * 2
    assert parse_scheme("85%/2 80%/3", False) == [(85, 2), (80, 3)]


def test_parse_repairs_unbalanced_parens():
    assert parse_scheme("(85%/2+1", True) == [(85, [2, 1])]
    assert parse_scheme("90%/1+1)3", True) == [(90, [1, 1])] * 3


def test_parse_max_singles():
    assert parse_scheme("95%+/1", False) == [(95, 1)]
    assert parse_scheme("max-5", False) == [(90, 1)]
    assert parse_scheme("max (90%/2)3", False) == [(90, 1)] + [(90, 2)] * 3
    assert parse_scheme("singles to max, (max-10, max-5, max)3", False) == [(90, 1)] * 9
    assert parse_scheme("(max-10, max-5, max03", False) == [(90, 1)] * 3


def test_parse_added_kg_strips_to_base():
    assert parse_scheme("(100%+10 Kg/4)5", False) == [(100, 4)] * 5
    assert parse_scheme("(105% + 10 Kg/2)6", False) == [(105, 2)] * 6


def test_split_complex_prefers_known_pair():
    assert split_complex(("Other Clean", "Other Squat", "Jerk")) == (
        ("Other Clean", "Jerk"),
        ("Other Squat",),
    )


def test_build_session_produces_schema_json(tmp_path):
    session = build_session(
        [
            "1) Snatch: 50%/3, 60%/3, (70%/2)2   13:13:13",
            "2) Clean & Jerk: 60%/2+1   15:15:98",
            "3) Back Squat: (80%/3)2   12:27:110",
        ],
        0,
    )
    assert session["day"] == 0
    # his 50% warmups fold to the 60 base, like below-range maps below
    assert session["movements"]["Snatch"] == [6, 4, 0, 0, 0]
    assert session["movements"]["Squat"] == [0, 0, 0, 6, 0]
    assert session["movements"]["Clean"] == [2, 0, 0, 0, 0]
    assert session["movements"]["Jerk"] == [1, 0, 0, 0, 0]
    key = ("Clean", "Jerk")
    assert session["pairs"][key][0] == "Clean"
    assert list(session["pairs"][key][1]) == session["movements"]["Clean"]
    assert list(session["pairs"][key][2]) == session["movements"]["Jerk"]
    by_move = {sl["movement"]: sl["seq"] for sl in session["slots"]}
    assert by_move["Snatch"] == [[60, 3], [60, 3], [70, 2], [70, 2]]
    assert by_move["Clean+Jerk"] == [[60, [2, 1]]]
    assert by_move["Squat"] == [[80, 3], [80, 3]]


def _load_fixture(cls):
    import json

    from wlir import from_ir

    with open(f"tests/fixtures/takano-{cls}.json") as f:
        return from_ir(json.load(f))


def test_fixtures_load_all_sessions():
    # the I key lumps four book programs; each loads fully into our grid.
    # AM/PM split (2026-11-01): MS 83 days -> 117 sessions (+34 split
    # days), MSIC 95 days -> 133 sessions (+37 split days + 1 implicit
    # morning block); III/II/I/CMS have no markers, counts unchanged.
    counts = {"III": 26, "II": 29, "I": 50, "CMS": 55, "MS": 117, "MSIC": 133}
    for cls, want in counts.items():
        got = sum(
            len(w["sessions"]) for m in _load_fixture(cls)["mesos"] for w in m["weeks"]
        )
        assert got == want, (cls, got)


def test_fixtures_render_and_score():
    from wlgen import to_html
    from wlscore import _score_items

    # illegal/gaps/soft are his genuine rule breaks under our
    # movement rules; clash/idle are grid artifacts (empty weeks past his
    # shorter programs, his day mixes predate our templates). Removing
    # pairs neither book programs raises clash by the sessions that
    # co-hosted them.
    # AM/PM split (2026-11-01): illegal/soft/idle pin the dose and are
    # unchanged (halves sum to the same day movements); clash rises
    # (per-session slot_match over more sessions: MS 38->44, MSIC 52->55)
    # and gaps fall to zero (the five whole-day gap sessions — MS day0
    # vol148, day4 vol115, day3 vol106; MSIC (m0,w1,d4) vol104 and
    # (m0,w5,d4) vol129 — split into halves with no unjustified holes).
    pins = {
        "III": {"illegal": 6, "clash": 12, "idle": 5, "gaps": 0, "soft": 9.0},
        "II": {"illegal": 14, "clash": 15, "idle": 6, "gaps": 0, "soft": 6.0},
        "I": {"illegal": 47, "clash": 24, "idle": 7, "gaps": 0, "soft": 13.0},
        "CMS": {"illegal": 71, "clash": 21, "idle": 4, "gaps": 2, "soft": 15.0},
        "MS": {"illegal": 109, "clash": 44, "idle": 9, "gaps": 0, "soft": 36.0},
        "MSIC": {
            "illegal": 126,
            "clash": 55,
            "idle": 10,
            "gaps": 0,
            "soft": 45.0,
        },
    }
    for cls, pin in pins.items():
        plan = _load_fixture(cls)
        html = to_html(plan)
        assert "Training Plan" in html
        raw = _score_items([(plan["class"], plan)])
        for key, value in pin.items():
            assert raw[key] == value, (cls, key)


def test_adjacent_paren_groups_are_not_one_wave():
    # III w1 Tue: "(70%/4)2 (75%/4)2" is two waves, not one wave x2
    assert parse_scheme("(70%/4)2 (75%/4)2", False) == [(70, 4)] * 2 + [(75, 4)] * 2
    assert (
        parse_scheme("60%/4, (70%/4)2 (75%/4)3", False)
        == [(60, 4)] + [(70, 4)] * 2 + [(75, 4)] * 3
    )


def test_absurd_reps_drop_loudly():
    # II w4 Mon: "(70%/302" is a corrupted paren, not a 302-rep set
    assert parse_scheme("60%/3, 65%/3, (70%/302", False) == [(60, 3), (65, 3)]


def test_stray_trailing_token_keeps_valid_group():
    # I w26 Fri: "(X/5)4 2" keeps its 4 sets, drops the stray
    assert parse_scheme("(X/5)4 2", False) == [(80, 5)] * 4


def test_transposed_comma_repairs():
    # I w33 Thu: "60%/,2" is OCR for "60%/2", backed by its tally
    assert parse_scheme("60%/,2 65%/2", False) == [(60, 2), (65, 2)]


def test_spurious_colon_in_name_still_maps():
    # III w7 Thu: "Snatch: Extension:" is the Snatch Extension exercise
    session = build_session(["3) Snatch: Extension: (80%/2)4"], 3)
    assert session["movements"].get("SnPull") == [8, 0, 0, 0]
    assert "Snatch" not in session["movements"]


def test_semicolon_separator_maps_like_colon():
    # CMS w17 Thu: "3) Press; (X/3)4" uses a semicolon, backed by its tally
    session = build_session(["3) Press; (X/3)4"], 3)
    assert session["slots"] == [{"movement": "Press", "seq": [[80, 3]] * 4}]


def test_unspaced_number_and_colon_still_map():
    # II w34 Fri: "1)Power Snatch: 60%/3, ..." skips every space
    session = build_session(["1)Power Snatch:60%/2, 70%/2"], 4)
    assert session["slots"][0]["movement"] == "Other Snatch"
    assert session["slots"][0]["seq"] == [[60, 2], [70, 2]]


def test_colon_less_line_with_known_name_maps():
    # MS w8 Sat: halting deadlift line carries no colon at all
    session = build_session(["4) Halting Clean Deadlift with 2 halts (80%/3)5"], 5)
    assert session["slots"][0]["movement"] == "ClPull"
    assert session["slots"][0]["seq"] == [[80, 3]] * 5


def test_unbalanced_open_repeat_applies_to_whole_chunk():
    # I w57 Tue: "(60%/1+1, 70%/1+1, (75%/1+1)3" repeats all three groups
    assert (
        parse_scheme("(60%/1+1, 70%/1+1, (75%/1+1)3", True)
        == [
            (60, [1, 1]),
            (70, [1, 1]),
            (75, [1, 1]),
        ]
        * 3
    )
    assert parse_scheme("(60%/1+1", True) == [(60, [1, 1])]


def test_build_program_groups_phase_runs_into_mesos():
    from takano import build_program

    weeks = [
        {"n": 1, "meso": "Preparation", "plan": 100, "days": []},
        {"n": 2, "meso": "Preparation", "plan": 100, "days": []},
        {"n": 3, "meso": "Pre-competition", "plan": 100, "days": []},
    ]
    sessions, mesos = build_program(weeks)
    assert sessions == []
    assert [m["phase"] for m in mesos] == ["prep", "precomp"]
    assert [m["name"] for m in mesos] == ["Preparation 1-2", "Pre-competition 3-3"]


def test_macrocycle_header_phases_as_precompetition():
    # CMS week 9 reads 'Week 9 (Pre-competition Macrocycle)': the book
    # means a mesocycle, and the week must phase precomp, not inherit
    # prep. The parser tags Macrocycle headers as mesocycles; the phase
    # rule keys on the Pre-competition prefix.
    assert _week_phase("Pre-competition Macrocycle", "prep") == "precomp"
    plan = _load_fixture("CMS")
    names = [m["name"] for m in plan["mesos"]]
    assert names == ["Preparation 1-8", "Pre-competition 9-12"]
    import json

    with open("tests/fixtures/takano-CMS.json") as f:
        flat = json.load(f)
    ninths = [s for s in flat["sessions"] if (s["meso"], s["week"]) == (1, 0)]
    assert len(ninths) == 4 and {s["meso"] for s in ninths} == {1}


def test_build_session_defaults_to_whole_day():
    # no half given: whole-day session, the III/II/I/CMS shape
    session = build_session(["1) Back Squat: (80%/3)2"], 0)
    assert session["day"] == 0
    assert session["half"] is None


def test_build_session_carries_half():
    am = build_session(["1) Back Squat: (80%/3)2"], 0, "AM")
    pm = build_session(["4) Snatch: 60%/3, 70%/3"], 0, "PM")
    assert am["half"] == "AM"
    assert pm["half"] == "PM"
    assert am["day"] == pm["day"] == 0


def test_build_program_splits_day_into_half_sessions():
    from takano import build_program

    weeks = [
        {
            "n": 1,
            "meso": "Preparation",
            "plan": 148,
            "days": [
                {
                    "n": 1,
                    "plan": 148,
                    "weekday": "Monday",
                    "ex": ["1) Back Squat: (80%/3)2", "4) Snatch: 60%/3"],
                    "blocks": [
                        {"half": "AM", "ex": ["1) Back Squat: (80%/3)2"]},
                        {"half": "PM", "ex": ["4) Snatch: 60%/3"]},
                    ],
                },
            ],
        }
    ]
    sessions, _ = build_program(weeks)
    assert len(sessions) == 2
    assert [(s["day"], s["half"]) for s in sessions] == [(0, "AM"), (0, "PM")]
    # halves sum to the whole day: no dose created or lost
    whole = build_session(["1) Back Squat: (80%/3)2", "4) Snatch: 60%/3"], 0)
    for g, vec in whole["movements"].items():
        assert sum(sum(s["movements"].get(g, [0] * len(vec))) for s in sessions) == sum(
            vec
        )


def test_build_program_single_pm_day_is_one_pm_session():
    # MS week-1 Saturday: PM marker only, one session half=PM
    from takano import build_program

    weeks = [
        {
            "n": 1,
            "meso": "Preparation",
            "plan": 63,
            "days": [
                {
                    "n": 6,
                    "plan": 63,
                    "weekday": "Saturday",
                    "ex": ["1) Back Squat: (80%/2)3"],
                    "blocks": [{"half": "PM", "ex": ["1) Back Squat: (80%/2)3"]}],
                },
            ],
        }
    ]
    sessions, _ = build_program(weeks)
    assert len(sessions) == 1
    assert sessions[0]["half"] == "PM"


def _fixture_sessions(cls):
    import json

    with open(f"tests/fixtures/takano-{cls}.json") as f:
        return json.load(f)["sessions"]


def test_ms_week_one_is_nine_half_sessions():
    # MS week 1: 6 days -> 9 sessions (Mon/We/Fri split, Sat PM-only)
    got = [
        (s["day"], s["half"])
        for s in _fixture_sessions("MS")
        if (s["meso"], s["week"]) == (0, 0)
    ]
    assert got == [
        (0, "AM"),
        (0, "PM"),
        (1, "AM"),
        (2, "AM"),
        (2, "PM"),
        (3, "AM"),
        (4, "AM"),
        (4, "PM"),
        (5, "PM"),
    ]


def test_ims_day_three_leading_block_is_am():
    # MSIC week 1 Wednesday: exercises precede a mid-day PM marker, so
    # the leading block is the implicit morning session (day vol 156)
    got = [
        (s["day"], s["half"])
        for s in _fixture_sessions("MSIC")
        if (s["meso"], s["week"]) == (0, 0)
    ]
    wed = [h for d, h in got if d == 2]
    assert wed == ["AM", "PM"]


def test_fixture_session_keys_unique_and_halves_sum_to_days():
    import json

    from wlir import from_ir

    for cls in ("III", "II", "I", "CMS", "MS", "MSIC"):
        with open(f"tests/fixtures/takano-{cls}.json") as f:
            ir = json.load(f)
        keys = [(s["meso"], s["week"], s["day"], s["half"]) for s in ir["sessions"]]
        assert len(set(keys)) == len(keys), cls
        assert {s["half"] for s in ir["sessions"]} <= {None, "AM", "PM"}, cls
        # halves sum to whole-day volumes: fixture day totals match the
        # restored plan's day totals session for session
        want = {}
        for s in ir["sessions"]:
            want.setdefault((s["meso"], s["week"], s["day"]), 0)
            want[(s["meso"], s["week"], s["day"])] += sum(
                sum(v) for v in s["movements"].values()
            )
        plan = from_ir(ir)
        got = {}
        for mi, m in enumerate(plan["mesos"]):
            for wi, w in enumerate(m["weeks"]):
                for s in w["sessions"]:
                    got.setdefault((mi, wi, s["day"]), 0)
                    got[(mi, wi, s["day"])] += s["vol"]
        assert got == want, cls
    halves = {}
    for s in _fixture_sessions("MS"):
        if (s["meso"], s["week"]) == (0, 0) and s["day"] == 0:
            halves[s["half"]] = sum(sum(v) for v in s["movements"].values())
    assert halves == {"AM": 52, "PM": 96}  # day plan 148
