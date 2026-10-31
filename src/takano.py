"""Takano programs in our JSON format.

The source is the parsed PDF dump (tests/fixtures/takano_prog.json):
session lines in his notation, e.g. "Hang Power Snatch: 50%/3, 60%/3,
(70%/2)2". This module maps his exercise names to our groups, floors
his off-grid zones down to our ladders, infers a zone for unloaded X
sets from their reps, and builds schema-valid JSON (class + sessions
with movements, pairs and slots). from_ir loads III and II fully; the
58-week I program loads its overlapping prefix, the full file stays on
disk for direct analysis.
"""

import json
import re

from wlconfig import BIN_GROUP, BIN_ZONES, PAIR_REF
from wlir import to_ir

# Raw exercise name to our groups. Auditable: every name in the source
# appears here exactly. Decisions: & complexes stay combined, extension
# is a pull, behind-neck and rack jerks are assistance, jumping and
# overhead squats assist legs, bench presses with press, hinges and
# hypers are base work, lunges drop, unloaded X sets infer zone by reps.
EXERCISE_MAP = {
    "Back Squat": ("single", ("Squat",)),
    "Back Squats": ("single", ("Squat",)),
    "Behind the Neck Jerk Off Rack": ("single", ("Other Jerk",)),
    "Behind the Neck Power Jerk": ("single", ("Other Jerk",)),
    "Behind the Neck Push Press": ("single", ("Press",)),
    "Bench Press": ("single", ("Press",)),
    "Clean": ("single", ("Clean",)),
    "Clean & Jerk": ("pair", ("Clean", "Jerk")),
    "Clean Deadlift": ("single", ("ClPull",)),
    "Clean Deadlift (up in 10 seconds)": ("single", ("ClPull",)),
    "Clean Extension": ("single", ("ClPull",)),
    "Clean Extensions": ("single", ("ClPull",)),
    "Clean Halting Deadlift": ("single", ("ClPull",)),
    "Clean High Pull": ("single", ("ClPull",)),
    "Clean High Pull & Clean": ("pair", ("ClPull", "Clean")),
    "Clean High Pull and Clean": ("pair", ("ClPull", "Clean")),
    "Clean High Pull off blocks": ("single", ("ClPull",)),
    "Clean High Pulls": ("single", ("ClPull",)),
    "Clean deadlift": ("single", ("ClPull",)),
    "Cleans": ("single", ("Clean",)),
    "Front Squat": ("single", ("Other Squat",)),
    "Good Morning": ("single", ("Fundamental",)),
    "Halting Clean Deadlift with 2 Halts": ("single", ("ClPull",)),
    "Halting Clean Deadlift with 2 halts": ("single", ("ClPull",)),
    "Halting Snatch Deadlift with 2 Halts": ("single", ("SnPull",)),
    "Hang Clean": ("single", ("Clean",)),
    "Hang Power Clean": ("single", ("Other Clean",)),
    "Hang Power Snatch": ("single", ("Other Snatch",)),
    "Hang Snatch": ("single", ("Snatch",)),
    "Hang Snatch High Pulls from below Knees": ("single", ("SnPull",)),
    "Hyperextension": ("single", ("Fundamental",)),
    "Jerk": ("single", ("Jerk",)),
    "Jerk Behind Neck": ("single", ("Other Jerk",)),
    "Jerk Drive": ("single", ("Other Jerk",)),
    "Jerk off Rack": ("single", ("Jerk",)),
    "Jerk off rack": ("single", ("Jerk",)),
    "Jumping Back Squat": ("single", ("Other Squat",)),
    "Lunge": "drop",
    "Lunge with bar between legs": "drop",
    "Overhead Lunge": "drop",
    "Overhead Squat": ("single", ("Other Squat",)),
    "Power Clean": ("single", ("Other Clean",)),
    "Power Clean & Front Squat & Jerk": (
        "triple",
        ("Other Clean", "Other Squat", "Jerk"),
    ),
    "Power Clean & Front Squat and Jerk": (
        "triple",
        ("Other Clean", "Other Squat", "Jerk"),
    ),
    "Power Clean & Jerk": ("pair", ("Other Clean", "Jerk")),
    "Power Clean & Power Jerk": ("pair", ("Other Clean", "Other Jerk")),
    "Power Jerk": ("single", ("Other Jerk",)),
    "Power Snatch": ("single", ("Other Snatch",)),
    "Power Snatch & Behind the Neck Push Press": ("pair", ("Other Snatch", "Press")),
    "Power Snatch & Overhead Squat": ("pair", ("Other Snatch", "Other Squat")),
    "Press": ("single", ("Press",)),
    "Push Press": ("single", ("Press",)),
    "Romanian Deadlift": ("single", ("Fundamental",)),
    "Roumanian Deadlift": ("single", ("Fundamental",)),
    "Snatch": ("single", ("Snatch",)),
    "Snatch Deadlift": ("single", ("SnPull",)),
    "Snatch Deadlift on Block": ("single", ("SnPull",)),
    "Snatch Deadlift on blocks": ("single", ("SnPull",)),
    "Snatch Deadlift with 2 halts": ("single", ("SnPull",)),
    "Snatch Deadlifts (up in 10 seconds)": ("single", ("SnPull",)),
    "Snatch Deadlifts up in 15 seconds": ("single", ("SnPull",)),
    "Snatch Exensions": ("single", ("SnPull",)),
    "Snatch Extension": ("single", ("SnPull",)),
    "Snatch Extensions": ("single", ("SnPull",)),
    "Snatch High Pull": ("single", ("SnPull",)),
    "Snatch High Pull & Snatch": ("pair", ("SnPull", "Snatch")),
    "Snatch High Pull and Snatch": ("pair", ("SnPull", "Snatch")),
    "Snatch High Pull off blocks": ("single", ("SnPull",)),
    "Snatch High Pulls": ("single", ("SnPull",)),
    "Snatch off blocks": ("single", ("Snatch",)),
    "Squat Snatch Press": ("single", ("Press",)),
}

LOG: list = []

WEEKDAYS = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
}


def floor_zone(value, grid):
    """Round an off-grid zone down to our ladder; below-range lands base."""
    if value <= grid[0]:
        return grid[0]
    return max(z for z in grid if z <= value)


def infer_x_zone(reps):
    """Zone for unloaded sets from their reps: 4s sit 80-85, 7s 70-75."""
    if reps >= 7:
        return 75
    if reps >= 5:
        return 80
    if reps >= 3:
        return 85
    return 90


_TALLY_RE = re.compile(r"\s*\d+:\d+:[\d:]+\s*$")
_GROUP_RE = re.compile(
    r"^\(?\s*(X|\d+)%?\+?\s*(?:\+\s*\d+\s*Kg\s*)?"
    r"/\s*((?:[X\d]+(?:\s*\+\s*[X\d]+)*)?)\s*/?\)?\s*(\d*)\s*$"
)
_NOSLASH_RE = re.compile(r"^\(?\s*(\d+)%\s*(\d+)\s*\)?\s*(\d*)\s*$")
_SPLIT_RE = re.compile(r"\s+(?=\(?\s*(?:X|\d+)%?\s*/)")


def _space_split(text):
    """Split on spaces that start a new group, but never inside an
    unclosed paren: shredding "(A, B, (C)N" loses B to the comma."""
    parts, depth, cur = [], 0, ""
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "(":
            depth += 1
            cur += ch
        elif ch == ")":
            depth = max(0, depth - 1)
            cur += ch
        elif ch.isspace() and depth == 0 and _SPLIT_RE.match(text, i):
            parts.append(cur)
            cur = ""
            while i < len(text) and text[i].isspace():
                i += 1
            continue
        else:
            cur += ch
        i += 1
    parts.append(cur)
    return parts


def _depth(text):
    """Unclamped paren depth: positive means unclosed opens."""
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
    return depth


def _paren_split(text):
    """Split on commas outside parens; a parenthesised comma group
    "(A, B)N" is one wave chunk parsed inner-first below."""
    parts, depth, cur = [], 0, ""
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return parts


def _sets_for(zone, sides, repeat, complex) -> list[tuple[object, object]]:
    if zone == "X":
        zone = infer_x_zone(max(sides))
    if complex:
        return [(zone, sides if len(sides) > 1 else [sides[0], sides[0]])] * repeat
    return [(zone, s) for s in sides] * repeat


def parse_scheme(body, complex) -> list[tuple[object, object]]:
    """Flat set list from his scheme text: (zone, reps) singles with +
    meaning consecutive sets, (zone, [a, b]) complexes with + per side.
    Tallies and strays never match the group pattern and fall away;
    unbalanced parens from the PDF parse repair by balancing; max work
    becomes singles at 90."""
    sets: list[tuple[object, object]] = []
    for m in re.finditer(r"\bmax-(\d+)\b", body):
        sets.extend([(90, 1)] * int(m.group(1)))
    bare_max = bool(re.search(r"(?<!-)max(?![-\w])", body))
    text = re.sub(r"\bsingles to max\.?", "", body)
    text = re.sub(r"(?<!-)max(?![-\w])", "", text)
    text = re.sub(r"\bmax-\d+\b", "", text)
    text = _TALLY_RE.sub("", text)
    text, n1 = re.subn(r"(\d+)%(\d+)", r"\1%/\2", text)
    text, n2 = re.subn(r"(\d+)%/,(\d+)", r"\1%/\2", text)
    if n1 + n2:
        LOG.append(f"slash repaired x{n1 + n2}: {body!r}")
    chunks = []
    for comma_part in _paren_split(text):
        comma_part = comma_part.strip()
        if re.match(r"^\([^()]*\)\s*\d+\s*$", comma_part):
            chunks.append(comma_part)
        else:
            chunks.extend(_space_split(comma_part))
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        if _depth(chunk) > 0:
            LOG.append(f"unbalanced parens stripped: {chunk!r} in {body!r}")
            wm = re.match(r"^(.*)\)\s*(\d+)\s*$", chunk)
            if wm is not None:
                core, rep = wm.group(1), int(wm.group(2))
            else:
                core, rep = chunk, 1
            core = core.replace("(", "").replace(")", "")
            for _ in range(rep):
                for part in _paren_split(core):
                    for bit in _SPLIT_RE.split(part):
                        sets.extend(parse_scheme(bit.strip(), complex))
            continue
        gm = _GROUP_RE.match(chunk)
        if gm is None:
            tail = re.match(r"^(.*\S)\s+\d+\s*$", chunk)
            if tail is not None:
                gm = _GROUP_RE.match(tail.group(1))
                if gm is not None:
                    LOG.append(f"stray tail dropped: {chunk!r} in {body!r}")
        nm = None if gm is not None else _NOSLASH_RE.match(chunk)
        if gm is None:
            if nm is not None:
                LOG.append(f"slash restored: {chunk!r} in {body!r}")
                zraw, rraw, nraw = nm.groups()
            else:
                w = re.match(r"^\(([^()]*)\)\s*(\d+)\s*$", chunk)
                if w is not None:
                    for _ in range(int(w.group(2))):
                        for inner in _paren_split(w.group(1)):
                            sets.extend(parse_scheme(inner.strip(), complex))
                    continue
                if re.search(r"\d", chunk):
                    LOG.append(f"dropped chunk: {chunk!r} in {body!r}")
                continue
        else:
            assert gm is not None
            zraw, rraw, nraw = gm.groups()
        if not rraw.strip():
            LOG.append(f"no reps, dropped: {chunk!r} in {body!r}")
            continue
        sides: list = []
        for side in rraw.split("+"):
            side = side.strip().rstrip("/")
            if not side:
                continue
            if side == "X" or not side.isdigit():
                LOG.append(f"bad reps, dropped: {chunk!r} in {body!r}")
                sides = []
                break
            if int(side) > 10:
                LOG.append(f"absurd reps, dropped: {chunk!r} in {body!r}")
                sides = []
                break
            sides.append(int(side))
        if not sides:
            continue
        zone_nr = -1 if zraw == "X" else int(zraw)
        if zraw != "X" and not 40 <= zone_nr <= 120:
            LOG.append(f"zone out of range, dropped: {chunk!r} in {body!r}")
            continue
        sets.extend(
            _sets_for(
                zraw if zraw == "X" else zone_nr,
                sides,
                int(nraw) if nraw else 1,
                complex,
            )
        )
    if not sets and bare_max:
        sets.append((90, 1))
    return sets


def split_complex(members):
    """Split a triple into a known pair plus a single: adjacent members
    first, then first with last."""
    a, b, c = members
    for pair, single in (((a, b), (c,)), ((b, c), (a,)), ((a, c), (b,))):
        if pair in PAIR_REF or (pair[1], pair[0]) in PAIR_REF:
            return pair, single
    return (a, b), (c,)


def _add(vec, grid, zone, lifts):
    vec[grid.index(floor_zone(zone, grid))] += lifts


def build_session(ex_list, day):
    """One session in our JSON shape from his exercise lines."""
    movements: dict = {}
    pairs: dict = {}
    slots: list = []

    def mov(g):
        return movements.setdefault(g, [0] * len(BIN_ZONES[BIN_GROUP[g]]))

    def pair_slot(a, b, sets):
        ref = PAIR_REF.get((a, b), PAIR_REF.get((b, a), a))
        lo = BIN_ZONES[BIN_GROUP[ref]]
        va = [0] * len(lo)
        vb = [0] * len(lo)
        seq = []
        for zone, value in sets:
            z = floor_zone(zone, lo)
            sides = value if isinstance(value, list) else [value, value]
            va[lo.index(z)] += sides[0]
            vb[lo.index(z)] += sides[1]
            _add(mov(a), BIN_ZONES[BIN_GROUP[a]], zone, sides[0])
            _add(mov(b), BIN_ZONES[BIN_GROUP[b]], zone, sides[1])
            seq.append([z, list(sides)])
        pairs[(a, b)] = [ref, va, vb]
        slots.append({"movement": f"{a}+{b}", "seq": seq})

    for ex in ex_list:
        text = re.sub(r"^\d+\)\s*", "", ex).strip()
        text = text.replace(": ", " ")
        name = None
        for key in sorted(EXERCISE_MAP, key=len, reverse=True):
            if text == key or text.startswith(key + " ") or text.startswith(key + ":"):
                name = key
                break
        if name is None:
            LOG.append(f"unmapped exercise: {text!r}")
            continue
        body = text[len(name):].lstrip(":").strip()
        mapped = EXERCISE_MAP[name]
        if mapped == "drop":
            continue
        assert isinstance(mapped, tuple)
        kind, members = mapped
        if kind == "single":
            (g,) = members
            grid = BIN_ZONES[BIN_GROUP[g]]
            seq = []
            for zone, value in parse_scheme(body, False):
                z = floor_zone(zone, grid)
                sides = value if isinstance(value, list) else [value]
                for s in sides:
                    mov(g)[grid.index(z)] += s
                    seq.append([z, s])
            slots.append({"movement": g, "seq": seq})
        elif kind == "pair":
            a, b = members
            sets = [
                (zone, value if isinstance(value, list) else [value, value])
                for zone, value in parse_scheme(body, True)
            ]
            pair_slot(a, b, sets)
        else:
            pair, (single,) = split_complex(members)
            a, b = pair
            psets, ssets = [], []
            for zone, value in parse_scheme(body, True):
                sides = value if isinstance(value, list) else [value, value]
                psets.append((zone, sides[:2]))
                ssets.append((zone, sides[2] if len(sides) > 2 else sides[-1]))
            pair_slot(a, b, psets)
            grid = BIN_ZONES[BIN_GROUP[single]]
            seq = []
            for zone, reps in ssets:
                z = floor_zone(zone, grid)
                mov(single)[grid.index(z)] += reps
                seq.append([z, reps])
            slots.append({"movement": single, "seq": seq})
    return {
        "day": day,
        "movements": movements,
        "pairs": pairs,
        "slots": slots,
    }


def build_program(weeks):
    """Schema-valid JSON: sequential meso/week keys over our grid."""
    sessions = []
    for wk, w in enumerate(weeks):
        used = set()
        for day in w["days"]:
            d = WEEKDAYS.get(day.get("weekday"), None)
            if d is None or d in used:
                free = [i for i in range(6) if i not in used]
                assert free, f"week {wk} has no free day"
                d = free[0]
                LOG.append(f"week {wk}: weekday assigned to {d}")
            used.add(d)
            s = build_session(day["ex"], d)
            s["meso"] = wk // 4
            s["week"] = wk % 4
            sessions.append(s)
    return sessions


def main():
    global LOG
    with open("tests/fixtures/takano_prog.json") as f:
        data = json.load(f)
    for cls in ("III", "II", "I"):
        LOG = []
        sessions = build_program(data[cls])
        mesos = []
        for mi in range(max(s["meso"] for s in sessions) + 1):
            mesos.append(
                {
                    "weeks": [
                        {
                            "sessions": [
                                s
                                for s in sessions
                                if s["meso"] == mi and s["week"] == wi
                            ]
                        }
                        for wi in range(4)
                    ]
                }
            )
        ir = to_ir({"class": cls, "mesos": mesos})
        with open(f"tests/fixtures/takano-{cls}.json", "w") as f:
            json.dump(ir, f)
        print(cls, "sessions:", len(sessions), "log lines:", len(LOG))
        for line in LOG[:20]:
            print("   ", line)


if __name__ == "__main__":
    main()
