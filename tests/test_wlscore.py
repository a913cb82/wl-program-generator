import json

import wlgen
from wlgen import build_plan, from_ir, to_html, to_ir
from wlscore import _score_items, audit, score_book, score_class, score_ir


def _copy_week(plan, mi=0, wi=0):
    import copy

    return copy.deepcopy(plan["mesos"][mi]["weeks"][wi])


def test_ir_round_trip():
    plan = build_plan("III")
    ir = to_ir(plan)
    json.loads(json.dumps(ir))  # plain JSON types only
    assert from_ir(json.loads(json.dumps(ir))) == plan


def test_html_from_ir_matches():
    plan = build_plan("III")
    assert to_html(from_ir(to_ir(plan))) == to_html(plan)


def test_outputs_html_comes_from_json(tmp_path):
    import json

    from wlgen import write_outputs

    write_outputs(path=str(tmp_path), jobs=1)
    for cls in ("III",):
        ir = json.loads((tmp_path / f"{cls}.json").read_text())
        assert (tmp_path / f"{cls}.html").read_text() == to_html(from_ir(ir))


def test_ir_scores_like_build():
    plan = build_plan("III")
    assert score_ir(to_ir(plan))["score"] == score_class("III")["score"]


def test_shipped_scores_clean():
    for cls in ("III", "II", "I", "CMS", "MS"):
        raw = _score_items([(cls, build_plan(cls))])
        assert raw["illegal"] == 0, cls
        assert raw["clash"] == 0, cls
        assert raw["gaps"] == 0, cls
        assert raw["idle"] == 0, cls
        assert raw["idle_meso"] == 0, cls
        assert raw["ob_micro"] == 0, cls
        assert raw["iv_micro"] == 0, cls
        for key in ("strain", "size", "rhythm", "drift", "score"):
            assert score_class(cls)[key] >= 0, (cls, key)


def test_book_numbers_match_research():
    book = score_book()
    assert round(book["excess"], 1) == 153.4
    # one hosted cell in the book lands just under the floor
    assert book["shortfall"] < 0.1
    assert book["instructions"] == 9312
    assert book["slots"] == 1291
    assert book["longest"] == 25


def test_score_detects_gap():
    plan = build_plan("III")
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
    plan = build_plan("III")
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
    plan = build_plan("III")
    week = _copy_week(plan)
    s = week["sessions"][0]
    nz = max(len(v) for v in s["movements"].values())
    for g in clash:
        s["movements"][g] = [6] + [0] * (nz - 1)
    plan["mesos"][0]["weeks"][0] = week
    assert score_class("III", plan)["clash"] >= 1


def test_audit_runs():
    assert audit(["III"]) >= 0
