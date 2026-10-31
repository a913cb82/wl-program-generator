"""The intermediate representation: the plan as pure training data.

The file JSON is only the class label and the sessions: each session
knows its mesocycle, week and weekday plus the executed slots (movement
name and atom scheme per slot). Volumes, groups, bins, nominals, names
and phases all derive from the sessions and the class ground truth
tables, for rendering and scoring. from_ir rebuilds the rich structure;
nothing redundant is stored.
"""

from functools import cache

from wlconfig import BIN_GROUP, BIN_ZONES, CLASSES, GROUPS

MACRO_DAYS_PER_WEEK = 7


@cache
def _allocate_cached(total, weights):
    raw = [total * w / sum(weights) for w in weights]
    out = [int(x) for x in raw]
    order = sorted(range(len(weights)), key=lambda i: raw[i] - out[i], reverse=True)
    for i in order[: total - sum(out)]:
        out[i] += 1
    return tuple(out)


def allocate(total, weights):
    """Largest-remainder split of total over weights. Memoized: week, meso
    and day cuts repeat the same shares across groups and classes."""
    return list(_allocate_cached(total, tuple(weights)))


def macro_days(macro):
    return MACRO_DAYS_PER_WEEK * sum(len(m[2]) for m in macro)


def _tuples(value):
    if isinstance(value, list):
        return tuple(_tuples(v) for v in value)
    if isinstance(value, dict):
        return {k: _tuples(v) for k, v in value.items()}
    return value


def atom_text(value):
    return str(value) if isinstance(value, int) else f"{value[0]}+{value[1]}"


@cache
def _render_items(items):
    parts = []
    for item in items:
        if item[0] == "wave":
            parts.append(f"{item[1]}*({_render_items(item[2])})")
        else:
            _, zlo, pairs = item
            body = ",".join(
                f"{atom_text(value)}*{count}" if count > 1 else atom_text(value)
                for value, count in pairs
            )
            parts.append(f"{zlo}%/{body}")
    return ", ".join(parts)


@cache
def _normalize(items):
    out: list = []
    for item in items:
        if (
            item[0] == "group"
            and out
            and out[-1][0] == "group"
            and out[-1][1] == item[1]
        ):
            out[-1] = ("group", item[1], out[-1][2] + tuple(item[2]))
        else:
            out.append(item)
    return tuple(out)


@cache
def _parse(seq):
    """Compact phrase tree: (phrase count, text, items)."""
    if not seq:
        return 0, "", ()
    best = None

    def take(count, items):
        nonlocal best
        text = _render_items(items)
        key = (count, len(text), text)
        if best is None or key < best[0]:
            best = (key, count, text, items)

    first = seq[0]
    j = 1
    while j < len(seq) and seq[j] == first:
        j += 1
    rest = _parse(seq[j:])
    count = 1 + rest[0]
    if best is None or count <= best[1]:
        take(count, _normalize((("group", first[0], ((first[1], j),)),) + rest[2]))
    for i in range(1, len(seq)):
        left = _parse(seq[:i])
        right = _parse(seq[i:])
        count = left[0] + right[0]
        if best is None or count <= best[1]:
            take(count, _normalize(left[2] + right[2]))
    for p in range(1, len(seq) // 2 + 1):
        k = 1
        while (k + 1) * p <= len(seq) and seq[k * p : (k + 1) * p] == seq[:p]:
            k += 1
        if k >= 2:
            inner = _parse(seq[:p])
            rest = _parse(seq[k * p :])
            count = inner[0] + rest[0]
            if best is None or count <= best[1]:
                take(count, _normalize((("wave", k, inner[2]),) + rest[2]))
    assert best is not None
    return best[1], best[2], best[3]


def _macro_vol(cls):
    return round(CLASSES[cls]["annual"] * macro_days(CLASSES[cls]["macro"]) / 365)


def meso_vol(cls, mi):
    """Planned mesocycle volume from the class ground truth tables."""
    return allocate(_macro_vol(cls), [m[3] for m in CLASSES[cls]["macro"]])[mi]


def week_vol(cls, mi, wi):
    """Planned week volume from the class ground truth tables."""
    return allocate(meso_vol(cls, mi), CLASSES[cls]["macro"][mi][2])[wi]


def _jsonable_seq(seq):
    return [[z, list(v) if isinstance(v, (list, tuple)) else v] for z, v in seq]


def to_ir(plan):
    """Minimal file JSON: the class label and the sessions. Each session
    carries its mesocycle, week and weekday plus the executed slots."""
    sessions = []
    for mi, m in enumerate(plan["mesos"]):
        for wi, w in enumerate(m["weeks"]):
            for s in w["sessions"]:
                if "slots" not in s:
                    raise ValueError(
                        "session is missing 'slots': attach them with "
                        "ir_with_slots before writing JSON"
                    )
                sessions.append(
                    {
                        "meso": mi,
                        "week": wi,
                        "day": s["day"],
                        "movements": {g: list(v) for g, v in s["movements"].items()},
                        "pairs": {
                            f"{a}+{b}": [ref, list(va), list(vb)]
                            for (a, b), (ref, va, vb) in s["pairs"].items()
                        },
                        "slots": [
                            {
                                "movement": sl["movement"],
                                "seq": _jsonable_seq(sl["seq"]),
                            }
                            for sl in s["slots"]
                        ],
                    }
                )
    return {"class": plan["class"], "sessions": sessions}


def _restore_sessions(stored, movements_list, vols):
    """Sessions back from stored JSON: pair keys split, seqs parsed."""
    sessions = []
    for s, movements, vol in zip(stored, movements_list, vols):
        pairs = {}
        for key, (ref, va, vb) in s["pairs"].items():
            a, b = key.split("+")
            pairs[(a, b)] = (ref, tuple(va), tuple(vb))
        seqs = [_tuples(sl["seq"]) for sl in s["slots"]]
        sessions.append(
            {
                "day": s["day"],
                "vol": vol,
                "movements": movements,
                "pairs": pairs,
                "slots": [
                    {
                        "movement": sl["movement"],
                        "seq": seq,
                        "items": _parse(seq)[2],
                    }
                    for sl, seq in zip(s["slots"], seqs)
                ],
            }
        )
    return sessions


def _week_entry(cls, mi, wi, sessions, vol=None):
    bins: dict = {}
    groups: dict = {g: 0 for g in GROUPS}
    vols = []
    for s in sessions:
        movements = {g: list(v) for g, v in s["movements"].items()}
        vols.append(sum(sum(v) for v in movements.values()))
        for g, vec in movements.items():
            groups[g] += sum(vec)
            row = bins.setdefault(g, [0] * len(vec))
            for z, n in enumerate(vec):
                row[z] += n
    for g in GROUPS:
        bins.setdefault(g, [0] * len(BIN_ZONES[BIN_GROUP[g]]))
    return {
        "vol": week_vol(cls, mi, wi) if vol is None else vol,
        "groups": groups,
        "sessions": [],
        "bins": bins,
        "_vols": vols,
        "_movements": [
            {g: list(v) for g, v in s["movements"].items()} for s in sessions
        ],
    }


def from_ir(ir):
    """Rebuild the rich plan from minimal JSON: sessions grouped into
    weeks and mesocycles, volumes and bins rolled up from the slots,
    nominals from the class ground truth tables. Rendering and scoring
    accept the result as built."""
    cls = ir["class"]
    by_week: dict = {}
    order: list = []
    for s in ir["sessions"]:
        key = (s["meso"], s["week"])
        if key not in by_week:
            by_week[key] = []
            order.append(key)
        by_week[key].append(s)
    meta = ir.get("mesos")
    if meta is not None:
        return _from_ir_stored(cls, ir.get("title"), meta, by_week, order)
    return _from_ir_macro(cls, by_week)


def _from_ir_stored(cls, title, meta, by_week, order):
    """Rebuild from the JSON's own mesocycle list: weeks come from the
    sessions themselves, never from a fixed grid. Volumes roll up from
    the slots; no prescription exists, so actuals stand as planned."""
    meso_ids = []
    for mi, _wi in order:
        if mi not in meso_ids:
            meso_ids.append(mi)
    mesos = []
    for mi in meso_ids:
        info = meta[mi] if mi < len(meta) else {}
        weeks = []
        for key in [k for k in order if k[0] == mi]:
            stored = by_week[key]
            actual = sum(
                sum(v) for s in stored for v in s["movements"].values()
            )
            entry = _week_entry(cls, mi, key[1], stored, vol=actual)
            entry["sessions"] = _restore_sessions(
                stored, entry["_movements"], entry["_vols"]
            )
            del entry["_vols"]
            del entry["_movements"]
            weeks.append(entry)
        mesos.append(
            {
                "name": info.get("name", f"Meso {mi + 1}"),
                "phase": info.get("phase", "prep"),
                "vol": sum(w["vol"] for w in weeks),
                "groups": {
                    g: sum(w["groups"][g] for w in weeks) for g in GROUPS
                },
                "weeks": weeks,
            }
        )
    return {
        "macro": title or f"Soviet year ({cls})",
        "class": cls,
        "annual": sum(m["vol"] for m in mesos),
        "groups": {g: sum(m["groups"][g] for m in mesos) for g in GROUPS},
        "mesos": mesos,
    }


def _from_ir_macro(cls, by_week):
    """Legacy rebuild over the class macro grid (our own minimal JSON,
    which carries no mesocycle list): planned volumes from the class
    ground truth tables."""
    macro = CLASSES[cls]["macro"]
    mesos = []
    for mi, (name, phase, _, _) in enumerate(macro):
        weeks = []
        for wi in range(len(macro[mi][2])):
            stored = by_week.get((mi, wi), [])
            entry = _week_entry(cls, mi, wi, stored)
            entry["sessions"] = _restore_sessions(
                stored, entry["_movements"], entry["_vols"]
            )
            del entry["_vols"]
            del entry["_movements"]
            weeks.append(entry)
        mesos.append(
            {
                "name": name,
                "phase": phase,
                "vol": meso_vol(cls, mi),
                "groups": {g: sum(w["groups"][g] for w in weeks) for g in GROUPS},
                "weeks": weeks,
            }
        )
    return {
        "macro": f"Soviet year ({cls})",
        "class": cls,
        "annual": CLASSES[cls]["annual"],
        "groups": {g: sum(m["groups"][g] for m in mesos) for g in GROUPS},
        "mesos": mesos,
    }
