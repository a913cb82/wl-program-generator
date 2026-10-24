"""Score a program from its intermediate representation.

The scorer reads the plain-JSON plan (see ``to_ir``/``from_ir`` in wlgen)
and returns the scoring system from the design doc: strain, size, rhythm
and drift, plus the single score. Lower is better everywhere.
"""

from statistics import median

from wlconfig import (
    BIN_GROUP,
    BIN_ZONES,
    CLASSES,
    GROUPS,
    PAIR_REF,
    PAIRED_GROUPS,
    PRILEPIN_CLASSIC,
    REPS,
    TOL,
)
from wlgen import (
    _parse,
    _transition_ok,
    allocate,
    atom_total,
    build_plan,
    complexity,
    from_ir,
    macro_days,
    prilepin_score,
    scheme_entries,
    session_dose,
    slot_match,
)

FLOOR = 0.25  # smallest useful dose in one session, in session units
TOL_CLASSIC = 1.5
TOL_STRENGTH = 2.0


def _tolerance(family):
    return TOL_CLASSIC if family in PRILEPIN_CLASSIC else TOL_STRENGTH


def _nominal(cls, phase, week_vol):
    """Planned weekly lifts per group: the class ratio split of the week."""
    ratios = CLASSES[cls]["ratios"][phase]
    return dict(
        zip(GROUPS, allocate(week_vol, [ratios[i] for i in range(len(GROUPS))]))
    )


def _macro_vol(cls):
    macro = CLASSES[cls]["macro"]
    return round(CLASSES[cls]["annual"] * macro_days(macro) / 365)


def _band(nominal, weeks, paired):
    """Allowed miss around a planned amount over several weeks."""
    return max(weeks, round(TOL * nominal)) + (2 * weeks if paired else 0)


def _slot_total(items):
    """Total reps prescribed by parsed scheme items; waves repeat."""
    total = 0
    for item in items:
        if item[0] == "wave":
            total += item[1] * _slot_total(item[2])
        else:
            _, _, pairs = item
            for value, count in pairs:
                reps = value
                while isinstance(reps, tuple):
                    reps = sum(reps)
                total += reps * count
    return total


def _entry_problems(text, seq, session):
    """Ways one scheme entry breaks the training rules, if any."""
    problems = []
    parts = text.split("+")
    seq = tuple(seq)
    if len(parts) == 1:
        (g,) = parts
        fam = BIN_GROUP[g]
        zones = BIN_ZONES[fam]
        if any(zlo not in zones for zlo, _ in seq):
            problems.append(f"{text}: zone outside the {fam} ladder")
        cap = {z: max(REPS[fam][z]) for z in zones if z in REPS[fam]}
        if any(
            not isinstance(v, int) or v < 1 or v > cap.get(zlo, v) for zlo, v in seq
        ):
            problems.append(f"{text}: set size outside the ladder")
        present = sorted({zlo for zlo, _ in seq})
        seen: set = set()
        prev = None
        for zlo, value in seq:
            if prev is not None and not _transition_ok(
                prev[0], prev[1], zlo, value, seen, present
            ):
                problems.append(f"{text}: illegal order at {zlo}%")
                break
            seen.add(zlo)
            prev = (zlo, value)
        if _slot_total(_parse(seq)[2]) != sum(session["movements"].get(g, [])):
            problems.append(f"{text}: scheme does not match the cell")
    else:
        a, b = parts
        key = (a, b) if (a, b) in PAIR_REF else (b, a)
        ref = session.get("pairs", {}).get(key, (PAIR_REF.get(key),))[0]
        ref = ref or PAIR_REF[key]
        zones = BIN_ZONES[BIN_GROUP[ref]]
        if any(zlo not in zones for zlo, _ in seq):
            problems.append(f"{text}: zone outside the {ref} ladder")
        fa, fb = BIN_GROUP[a], BIN_GROUP[b]
        for zlo, value in seq:
            if not isinstance(value, tuple) or len(value) != 2:
                problems.append(f"{text}: complex set is not a pair")
                break
            if atom_total(value) < 1 or any(v < 0 for v in value):
                problems.append(f"{text}: empty complex set")
                break
            caps = [
                max(REPS[f][zlo]) if zlo in REPS.get(f, {}) else value[i]
                for i, f in enumerate((fa, fb))
            ]
            if any(v > c for v, c in zip(value, caps)):
                problems.append(f"{text}: complex side above the ladder")
                break
        present = sorted({zlo for zlo, _ in seq})
        seen = set()
        prev = None
        for zlo, value in seq:
            if prev is not None and not _transition_ok(
                prev[0], prev[1], zlo, value, seen, present
            ):
                problems.append(f"{text}: illegal order at {zlo}%")
                break
            seen.add(zlo)
            prev = (zlo, value)
        want = sum(session["movements"].get(a, [])) + sum(
            session["movements"].get(b, [])
        )
        if _slot_total(_parse(seq)[2]) != want:
            problems.append(f"{text}: scheme does not match the cell")
    return problems


def _week_rhythm(vols):
    """One week's shape: amplitude miss plus missing turns plus peaks away
    from one. Only moves of at least a tenth of the week's range steer the
    turns and the peaks."""
    n = len(vols)
    lo, hi = min(vols), max(vols)
    amplitude = abs(hi / lo - 2.75) / 0.25 if lo else 0.0
    bar = (hi - lo) / 10
    big = [d for d in (b - a for a, b in zip(vols, vols[1:])) if d and abs(d) >= bar]
    possible = max(0, len(big) - 1)
    turns = sum(1 for x, y in zip(big, big[1:]) if (x > 0) != (y > 0))
    peaks = 0
    for i, v in enumerate(vols):
        neigh = ([vols[i - 1]] if i > 0 else []) + ([vols[i + 1]] if i < n - 1 else [])
        if neigh and all(v > u for u in neigh) and v - max(neigh) >= bar:
            peaks += 1
    return {
        "contrast": hi / lo if lo else 0.0,
        "amplitude": amplitude,
        "turns": turns,
        "possible": possible,
        "missing": possible - turns,
        "peaks": peaks,
        "away": abs(peaks - 1),
        "total": amplitude + (possible - turns) + abs(peaks - 1),
    }


def _unjustified_gaps(session, sessions, week_bins):
    """Zone gaps in one session's cells that the week could have covered,
    mirroring the contiguity test: a gap stands only where the week cannot
    cover every session spanning it."""
    count = 0
    for g, counts in session["movements"].items():
        used = [z for z, x in enumerate(counts) if x]
        if len(used) < 2:
            continue
        nz = len(counts)
        pros = [t["movements"].get(g, [0] * nz) for t in sessions]
        week_base = next((z for z, x in enumerate(week_bins[g]) if x), None)
        for z in range(used[0], used[-1] + 1):
            if counts[z] or week_base is None:
                continue
            if z == week_base:
                spanning = sum(1 for t in pros if sum(t[z + 1 :]))
            else:
                spanning = sum(1 for t in pros if sum(t[:z]) and sum(t[z + 1 :]))
            locked = sum(
                t[z]
                for t, s in zip(pros, sessions)
                if any(g in p for p in s.get("pairs", {}))
                and not (
                    sum(t[:z]) and sum(t[z + 1 :])
                    if z != week_base
                    else sum(t[z + 1 :])
                )
            )
            if not (week_bins[g][z] - locked < spanning):
                count += 1
    return count


def _score_items(items, seconds=None):
    """Additive breakdown over (cls, plan) pairs; the book total is just
    the same loop over more classes."""
    out: dict = {
        "excess": 0.0,
        "shortfall": 0.0,
        "instructions": 0,
        "longest": 0,
        "slots": 0,
        "rhythms": [],
        "ob_micro": 0.0,
        "iv_micro": 0.0,
        "ob_meso": 0.0,
        "iv_meso": 0.0,
        "ob_macro": 0.0,
        "iv_macro": 0.0,
        "illegal": 0,
        "clash": 0,
        "gaps": 0,
        "idle": 0,
        "idle_meso": 0,
        "spread_num": 0.0,
        "spread_den": 0,
        "meso_spread_num": 0.0,
        "meso_spread_den": 0,
    }
    for cls, plan in items:
        macro_nom = {g: 0 for g in GROUPS}
        macro_act = {g: 0 for g in GROUPS}
        for m in plan["mesos"]:
            meso_nom = {g: 0 for g in GROUPS}
            hosted_days: dict = {g: 0 for g in GROUPS}
            shares: dict = {g: [] for g in GROUPS}
            for w in m["weeks"]:
                nom = _nominal(cls, m["phase"], w["vol"])
                vols = [s["vol"] for s in w["sessions"]]
                out["rhythms"].append(_week_rhythm(vols)["total"])
                week_tot = 0
                for g in GROUPS:
                    actual = w["groups"].get(g, 0)
                    macro_nom[g] += nom[g]
                    macro_act[g] += actual
                    meso_nom[g] += nom[g]
                    out["ob_micro"] += max(
                        0,
                        abs(actual - nom[g]) - _band(nom[g], 1, g in PAIRED_GROUPS),
                    )
                    week_tot += actual
                    days = [
                        j
                        for j, s in enumerate(w["sessions"])
                        if sum(s["movements"].get(g, []))
                    ]
                    n = len(w["sessions"])
                    if abs(nom[g]) > _band(nom[g], 1, g in PAIRED_GROUPS) and not days:
                        out["idle"] += 1
                    hosted_days[g] += len(days)
                    shares[g].append(len(days) / n if n else 0)
                    if len(days) >= 2 and n > 1:
                        idx = sorted(days)
                        gaps = [b - a for a, b in zip(idx, idx + [idx[0] + n])]
                        out["spread_num"] += (max(gaps) - min(gaps)) / n
                        out["spread_den"] += 1
                out["iv_micro"] += abs(week_tot - w["vol"])
                for s in w["sessions"]:
                    hosted = {g for g, z in s["movements"].items() if sum(z)}
                    if not slot_match(hosted):
                        out["clash"] += 1
                    out["gaps"] += _unjustified_gaps(s, w["sessions"], w["bins"])
                    for text, seq in scheme_entries(s):
                        t = tuple(seq)
                        out["instructions"] += complexity(t)
                        out["longest"] = max(out["longest"], len(t))
                        out["slots"] += 1
                        out["illegal"] += len(_entry_problems(text, seq, s))
                    for g, dose in session_dose(s).items():
                        score = prilepin_score(dose)
                        tol = _tolerance(BIN_GROUP[g])
                        out["excess"] += max(0.0, score - tol)
                        if score < FLOOR:
                            out["shortfall"] += FLOOR - score
            nweeks = len(m["weeks"])
            for g in GROUPS:
                actual = m["groups"].get(g, 0)
                out["ob_meso"] += max(
                    0,
                    abs(actual - meso_nom[g])
                    - _band(meso_nom[g], nweeks, g in PAIRED_GROUPS),
                )
                if (
                    abs(meso_nom[g]) > _band(meso_nom[g], nweeks, g in PAIRED_GROUPS)
                    and hosted_days[g] == 0
                ):
                    out["idle_meso"] += 1
                vals = shares[g]
                if vals:
                    out["meso_spread_num"] += max(vals) - min(vals)
                    out["meso_spread_den"] += 1
            out["iv_meso"] += abs(sum(m["groups"].values()) - m["vol"])
        for g in GROUPS:
            out["ob_macro"] += max(
                0,
                abs(macro_act[g] - macro_nom[g])
                - _band(macro_nom[g], 20, g in PAIRED_GROUPS),
            )
        out["iv_macro"] += abs(sum(macro_act.values()) - _macro_vol(cls))
    if seconds is not None:
        out["seconds"] = seconds
    return out


def _finalize(raw, seconds=None):
    strain = (raw["excess"] + raw["shortfall"]) / 150
    size = (raw["instructions"] / 9300 + raw["longest"] / 25) / 2
    rhythm = median(raw["rhythms"]) if raw["rhythms"] else 0.0
    spread_micro = raw["spread_num"] / raw["spread_den"] if raw["spread_den"] else 0.0
    spread_meso = (
        raw["meso_spread_num"] / raw["meso_spread_den"]
        if raw["meso_spread_den"]
        else 0.0
    )
    slow = max(0.0, (seconds if seconds is not None else 0.0) - 3) / 6
    drift = (
        raw["ob_micro"] / 40
        + raw["iv_micro"] / 40
        + raw["ob_meso"] / 160
        + raw["iv_meso"] / 160
        + raw["ob_macro"] / 800
        + raw["iv_macro"] / 800
        + 5 * (raw["illegal"] + raw["clash"] + raw["gaps"])
        + 2 * raw["idle"]
        + 4 * raw["idle_meso"]
        + spread_micro
        + spread_meso
        + slow
    )
    return {
        "excess": raw["excess"],
        "shortfall": raw["shortfall"],
        "strain": strain,
        "instructions": raw["instructions"],
        "longest": raw["longest"],
        "slots": raw["slots"],
        "size": size,
        "rhythm_weeks": list(raw["rhythms"]),
        "rhythm": rhythm,
        "ob_micro": raw["ob_micro"],
        "iv_micro": raw["iv_micro"],
        "ob_meso": raw["ob_meso"],
        "iv_meso": raw["iv_meso"],
        "ob_macro": raw["ob_macro"],
        "iv_macro": raw["iv_macro"],
        "illegal": raw["illegal"],
        "clash": raw["clash"],
        "gaps": raw["gaps"],
        "idle": raw["idle"],
        "idle_meso": raw["idle_meso"],
        "spread_micro": spread_micro,
        "spread_meso": spread_meso,
        "slow": slow,
        "drift": drift,
        "score": 0.4 * strain + 0.3 * size + 0.1 * rhythm + 0.2 * drift,
    }


def score_class(cls, plan=None, seconds=None):
    """Score one class; builds the plan unless one is given."""
    plan = build_plan(cls) if plan is None else plan
    return _finalize(_score_items([(cls, plan)], seconds), seconds)


def score_book(items=None, seconds=None):
    """Score the whole book; the totals are the same loop over classes."""
    from wlconfig import CLASSES as _CLASSES

    if items is None:
        items = [(cls, build_plan(cls)) for cls in _CLASSES]
    return _finalize(_score_items(items, seconds), seconds)


def score_ir(ir, seconds=None):
    """Score an intermediate-representation dict (parsed JSON)."""
    return score_class(ir["class"], from_ir(ir), seconds)


def _row(label, r):
    return (
        f"{label:8} strain {r['strain']:5.2f} (exc {r['excess']:6.1f} "
        f"short {r['shortfall']:5.1f}) | size {r['size']:4.2f} "
        f"(instr {r['instructions']:5d} longest {r['longest']:3d} "
        f"slots {r['slots']:4d}) | rhythm {r['rhythm']:4.2f} | drift "
        f"{r['drift']:6.2f} (off {r['ob_micro'] + r['ob_meso'] + r['ob_macro']:5.1f} "
        f"vol {r['iv_micro'] + r['iv_meso'] + r['iv_macro']:5.1f} "
        f"bad {r['illegal'] + r['clash'] + r['gaps'] + r['idle'] + r['idle_meso']:d} "
        f"spread {r['spread_micro'] + r['spread_meso']:4.2f}) | "
        f"score {r['score']:.3f}"
    )


def print_breakdown(r, label="plan"):
    print(_row(label, r))
    print(
        "  rhythm weeks: "
        + " ".join(f"{v:.1f}" for v in r["rhythm_weeks"])
        + f"  (median {r['rhythm']:.2f})"
    )


def audit(classes=None, seconds=None):
    """Build every class, score each plus the book, print the scoreboard."""
    import time

    from wlconfig import CLASSES as _CLASSES

    classes = list(classes or _CLASSES)
    if seconds is None:
        t0 = time.perf_counter()
        plans = [(cls, build_plan(cls)) for cls in classes]
        seconds = time.perf_counter() - t0
    else:
        plans = [(cls, build_plan(cls)) for cls in classes]
    for cls, plan in plans:
        print_breakdown(score_class(cls, plan), cls)
    print_breakdown(score_book(plans), "book")
    return seconds
