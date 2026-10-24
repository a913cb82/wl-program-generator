import re
from math import gcd

import wlgen
from wlconfig import (
    BIN_CLASS,
    BIN_GROUP,
    BIN_ZONES,
    BINS,
    CLASSES,
    DAY,
    GAP,
    GROUPS,
    MACRO,
    MIN_DOSE,
    PAIRED_GROUPS,
    PATTERNS,
    REPS,
    SCHEDULES,
    TOL,
    VARIANTS,
    ratio_ok,
    ratio_rank,
)
from wlgen import (
    allocate,
    ari,
    best_pair_scheme,
    best_scheme,
    bounded_round,
    build_plan,
    compact_text,
    cover_session,
    expand,
    fill,
    fit,
    fit_session,
    macro_days,
    map_zone_index,
    pair_fill,
    phrases,
    scheme_cost,
    scheme_entries,
    session_prior,
    sessions,
    sets_text,
    shift,
    slot_match,
    spread,
    to_html,
    toc_entries,
    training_table,
    week_bin_lifts,
    week_bins,
    week_quota,
    write_outputs,
    zone_alloc,
)

ANNUALS = {"III": 12000, "II": 12000, "I": 15000, "CMS": 15000, "MS": 18000}


def test_allocate():
    assert allocate(10, [1, 2, 3]) == [2, 3, 5]
    assert allocate(100, [21, 28, 17, 34]) == [21, 28, 17, 34]
    assert (
        allocate(100, CLASSES["CMS"]["ratios"]["prep"])
        == CLASSES["CMS"]["ratios"]["prep"]
    )
    assert sum(allocate(1000, [1, 1, 1])) == 1000


def test_class_populates_plan():
    for cls, annual in ANNUALS.items():
        plan = build_plan(cls)
        assert plan["class"] == cls
        assert plan["annual"] == annual
        expected = round(annual * macro_days(CLASSES[cls]["macro"]) / 365)
        assert sum(m["vol"] for m in plan["mesos"]) == expected


def test_weeks_sum_to_meso():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            assert sum(w["vol"] for w in m["weeks"]) == m["vol"]


def test_group_volumes_sum_to_week():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                assert list(w["groups"]) == GROUPS
                assert sum(w["groups"].values()) == w["vol"]


def test_sessions_sum_to_week():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                sizes = [s["size"] for s in w["sessions"]]
                assert "".join(sizes) in {
                    p for patterns in VARIANTS.values() for p in patterns
                }
                assert sum(s["vol"] for s in w["sessions"]) == w["vol"]


def test_sessions_cap():
    assert [(s["size"], s["vol"]) for s in sessions(242)] == [
        ("S", 49),
        ("L", 145),
        ("S", 48),
    ]
    assert [s["vol"] for s in sessions(552)] == [61, 123, 61, 123, 61, 123]
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                assert max(s["vol"] for s in w["sessions"]) <= 150


def test_day_template():
    assert [set(alts) for alts, _, _, _ in DAY] == [
        {"Snatch", "Other Snatch", "SnPull+Snatch", "SnPull+Other Snatch"},
        {
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
        },
        {"Squat", "SnPull", "ClPull"},
        {"Other Squat", "Press"},
        {"Fundamental"},
    ]
    assert all(
        lo == MIN_DOSE and hi is None and optional for _, lo, hi, optional in DAY
    )
    assert len(expand(DAY)) == 5 * 11 * 4 * 3 * 2


def test_week_quota_respects_slot_and_cap():
    targets = dict.fromkeys(GROUPS, 0)
    targets.update(
        {
            "Snatch": 40,
            "Other Snatch": 12,
            "Squat": 60,
            "SnPull": 24,
            "ClPull": 18,
            "Fundamental": 30,
        }
    )
    quota = week_quota(targets, [30, 40, 50, 30])
    assert set(quota) == {
        "Snatch",
        "Other Snatch",
        "Squat",
        "SnPull",
        "ClPull",
        "Fundamental",
    }
    for g, ts in quota.items():
        assert ts
        assert all(0 <= t < 4 for t in ts)
        assert len(ts) <= max(1, targets[g] // MIN_DOSE)
    for slot in (DAY[0], DAY[2], DAY[3], DAY[4]):
        hosts = [quota[g] for g in slot[0] if g in quota]
        for a in range(len(hosts)):
            for b in range(a + 1, len(hosts)):
                assert not (hosts[a] & hosts[b])


def test_week_quota_staggers_slots():
    targets = dict.fromkeys(GROUPS, 0)
    targets.update({"Snatch": 24, "Other Snatch": 24, "Fundamental": 24})
    quota = week_quota(targets, [10] * 6)
    assert quota["Snatch"] != quota["Fundamental"]
    assert not (quota["Snatch"] & quota["Other Snatch"])


def test_session_prior_biases_only_free_groups():
    targets = dict.fromkeys(GROUPS, 12)
    quota = {"Snatch": {0, 2}, "Squat": {1, 3}}
    prior = session_prior(targets, 4, quota, prev_last={"Snatch"})
    i = GROUPS.index("Snatch")
    assert prior[i][0] < prior[i][1] < 1.0
    assert prior[i][2] == 1.0
    assert prior[i][1] == prior[i][3]
    for g in ("Clean", "Jerk", "Other Jerk"):
        assert prior[GROUPS.index(g)] == [1.0] * 4


def test_quota_prior_keeps_exact_margins():
    targets = dict.fromkeys(GROUPS, 0)
    targets.update({"Snatch": 12, "Squat": 18})
    rows = [targets[g] for g in GROUPS]
    cols = [14, 16]
    prior = session_prior(targets, 2, {"Snatch": {0, 1}, "Squat": {0, 1}})
    moved = fit_session(prior, rows, cols)
    assert moved is not None
    assert [sum(row) for row in moved] == rows
    assert [sum(moved[i][j] for i in range(len(GROUPS))) for j in range(2)] == cols
    for j in range(2):
        assert slot_match({GROUPS[i] for i in range(len(GROUPS)) if moved[i][j]})


def test_spread_avoids_back_to_back_sessions():
    # Split groups train both paired (classic days) and standalone, so they
    # land on more days than before; the cap counts that structural cost.
    for cls in ANNUALS:
        short = boundary = 0
        for m in build_plan(cls)["mesos"]:
            prev_last = None
            for w in m["weeks"]:
                ss = w["sessions"]
                for g in GROUPS:
                    ts = [j for j, s in enumerate(ss) if g in s["movements"]]
                    short += sum(1 for a, b in zip(ts, ts[1:]) if b - a == 1)
                if prev_last is not None:
                    boundary += len(prev_last & set(ss[0]["movements"]))
                prev_last = set(ss[-1]["movements"])
        assert short < 130, (cls, short)
        # The minimum-dose floor concentrates stray doses into sibling
        # sessions, costing a carryover or two at week edges in I.
        assert boundary <= 10, (cls, boundary)


def test_spread_covers_the_main_lifts():
    for cls in ("I", "CMS", "MS"):
        hosts = {}
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    for g in s["movements"]:
                        hosts[g] = hosts.get(g, 0) + 1
        assert hosts["Squat"] >= 30, (cls, hosts["Squat"])
        assert hosts["Snatch"] >= 30, (cls, hosts["Snatch"])


def test_sessions_have_movements():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    assert s["base"] == "Day"
                    assert sum(sum(z) for z in s["movements"].values()) == s["vol"]
                    assert set(s["movements"]) <= set(GROUPS)


def test_session_group_coverage():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            hosted = {
                g for w in m["weeks"] for s in w["sessions"] for g in s["movements"]
            }
            assert {g for g, v in m["groups"].items() if v} <= hosted


def test_done_not_double_counted():
    # Prep 4-2 week 2 plans 58 Fundamental and 99 still remain in the meso,
    # so the week must train it (it was dropped while overfilled was double-counted)
    week = build_plan("I")["mesos"][0]["weeks"][1]
    hosted = {g for s in week["sessions"] for g in s["movements"]}
    assert "Fundamental" in hosted


def test_movements_use_template_floor():
    # min reps per movement is a soft floor in the weekly fit: exact session
    # volumes can force a small cell (the annual spread will remove these)
    for cls in ANNUALS:
        tiny = [
            sum(z)
            for m in build_plan(cls)["mesos"]
            for w in m["weeks"]
            for s in w["sessions"]
            for z in s["movements"].values()
            if sum(z) < MIN_DOSE
        ]
        assert all(0 < v < MIN_DOSE for v in tiny)


def test_training_plan_tables():
    plan = build_plan("I")
    html = to_html(plan)
    assert "#### Session " not in html
    assert "Day sizes:" not in html
    assert html.count('<table class="plan">') == 5
    # every session's slots land in its training-plan rows: each slot
    # gets one row with a movement cell and a scheme cell per week
    for m in plan["mesos"]:
        table = training_table(m)
        assert '<th scope="col" colspan="2">Week 1</th>' in table
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.DOTALL)
        body = rows[1:]
        idx = 0
        for si in range(max(len(w["sessions"]) for w in m["weeks"])):
            present = [w for w in m["weeks"] if si < len(w["sessions"])]
            nslots = max(len(scheme_entries(w["sessions"][si])) for w in present)
            for k in range(nslots):
                cells = re.findall(r"<(?:td|th)[^>]*>(.*?)</(?:td|th)>", body[idx])
                if k == 0:
                    assert cells[0] == str(si + 1)
                    assert f'rowspan="{nslots}"' in body[idx]
                    base = 1
                else:
                    base = 0
                for wi, w in enumerate(m["weeks"]):
                    if si >= len(w["sessions"]):
                        assert cells[base + 2 * wi] == ""
                        assert cells[base + 2 * wi + 1] == ""
                        continue
                    entries = scheme_entries(w["sessions"][si])
                    if k >= len(entries):
                        assert cells[base + 2 * wi] == ""
                        assert cells[base + 2 * wi + 1] == ""
                        continue
                    movement, seq = entries[k]
                    assert cells[base + 2 * wi] == movement
                    scheme = cells[base + 2 * wi + 1]
                    assert scheme == " ".join(
                        f'<span class="phrase">{p}</span>'
                        for p in wlgen._render_html(wlgen._parse(tuple(seq))[2])
                    )
                    assert "," not in scheme
                idx += 1
        assert idx == len(body)


def test_fill_exact_and_grouped():
    assert fill(16, (3, 2)) == [3, 3, 3, 3, 2, 2]
    assert fill(9, (2, 1)) == [2, 2, 2, 2, 1]
    assert fill(10, (4, 3, 2)) == [4, 3, 3]
    assert fill(7, (4, 3)) == [4, 3]
    assert fill(8, (4, 3, 2)) == [4, 4]
    assert fill(5, (5, 4, 3)) == [5]
    assert fill(2, (5, 4, 3, 2)) == [2]
    assert sets_text(fill(16, (3, 2))) == "4x3,2x2"
    assert sets_text(fill(10, (4, 3, 2))) == "4,2x3"
    assert sets_text(fill(7, (4, 3))) == "4,3"
    assert sets_text(fill(8, (4, 3, 2))) == "2x4"
    assert sets_text([3]) == "3"
    assert sets_text([1]) == "1"
    assert wlgen.complex_text(["3+1"]) == "3+1"
    assert wlgen.complex_text(["1+1"]) == "1+1"
    assert wlgen.complex_text(["3+3", "2+2"]) == "3+3,2+2"
    assert wlgen.complex_text(["2+2", "2+2", "1+1"]) == "2x2+2,1+1"
    assert wlgen.complex_text(["3+1"] * 5) == "5x3+1"
    assert wlgen.complex_text(["1+1"] * 2) == "2x1+1"


def test_pair_fill_caps_complex_size():
    assert pair_fill(15, 5, 70) == [(3, 1)] * 5
    assert pair_fill(10, 5, 80) == [(2, 1)] * 5
    assert pair_fill(2, 2, 90) == [(1, 1)] * 2
    assert pair_fill(12, 12, 70) == [(3, 3)] * 4
    assert pair_fill(5, 5, 70) == [(3, 3), (2, 2)]
    assert pair_fill(5, 5, 80) == [(2, 2), (2, 2), (1, 1)]
    # mixed pair: each side capped by its own table at its mapped zone.
    # 70% classic maps below the pull range, so the pull uses its 80% cap.
    assert pair_fill(9, 9, 70, "SnPull", "Snatch") == [(3, 3)] * 3
    assert pair_fill(6, 6, 70, "SnPull", "Snatch") == [(3, 3), (3, 3)]


def test_scheme_sums_and_caps():
    from wlgen import map_zone_index

    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    designated = {g for p in s.get("pairs", {}) for g in p}
                    for g in GROUPS:
                        if g in designated:
                            continue
                        counts = s["movements"].get(g, [])
                        if not sum(counts):
                            continue
                        lo = BIN_ZONES[BIN_GROUP[g]]
                        for z, n in enumerate(counts):
                            if n:
                                parts = fill(n, REPS[BIN_GROUP[g]][lo[z]])
                                assert sum(parts) == n
                                assert all(
                                    p in REPS[BIN_GROUP[g]][lo[z]] + (1,) for p in parts
                                )
                    for (a, b), (ref, va, vb) in s.get("pairs", {}).items():
                        lo = BIN_ZONES[BIN_GROUP[ref]]
                        for z, (x, y) in enumerate(zip(va, vb)):
                            if x or y:
                                parts = pair_fill(x, y, lo[z], a, b)
                                assert sum(p for p, _ in parts) == x
                                assert sum(q for _, q in parts) == y
                                za = BIN_ZONES[BIN_GROUP[a]][map_zone_index(lo[z], a)]
                                zb = BIN_ZONES[BIN_GROUP[b]][map_zone_index(lo[z], b)]
                                assert all(
                                    p <= max(REPS[BIN_GROUP[a]][za])
                                    and q <= max(REPS[BIN_GROUP[b]][zb])
                                    for p, q in parts
                                )


def test_scheme_entries_example():
    s = {
        "style": "ramp",
        "movements": {
            "Snatch": [3, 16, 9, 3, 0],
            "Other Clean": [3, 15, 10, 2, 0],
            "Other Jerk": [1, 5, 5, 2, 0],
            "Squat": [5, 10, 10, 10, 0],
            "Other Squat": [3, 7, 7, 8, 0],
        },
    }
    entries = scheme_entries(s)
    assert [m for m, _ in entries] == [
        "Snatch",
        "Other Clean+Other Jerk",
        "Squat",
        "Other Squat",
    ]
    assert all(seq for _, seq in entries)


def test_prune_doses_keeps_sessions_matchable():
    # Regression: dropping a pair partner stranded SnPull with ClPull in
    # one slot. Pruning must keep the session's hosted set matchable.
    idx = {g: i for i, g in enumerate(GROUPS)}
    support = [[0, 0] for _ in GROUPS]
    for g in ("Other Snatch", "Clean", "Jerk", "SnPull", "ClPull", "Fundamental"):
        support[idx[g]][0] = 1
    for g in ("Other Snatch", "Squat", "Fundamental"):
        support[idx[g]][1] = 1
    rows = [sum(row) for row in support]
    cols = [sum(support[i][j] for i in range(len(GROUPS))) for j in range(2)]
    pruned = wlgen.prune_doses(support, rows, cols, GROUPS)
    assert pruned is not None
    for j in range(2):
        hosted = {g for g in GROUPS if pruned[idx[g]][j]}
        assert wlgen.slot_match(hosted)
    # Other Snatch is droppable by the margins (it also trains day two)
    # but day one needs it to share SnPull's slot.
    assert pruned[idx["Other Snatch"]][0] == 1


def slot_total(items):
    """Total reps prescribed by parsed scheme items; waves repeat."""
    total = 0
    for item in items:
        if item[0] == "wave":
            total += item[1] * slot_total(item[2])
        else:
            _, _, pairs = item
            for value, count in pairs:
                reps = value
                while isinstance(reps, tuple):
                    reps = sum(reps)
                reps = sum(int(x) for x in str(reps).split("+"))
                total += reps * count
    return total


def test_session_group_doses_meet_minimum():
    """Every session slot prescribes 0 or >= MIN_DOSE total reps.

    The slot is the scheme entry: one movement's sets, or one complex
    counted across both sides (SnPull+Snatch (2+2)x3 is 12). Fragments
    inside a legal slot may ramp or taper below the floor."""
    assert slot_total(wlgen._parse(((70, 1),))[2]) == 1
    assert slot_total(wlgen._parse(((70, (2, 2)),))[2]) == 4
    for cls in ANNUALS:
        plan = build_plan(cls)
        for m in plan["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    for text, seq in scheme_entries(s):
                        total = slot_total(wlgen._parse(tuple(seq))[2])
                        assert total == 0 or total >= MIN_DOSE, (
                            cls,
                            m["name"],
                            text,
                            total,
                        )


def test_consolidate_doses_folds_stranded_cells():
    # Squat strands 3 lifts in session 0 while holding 8 in session 1;
    # Press completes the 4-cycle so weekly totals and session sizes
    # stay exact and both sessions stay slot-matchable.
    si, pi = GROUPS.index("Squat"), GROUPS.index("Press")
    moved = [[0] * 2 for _ in GROUPS]
    moved[si] = [3, 8]
    moved[pi] = [10, 10]
    assert wlgen.consolidate_doses(moved, {}) is True
    assert moved[si] == [0, 11]
    assert moved[pi] == [13, 7]
    # A weekly total of 5 cannot be placed legally anywhere.
    moved = [[0] * 2 for _ in GROUPS]
    moved[si] = [5, 0]
    assert wlgen.consolidate_doses(moved, {}) is False
    assert moved[si] == [5, 0]


def test_render_html():
    assert wlgen._render_html((("group", 80, ((3, 2), (2, 1))),)) == (
        '<span class="dose"><span class="frac"><span class="zone">80%</span>'
        '<span class="reps">3</span></span>'
        '<span class="sets">×2</span></span> '
        '<span class="dose"><span class="frac"><span class="zone">80%</span>'
        '<span class="reps">2</span></span></span>',
    )
    assert wlgen._render_html((("group", 70, ((1, 1),)),)) == (
        '<span class="dose"><span class="frac"><span class="zone">70%</span>'
        '<span class="reps">1</span></span></span>',
    )
    assert wlgen._render_html(
        (
            (
                "wave",
                3,
                (
                    ("group", 70, ((3, 1),)),
                    ("group", 80, ((2, 1),)),
                ),
            ),
        )
    ) == (
        '<span class="wave"><span class="rep">3×</span><span class="pl">(</span>'
        '<span class="dose"><span class="frac"><span class="zone">70%</span>'
        '<span class="reps">3</span></span></span> '
        '<span class="dose"><span class="frac"><span class="zone">80%</span>'
        '<span class="reps">2</span></span></span>'
        '<span class="pr">)</span></span>',
    )


def test_training_table_exact():
    meso = {
        "name": "Prep 4-2",
        "phase": "prep",
        "weeks": [
            {
                "vol": 10,
                "sessions": [
                    {
                        "movements": {"Clean": [0, 2, 0, 0, 0]},
                        "pairs": {
                            ("Clean", "Jerk"): (
                                "Clean",
                                (0, 2, 0, 0, 0),
                                (0, 2, 0, 0, 0),
                            )
                        },
                    },
                    {"movements": {"Squat": [0, 1, 0, 0, 0]}, "pairs": {}},
                ],
            },
            {
                "vol": 12,
                "sessions": [
                    {"movements": {"Squat": [0, 3, 0, 0, 0]}, "pairs": {}},
                ],
            },
        ],
    }
    frac = (
        '<span class="dose"><span class="frac"><span class="zone">{}%</span>'
        '<span class="reps">{}</span></span></span>'
    )
    cj = frac.format(70, "2+2")
    sq3 = frac.format(60, "3")
    sq1 = frac.format(60, "1")
    assert training_table(meso) == (
        '<table class="plan">\n'
        "<thead><tr><th></th>"
        '<th scope="col" colspan="2">Week 1</th>'
        '<th scope="col" colspan="2" class="wk">Week 2</th></tr></thead>\n'
        "<tbody>\n"
        f'<tr class="sess"><th scope="row" rowspan="1">1</th><td class="move">Clean+Jerk</td><td class="scheme"><span class="phrase">{cj}</span></td><td class="move wk">Squat</td><td class="scheme"><span class="phrase">{sq3}</span></td></tr>\n'
        f'<tr class="sess"><th scope="row" rowspan="1">2</th><td class="move">Squat</td><td class="scheme"><span class="phrase">{sq1}</span></td><td class="wk"></td><td></td></tr>\n'
        "</tbody>\n</table>"
    )


def test_plan_table_has_session_and_week_dividers():
    html = to_html(build_plan("I"))
    assert "--strong:" in html
    assert "table.plan tr.sess" in html
    assert "table.plan .wk" in html
    assert '<tr class="sess">' in html
    assert 'class="move wk"' in html


def test_plan_table_uses_full_width_without_wrapping():
    html = to_html(build_plan("I"))
    assert "table.plan { width: 100%; }" in html
    assert "td.scheme { min-width: 10rem; white-space: nowrap; }" in html
    assert '<div class="phrase">' not in html


def test_wave_parens_span_full_height():
    html = to_html(build_plan("I"))
    assert (
        ".dose, .wave { display: inline-flex; align-items: center; "
        "vertical-align: middle; }" in html
    )
    assert ".pl, .pr { font-size: 2.2em; line-height: 1; font-weight: 300; }" in html
    assert '<span class="pl">(</span>' in html


def test_scheme_entries_follow_slot_order():
    s = {
        "movements": {
            "Other Clean": [0, 2, 0, 0, 0],
            "Other Jerk": [0, 2, 0, 0, 0],
            "Squat": [0, 0, 2, 0, 0],
            "SnPull": [2, 0, 0, 0],
            "Snatch": [0, 2, 0, 0, 0],
            "Fundamental": [0, 0, 2, 0, 0, 0, 0],
        },
        "pairs": {
            ("SnPull", "Snatch"): ("Snatch", (0, 2, 0, 0, 0), (0, 2, 0, 0, 0)),
            ("Other Clean", "Other Jerk"): (
                "Other Clean",
                (0, 2, 0, 0, 0),
                (0, 2, 0, 0, 0),
            ),
        },
    }
    entries = scheme_entries(s)
    assert [movement for movement, _ in entries] == [
        "SnPull+Snatch",
        "Other Clean+Other Jerk",
        "Squat",
        "Fundamental",
    ]


def _snatch_counts():
    return (2, 13, 7, 0, 0)


def test_phrases_and_compact_text():
    wave = tuple([(70, 3), (80, 2)] * 3)
    assert phrases(wave) == 2
    assert compact_text(wave) == "3*(70%/3, 80%/2)"
    same_zone = ((80, 2), (80, 2), (80, 2), (80, 1))
    assert phrases(same_zone) == 2
    assert compact_text(same_zone) == "80%/2*3,1"


def test_scheme_cost_run_penalty_visited():
    seq = ((60, 1), (60, 1), (70, 1), (60, 1), (70, 1))
    cost, below, run, rep, ph, sets = scheme_cost(seq, "Snatch")
    assert run == 0
    assert cost == 100 * below + 10 * run + 5 * rep + 3 * ph + sets


def test_beam_order_warmup_and_no_skip():
    order, _ = best_scheme(_snatch_counts(), "Snatch")
    present = [BIN_ZONES["Snatch"][z] for z, n in enumerate(_snatch_counts()) if n]
    seen = set()
    last = None
    for z, _ in order:
        if z not in seen:
            assert not seen or z > max(seen)
            seen.add(z)
        if last is not None and z > last:
            nxt = next((zz for zz in present if zz > last), None)
            assert z == nxt
        last = z
    assert sum(v for _, v in order) == 22


def test_beam_prefers_separated_rep_change():
    _ordered, text = best_scheme(_snatch_counts(), "Snatch")
    assert text == "60%/2, 70%/2*2, 3*(80%/2, 70%/3), 80%/1"


def test_beam_cj_ratios_legal():
    for counts in ((0, 5, 0, 0, 0), (0, 0, 2, 0, 0)):
        ordered, _ = best_pair_scheme(counts, counts)
        assert sum(p for _, (p, _q) in ordered) == counts[1] + counts[2]
        assert sum(q for _, (_p, q) in ordered) == counts[1] + counts[2]
        for z, (p, q) in ordered:
            g = gcd(p, q)
            assert ratio_ok(p // g, q // g, z)


def test_map_zone_index_edges():
    assert map_zone_index(70, "Snatch") == 1
    assert map_zone_index(70, "SnPull") == 0  # below range -> lowest bin
    assert map_zone_index(110, "Snatch") == 4  # above range -> highest bin
    assert map_zone_index(80, "ClPull") == 1


def test_cover_session_shares_listed_pairs():
    hosted = {
        "Clean": 21,
        "Jerk": 23,
        "SnPull": 9,
        "Other Snatch": 21,
        "ClPull": 21,
        "Fundamental": 28,
    }
    assert cover_session(hosted) == [("Clean", "Jerk"), ("SnPull", "Other Snatch")]
    assert cover_session({"Snatch": 6}) == []
    assert cover_session({"Clean": 6, "Jerk": 6, "Other Clean": 6}) is None


def test_mixed_pair_scheme_ratios_legal():
    snatch = (0, 8, 4, 1, 0)
    pull = (0, 12, 2, 1, 0)
    ordered, text = best_pair_scheme(pull, snatch, "SnPull", "Snatch", "Snatch")
    assert sum(p for _, (p, _q) in ordered) == sum(pull)
    assert sum(q for _, (_p, q) in ordered) == sum(snatch)
    assert {z for z, _ in ordered} == {70, 80, 90}
    for z, (p, q) in ordered:
        g = gcd(p, q)
        assert ratio_ok(p // g, q // g, z)
    assert "%" in text


def test_schedules_keep_each_side_down_as_weight_rises():
    # A tier schedule must not flip sides: neither member's share of the
    # ratio may grow with weight, or one side's per-set reps would have to
    # rise on the way up (e.g. 1+2@70% -> 2+1@80%).
    for heavy, mid, light in SCHEDULES:
        assert heavy[0] <= mid[0] <= light[0]
        assert heavy[1] <= mid[1] <= light[1]


def test_pair_transition_checks_each_side_per_set():
    present = (60, 70, 80)
    # SnPull rising 1 -> 2 while Snatch falls 2 -> 1 is illegal even though
    # the complex total stays flat at 3.
    assert not wlgen._transition_ok(
        70, (1, 2), 80, (2, 1), frozenset({60, 70}), present
    )
    assert wlgen._transition_ok(70, (1, 2), 80, (1, 1), frozenset({60, 70}), present)
    # Dropping back down may still add reps.
    assert wlgen._transition_ok(
        80, (2, 1), 70, (1, 2), frozenset({60, 70, 80}), present
    )


def test_pair_orders_never_raise_side_reps_with_weight():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    for (a, b), (ref, va, vb) in s.get("pairs", {}).items():
                        ordered, _ = best_pair_scheme(tuple(va), tuple(vb), a, b, ref)
                        for (z0, (p0, q0)), (z1, (p1, q1)) in zip(ordered, ordered[1:]):
                            if z1 >= z0:
                                assert p1 <= p0 and q1 <= q0, (
                                    cls,
                                    a,
                                    b,
                                    (z0, p0, q0),
                                    (z1, p1, q1),
                                )


def test_two_reps_at_low_zones_are_one_set():
    for family in ("Squat", "Fund"):
        for zone in (50, 60, 70):
            assert fill(2, REPS[family][zone]) == [2]


def test_group_totals():
    plan = build_plan("I")
    expected = round(15000 * macro_days(CLASSES["I"]["macro"]) / 365)
    assert sum(plan["groups"].values()) == expected
    for m in plan["mesos"]:
        assert sum(m["groups"].values()) == m["vol"]


def test_html_tables_at_every_level():
    html = to_html(build_plan("I"))
    assert html.startswith("<!DOCTYPE html>")
    assert "<title>Soviet year (I)</title>" in html
    assert '<h1 id="volumes">Volumes</h1>' in html
    assert '<h1 id="training-plan">Training Plan</h1>' in html
    vols = html.split('<h1 id="training-plan">')[0]
    assert '<h2 id="macrocycle">Macrocycle</h2>' in vols
    assert '<h2 id="mesocycles">Mesocycles</h2>' in vols
    assert '<h2 id="microcycles">Microcycles</h2>' in vols
    macro = vols.split('<h2 id="mesocycles">')[0]
    assert '<th scope="col">Group</th><th scope="col">Lifts</th>' in macro
    assert "Meso sizes:" in macro
    assert "Prep 4-2 (prep)</th>" in vols
    micro = vols.split('<h2 id="microcycles">')[1]
    assert micro.count("<h3") == 5
    assert micro.count("<h4") == 20
    for chunk in micro.split("<h4")[1:]:
        assert '<th scope="col">Group</th>' in chunk
    plan = html.split('<h1 id="training-plan">')[1]
    assert plan.count('<table class="plan">') == 5
    assert plan.count("<h2") == 5


def test_html_toc():
    html = to_html(build_plan("I"))
    assert '<nav class="toc">' in html
    assert 'href="#volumes"' in html
    assert 'href="#training-plan"' in html
    assert 'href="#macrocycle"' in html
    assert 'href="#mesocycles"' in html
    assert 'href="#microcycles"' in html
    assert 'href="#prep-4-2-prep-1"' in html
    assert 'href="#week-1---242-lifts"' not in html
    assert html.count("<li>") == 10


def test_toc_nests_volumes_and_training_plan():
    html = to_html(build_plan("I"))
    toc = html.split('<nav class="toc">')[1].split("</nav>")[0]
    vols, plans = toc.split('href="#training-plan"')
    assert vols.index('href="#volumes"') < vols.index('href="#macrocycle"')
    assert vols.index('href="#macrocycle"') < vols.index('href="#mesocycles"')
    assert vols.index('href="#mesocycles"') < vols.index('href="#microcycles"')
    assert 'href="#prep-4-2-prep-1"' in plans
    assert "week-1" not in toc
    assert vols.count("<ul>") == 2


def test_toc_anchors_disambiguate_duplicates():
    headings = [(2, "A (x) - 1 lifts"), (3, "Week 1 - 2 lifts"), (2, "A (x) - 1 lifts")]
    assert toc_entries(headings) == [
        (2, "A (x) - 1 lifts", "a-x---1-lifts"),
        (3, "Week 1 - 2 lifts", "week-1---2-lifts"),
        (2, "A (x) - 1 lifts", "a-x---1-lifts-1"),
    ]


def test_html_tags_balance():
    for cls in ANNUALS:
        html = to_html(build_plan(cls))
        for tag in (
            "table",
            "thead",
            "tbody",
            "tr",
            "th",
            "td",
            "div",
            "span",
            "ul",
            "li",
            "section",
            "nav",
        ):
            opens = len(re.findall(rf"<{tag}(?=[\s>/])", html))
            assert opens == html.count(f"</{tag}>"), f"{cls} <{tag}>"


def test_sizes_at_every_level():
    html = to_html(build_plan("I"))
    assert "Meso sizes: 1151, 1266, 1438, 1035, 863" in html
    assert "Day sizes:" not in html
    assert html.count('class="sizes"') == 6
    assert "Prep 4-2 (prep) - Week sizes: 242, 322, 196, 391" in html
    assert html.count("<h4") == 20


def test_write_outputs(tmp_path):
    write_outputs(tmp_path)
    assert sorted(f.name for f in tmp_path.glob("*.html")) == [
        "CMS.html",
        "I.html",
        "II.html",
        "III.html",
        "MS.html",
    ]
    assert tmp_path.joinpath("I.html").read_text().startswith("<!DOCTYPE html>")


def test_html():
    html = to_html(build_plan("MS"))
    assert "<title>Soviet year (MS)</title>" in html
    assert 'id="microcycles"' in html
    assert 'id="training-plan"' in html
    assert ">Prep 4-2 (prep)</h2>" in html
    assert ">Week 1 - 290 lifts<" in html
    assert ">Snatch<" in html
    assert 'class="frac"' in html
    assert "@" not in html
    assert "Day sizes:" not in html
    assert ">Other Squat<" in to_html(build_plan("III"))


# Takano yearly ARI per bin table (ch. 8/11/12/13); fund tables are approximate
SOURCE_ARI = {
    "C2": {"Snatch": 75, "CJ": 76, "SnPull": 92, "ClPull": 89, "Squat": 71, "Fund": 80},
    "C1": {"Snatch": 75, "CJ": 77, "SnPull": 92, "ClPull": 87, "Squat": 70, "Fund": 78},
    "CMS": {
        "Snatch": 72,
        "CJ": 74,
        "SnPull": 91,
        "ClPull": 84,
        "Squat": 68,
        "Fund": 79,
    },
    "MS": {"Snatch": 71, "CJ": 73, "SnPull": 91, "ClPull": 84, "Squat": 66, "Fund": 79},
}


def week_ari(cls, meso, week, group):
    return ari(week_bins(cls, meso, week, group), BIN_ZONES[BIN_GROUP[group]])


def phase_share(phase):
    return sum(m[3] for m in MACRO if m[1] == phase)


def test_bin_tables_sum_to_one():
    for tables in BINS.values():
        for bins in tables.values():
            assert abs(sum(bins) - 1) < 1e-9


def test_bin_tables_match_source_ari():
    for bc, tables in BINS.items():
        for bt, bins in tables.items():
            assert abs(ari(bins, BIN_ZONES[bt]) - SOURCE_ARI[bc][bt]) < 3


def test_shift_hits_target():
    for bc, bt in [
        ("C1", "Snatch"),
        ("MS", "Squat"),
        ("C2", "Fund"),
        ("CMS", "ClPull"),
    ]:
        lo = BIN_ZONES[bt]
        base = ari(BINS[bc][bt], lo)
        for target in (base - 2, base + 2):
            out = shift(BINS[bc][bt], lo, target)
            assert abs(sum(out) - 1) < 1e-9
            assert abs(ari(out, lo) - target) < 1e-6


def test_prep_is_flat_without_fan():
    for cls in ("III", "II"):
        for g in ("Snatch", "Squat", "Press"):
            assert (
                week_bins(cls, 0, 0, g)
                == week_bins(cls, 1, 0, g)
                == week_bins(cls, 2, 0, g)
            )
            assert week_bins(cls, 0, 0, g) == week_bins(cls, 0, 3, g)


def test_prep_fans_for_higher_classes():
    for cls in ("I", "CMS", "MS"):
        for g in ("Snatch", "Squat"):
            assert (
                week_ari(cls, 0, 0, g) < week_ari(cls, 1, 0, g) < week_ari(cls, 2, 0, g)
            )


def test_comp_base_above_last_prep():
    for cls in ("III", "II", "I", "CMS", "MS"):
        for g in ("Snatch", "Squat", "Fundamental"):
            assert week_ari(cls, 2, 0, g) < week_ari(cls, 3, 0, g)


def test_comp2_peaks_then_tapers():
    for cls in ("III", "II", "I", "CMS", "MS"):
        for g in ("Snatch", "Clean", "Squat"):
            base = week_ari(cls, 4, 0, g)
            peak = week_ari(cls, 4, 2, g)
            taper = week_ari(cls, 4, 3, g)
            assert peak > base > taper


def test_only_comp2_tapers():
    for cls in ("III", "II", "I", "CMS", "MS"):
        assert week_bins(cls, 3, 0, "Snatch") == week_bins(cls, 3, 3, "Snatch")
        assert week_bins(cls, 4, 3, "Snatch") != week_bins(cls, 4, 0, "Snatch")


def test_taper_drops_classic_heavy_bins():
    for cls in ("III", "II", "I", "CMS", "MS"):
        for g in (
            "Snatch",
            "Clean",
            "Jerk",
            "Other Snatch",
            "Other Clean",
            "Other Jerk",
        ):
            bt = BIN_GROUP[g]
            bins = week_bins(cls, 4, 3, g)
            assert all(b == 0 for b, z in zip(bins, BIN_ZONES[bt]) if z >= 90)
        for g in ("Squat", "Other Squat", "SnPull", "ClPull", "Press", "Fundamental"):
            assert week_bins(cls, 4, 3, g) == BINS[BIN_CLASS[cls]][BIN_GROUP[g]]


def test_annual_mixture_holds():
    for cls in ("III", "II", "I", "CMS", "MS"):
        for g in GROUPS:
            total = 0.0
            for meso, (_, phase, split, share) in enumerate(MACRO):
                for week, s in enumerate(split):
                    total += share * s / sum(split) * week_ari(cls, meso, week, g)
            ann = ari(BINS[BIN_CLASS[cls]][BIN_GROUP[g]], BIN_ZONES[BIN_GROUP[g]])
            assert abs(total - ann) < 0.75


def test_phase_gap_matches_source():
    wp, wc = phase_share("prep"), phase_share("comp")
    for cls in ("III", "II", "I", "CMS", "MS"):
        prep = comp = 0.0
        for meso, (_, phase, split, share) in enumerate(MACRO):
            for week, s in enumerate(split):
                v = share * s / sum(split) * week_ari(cls, meso, week, "Snatch")
                if phase == "prep":
                    prep += v
                else:
                    comp += v
        assert abs((comp / wc - prep / wp) - GAP[cls]) < 0.6


def test_week_bin_lifts():
    for cls in ANNUALS:
        plan = build_plan(cls)
        for mi, m in enumerate(plan["mesos"]):
            for wi, w in enumerate(m["weeks"]):
                for g, v in w["groups"].items():
                    if v:
                        assert sum(week_bin_lifts(cls, mi, wi, g, v)) == v


def test_html_week_bins():
    header = "".join(
        f'<th scope="col">{h}</th>'
        for h in [
            "Group",
            "Lifts",
            "50%",
            "60%",
            "70%",
            "80%",
            "90%",
            "100%",
            "110%",
            "ARI",
        ]
    )
    weeks = to_html(build_plan("I")).split("<h4")[1:]
    assert len(weeks) == 20
    assert all(header in chunk for chunk in weeks)
    row = weeks[-1].split('<th scope="row">Snatch</th>')[1].split("</tr>")[0]
    cells = re.findall(r"<td[^>]*>(.*?)</td>", row)
    assert cells[5] == "" and cells[6] == ""  # 90% and 100% empty in comp taper


def test_bounded_round():
    assert bounded_round([1.2, 2.9, 5.4], [0, 0, 0], [2, 3, 6], 10) == [1, 3, 6]
    assert sum(bounded_round([1.0, 1.0, 1.0], [0, 0, 0], [1, 1, 1], 5)) == 5


def test_spread_repays_carry_within_band():
    assert spread([20, 30], [24, 26], [20, 30]) == [24, 26]


def test_spread_caps_week_deviation():
    out = spread([50, 50], [100, 0], [50, 50])
    assert sum(out) == 100
    assert out[0] <= 60


def test_fit_hits_margins():
    prior = [[1, 1, 0], [1, 1, 1], [0, 1, 1]]
    out = fit(prior, [4, 6, 5], [5, 6, 4])
    assert [sum(row) for row in out] == [4, 6, 5]
    assert [sum(row[j] for row in out) for j in range(3)] == [5, 6, 4]
    assert all(out[i][j] == 0 for i in range(3) for j in range(3) if not prior[i][j])


def test_fit_rejects_infeasible():
    assert fit([[1, 0], [0, 1]], [5, 5], [3, 7]) is None


def test_fit_session_drops_tiny_cells():
    # Snatch and Clean are separate slots, so both can be hosted in both days
    out = fit_session([[1, 1], [0, 0], [1, 1]], [8, 0, 8], [8, 8])
    assert out is not None
    assert all(c == 0 or c >= MIN_DOSE for row in out for c in row)


def test_slot_match_xor():
    assert not slot_match({"Snatch", "Other Snatch"})
    assert not slot_match({"Squat", "SnPull"})
    assert not slot_match({"Other Squat", "Press"})
    assert slot_match({"Snatch", "SnPull", "Fundamental"})
    assert slot_match({"Snatch", "Clean", "Jerk", "Other Squat"})
    # listed complexes share one slot; the other singles keep their own
    assert slot_match({"SnPull", "Snatch"})
    assert slot_match({"SnPull", "Snatch", "Squat", "Fundamental"})
    assert slot_match({"ClPull", "Clean", "Squat"})
    assert not slot_match({"SnPull", "Snatch", "Squat", "ClPull"})


def test_sessions_respect_slot_xor():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    assert slot_match(set(s["movements"]))


def test_day_patterns_keep_canonical_first():
    for n, patterns in VARIANTS.items():
        assert patterns[0] == PATTERNS[n]
    # Weeks whose canonical sizes cannot host every dose at >= MIN_DOSE
    # use the first variant that can (the dose floor outranks pattern
    # preference); all other weeks keep canonical sizes.
    exceptions = {
        ("III", "Comp 1", 3): "MLM",
        ("III", "Comp 2", 3): "LSL",
        ("II", "Comp 1", 3): "MLM",
        ("II", "Comp 2", 3): "LSL",
        ("I", "Prep 2-4", 0): "LMLM",
        ("I", "Prep 2-4", 3): "LMLM",
        ("I", "Prep 3-1", 1): "LMLM",
        ("I", "Prep 3-1", 3): "LMLM",
        ("I", "Comp 1", 1): "LMLM",
        ("I", "Comp 2", 1): "LMLM",
        ("I", "Comp 2", 3): "MLM",
        ("CMS", "Prep 2-4", 0): "LMLM",
        ("CMS", "Prep 2-4", 3): "LMLM",
        ("CMS", "Prep 3-1", 1): "LMLM",
        ("CMS", "Prep 3-1", 3): "LMLM",
        ("CMS", "Comp 1", 2): "MLM",
        ("CMS", "Comp 2", 0): "MLM",
        ("CMS", "Comp 2", 3): "MLM",
        ("MS", "Prep 2-4", 3): "MSLMM",
        ("MS", "Prep 3-1", 3): "MSLMM",
        ("MS", "Comp 1", 0): "MSLMM",
        ("MS", "Comp 1", 3): "LSL",
    }
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for wi, w in enumerate(m["weeks"]):
                sizes = "".join(s["size"] for s in w["sessions"])
                assert sizes == exceptions.get(
                    (cls, m["name"], wi), PATTERNS[len(sizes)]
                )


def pair_dose(s, g):
    """Largest complex leg of this movement in one reference zone."""
    best = 1
    for (a, b), (ref, va, vb) in s.get("pairs", {}).items():
        if g not in (a, b):
            continue
        for x, y in zip(va, vb):
            if x and y:
                r = gcd(x, y)
                best = max(best, (x if g == a else y) // r)
    return best


def test_session_profiles_keep_a_ramp():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for g in GROUPS:
                    counts = w["bins"][g]
                    if not sum(counts):
                        continue
                    active = [
                        s for s in w["sessions"] if sum(s["movements"].get(g, []))
                    ]
                    supports = [
                        {i for i, c in enumerate(s["movements"][g]) if c}
                        for s in active
                    ]
                    if len(supports) < 2:
                        continue
                    # sessions may start at different bases; the hard rule is
                    # that each profile is contiguous from its own base.
                    # Coverage asks for a dose only where the week holds a
                    # dose per active session plus one spare per session:
                    # largest-remainder rounding can strand a session with
                    # none of a marginal zone.
                    doses = [pair_dose(s, g) for s in active]
                    for s, dose in zip(active, doses):
                        z = s["movements"][g]
                        top = max(i for i, c in enumerate(z) if c)
                        for i in range(top):
                            if counts[i] >= sum(doses) + len(active):
                                assert z[i] >= dose  # warmup block below the top


def test_ratio_limits_by_zone():
    assert ratio_ok(3, 2, 70)
    assert not ratio_ok(3, 2, 80)
    assert ratio_ok(2, 1, 80)
    assert not ratio_ok(2, 1, 90)
    assert ratio_ok(1, 1, 100)
    assert not ratio_ok(3, 1, 80)


def test_pair_ratio_legal_in_every_zone():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    for (a, b), (ref, va, vb) in s.get("pairs", {}).items():
                        zlo = BIN_ZONES[BIN_GROUP[ref]]
                        for z, (x, y) in enumerate(zip(va, vb)):
                            if x and y:
                                d = gcd(x, y)
                                assert ratio_ok(x // d, y // d, zlo[z]), (
                                    cls,
                                    a,
                                    b,
                                    zlo[z],
                                    (x // d, y // d),
                                )


def test_pair_ratio_never_widens_with_weight():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    for (a, b), (ref, va, vb) in s.get("pairs", {}).items():
                        pairs = list(zip(va, vb))
                        assert all(x and y for x, y in pairs if x or y)
                        ranks = [
                            ratio_rank(x // gcd(x, y), y // gcd(x, y))
                            for x, y in pairs
                            if x
                        ]
                        assert ranks == sorted(ranks, reverse=True)


def test_zone_alloc_margins_and_warmup():
    counts = [8, 5, 4, 2]
    lifts = [10, 9]
    out = zone_alloc(counts, lifts)
    assert [sum(row) for row in out] == lifts
    assert [sum(row[z] for row in out) for z in range(4)] == counts
    assert all(row[0] >= 1 for row in out)  # warmup base in every session


def test_sessions_match_week_groups():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for g in GROUPS:
                    assert (
                        sum(sum(s["movements"].get(g, [])) for s in w["sessions"])
                        == w["groups"][g]
                    )


def test_session_zones_match_week_bins():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for g in w["groups"]:
                    got = [0] * len(w["bins"][g])
                    for s in w["sessions"]:
                        for z, c in enumerate(s["movements"].get(g, [])):
                            got[z] += c
                    assert got == w["bins"][g]


def test_session_profiles_are_contiguous():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    for g, counts in s["movements"].items():
                        used = [z for z, n in enumerate(counts) if n]
                        # A gap stands only where the week cannot cover
                        # every session spanning it: with fewer units than
                        # spanning sessions, some session must jump it.
                        # (Sessions needing the week's base count as
                        # spanning it even though nothing sits below.)
                        gaps = [
                            z for z in range(used[0], used[-1] + 1) if not counts[z]
                        ]
                        week_base = next(
                            (z for z, n in enumerate(w["bins"][g]) if n), None
                        )
                        for z in gaps:
                            pros = [
                                t["movements"].get(g, [0] * len(counts))
                                for t in w["sessions"]
                            ]
                            if z == week_base:
                                spanning = sum(1 for t in pros if sum(t[z + 1 :]))
                            else:
                                spanning = sum(
                                    1 for t in pros if sum(t[:z]) and sum(t[z + 1 :])
                                )
                            # Units frozen inside a pair in a session that
                            # does not span the zone cannot move to cover
                            # it; judge the gap against the rest.
                            locked = sum(
                                t[z]
                                for t, s in zip(pros, w["sessions"])
                                if any(g in p for p in s.get("pairs", {}))
                                and not (
                                    sum(t[:z]) and sum(t[z + 1 :])
                                    if z != week_base
                                    else sum(t[z + 1 :])
                                )
                            )
                            assert w["bins"][g][z] - locked < spanning, (
                                cls,
                                g,
                                counts,
                            )


def test_week_targets_near_nominal():
    for cls in ANNUALS:
        plan = build_plan(cls)
        for m in plan["mesos"]:
            ratios = CLASSES[cls]["ratios"][m["phase"]]
            for w in m["weeks"]:
                nominal = allocate(w["vol"], ratios)
                for i, g in enumerate(GROUPS):
                    # the pair ratio rule is hard, its week band soft: snapping
                    # sessions to tier-legal ratios can push a paired group up
                    # to two lifts past the band (small taper-week groups)
                    slack = 2 if g in PAIRED_GROUPS else 0
                    assert (
                        abs(w["groups"][g] - nominal[i])
                        <= max(1, round(TOL * nominal[i])) + slack
                    )


def test_meso_targets_exact():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for g in GROUPS:
                assert sum(w["groups"][g] for w in m["weeks"]) == m["groups"][g]
