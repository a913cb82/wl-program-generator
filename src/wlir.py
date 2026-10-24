"""The intermediate representation: plain JSON between generation and use.

A plan is nested dicts and lists of ints and strings. Tuple pair keys
"(a, b)" become ""a+b"" strings and every other tuple becomes a list,
so the whole thing round-trips through json unchanged. from_ir
restores the tuples. Sessions may carry slots (see wlgen): each slot
holds the movement name, the atom scheme and its parsed items, all
tuple-restored the same way.
"""

from functools import cache

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


def to_ir(plan):
    """Plain-JSON version of a built plan. Copies structure only; any
    ``slots`` already attached to sessions ride along unchanged."""
    out = {
        "macro": plan["macro"],
        "class": plan["class"],
        "annual": plan["annual"],
        "groups": dict(plan["groups"]),
        "mesos": [],
    }
    for m in plan["mesos"]:
        weeks = []
        for w in m["weeks"]:
            sessions = []
            for s in w["sessions"]:
                entry = {
                    "size": s["size"],
                    "vol": s["vol"],
                    "base": s.get("base", "Day"),
                    "movements": {g: list(v) for g, v in s["movements"].items()},
                    "pairs": {
                        f"{a}+{b}": [ref, list(va), list(vb)]
                        for (a, b), (ref, va, vb) in s.get("pairs", {}).items()
                    },
                }
                if s.get("slots"):
                    entry["slots"] = [
                        {
                            "movement": sl["movement"],
                            "seq": [
                                [z, list(v) if isinstance(v, tuple) else v]
                                for z, v in sl["seq"]
                            ],
                            "items": sl["items"],
                        }
                        for sl in s["slots"]
                    ]
                sessions.append(entry)
            weeks.append(
                {
                    "vol": w["vol"],
                    "groups": dict(w["groups"]),
                    "sessions": sessions,
                    "bins": {g: list(v) for g, v in w["bins"].items()},
                }
            )
        out["mesos"].append(
            {
                "name": m["name"],
                "phase": m["phase"],
                "vol": m["vol"],
                "groups": dict(m["groups"]),
                "weeks": weeks,
            }
        )
    return out


def from_ir(ir):
    """Restore a built-plan structure from ``to_ir`` output (or its JSON
    round trip). Rendering and scoring accept the result as built."""
    plan = {
        "macro": ir["macro"],
        "class": ir["class"],
        "annual": ir["annual"],
        "groups": dict(ir["groups"]),
        "mesos": [],
    }
    for m in ir["mesos"]:
        weeks = []
        for w in m["weeks"]:
            sessions = []
            for s in w["sessions"]:
                pairs = {}
                for key, (ref, va, vb) in s.get("pairs", {}).items():
                    a, b = key.split("+")
                    pairs[(a, b)] = (ref, tuple(va), tuple(vb))
                entry = {
                    "size": s["size"],
                    "vol": s["vol"],
                    "base": s.get("base", "Day"),
                    "movements": {g: list(v) for g, v in s["movements"].items()},
                    "pairs": pairs,
                }
                if s.get("slots"):
                    entry["slots"] = [
                        {
                            "movement": sl["movement"],
                            "seq": _tuples(sl["seq"]),
                            "items": _tuples(sl["items"]),
                        }
                        for sl in s["slots"]
                    ]
                sessions.append(entry)
            weeks.append(
                {
                    "vol": w["vol"],
                    "groups": dict(w["groups"]),
                    "sessions": sessions,
                    "bins": {g: list(v) for g, v in w["bins"].items()},
                }
            )
        plan["mesos"].append(
            {
                "name": m["name"],
                "phase": m["phase"],
                "vol": m["vol"],
                "groups": dict(m["groups"]),
                "weeks": weeks,
            }
        )
    return plan
