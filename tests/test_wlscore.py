import json
import subprocess
import sys

import wlgen
from wlgen import build_plan, ir_with_slots, to_html
from wlir import from_ir, to_ir
from wlscore import (
    _score_items,
    audit,
    generate_json,
    score_book,
    score_class,
    score_json,
)


def _plan(cls="III"):
    """A restored plan from minimal JSON, the scorer's whole input."""
    return from_ir(to_ir(ir_with_slots(build_plan(cls))))


def _copy_week(plan, mi=0, wi=0):
    import copy

    return copy.deepcopy(plan["mesos"][mi]["weeks"][wi])


def test_ir_round_trip():
    plan = _plan()
    ir = to_ir(plan)
    json.loads(json.dumps(ir))  # plain JSON types only
    assert from_ir(json.loads(json.dumps(ir))) == plan


def test_html_from_ir_matches():
    plan = _plan()
    assert to_html(from_ir(to_ir(plan))) == to_html(plan)


def test_outputs_html_comes_from_json(tmp_path):
    import json

    from wlgen import write_outputs

    write_outputs(path=str(tmp_path), jobs=1)
    for cls in ("III",):
        ir = json.loads((tmp_path / f"{cls}.json").read_text())
        assert (tmp_path / f"{cls}.html").read_text() == to_html(from_ir(ir))


def test_ir_scores_like_build():
    plan = _plan()
    assert score_json(to_ir(plan))["score"] == score_class("III")["score"]


def _sess(day, vol):
    return {"day": day, "vol": vol}


def test_wave_rhythm_rewards_his_shape():
    from wlscore import _week_rhythm

    # his Class 3 week: Mon 83, Wed 51, Fri 63, rest days zero
    r = _week_rhythm([_sess(0, 83), _sess(2, 51), _sess(4, 63)])
    assert r["total"] < 0.5, r


def test_wave_rhythm_leaves_multi_peak_free():
    from wlscore import _week_rhythm

    # his Class 2 week: two peaks over seven days with zeros
    r = _week_rhythm([_sess(0, 69), _sess(1, 110), _sess(3, 47), _sess(5, 88)])
    assert r["total"] < 0.5, r


def test_wave_rhythm_likes_work_rest_waves():
    from wlscore import _week_rhythm

    # three equal days with rest between: clear rhythm, no shortfall
    r = _week_rhythm([_sess(0, 60), _sess(2, 60), _sess(4, 60)])
    assert r["total"] == 0, r


def test_wave_rhythm_punishes_flat_weeks():
    from wlscore import _week_rhythm

    # six equal days and one rest: no wave, pays the shortfall
    r = _week_rhythm([_sess(d, 60) for d in range(6)])
    assert r["total"] > 0.4, r


def _intensity_plan(zones):
    """One meso of single-session weeks at the given mean zones."""
    from wlconfig import BIN_GROUP, BIN_ZONES

    plan = {"mesos": []}
    weeks = []
    for z in zones:
        grid = BIN_ZONES[BIN_GROUP["Squat"]]
        idx = min(range(len(grid)), key=lambda i: abs(grid[i] - z))
        vec = [0] * len(grid)
        vec[idx] = 10
        weeks.append({"sessions": [{"day": 0, "vol": 10, "movements": {"Squat": vec}, "pairs": {}}]})
    plan["mesos"].append({"weeks": weeks})
    return plan


def test_intensity_wave_rewards_buildup():
    from wlscore import _intensity_shortfall

    # rises into a comp peak, meet week dropped: contains a wave
    plan = _intensity_plan([68, 70, 72, 74, 76, 78, 76, 70])
    assert _intensity_shortfall(plan) == 0


def test_intensity_wave_punishes_flat():
    from wlscore import _intensity_shortfall

    plan = _intensity_plan([72] * 8)
    assert _intensity_shortfall(plan) > 0.9


def _rest_week(vols_by_day):
    return {"sessions": [
        {"day": d, "vol": v} for d, v in sorted(vols_by_day.items()) if v
    ]}


def test_rest_corr_rewards_heavy_after_rest():
    from wlscore import _week_rest_corr

    # heavy Monday after the weekend gap, light midweek after short gaps
    assert _week_rest_corr(_rest_week({0: 100, 2: 40, 4: 40})) > 0.9


def test_rest_corr_punishes_heavy_after_short_rest():
    from wlscore import _week_rest_corr

    # light Monday after the weekend, heavy midweek after one rest day
    assert _week_rest_corr(_rest_week({0: 40, 2: 100, 4: 100})) < -0.9


def test_rest_corr_abstains_on_flat_weeks():
    from wlscore import _week_rest_corr

    assert _week_rest_corr(_rest_week({0: 60, 2: 60, 4: 60})) is None


def test_per_session_floor_passes_light_heavy_light():
    from wlscore import RHYTHM_FLOOR, _week_rhythm

    r = _week_rhythm([{"day": 0, "vol": 60}, {"day": 2, "vol": 60}, {"day": 4, "vol": 60}])
    assert r["shortfall"] == 0


def test_per_session_floor_fails_flat_block():
    from wlscore import RHYTHM_FLOOR, _week_rhythm

    r = _week_rhythm([{"day": d, "vol": 60} for d in range(6)])
    assert r["shortfall"] > 0.4


def test_wave_rhythm_needs_days():
    import pytest

    from wlscore import _week_rhythm

    with pytest.raises(ValueError):
        _week_rhythm([{"vol": 60}])


def test_shipped_scores_clean():
    for cls in ("III", "II", "I", "CMS", "MS"):
        raw = _score_items([(cls, _plan(cls))])
        assert raw["illegal"] == 0, cls
        assert raw["clash"] == 0, cls
        assert raw["gaps"] == {"III": 0, "II": 0, "I": 0, "CMS": 0, "MS": 0}[cls], cls
        # taper slack plus phase peak (2026-10-26): fewer soft openers;
        # walled shift (2026-10-31): heat pools at 90, pricing a few more
        # low-class 90-openers the books prescribe; dead-pair removal
        # (2026-10-31): variant-fusion soft openers gone (I/CMS/MS down)
        assert (
            raw["soft"]
            == {"III": 6.0, "II": 26.0, "I": 24.0, "CMS": 16.0, "MS": 24.0}[cls]
        ), cls
        assert raw["idle"] == 0, cls
        assert raw["idle_meso"] == 0, cls
        assert raw["ob_micro"] == 0, cls
        assert raw["iv_micro"] == 0, cls
        for key in ("strain", "size", "rhythm", "drift", "score"):
            assert score_class(cls)[key] >= 0, (cls, key)


def test_book_numbers_match_research():
    book = score_book()
    # Walled shift (2026-10-31): no invented 100s, heat pools at 90.
    # Excess falls (less over-capacity stacking); instructions fall with
    # fewer top fragments; soft redistributes toward prescribed 90s.
    # Dead pairs (2026-10-31): fusion gone, mass re-hosts solo/paired;
    # soft falls (fewer variant soft openers), one squat slot grows
    # 30->33 sets (marathon class pre-exists; pairing reshape lands here).
    assert round(book["excess"], 1) == 188.6
    # phase peak starves a few thin tops just under the floor
    assert book["shortfall"] < 0.2
    assert book["instructions"] == 9325
    assert book["slots"] == 1428
    assert book["longest"] == 33


def test_score_detects_gap():
    plan = _plan()
    week = _copy_week(plan)
    target = None
    for s in week["sessions"]:
        for g, counts in s["movements"].items():
            used = [z for z, n in enumerate(counts) if n]
            if len(used) >= 3:
                target = (s, g, used[len(used) // 2])
                break
        if target:
            break
    assert target, "no multi-zone cell to break"
    s, g, z = target
    s["movements"][g][z] = 0
    week["bins"][g][z] = sum(
        t["movements"].get(g, [0] * len(s["movements"][g]))[z] for t in week["sessions"]
    )
    plan["mesos"][0]["weeks"][0] = week
    assert score_class("III", plan)["gaps"] >= 1


def test_score_detects_idle():
    plan = _plan()
    week = _copy_week(plan)
    grown = None
    for g in wlgen.GROUPS:
        if week["groups"].get(g, 0) <= 0:
            continue
        hosted = sum(sum(s["movements"].get(g, [])) for s in week["sessions"])
        if hosted > 0:
            grown = g
            break
    assert grown, "no hosted group to idle"
    for s in week["sessions"]:
        if grown in s["movements"]:
            s["movements"][grown] = [0] * len(s["movements"][grown])
    week["bins"][grown] = [0] * len(week["bins"][grown])
    plan["mesos"][0]["weeks"][0] = week
    assert score_class("III", plan)["idle"] >= 1


def test_score_detects_clash():
    import itertools

    from wlgen import slot_match

    clash = next(
        (
            set(p)
            for p in itertools.combinations(wlgen.GROUPS, 2)
            if not slot_match(set(p))
        ),
        None,
    )
    assert clash, "no clashing pair found"
    plan = _plan()
    week = _copy_week(plan)
    s = week["sessions"][0]
    nz = max(len(v) for v in s["movements"].values())
    for g in clash:
        s["movements"][g] = [6] + [0] * (nz - 1)
    plan["mesos"][0]["weeks"][0] = week
    assert score_class("III", plan)["clash"] >= 1


def test_audit_runs():
    assert audit(["III"]) >= 0


def test_missing_slots_raises():
    import pytest

    with pytest.raises(ValueError, match="slots"):
        score_json(to_ir(build_plan("III")))


def test_generate_json_writes_scorable_files(tmp_path):
    paths = generate_json(tmp_path, classes=["III"], jobs=1)
    assert [p.name for p in paths] == ["III.json"]
    scored = score_json(paths[0])
    assert scored["score"] == score_class("III")["score"]
    assert scored["score"] >= 0
    assert scored["pace"] == 0


def test_score_needs_no_generator(tmp_path):
    generate_json(tmp_path, classes=["III"], jobs=1)
    code = (
        "import sys; sys.modules['wlgen'] = None;"
        "sys.path.insert(0, 'src');"
        f"from wlscore import score_json;"
        f"print(score_json({str(tmp_path / 'III.json')!r})['score'])"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, cwd="."
    )
    assert proc.returncode == 0, proc.stderr
    assert float(proc.stdout.strip()) == score_class("III")["score"]


def test_pace_is_zero_without_cpu():
    assert score_class("III")["pace"] == 0


def test_pace_prices_ratio():
    from wlscore import CPU_BOOK

    plan = _plan()
    assert score_class("III", plan, cpu=CPU_BOOK)["pace"] == 0
    assert score_class("III", plan, cpu=2 * CPU_BOOK)["pace"] == 3
    assert score_class("III", plan, cpu=CPU_BOOK / 2)["pace"] == -0.75


def test_entry_problems_allows_clean_ramp():
    from wlscore import _entry_problems

    session = {"movements": {"Squat": [0, 0, 0, 0, 0]}, "pairs": {}}
    seq = ((50, 5), (60, 5), (70, 4), (80, 3), (90, 2))
    assert _entry_problems("Squat", seq, [], session) == []


def test_bin_gaps_counts_interior_holes():
    from wlscore import _bin_gaps

    assert _bin_gaps({"Squat": [5, 0, 3]}) == 1
    assert _bin_gaps({"Squat": [5, 3]}) == 0
    assert _bin_gaps({"Squat": [5, 0, 0]}) == 0
    assert _bin_gaps({"Squat": [0, 0, 0]}) == 0


def test_entry_problems_allows_peaked_backoff():
    from wlscore import _entry_problems

    # Takano's shape: singles to a peak, then volume below it
    session = {"movements": {"Squat": [0] * 5}, "pairs": {}}
    seq = ((60, 1), (70, 1), (80, 1), (90, 1), (80, 3), (80, 3))
    assert _entry_problems("Squat", seq, [], session) == []


def test_entry_problems_allows_climb_rise():
    from wlscore import _entry_problems

    # Takano ramps 50/2 into 60/3; caps (not order) bound the climb
    session = {"movements": {"Squat": [0, 0, 0, 0, 0]}, "pairs": {}}
    assert _entry_problems("Squat", ((50, 2), (60, 3)), [], session) == []


def test_entry_problems_flags_flat_total_flip():
    from wlscore import _entry_problems

    # 1+2 -> 2+1 flips sides on a flat total; a rising total is free
    session = {
        "movements": {"Clean": [0] * 5, "Jerk": [0] * 5},
        "pairs": {("Clean", "Jerk"): ("Clean", (0,) * 5, (0,) * 5)},
    }
    seq = ((70, (1, 2)), (80, (2, 1)))
    problems = _entry_problems("Clean+Jerk", seq, [], session)
    assert problems == ["Clean+Jerk: illegal order at 80%"], problems
    seq2 = ((70, (1, 1)), (80, (2, 1)))
    assert _entry_problems("Clean+Jerk", seq2, [], session) == []


def test_entry_problems_allows_flat_waves():
    from wlscore import _entry_problems

    session = {"movements": {"Squat": [0, 0, 0, 0, 0]}, "pairs": {}}
    seq = ((60, 2), (70, 2), (70, 2), (80, 2), (80, 2))
    assert _entry_problems("Squat", seq, [], session) == []


def test_entry_problems_ignores_hard_opener():
    from wlscore import _entry_problems

    # openers are soft-priced now, never a defect
    session = {"movements": {"Squat": [0, 0, 0, 0, 0]}, "pairs": {}}
    assert _entry_problems("Squat", ((50, 12), (60, 7)), [], session) == []


def test_soft_opener_prices_excess_reps():
    from wlscore import _soft_opener

    assert _soft_opener([]) == 0
    assert _soft_opener([(50, 5)]) == 0
    assert _soft_opener([(50, 12), (60, 7)]) == 7
    assert _soft_opener([(80, (2, 1))]) == 0


def test_precomp_phase_scores_as_competition_period():
    from wlscore import _nominal

    # Takano headers name three phases; ours knows two. Pre-competition
    # belongs to the competition period, so it shares comp ratios.
    assert _nominal("III", "precomp", 100) == _nominal("III", "comp", 100)
