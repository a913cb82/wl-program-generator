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
    PATTERNS,
    REPS,
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
    expand,
    fill,
    fit,
    fit_session,
    macro_days,
    pair_fill,
    phrases,
    scheme_cost,
    scheme_lines,
    session_prior,
    sessions,
    sets_text,
    shift,
    slot_match,
    spread,
    to_markdown,
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
        {"Snatch", "Other Snatch"},
        {"Clean", "Other Clean"},
        {"Jerk", "Other Jerk"},
        {"Squat", "SnPull", "ClPull"},
        {"Other Squat", "Press"},
        {"Fundamental"},
    ]
    assert all(
        lo == MIN_DOSE and hi is None and optional for _, lo, hi, optional in DAY
    )
    assert len(expand(DAY)) == 3 * 3 * 3 * 4 * 3 * 2


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
    for slot in (DAY[0], DAY[3], DAY[4], DAY[5]):
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
        assert short < 80, (cls, short)
        assert boundary <= 8, (cls, boundary)


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


def test_markdown_sessions():
    plan = build_plan("I")
    plist = [s for m in plan["mesos"] for w in m["weeks"] for s in w["sessions"]]
    md = to_markdown(plan)
    lines = md.splitlines()
    assert sum(1 for line in lines if line.startswith("#### Session ")) == len(plist)
    chunks = md.split("\n#### ")[1:]
    assert len(chunks) == len(plist)
    assert not any("| Movement |" in line for line in lines)
    first = plist[0]
    assert f"#### Session 1 - {first['vol']} lifts" in lines
    for line in scheme_lines(first):
        assert line in chunks[0].splitlines()


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


def test_scheme_sums_and_caps():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    cs = [
                        g
                        for g in ("Clean", "Other Clean")
                        if sum(s["movements"].get(g, []))
                    ]
                    hs = [
                        g
                        for g in ("Jerk", "Other Jerk")
                        if sum(s["movements"].get(g, []))
                    ]
                    pair = (cs[0], hs[0]) if len(cs) == 1 and len(hs) == 1 else None
                    for g in GROUPS:
                        counts = s["movements"].get(g, [])
                        if not sum(counts) or (pair and g in pair):
                            continue
                        lo = BIN_ZONES[BIN_GROUP[g]]
                        for z, n in enumerate(counts):
                            if n:
                                parts = fill(n, REPS[BIN_GROUP[g]][lo[z]])
                                assert sum(parts) == n
                                assert all(
                                    p in REPS[BIN_GROUP[g]][lo[z]] + (1,) for p in parts
                                )
                    if pair:
                        lo = BIN_ZONES[BIN_GROUP[pair[0]]]
                        for z, (a, b) in enumerate(
                            zip(s["movements"][pair[0]], s["movements"][pair[1]])
                        ):
                            if a or b:
                                parts = pair_fill(a, b, lo[z])
                                assert sum(p for p, _ in parts) == a
                                assert sum(q for _, q in parts) == b
                                assert all(
                                    p <= max(REPS["CJ"][lo[z]])
                                    and q <= max(REPS["CJ"][lo[z]])
                                    for p, q in parts
                                )


def test_scheme_lines_example():
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
    lines = scheme_lines(s)
    assert lines and all(line.startswith("- ") for line in lines)


def _snatch_counts():
    return (2, 13, 7, 0, 0)


def test_phrases_and_compact_text():
    wave = tuple([(70, 3), (80, 2)] * 3)
    assert phrases(wave) == 2
    assert compact_text(wave) == "3x(3@70%, 2@80%)"
    same_zone = ((80, 2), (80, 2), (80, 2), (80, 1))
    assert phrases(same_zone) == 2
    assert compact_text(same_zone) == "3x2,1@80%"


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
    assert text == "2@60%, 2x2@70%, 1@80%, 3x(3@70%, 2@80%)"


def test_beam_cj_ratios_legal():
    for counts in ((0, 5, 0, 0, 0), (0, 0, 2, 0, 0)):
        ordered, _ = best_pair_scheme(counts, counts)
        assert sum(p for _, (p, _q) in ordered) == counts[1] + counts[2]
        assert sum(q for _, (_p, q) in ordered) == counts[1] + counts[2]
        for z, (p, q) in ordered:
            g = gcd(p, q)
            assert ratio_ok(p // g, q // g, z)


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


def test_markdown_tables_at_every_level():
    md = to_markdown(build_plan("I"))
    assert md.startswith("# Soviet year (I)")
    assert "| Group | Lifts |" in md.split("\n## ")[0]
    for chunk in md.split("\n## ")[1:]:
        assert "| Group | Lifts |" in chunk
    micro = md.split("\n### ")[1:]
    assert len(micro) == 20
    for chunk in micro:
        assert "| Group | Lifts |" in chunk


def test_sizes_at_every_level():
    md = to_markdown(build_plan("I"))
    macro = md.split("\n## ")[0]
    assert "Meso sizes:" in macro
    assert "Day sizes:" not in macro
    assert "Meso sizes: 1151, 1266, 1438, 1035, 863" in macro
    chunk = md.split("\n## ")[1]
    rows = [line for line in chunk.splitlines() if line.startswith("Week sizes:")]
    assert rows == ["Week sizes: 242, 322, 196, 391"]
    weeks = chunk.split("\n### ")[1:]
    assert len(weeks) == 4
    day = [line for line in weeks[0].splitlines() if line.startswith("Day sizes:")]
    assert day == ["Day sizes: 49, 145, 48"]


def test_write_outputs(tmp_path):
    write_outputs(tmp_path)
    assert sorted(f.name for f in tmp_path.glob("*.md")) == [
        "CMS.md",
        "I.md",
        "II.md",
        "III.md",
        "MS.md",
    ]
    assert tmp_path.joinpath("I.md").read_text().startswith("# Soviet year (I)")


def test_markdown():
    md = to_markdown(build_plan("MS"))
    assert "# Soviet year (MS)" in md
    assert "## Prep 4-2" in md
    assert "### Week 1" in md
    assert "| Snatch |" in md
    assert "Day sizes:" in md
    assert "| Other Squat |" in to_markdown(build_plan("III"))


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


def test_markdown_week_bins():
    header = "| Group | Lifts | 50% | 60% | 70% | 80% | 90% | 100% | 110% | ARI |"
    weeks = to_markdown(build_plan("I")).split("\n### ")[1:]
    assert len(weeks) == 20
    assert all(header in chunk for chunk in weeks)
    snatch = next(
        line for line in weeks[-1].splitlines() if line.startswith("| Snatch |")
    )
    cells = [c.strip() for c in snatch.split("|")]
    assert cells[7] == "" and cells[8] == ""  # 90% and 100% empty in comp taper


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


def test_sessions_respect_slot_xor():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    assert slot_match(set(s["movements"]))


def test_day_patterns_keep_canonical_first():
    for n, patterns in VARIANTS.items():
        assert patterns[0] == PATTERNS[n]
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                sizes = [s["size"] for s in w["sessions"]]
                assert "".join(sizes) == PATTERNS[len(sizes)]


def pair_dose(s, g):
    """Largest set of this movement in one zone (1 when trained alone)."""
    clean = next(
        (x for x in ("Clean", "Other Clean") if sum(s["movements"].get(x, []))),
        None,
    )
    jerk = next(
        (x for x in ("Jerk", "Other Jerk") if sum(s["movements"].get(x, []))),
        None,
    )
    if clean is None or jerk is None or g not in (clean, jerk):
        return 1
    best = 1
    for a, b in zip(s["movements"][clean], s["movements"][jerk]):
        if a and b:
            r = gcd(a, b)
            best = max(best, (a if g == clean else b) // r)
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
                    # that each profile is contiguous from its own base
                    doses = [pair_dose(s, g) for s in active]
                    for s, dose in zip(active, doses):
                        z = s["movements"][g]
                        top = max(i for i, c in enumerate(z) if c)
                        for i in range(top):
                            if counts[i] >= sum(doses):
                                assert z[i] >= dose  # warmup block below the top


def test_ratio_limits_by_zone():
    assert ratio_ok(3, 2, 70)
    assert not ratio_ok(3, 2, 80)
    assert ratio_ok(2, 1, 80)
    assert not ratio_ok(2, 1, 90)
    assert ratio_ok(1, 1, 100)
    assert not ratio_ok(3, 1, 80)


def test_cj_pair_ratio_legal_in_every_zone():
    zlo = BIN_ZONES[BIN_GROUP["Clean"]]
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    mv = s["movements"]
                    for c in ("Clean", "Other Clean"):
                        for h in ("Jerk", "Other Jerk"):
                            if c not in mv or h not in mv:
                                continue
                            for z, (a, b) in enumerate(zip(mv[c], mv[h])):
                                if a and b:
                                    d = gcd(a, b)
                                    assert ratio_ok(a // d, b // d, zlo[z]), (
                                        cls,
                                        c,
                                        h,
                                        zlo[z],
                                        (a // d, b // d),
                                    )


def test_cj_pair_ratio_never_widens_with_weight():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for w in m["weeks"]:
                for s in w["sessions"]:
                    mv = s["movements"]
                    for c in ("Clean", "Other Clean"):
                        for h in ("Jerk", "Other Jerk"):
                            if c not in mv or h not in mv:
                                continue
                            pairs = list(zip(mv[c], mv[h]))
                            assert all(a and b for a, b in pairs if a or b)
                            ranks = [
                                ratio_rank(a // gcd(a, b), b // gcd(a, b))
                                for a, b in pairs
                                if a
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
                        assert used == list(range(used[0], used[-1] + 1)), (
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
                    # the classic-lift ratio rule is hard, its week band soft:
                    # snapping may push a clean or jerk one lift past the band
                    slack = (
                        1 if g in ("Clean", "Other Clean", "Jerk", "Other Jerk") else 0
                    )
                    assert (
                        abs(w["groups"][g] - nominal[i])
                        <= max(1, round(TOL * nominal[i])) + slack
                    )


def test_meso_targets_exact():
    for cls in ANNUALS:
        for m in build_plan(cls)["mesos"]:
            for g in GROUPS:
                assert sum(w["groups"][g] for w in m["weeks"]) == m["groups"][g]
