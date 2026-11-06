"""Parse Takano's sample programs into (class, week, day, exercises).
Week/Day headers carry planned totals; exercise lines carry set schemes.
Tolerant of the PDF dump's damage: parenthesised counts, missing dashes,
bare rest days, "reps" for "repetitions", wrapped scheme tails, max-out
lines without percentages."""

import json
import re
import sys

sys.path.insert(0, "/tmp/wta/src")
from takano import EXERCISE_MAP

text = open("/tmp/takano.txt").read().split("\n")
cls_pat = re.compile(r"Sample\s+Class\s+(\d+)\s+Training\s+Program")
week_pat = re.compile(
    r"^Week\s*(\d+).*?\(?\s*(\d+)\s*\)?\s*(?:[Rr]epetitions|[Rr]eps?)\b"
)
meso_pat = re.compile(
    r"Week \d+\s*[—\-:]*\s*\((.*?)[Mm](?:esocycle|acrocycle)(?:\s*(\d+))?\)"
)
day_pat = re.compile(
    r"^Day\s*(\d+)\s*(?:[—\-:—]+\s*[A-Za-z,]*\s*)?"
    r"\(?\s*(\d+)?\s*\)?\s*([Rr]epetitions|[Rr]eps?)?([^A-Za-z(]*)$"
)
wd_pat = re.compile(
    r"^Day\s*\d+\s*[—\-:]+\s*(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
)
ex_pat = re.compile(r"^\d+\)\s*(.+?)[;:]\s*(\S.*)?$")
app_pat = re.compile(r"^APPENDIX")
colonless_pat = re.compile(r"^(\d+\)\s*)(.+)$")
LOG = []


def known_name(name):
    for key in sorted(EXERCISE_MAP, key=len, reverse=True):
        if name == key or name.startswith(key + " ") or name.startswith(key + ":"):
            return True
    return False


def split_name_body(line):
    m = re.match(r"^\d+\)\s*(.+?)[;:]\s*(\S.*)?$", line)
    if not m:
        return None, None
    return m.group(1).strip(), (m.group(2) or "").strip()


def is_exercise(line, day_open):
    if not ex_pat.match(line) or not day_open:
        return False
    name, body = split_name_body(line)
    if "/" in line:
        return True
    if body == "":
        return known_name(name)
    low = line.lower()
    if "max" in low and known_name(name):
        return True
    return False


programs = {}
cls = week = day = None
pending = None


def flush_pending():
    global pending
    pending = None


def cur():
    return (
        programs[cls][-1]["days"][-1]["ex"]
        if (cls and programs.get(cls) and programs[cls][-1]["days"])
        else None
    )


def cls_name(c):
    return {"3": "III", "2": "II", "1": "I"}.get(c, c)


done = False
for i, line in enumerate(text):
    line = line.strip()
    if done:
        continue
    if app_pat.match(line):
        done = True
        cls = week = day = None
        flush_pending()
        continue
    cm = colonless_pat.match(line)
    if cm and ":" not in cm.group(2) and ";" not in cm.group(2):
        for key in sorted(EXERCISE_MAP, key=len, reverse=True):
            rest = cm.group(2)
            if rest == key or rest.startswith(key + " ") or rest.startswith(key + "("):
                tail = rest[len(key) :].strip()
                if "/" in tail or "X/" in tail or "max" in tail.lower():
                    line = cm.group(1).rstrip() + " " + key + ": " + tail
                break
    m = cls_pat.match(line)
    if m:
        cls = cls_name(m.group(1))
        week = day = None
        programs.setdefault(cls, [])
        flush_pending()
        continue
    m = week_pat.match(line)
    if m and cls:
        mm = meso_pat.match(line)
        label = None
        if mm:
            # IMS week 1 reads 'Preparation mesocycle 1': keep the number
            label = mm.group(1).strip() + (f" {mm.group(2)}" if mm.group(2) else "")
        week = {
            "n": int(m.group(1)),
            "plan": int(m.group(2)),
            "days": [],
            "meso": label if label else "?",
        }
        programs[cls].append(week)
        day = None
        flush_pending()
        continue
    m = day_pat.match(line)
    if m and week is not None:
        n = int(m.group(1))
        count, reps, junk = m.group(2), m.group(3), m.group(4)
        if count and not reps and junk.strip(") "):
            LOG.append(f"day rejected (count without reps-word): {line!r}")
            flush_pending()
            continue
        days = week["days"]
        if days and n <= days[-1]["n"]:
            LOG.append(f"day rejected (not after {days[-1]['n']}): {line!r}")
            flush_pending()
            continue
        if count is None or count == "0":
            nxt = ""
            for ahead in text[i + 1 :]:
                a = ahead.strip()
                if a == "" or a in ("AM", "PM", "A M"):
                    continue
                nxt = a
                break
            if nxt.lower() not in (
                "rest",
                "competition",
                "day off",
            ) and not is_exercise(nxt, True):
                LOG.append(f"bare day rejected (next is {nxt[:40]!r}): {line!r}")
                flush_pending()
                continue
        wd = wd_pat.match(line)
        day = {
            "n": n,
            "plan": int(m.group(2)) if m.group(2) else 0,
            "ex": [],
            "weekday": wd.group(1) if wd else "?",
            "marks": [],
        }
        week["days"].append(day)
        flush_pending()
        continue
    if line in ("AM", "PM", "A M"):
        flush_pending()
        if day is not None:
            half = "AM" if line == "A M" else line
            day["marks"].append((len(day["ex"]), half))
        continue
    if is_exercise(line, day is not None):
        name, body = split_name_body(line)
        if body == "":
            day["ex"].append(f"1) {name}:")
            pending = f"1) {name}:"
        else:
            day["ex"].append(line)
            pending = line if line.rstrip().endswith(",") else None
        continue
    ex = cur()
    if (
        ex
        and pending is not None
        and ("%" in line or "X/" in line or ("max" in line.lower() and "(" in line))
    ):
        ex[-1] = pending + " " + line
        pending = ex[-1] if ex[-1].rstrip().endswith(",") else None
        continue
    if pending is not None and line == "":
        continue
    flush_pending()

print(
    "classes:",
    {c: (len(v), sum(len(w["days"]) for w in v)) for c, v in programs.items()},
)
dropped_bare = sum(1 for x in LOG if x.startswith("bare day rejected"))
print("bare-day rejects:", dropped_bare)
for x in LOG[:10]:
    print("  ", x)
# week planned vs day-sum consistency and day counts
for c, weeks in programs.items():
    bad = 0
    for w in weeks:
        s = sum(d["plan"] for d in w["days"])
        if abs(s - w["plan"]) > 2:
            bad += 1
    print(c, "weeks:", len(weeks), "plan-vs-days mismatches:", bad)


def split_blocks(day):
    """Exercise blocks split at standalone AM/PM marker indices.
    Each block takes the half of its preceding marker; a day with no
    markers is one whole-day block (half None). A leading unmarked
    block ahead of a PM marker is the implicit morning session, so it
    takes AM (book: >100-rep days split breakfast/afternoon)."""
    ex = day.get("ex", [])
    marks = sorted(day.get("marks", []))
    cuts = sorted(set([0] + [i for i, _ in marks] + [len(ex)]))
    blocks = []
    for s, e in zip(cuts, cuts[1:]):
        if e <= s:
            continue
        half = None
        for idx, h in marks:
            if idx <= s:
                half = h
            else:
                break
        blocks.append({"half": half, "ex": ex[s:e]})
    if len(blocks) > 1 and blocks[0]["half"] is None:
        LOG.append(f"leading block takes AM: {day.get('n')}")
        blocks[0]["half"] = "AM"
    if [b["half"] for b in blocks] not in ([[None], ["AM"], ["PM"], ["AM", "PM"]]):
        LOG.append(
            f"odd half pattern {[b['half'] for b in blocks]}: day {day.get('n')}"
        )
    day["blocks"] = blocks


for c, weeks in programs.items():
    for w in weeks:
        for d in w["days"]:
            split_blocks(d)
nhalf = sum(
    len(d["blocks"]) for weeks in programs.values() for w in weeks for d in w["days"]
)
nday = sum(len(w["days"]) for weeks in programs.values() for w in weeks)
print("days:", nday, "half-day blocks:", nhalf)
json.dump(programs, open("/tmp/takano_prog.json", "w"))
print("saved")
