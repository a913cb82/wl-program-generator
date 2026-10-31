"""Parse Takano's sample programs into (class, week, day, exercises).
Week/Day headers carry planned totals; exercise lines carry set schemes.
Tolerant of the PDF dump's damage: parenthesised counts, missing dashes,
bare rest days, "reps" for "repetitions", wrapped scheme tails, max-out
lines without percentages."""
import re, json, sys
sys.path.insert(0, '/home/abrai/projects/wl-program-generator/src')
from takano import EXERCISE_MAP

text = open('/tmp/takano.txt').read().split('\n')
cls_pat = re.compile(r'Sample\s+Class\s+(\d+)\s+Training\s+Program')
week_pat = re.compile(r'^Week\s*(\d+).*?\(?\s*(\d+)\s*\)?\s*(?:[Rr]epetitions|[Rr]eps?)\b')
meso_pat = re.compile(r'Week \d+ \((.+?)[Mm]esocycle\)')
day_pat = re.compile(
    r'^Day\s*(\d+)\s*(?:[—\-:—]+\s*[A-Za-z,]*\s*)?'
    r'\(?\s*(\d+)?\s*\)?\s*([Rr]epetitions|[Rr]eps?)?([^A-Za-z(]*)$'
)
wd_pat = re.compile(r'^Day\s*\d+\s*[—\-:]+\s*(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)')
ex_pat = re.compile(r'^\d+\)\s*(.+?)[;:]\s*(\S.*)?$')
app_pat = re.compile(r'^APPENDIX')
colonless_pat = re.compile(r'^(\d+\)\s*)(.+)$')
LOG = []


def known_name(name):
    for key in sorted(EXERCISE_MAP, key=len, reverse=True):
        if name == key or name.startswith(key + ' ') or name.startswith(key + ':'):
            return True
    return False


def split_name_body(line):
    m = re.match(r'^\d+\)\s*(.+?)[;:]\s*(\S.*)?$', line)
    if not m:
        return None, None
    return m.group(1).strip(), (m.group(2) or '').strip()


def is_exercise(line, day_open):
    if not ex_pat.match(line) or not day_open:
        return False
    name, body = split_name_body(line)
    if '/' in line:
        return True
    if body == '':
        return known_name(name)
    low = line.lower()
    if 'max' in low and known_name(name):
        return True
    return False


programs = {}
cls = week = day = None
pending = None


def flush_pending():
    global pending
    pending = None


def cur():
    return programs[cls][-1]['days'][-1]['ex'] if (
        cls and programs.get(cls) and programs[cls][-1]['days']
    ) else None


def cls_name(c):
    return {'3': 'III', '2': 'II', '1': 'I'}.get(c, c)


done = False
for i, l in enumerate(text):
    l = l.strip()
    if done:
        continue
    if app_pat.match(l):
        done = True
        cls = week = day = None
        flush_pending()
        continue
    cm = colonless_pat.match(l)
    if cm and ':' not in cm.group(2) and ';' not in cm.group(2):
        for key in sorted(EXERCISE_MAP, key=len, reverse=True):
            rest = cm.group(2)
            if rest == key or rest.startswith(key + ' ') or rest.startswith(
                key + '('
            ):
                tail = rest[len(key):].strip()
                if '/' in tail or 'X/' in tail or 'max' in tail.lower():
                    l = cm.group(1).rstrip() + ' ' + key + ': ' + tail
                break
    m = cls_pat.match(l)
    if m:
        cls = cls_name(m.group(1)); week = day = None
        programs.setdefault(cls, [])
        flush_pending()
        continue
    m = week_pat.match(l)
    if m and cls:
        mm = meso_pat.match(l)
        week = {'n': int(m.group(1)), 'plan': int(m.group(2)), 'days': [],
                'meso': mm.group(1).strip() if mm else '?'}
        programs[cls].append(week)
        day = None
        flush_pending()
        continue
    m = day_pat.match(l)
    if m and week is not None:
        n = int(m.group(1))
        count, reps, junk = m.group(2), m.group(3), m.group(4)
        if count and not reps and junk.strip(') '):
            LOG.append(f'day rejected (count without reps-word): {l!r}')
            flush_pending()
            continue
        days = week['days']
        if days and n <= days[-1]['n']:
            LOG.append(f'day rejected (not after {days[-1]["n"]}): {l!r}')
            flush_pending()
            continue
        if count is None or count == '0':
            nxt = ''
            for ahead in text[i + 1:]:
                a = ahead.strip()
                if a == '' or a in ('AM', 'PM', 'A M'):
                    continue
                nxt = a
                break
            if nxt.lower() not in ('rest', 'competition', 'day off') and not is_exercise(
                nxt, True
            ):
                LOG.append(f'bare day rejected (next is {nxt[:40]!r}): {l!r}')
                flush_pending()
                continue
        wd = wd_pat.match(l)
        day = {'n': n, 'plan': int(m.group(2)) if m.group(2) else 0, 'ex': [],
               'weekday': wd.group(1) if wd else '?'}
        week['days'].append(day)
        flush_pending()
        continue
    if l in ('AM', 'PM', 'A M'):
        flush_pending()
        continue
    if is_exercise(l, day is not None):
        name, body = split_name_body(l)
        if body == '':
            day['ex'].append(f'1) {name}:')
            pending = f'1) {name}:'
        else:
            day['ex'].append(l)
            pending = l if l.rstrip().endswith(',') else None
        continue
    ex = cur()
    if (ex and pending is not None
            and ('%' in l or 'X/' in l or ('max' in l.lower() and '(' in l))):
        ex[-1] = pending + ' ' + l
        pending = ex[-1] if ex[-1].rstrip().endswith(',') else None
        continue
    if pending is not None and l == '':
        continue
    flush_pending()

print('classes:', {c: (len(v), sum(len(w['days']) for w in v)) for c, v in programs.items()})
dropped_bare = sum(1 for x in LOG if x.startswith('bare day rejected'))
print('bare-day rejects:', dropped_bare)
for x in LOG[:10]:
    print('  ', x)
# week planned vs day-sum consistency and day counts
for c, weeks in programs.items():
    bad = 0
    for w in weeks:
        s = sum(d['plan'] for d in w['days'])
        if abs(s - w['plan']) > 2: bad += 1
    print(c, 'weeks:', len(weeks), 'plan-vs-days mismatches:', bad)
json.dump(programs, open('/tmp/takano_prog.json', 'w'))
print('saved')
