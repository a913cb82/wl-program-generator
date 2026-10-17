import re
from functools import cache
from itertools import product
from math import gcd
from pathlib import Path

from wlconfig import (
    BEAM,
    BEAM_JOINT,
    BIN_CLASS,
    BIN_GROUP,
    BIN_ZONES,
    BINS,
    BOUNDARY,
    CAP,
    CAP_DEV,
    CLASSES,
    CLEAN,
    DAY,
    DISPLAY_ZONES,
    EPS,
    FAN,
    FREE_SLOTS,
    GAP,
    GROUPS,
    JERK,
    MACRO,
    MIN_DOSE,
    PATTERNS,
    REP_CHANGE,
    REPS,
    SCHEDULES,
    SIZE_WEIGHT,
    TOL,
    VARIANTS,
)


def expand(slots):
    out: list = [()]
    for alts, lo, hi, optional in slots:
        choices = [*alts, *([None] if optional else [])]
        out = [o + (c,) for o in out for c in choices]
    return out


def allocate(total, weights):
    raw = [total * w / sum(weights) for w in weights]
    out = [int(x) for x in raw]
    order = sorted(range(len(weights)), key=lambda i: raw[i] - out[i], reverse=True)
    for i in order[: total - sum(out)]:
        out[i] += 1
    return out


def bounded_round(values, lo, hi, total):
    """Round to integers summing to total, staying in [lo, hi] when possible."""
    out = [min(max(int(v), lo[i]), hi[i]) for i, v in enumerate(values)]
    order = sorted(range(len(values)), key=lambda i: values[i] - out[i], reverse=True)
    while sum(out) < total:
        room = [i for i in order if out[i] < hi[i]]
        for i in room or order:
            if sum(out) == total:
                break
            out[i] += 1
    while sum(out) > total:
        room = [i for i in order[::-1] if out[i] > lo[i]]
        for i in room or order[::-1]:
            if sum(out) == total:
                break
            out[i] -= 1
    return out


def spread(nominal, remaining, tail):
    """One microcycle's group targets: re-spread the remaining meso target in
    proportion to the remaining nominal share, within a band around the
    nominal week. Deviations are capped as a share of the week volume."""
    raw = [
        remaining[i] * nominal[i] / tail[i] if tail[i] else 0.0
        for i in range(len(nominal))
    ]
    lo = [max(0, n - max(1, round(TOL * n))) for n in nominal]
    hi = [n + max(1, round(TOL * n)) for n in nominal]
    raw = [min(max(raw[i], lo[i]), hi[i]) for i in range(len(nominal))]
    pos = sum(max(0.0, raw[i] - nominal[i]) for i in range(len(nominal)))
    k = min(1.0, CAP_DEV * sum(nominal) / pos) if pos else 1.0
    raw = [nominal[i] + k * (raw[i] - nominal[i]) for i in range(len(nominal))]
    return bounded_round(raw, lo, hi, sum(nominal))


def ari(bins, zones):
    # a zone's nominal % is its lower edge + 1, matching the source ARI column
    return sum(b * (z + 1) for b, z in zip(bins, zones))


def shift(bins, zones, target):
    """Move bin mass between adjacent zones to hit a target average intensity."""
    out = list(bins)
    delta = target - ari(out, zones)
    step = zones[1] - zones[0]
    if delta > 0:
        for i in range(len(out) - 2, -1, -1):
            x = min(out[i], delta / step)
            out[i] -= x
            out[i + 1] += x
            delta -= step * x
            if delta < 1e-9:
                break
    elif delta < 0:
        for i in range(len(out) - 1, 0, -1):
            x = min(out[i], -delta / step)
            out[i] -= x
            out[i - 1] += x
            delta += step * x
            if delta > -1e-9:
                break
    return out


def taper(bins, bt):
    """Competition taper: snatch/C&J lose all zones at 90% and above."""
    if bt not in ("Snatch", "CJ"):
        return list(bins)
    out = [0.0 if z >= 90 else b for b, z in zip(bins, BIN_ZONES[bt])]
    total = sum(out)
    return [b / total for b in out]


def week_bins(cls, meso, week, group):
    """Zone fractions for one microcycle (0-based meso and week index).

    The yearly bins are the anchor: prep sits below them, comp above, and the
    volume-weighted mixture over the 5 mesos reproduces the yearly bins. A
    single class gap applies to every group. Only the last meso tapers.
    """
    bt = BIN_GROUP[group]
    zones = BIN_ZONES[bt]
    bins = BINS[BIN_CLASS[cls]][bt]
    g = GAP[cls]
    wp = sum(m[3] for m in MACRO if m[1] == "prep")
    wc = sum(m[3] for m in MACRO if m[1] == "comp")
    n_prep = sum(1 for m in MACRO if m[1] == "prep")
    if meso < n_prep:
        fan = (-g, 0, 0.8 * g) if cls in FAN else (0, 0, 0)
        delta = -wc * g + fan[meso]
    elif meso < len(MACRO) - 1:
        delta = wp * g
    else:
        if week == 3:
            return taper(bins, bt)
        delta = wp * g + (g if week == 2 else 0)
    return shift(bins, zones, ari(bins, zones) + delta)


def close_bins(counts):
    """Move one rep down into any empty zone so a week's bins are contiguous."""
    out = list(counts)
    used = [z for z, n in enumerate(out) if n]
    if not used:
        return out
    for z in range(used[0], used[-1]):
        if out[z]:
            continue
        src = next(zz for zz in range(z + 1, len(out)) if out[zz])
        out[z] += 1
        out[src] -= 1
    return out


def week_bin_lifts(cls, meso, week, group, lifts):
    """Split a group's weekly lifts across its zones (largest remainder)."""
    return close_bins(allocate(lifts, week_bins(cls, meso, week, group)))


def ipf(prior, rows, cols, iters=1000):
    """Fractional matrix with the given margins, shaped by prior. Returns None
    when the margins cannot be met (structural zeros or bad supply/demand)."""
    nr, nc = len(rows), len(cols)
    m = [[float(x) for x in row] for row in prior]
    for it in range(iters):
        for i in range(nr):
            s = sum(m[i])
            if s:
                m[i] = [x * rows[i] / s for x in m[i]]
        for j in range(nc):
            s = sum(m[i][j] for i in range(nr))
            if s:
                for i in range(nr):
                    m[i][j] *= cols[j] / s
        if (
            it % 10 == 9
            and all(abs(sum(m[i]) - rows[i]) < 1e-6 for i in range(nr))
            and all(
                abs(sum(m[i][j] for i in range(nr)) - cols[j]) < 1e-6 for j in range(nc)
            )
        ):
            return m
    return None


def feasible(prior, rows, cols):
    """True when the margins fit the support: an exact max-flow check."""
    nr, nc = len(rows), len(cols)
    n = nr + nc + 2
    src, sink = n - 2, n - 1
    graph: list = [[] for _ in range(n)]

    def edge(a, b, cap):
        graph[a].append([b, cap, len(graph[b])])
        graph[b].append([a, 0, len(graph[a]) - 1])

    for i in range(nr):
        if rows[i]:
            edge(src, i, rows[i])
    for j in range(nc):
        if cols[j]:
            edge(nr + j, sink, cols[j])
    for i in range(nr):
        for j in range(nc):
            if prior[i][j] > 0:
                edge(i, nr + j, 10**9)
    flow, total = 0, sum(rows)
    while total == sum(cols) and flow < total:
        parent: list = [None] * n
        parent[src] = (src, -1)
        queue = [src]
        while queue and parent[sink] is None:
            u = queue.pop(0)
            for k, (v, cap, _) in enumerate(graph[u]):
                if cap > 0 and parent[v] is None:
                    parent[v] = (u, k)
                    queue.append(v)
        if parent[sink] is None:
            break
        aug = total
        v = sink
        while v != src:
            u, k = parent[v]
            aug = min(aug, graph[u][k][1])
            v = u
        v = sink
        while v != src:
            u, k = parent[v]
            graph[u][k][1] -= aug
            graph[v][graph[u][k][2]][1] += aug
            v = u
        flow += aug
    return flow == total


def fit(prior, rows, cols):
    """Integer matrix with exact row/column sums, shaped by prior. Prior zeros
    are structural; returns None when the margins cannot be met."""
    m = ipf(prior, rows, cols)
    if m is None:
        return None
    nr, nc = len(rows), len(cols)
    if not feasible(prior, rows, cols):
        return None
    out = [[int(x) for x in row] for row in m]
    for i in range(nr):
        order = sorted(
            (j for j in range(nc) if prior[i][j] > 0),
            key=lambda j: m[i][j] - out[i][j],
            reverse=True,
        )
        for j in order[: rows[i] - sum(out[i])]:
            out[i][j] += 1
    for _ in range(sum(cols) + nr):
        diff = [cols[j] - sum(out[i][j] for i in range(nr)) for j in range(nc)]
        if not any(diff):
            break
        over = [j for j, d in enumerate(diff) if d < 0]
        under = [j for j, d in enumerate(diff) if d > 0]
        moved = False
        for j in over:
            for k in under:
                for i in sorted(range(nr), key=lambda i: -out[i][j]):
                    if out[i][j] > 0 and prior[i][k] > 0:
                        out[i][j] -= 1
                        out[i][k] += 1
                        moved = True
                        break
                if moved:
                    break
            if moved:
                break
        if not moved:
            break
    if any(sum(out[i]) != rows[i] for i in range(nr)):
        return None
    if any(sum(out[i][j] for i in range(nr)) != cols[j] for j in range(nc)):
        return None
    return out


def prune_doses(support, rows, cols):
    """Drop cells below a usable dose where the margins stay feasible."""
    p = [row[:] for row in support]
    for _ in range(20):
        m = ipf(p, rows, cols)
        if m is None:
            return None
        drops = sorted(
            (m[i][j], i, j)
            for i in range(len(rows))
            for j in range(len(cols))
            if 0 < m[i][j] < MIN_DOSE
        )
        if not drops:
            break
        changed = False
        for _, i, j in drops:
            if p[i][j] <= 0:
                continue
            row_ok = sum(1 for jj in range(len(cols)) if p[i][jj] > 0) > 1
            col_ok = sum(1 for ii in range(len(rows)) if p[ii][j] > 0) > 1
            if not (row_ok and col_ok):
                continue
            keep = p[i][j]
            p[i][j] = 0
            if feasible(p, rows, cols):
                changed = True
            else:
                p[i][j] = keep
        if not changed:
            break
    return p


def fit_session(prior, rows, cols):
    """Session fit: pick a matchable group set per session (one movement per
    slot), then drop cells below a usable dose."""
    idx = {g: i for i, g in enumerate(GROUPS)}
    p = resolve_slots(prior, rows, cols, idx, [0], limit=2000)
    if p is None:
        return None
    p = prune_doses(p, rows, cols)
    if p is None:
        return None
    return fit(p, rows, cols)


def resolve_slots(prior, rows, cols, idx, calls, limit):
    """Choose one matchable group set per session so the exact margins fit;
    heaviest matchings first, pruned by the margins staying feasible."""
    nr, nc = len(rows), len(cols)
    opts = []
    for j in range(nc):
        live = [GROUPS[i] for i in range(nr) if prior[i][j] > 0]
        opts.append(session_options(live, {g: prior[idx[g]][j] for g in live}))
    chosen = [None] * nc

    def build(upto):
        q = [[0.0] * nc for _ in rows]
        for k in range(upto + 1):
            used = chosen[k]
            assert used is not None
            for g in used:
                q[idx[g]][k] = 1.0
        return q

    def rec(j):
        if j == nc:
            q = build(nc - 1)
            return q if fit(q, rows, cols) is not None else None
        for opt in opts[j]:
            chosen[j] = opt
            calls[0] += 1
            if calls[0] > limit:
                return None
            q = build(j)
            for k in range(j + 1, nc):
                for i in range(nr):
                    if prior[i][k] > 0:
                        q[i][k] = 1.0
            if feasible(q, rows, cols):
                out = rec(j + 1)
                if out is not None:
                    return out
        chosen[j] = None
        return None

    return rec(0)


def session_options(live, weight):
    """Matchable group subsets of the day template, heaviest first."""
    slots = [set(alts) for alts, lo, hi, optional in DAY]
    opts = []

    def rec(k, used, chosen):
        if k == len(live):
            opts.append(tuple(chosen))
            return
        g = live[k]
        rec(k + 1, used, chosen)
        for s, alts in enumerate(slots):
            if s not in used and g in alts:
                rec(k + 1, used | {s}, chosen + [g])

    rec(0, set(), [])
    opts.sort(key=lambda groups: -sum(weight[g] for g in groups))
    return opts


def slot_assign(groups, values):
    """Assign groups to distinct template slots (largest volume first), so each
    X|Y slot is filled by exactly one movement. Returns the matched groups."""
    slots = [set(alts) for alts, lo, hi, optional in DAY]
    taken: dict = {}

    def place(g, seen):
        for k, alts in enumerate(slots):
            if g in alts and k not in seen:
                seen.add(k)
                if k not in taken or place(taken[k], seen):
                    taken[k] = g
                    return True
        return False

    for g in sorted(groups, key=lambda g: values[g], reverse=True):
        place(g, set())
    return set(taken.values())


def slot_match(groups):
    """True when every group can take a distinct template slot."""
    groups = set(groups)
    return len(slot_assign(groups, {g: 1 for g in groups})) == len(groups)


def week_quota(targets, vols, prev_last=None):
    """Soft host targets for the free slots. Each slot shares the week's days
    equally up to the min-dose cap; phases are staggered per slot so groups
    from different slots do not always land on the same days. A group that
    trained last week avoids the first day when another day is free."""
    n = len(vols)
    quota: dict = {}
    for si, slot in enumerate(DAY):
        if slot not in FREE_SLOTS:
            continue
        live = [g for g in slot[0] if targets[g] > 0]
        if not live:
            continue
        caps = {g: min(n, max(1, targets[g] // MIN_DOSE)) for g in live}
        h = dict.fromkeys(live, 0)
        left = n
        while left > 0:
            cand = [g for g in live if h[g] < caps[g]]
            if not cand:
                break
            g = min(cand, key=lambda g: (h[g], -targets[g]))
            h[g] += 1
            left -= 1
        used = set()
        for g in sorted(live, key=lambda g: -targets[g]):
            for k in range(h[g]):
                j = ((2 * k + 1) * n // (2 * h[g]) + si) % n
                while j in used:
                    j = (j + 1) % n
                if j == 0 and prev_last and g in prev_last:
                    alt = next((x for x in range(1, n) if x not in used), None)
                    if alt is not None:
                        j = alt
                used.add(j)
                quota.setdefault(g, set()).add(j)
    return quota


def session_prior(targets, nsessions, quota=None, prev_last=None):
    """Hostability weight per group x session. Quota days weigh 1, other days
    a small epsilon, so the feasible-support search prefers the spread-out
    calendar but can still move a host when the exact amounts need it."""
    free = {g for slot in FREE_SLOTS for g in slot[0]}
    out = []
    for g in GROUPS:
        if targets[g] <= 0:
            out.append([0.0] * nsessions)
            continue
        if quota is None or g not in free:
            out.append([1.0] * nsessions)
            continue
        days = quota.get(g, set())
        row = []
        for j in range(nsessions):
            w = 1.0 if j in days else EPS
            if j == 0 and prev_last and g in prev_last:
                w = BOUNDARY
            row.append(w)
        out.append(row)
    return out


def zone_alloc(counts, lifts):
    """Split one group's week zone counts over its sessions. A flat prior gives
    every session a share of every zone, so each carries its own warmup ramp;
    larger sessions pick up more of the top through the column totals."""
    ztop = max((z for z, c in enumerate(counts) if c), default=0)
    rows = counts[: ztop + 1]
    m = fit([[1.0] * len(lifts) for _ in rows], rows, lifts)
    close_ramps(m)
    return [[m[z][s] for z in range(len(rows))] for s in range(len(lifts))]


def close_ramps(m):
    """Swap reps between sessions until every session's zone profile is
    contiguous from its own base. Volumes and week totals stay exact.
    m is zone-major: m[zone][session]."""
    nz, ns = len(m), len(m[0])
    base = next((z for z in range(nz) if any(m[z])), nz)
    if base == nz:
        return m

    def pass_once():
        changed = False
        for s in range(ns):
            while True:
                gaps = [
                    z
                    for z in range(base, nz)
                    if m[z][s] == 0 and any(m[zz][s] for zz in range(z + 1, nz))
                ]
                moved = False
                for z in gaps:
                    up = next(zz for zz in range(z + 1, nz) if m[zz][s])
                    # a donor can spare a gap rep; pay with s's next rep
                    donor = next(
                        (d for d in range(ns) if d != s and m[z][d] >= 2), None
                    )
                    if donor is not None:
                        m[z][s] += 1
                        m[z][donor] -= 1
                        m[up][s] -= 1
                        m[up][donor] += 1
                        moved = True
                        break
                    # move s's lowest upper rep to a holder of the gap, and
                    # take the holder's own base rep back
                    for d in range(ns):
                        if d == s or m[z][d] == 0:
                            continue
                        top = max(ww for ww in range(nz) if m[ww][d])
                        if m[up][d] == 0 and top + 1 != up:
                            continue
                        low = next(ww for ww in range(nz) if m[ww][d])
                        m[up][s] -= 1
                        m[up][d] += 1
                        m[low][d] -= 1
                        m[low][s] += 1
                        moved = True
                        break
                    if moved:
                        break
                if not moved:
                    break
                changed = True
        return changed

    for _ in range(nz * ns + 4):
        if not pass_once():
            break
    return m


def macro_days(macro):
    return 7 * sum(len(m[2]) for m in macro)


def cap(vols, weights, cap=CAP):
    vols = list(vols)
    if sum(vols) > len(vols) * cap:
        return vols
    for _ in range(100):
        excess = sum(v - cap for v in vols if v > cap)
        if not excess:
            break
        room = [i for i, v in enumerate(vols) if v < cap]
        for i, v in enumerate(vols):
            if v > cap:
                vols[i] = cap
        add = allocate(excess, [weights[i] for i in room])
        for i, a in zip(room, add):
            vols[i] += a
    return vols


def day_split(vol, pattern):
    weights = [SIZE_WEIGHT[s] for s in pattern]
    vols = allocate(vol, weights)
    return vols, [{"size": s, "vol": v} for s, v in zip(pattern, cap(vols, weights))]


def sessions(vol):
    for n in (3, 4, 5, 6):
        vols, session_list = day_split(vol, PATTERNS[n])
        if max(vols) <= CAP or n == 6:
            return session_list


def week_sessions(vol, targets, nom, cls, mi, wi, prev_last=None):
    """First session-size variant the week can host: the cap-driven day count
    first, source variants in table order, canonical (first) pattern preferred."""
    for n in range(len(sessions(vol)), 7):
        for pattern in VARIANTS[n]:
            vols, session_list = day_split(vol, pattern)
            if max(vols) > CAP and n != 6:
                continue
            try:
                return plan_sessions(session_list, targets, nom, cls, mi, wi, prev_last)
            except ValueError:
                continue
    raise ValueError("week has no feasible session-size variant")


@cache
def week_units(cls, mi, wi, t):
    """Paired units in the heavy, mid and light ratio tiers."""
    lo = BIN_ZONES[BIN_GROUP["Clean"]]
    counts = week_bin_lifts(cls, mi, wi, CLEAN[0], t)
    return (
        sum(c for c, z in zip(counts, lo) if z >= 90),
        sum(c for c, z in zip(counts, lo) if z == 80),
        sum(c for c, z in zip(counts, lo) if z < 80),
    )


def pair_options(c, h, cls, mi, wi):
    """Legal tier schedules for one session, closest to (c, h) first."""
    out = []
    for t in range(max(1, (c + h) // 5 - 2), (c + h) // 2 + 2):
        heavy, mid, light = week_units(cls, mi, wi, t)
        for rh, rm, rl in SCHEDULES:
            ac = rh[0] * heavy + rm[0] * mid + rl[0] * light
            aj = rh[1] * heavy + rm[1] * mid + rl[1] * light
            out.append((abs(ac - c) + abs(aj - h), -(ac + aj), ac, aj, t, (rh, rm, rl)))
    out.sort()
    return out


def pair_fit(moved, vols, targets, nom, prior, cls, mi, wi):
    """Snap every session that hosts a clean and a jerk to one small ratio,
    then refit the other groups. Week targets flex to what was planned."""
    idx = {g: i for i, g in enumerate(GROUPS)}
    pair = {}
    for j in range(len(vols)):
        c = next((g for g in CLEAN if moved[idx[g]][j]), None)
        h = next((g for g in JERK if moved[idx[g]][j]), None)
        if c and h:
            pair[j] = (c, h)
    if not pair:
        return moved, {}
    jlist = list(pair)
    free = [i for i, g in enumerate(GROUPS) if g not in CLEAN + JERK]
    lo = [nom[GROUPS[i]] - max(1, round(TOL * nom[GROUPS[i]])) for i in free]
    hi = [nom[GROUPS[i]] + max(1, round(TOL * nom[GROUPS[i]])) for i in free]
    prior = prior or session_prior(targets, len(vols))

    def snap(combo):
        work = [row[:] for row in moved]
        pairs = {}
        for j, (_, _, ac, aj, t, sched) in zip(jlist, combo):
            c, h = pair[j]
            work[idx[c]][j] = ac
            work[idx[h]][j] = aj
            pairs[j] = (c, h, ac, aj, t, sched)
        return work, pairs

    def band_excess(work):
        return sum(
            max(0, abs(sum(work[idx[g]]) - nom[g]) - max(1, round(TOL * nom[g])))
            for g in CLEAN + JERK
        )

    combos = list(
        product(
            *(
                pair_options(
                    moved[idx[pair[j][0]]][j],
                    moved[idx[pair[j][1]]][j],
                    cls,
                    mi,
                    wi,
                )[:6]
                for j in jlist
            )
        )
    )
    for strict in (True, False):
        ordered = (
            combos if strict else sorted(combos, key=lambda c: band_excess(snap(c)[0]))
        )
        for combo in ordered:
            work, pairs = snap(combo)
            if strict and band_excess(work):
                continue
            if any(
                sum(work[idx[g]][j] for g in CLEAN + JERK) > vols[j]
                for j in range(len(vols))
            ):
                continue
            delta = sum(sum(work[idx[g]]) for g in CLEAN + JERK) - sum(
                targets[g] for g in CLEAN + JERK
            )
            rows = [targets[GROUPS[i]] for i in free]
            step = -1 if delta > 0 else 1
            for _ in range(abs(delta)):
                room = [k for k in range(len(rows)) if lo[k] <= rows[k] + step <= hi[k]]
                if not room:
                    break
                k = max(
                    room,
                    key=lambda k: (hi[k] - rows[k]) if step > 0 else (rows[k] - lo[k]),
                )
                rows[k] += step
            if sum(rows) - sum(targets[GROUPS[i]] for i in free) != -delta:
                continue
            fixed = [0] * len(GROUPS)
            for i, v in zip(free, rows):
                fixed[i] = v
            cols = [
                vols[j] - sum(work[idx[g]][j] for g in CLEAN + JERK)
                for j in range(len(vols))
            ]
            block = [row[:] for row in prior]
            for g in CLEAN + JERK:
                block[idx[g]] = [0.0] * len(vols)
            support = resolve_slots(block, fixed, cols, idx, [0], limit=2000)
            if support is None:
                continue
            support = prune_doses(support, fixed, cols)
            if support is None:
                continue
            rest = fit(support, fixed, cols)
            if rest is None:
                continue
            for i in free:
                for j in range(len(vols)):
                    work[i][j] = rest[i][j]
            for i, g in enumerate(GROUPS):
                targets[g] = sum(work[i])
            return work, pairs
    return None, None


def pair_zones(cls, mi, wi, pairs):
    """One zone list per movement from the shared clean+jerk unit blocks.

    The tier schedule fixes each zone's ratio; the actual clean/jerk totals are
    returned too, so the free groups can absorb any rounding difference.
    """
    jlist = list(pairs)
    units = [pairs[j][4] for j in jlist]
    counts = week_bin_lifts(cls, mi, wi, CLEAN[0], sum(units))
    top = max((z for z, c in enumerate(counts) if c), default=0)
    counts = counts[: top + 1]
    m = fit([[1.0] * len(units) for _ in counts], counts, units)
    close_ramps(m)
    lo = BIN_ZONES[BIN_GROUP["Clean"]]
    out = {}
    actual = {}
    for k, j in enumerate(jlist):
        c, h, _ac, _aj, _t, (rh, rm, rl) = pairs[j]
        ratios = [
            rh if lo[z] >= 90 else rm if lo[z] == 80 else rl for z in range(len(counts))
        ]
        out[(j, c)] = [r[0] * m[z][k] for z, r in enumerate(ratios)]
        out[(j, h)] = [r[1] * m[z][k] for z, r in enumerate(ratios)]
        actual[j] = (sum(out[(j, c)]), sum(out[(j, h)]))
    return out, actual


def plan_sessions(session_list, targets, nom, cls, mi, wi, prev_last=None):
    """Fill each day with the day template and exact group x zone lifts."""
    vols = [s["vol"] for s in session_list]
    rows = [targets[g] for g in GROUPS]
    quota = week_quota(targets, vols, prev_last)
    prior = session_prior(targets, len(vols), quota, prev_last)
    moved = fit_session(prior, rows, vols)
    if moved is None:
        raise ValueError("week has no session mix that hosts every group")
    moved, pairs = pair_fit(moved, vols, targets, nom, prior, cls, mi, wi)
    if moved is None:
        raise ValueError("week has no session mix that hosts every group")
    for s in session_list:
        s["base"] = "Day"
        s["movements"] = {}
    paired, actual = pair_zones(cls, mi, wi, pairs) if pairs else ({}, {})
    idx = {g: i for i, g in enumerate(GROUPS)}
    free = [i for i, g in enumerate(GROUPS) if g not in CLEAN + JERK]
    for j, (c, h, _ac, _aj, _t, _s) in pairs.items():
        tc, tj = moved[idx[c]][j], moved[idx[h]][j]
        ac, aj = actual[j]
        moved[idx[c]][j] = ac
        moved[idx[h]][j] = aj
        need = tc + tj - ac - aj
        while need > 0:
            here = [i for i in free if moved[i][j] > 0]
            i = max(
                here,
                key=lambda i: (
                    nom[GROUPS[i]] + max(1, round(TOL * nom[GROUPS[i]])) - sum(moved[i])
                ),
                default=None,
            )
            if i is None:
                break
            moved[i][j] += 1
            need -= 1
        while need < 0:
            here = [i for i in free if moved[i][j] > 0]
            i = max(
                here,
                key=lambda i: (
                    sum(moved[i]) - nom[GROUPS[i]] + max(1, round(TOL * nom[GROUPS[i]]))
                ),
                default=None,
            )
            if i is None:
                break
            moved[i][j] -= 1
            need += 1
    for i, g in enumerate(GROUPS):
        targets[g] = sum(moved[i])
    for i, g in enumerate(GROUPS):
        targets[g] = sum(moved[i])
    for s in session_list:
        s["base"] = "Day"
        s["movements"] = {}
    for i, g in enumerate(GROUPS):
        nz = len(BIN_ZONES[BIN_GROUP[g]])
        active = [j for j in range(len(vols)) if moved[i][j] and (j, g) not in paired]
        if active:
            counts = week_bin_lifts(cls, mi, wi, g, sum(moved[i][j] for j in active))
            zones = zone_alloc(counts, [moved[i][j] for j in active])
            for j, z in zip(active, zones):
                session_list[j]["movements"][g] = z + [0] * (nz - len(z))
        for j in range(len(vols)):
            if (j, g) in paired:
                z = paired[(j, g)]
                session_list[j]["movements"][g] = z + [0] * (nz - len(z))
    return session_list


def session_bins(sessions):
    """Week zone totals exactly as planned in the session bullets."""
    out = {}
    for g in GROUPS:
        nz = len(BIN_ZONES[BIN_GROUP[g]])
        out[g] = [
            sum(s["movements"].get(g, [0] * nz)[z] for s in sessions) for z in range(nz)
        ]
    return out


# plans are deterministic; cache so repeated builds (e.g. tests) are cheap
@cache
def build_plan(cls):
    annual = CLASSES[cls]["annual"]
    macro, ratios = CLASSES[cls]["macro"], CLASSES[cls]["ratios"]
    macro_vol = round(annual * macro_days(macro) / 365)
    mesos = []
    prev_last = None
    for mi, ((name, phase, split, _), vol) in enumerate(
        zip(macro, allocate(macro_vol, [m[3] for m in macro]))
    ):
        week_vols = allocate(vol, split)
        nominal = [
            dict(
                zip(
                    GROUPS,
                    allocate(wv, [ratios[phase][i] for i in range(len(GROUPS))]),
                )
            )
            for wv in week_vols
        ]
        targets = {g: sum(n[g] for n in nominal) for g in GROUPS}
        planned = {g: 0 for g in GROUPS}
        weeks = []
        for wi, (wv, nom) in enumerate(zip(week_vols, nominal)):
            tail = {g: sum(n[g] for n in nominal[wi:]) for g in GROUPS}
            remaining = {g: targets[g] - planned[g] for g in GROUPS}
            groups = dict(
                zip(
                    GROUPS,
                    spread(
                        [nom[g] for g in GROUPS],
                        [remaining[g] for g in GROUPS],
                        [tail[g] for g in GROUPS],
                    ),
                )
            )
            sessions = week_sessions(wv, groups, nom, cls, mi, wi, prev_last)
            prev_last = set(sessions[-1]["movements"]) if sessions else None
            weeks.append(
                {
                    "vol": wv,
                    "groups": groups,
                    "sessions": sessions,
                    "bins": session_bins(sessions),
                }
            )
            for g in GROUPS:
                planned[g] += groups[g]
        mesos.append(
            {
                "name": name,
                "phase": phase,
                "vol": vol,
                "weeks": weeks,
                "groups": {g: sum(w["groups"][g] for w in weeks) for g in GROUPS},
            }
        )
    return {
        "macro": f"Soviet year ({cls})",
        "class": cls,
        "annual": annual,
        "mesos": mesos,
        "groups": {g: sum(m["groups"][g] for m in mesos) for g in GROUPS},
    }


def group_table(groups):
    return ["| Group | Lifts |", "|---|---|"] + [
        f"| {g} | {v} |" for g, v in groups.items() if v
    ]


def bin_header(title):
    labels = [f"{z}%" for z in DISPLAY_ZONES]
    return [
        f"| {title} | Lifts | " + " | ".join(labels) + " | ARI |",
        "|" + "---|" * (len(DISPLAY_ZONES) + 3),
    ]


def bin_line(group, total, counts):
    lo = BIN_ZONES[BIN_GROUP[group]]
    cells = [
        str(counts[lo.index(z)]) if z in lo and counts[lo.index(z)] else ""
        for z in DISPLAY_ZONES
    ]
    return (
        f"| {group} | {total} | "
        + " | ".join(cells)
        + f" | {ari(counts, lo) / total:.1f} |"
    )


def week_table(groups, bins):
    """Week group totals with each group split across its intensity zones."""
    lines = bin_header("Group")
    for g, v in groups.items():
        if v:
            lines.append(bin_line(g, v, bins[g]))
    return lines


def fill(n, reps):
    """Exact rep split: fewest sets, then largest smallest and largest set."""
    if not n:
        return []
    reps = sorted(set(reps) | {1}, reverse=True)
    best = None

    def rec(i, rem, parts):
        nonlocal best
        if rem == 0:
            key = (len(parts), -min(parts), -max(parts), tuple(parts))
            if best is None or key < best[0]:
                best = (key, parts)
            return
        if i == len(reps):
            return
        r = reps[i]
        for k in range(rem // r, -1, -1):
            rec(i + 1, rem - k * r, parts + [r] * k)

    rec(0, n, [])
    assert best is not None
    return best[1]


def sets_text(parts):
    """Grouped single-lift sets, e.g. 4x3,2x2, 4,3 or 3."""
    if len(parts) == 1:
        return str(parts[0])
    if len(set(parts)) == 1:
        return f"{len(parts)}x{parts[0]}"
    runs: list = []
    for part in parts:
        if runs and runs[-1][0] == part:
            runs[-1][1] += 1
        else:
            runs.append([part, 1])
    return ",".join(f"{n}x{r}" if n > 1 else str(r) for r, n in runs)


def complex_text(parts):
    """Grouped clean+jerk complexes, e.g. 5x3+1 or 3+3,2x2+2."""
    if len(parts) == 1:
        return parts[0]
    if len(set(parts)) == 1:
        return f"{len(parts)}x{parts[0]}"
    runs: list = []
    for part in parts:
        if runs and runs[-1][0] == part:
            runs[-1][1] += 1
        else:
            runs.append([part, 1])
    return ",".join(f"{n}x{r}" if n > 1 else r for r, n in runs)


def pair_fill(a, b, zlo):
    """Complex sets for a clean+jerk zone; size capped by the zone's reps."""
    m = gcd(a, b)
    p, q = a // m, b // m
    kmax = max(1, max(REPS["CJ"][zlo]) // max(p, q))
    return [(k * p, k * q) for k in fill(m, tuple(range(kmax, 0, -1)))]


def atom_total(value):
    return value if isinstance(value, int) else value[0] + value[1]


def atom_text(value):
    return str(value) if isinstance(value, int) else f"{value[0]}+{value[1]}"


def pref_min(family, zlo):
    return min(REPS[family][zlo])


def below_min(seq, family):
    total = 0
    for zlo, value in seq:
        size = max(value) if isinstance(value, tuple) else value
        total += max(0, pref_min(family, zlo) - size)
    return total


def run_penalty(seq):
    """Warm-up cost of a zone run followed by a heavier zone. A 1-set run is
    free once the heavier zone has already been visited; 3+ sets still cost."""
    runs: list = []
    for zlo, _ in seq:
        if runs and runs[-1][0] == zlo:
            runs[-1][1] += 1
        else:
            runs.append([zlo, 1])
    total = 0
    seen = set()
    for i, (zlo, n) in enumerate(runs):
        seen.add(zlo)
        if i + 1 < len(runs) and runs[i + 1][0] > zlo and runs[i + 1][0] not in seen:
            total += 1 if n == 1 else 0 if n == 2 else n - 1
    return total


def rep_changes(seq):
    """Rep changes inside one contiguous zone run."""
    total = 0
    last_zone = None
    last_value = None
    for zlo, value in seq:
        if zlo == last_zone and atom_total(value) != atom_total(last_value):
            total += 1
        last_zone, last_value = zlo, value
    return total


@cache
def phrases(seq):
    """Fewest compact phrases; a repeated wave adds no phrase for its count."""
    if not seq:
        return 0
    n = len(seq)
    best = 1 + phrases(seq[1:])
    j = 1
    while j < n and seq[j] == seq[0]:
        j += 1
    best = min(best, 1 + phrases(seq[j:]))
    for p in range(2, n // 2 + 1):
        k = 1
        while (k + 1) * p <= n and seq[k * p : (k + 1) * p] == seq[:p]:
            k += 1
        if k >= 2:
            best = min(best, phrases(seq[:p]) + phrases(seq[k * p :]))
    return best


def scheme_cost(seq, family):
    below = below_min(seq, family)
    run = run_penalty(seq)
    rep = rep_changes(seq)
    ph = phrases(seq)
    sets = len(seq)
    cost = 100 * below + 10 * run + REP_CHANGE * rep + 3 * ph + sets
    return cost, below, run, rep, ph, sets


@cache
def _render_items(items):
    parts = []
    for item in items:
        if item[0] == "wave":
            parts.append(f"{item[1]}x({_render_items(item[2])})")
        else:
            _, zlo, pairs = item
            body = ",".join(
                f"{count}x{atom_text(value)}" if count > 1 else atom_text(value)
                for value, count in pairs
            )
            parts.append(f"{body}@{zlo}%")
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
    take(
        1 + rest[0],
        _normalize((("group", first[0], ((first[1], j),)),) + rest[2]),
    )
    for i in range(1, len(seq)):
        left = _parse(seq[:i])
        right = _parse(seq[i:])
        take(left[0] + right[0], _normalize(left[2] + right[2]))
    for p in range(1, len(seq) // 2 + 1):
        k = 1
        while (k + 1) * p <= len(seq) and seq[k * p : (k + 1) * p] == seq[:p]:
            k += 1
        if k >= 2:
            inner = _parse(seq[:p])
            rest = _parse(seq[k * p :])
            take(inner[0] + rest[0], _normalize((("wave", k, inner[2]),) + rest[2]))
    assert best is not None
    return best[1], best[2], best[3]


@cache
def compact_text(seq):
    return _parse(tuple(seq))[1]


def _transition_ok(prev_zone, prev_value, zone, value, seen, present):
    if zone not in seen and seen and zone < max(seen):
        return False
    if prev_zone is not None and zone > prev_zone:
        nxt = next((z for z in present if z > prev_zone), None)
        if zone != nxt:
            return False
    return not (
        prev_zone is not None
        and zone >= prev_zone
        and atom_total(value) > atom_total(prev_value)
    )


def single_zones(counts, family):
    """Allowed set sizes per zone: (zone, total reps, ((size, value), ...))."""
    lo = BIN_ZONES[family]
    return tuple(
        (
            lo[z],
            n,
            tuple((r, r) for r in sorted(set(REPS[family][lo[z]]) | {1}, reverse=True)),
        )
        for z, n in enumerate(counts)
        if n
    )


def cj_zones(clean, jerk):
    """Clean+jerk zones: size is the shared unit count, value is the complex."""
    lo = BIN_ZONES["CJ"]
    out = []
    for z, (a, b) in enumerate(zip(clean, jerk)):
        if not (a or b):
            continue
        m = gcd(a, b)
        p, q = a // m, b // m
        kmax = max(1, max(REPS["CJ"][lo[z]]) // max(p, q))
        out.append((lo[z], m, tuple((k, (k * p, k * q)) for k in range(kmax, 0, -1))))
    return tuple(out)


@cache
def beam_search(zones, family):
    """Best legal fill and order under the session score; all styles compete."""
    present = tuple(z for z, _, _ in zones)
    start: tuple = (
        tuple(c for _, c, _ in zones),
        None,
        None,
        frozenset(),
        0,
        0,
        0,
        0,
        (),
    )
    beam: list = [start]
    finished: list = []

    def key(state):
        _caps, _lz, _lv, _seen, _rl, below, run, rep, prefix = state
        ph = phrases(prefix)
        return (
            100 * below + 10 * run + REP_CHANGE * rep + 3 * ph + len(prefix),
            ph,
            len(prefix),
        )

    while beam:
        nxt = []
        for (
            caps,
            last_zone,
            last_value,
            seen,
            run_len,
            below,
            run,
            rep,
            prefix,
        ) in beam:
            if not any(caps):
                ph = phrases(prefix)
                finished.append(
                    (
                        100 * below
                        + 10 * run
                        + REP_CHANGE * rep
                        + 3 * ph
                        + len(prefix),
                        ph,
                        prefix,
                    )
                )
                continue
            for i, (zone, _cap, choices) in enumerate(zones):
                current = caps[i]
                if not current:
                    continue
                for size, value in choices:
                    if size > current:
                        continue
                    if not _transition_ok(
                        last_zone, last_value, zone, value, seen, present
                    ):
                        continue
                    new_caps = list(caps)
                    new_caps[i] -= size
                    new_seen = seen | {zone}
                    amount = max(value) if isinstance(value, tuple) else value
                    new_below = below + max(0, pref_min(family, zone) - amount)
                    new_run, new_rep, new_run_len = run, rep, run_len
                    if last_zone is not None and zone == last_zone:
                        new_run_len = run_len + 1
                        if atom_total(value) != atom_total(last_value):
                            new_rep = rep + 1
                    else:
                        if (
                            last_zone is not None
                            and zone > last_zone
                            and zone not in seen
                        ):
                            n = run_len
                            new_run = run + (1 if n == 1 else 0 if n == 2 else n - 1)
                        new_run_len = 1
                    nxt.append(
                        (
                            tuple(new_caps),
                            zone,
                            value,
                            new_seen,
                            new_run_len,
                            new_below,
                            new_run,
                            new_rep,
                            prefix + ((zone, value),),
                        )
                    )
        alive = []
        for state in nxt:
            caps, _lz, _lv, seen, _rl, _below, _run, _rep, _prefix = state
            top = max(seen, default=-1)
            if any(
                caps[i] > 0 and z not in seen and z < top
                for i, (z, _cap, _choices) in enumerate(zones)
            ):
                continue
            alive.append(state)
        alive.sort(key=key)
        beam = alive[:BEAM_JOINT]
    if not finished:
        # All-ones ladder is always legal; only used if the beam is too narrow.
        ordered = []
        for zone, cap, choices in zones:
            for _ in range(cap):
                ordered.append((zone, choices[-1][1]))
        return tuple(ordered)
    best_cost, best_phrases, _ = min(finished, key=lambda item: (item[0], item[1]))
    tied = [
        prefix
        for cost, ph, prefix in finished
        if (cost, ph) == (best_cost, best_phrases)
    ]
    best_prefix = None
    best_text = None
    for prefix in tied:
        text = compact_text(prefix)
        if best_text is None or (len(text), text) < (len(best_text), best_text):
            best_prefix, best_text = prefix, text
    return best_prefix


@cache
def fixed_beam(types, family):
    """Best legal order of a fixed atom multiset; None if impossible."""
    present = tuple(sorted({z for z, _, _ in types}))
    start: tuple = (
        tuple(c for _, _, c in types),
        None,
        None,
        frozenset(),
        0,
        0,
        0,
        0,
        (),
    )
    beam: list = [start]
    finished: list = []

    def key(state):
        _rem, _lz, _lv, _seen, _rl, below, run, rep, prefix = state
        ph = phrases(prefix)
        return (
            100 * below + 10 * run + REP_CHANGE * rep + 3 * ph + len(prefix),
            ph,
            len(prefix),
        )

    while beam:
        nxt = []
        for rem, last_zone, last_value, seen, run_len, below, run, rep, prefix in beam:
            if not any(rem):
                ph = phrases(prefix)
                finished.append(
                    (
                        100 * below
                        + 10 * run
                        + REP_CHANGE * rep
                        + 3 * ph
                        + len(prefix),
                        ph,
                        prefix,
                    )
                )
                continue
            for i, (zone, value, _count) in enumerate(types):
                if rem[i] <= 0:
                    continue
                if not _transition_ok(
                    last_zone, last_value, zone, value, seen, present
                ):
                    continue
                new_rem = list(rem)
                new_rem[i] -= 1
                new_seen = seen | {zone}
                amount = max(value) if isinstance(value, tuple) else value
                new_below = below + max(0, pref_min(family, zone) - amount)
                new_run, new_rep, new_run_len = run, rep, run_len
                if last_zone is not None and zone == last_zone:
                    new_run_len = run_len + 1
                    if atom_total(value) != atom_total(last_value):
                        new_rep = rep + 1
                else:
                    if last_zone is not None and zone > last_zone and zone not in seen:
                        n = run_len
                        new_run = run + (1 if n == 1 else 0 if n == 2 else n - 1)
                    new_run_len = 1
                nxt.append(
                    (
                        tuple(new_rem),
                        zone,
                        value,
                        new_seen,
                        new_run_len,
                        new_below,
                        new_run,
                        new_rep,
                        prefix + ((zone, value),),
                    )
                )
        alive = []
        for state in nxt:
            rem, _lz, _lv, seen, _rl, _below, _run, _rep, _prefix = state
            top = max(seen, default=-1)
            if any(
                rem[i] > 0 and z not in seen and z < top
                for i, (z, _value, _count) in enumerate(types)
            ):
                continue
            alive.append(state)
        alive.sort(key=key)
        beam = alive[:BEAM]
    if not finished:
        return None
    best_cost, best_phrases, _ = min(finished, key=lambda item: (item[0], item[1]))
    tied = [
        prefix
        for cost, ph, prefix in finished
        if (cost, ph) == (best_cost, best_phrases)
    ]
    best_prefix = None
    best_text = None
    for prefix in tied:
        text = compact_text(prefix)
        if best_text is None or (len(text), text) < (len(best_text), best_text):
            best_prefix, best_text = prefix, text
    return best_prefix


@cache
def best_scheme(counts, family):
    """Preferred fill first; joint capacity search only when it cannot order."""
    lo = BIN_ZONES[family]
    types = []
    for z, n in enumerate(counts):
        if not n:
            continue
        parts = fill(n, REPS[family][lo[z]])
        for r in sorted(set(parts)):
            types.append((lo[z], r, parts.count(r)))
    order = fixed_beam(tuple(types), family)
    if order is None:
        order = beam_search(single_zones(counts, family), family)
    return order, compact_text(order)


@cache
def best_pair_scheme(clean, jerk):
    """Preferred complex fill first, joint search only when it cannot order."""
    lo = BIN_ZONES["CJ"]
    types = []
    for z, (a, b) in enumerate(zip(clean, jerk)):
        if not (a or b):
            continue
        parts = pair_fill(a, b, lo[z])
        for p in sorted(set(parts)):
            types.append((lo[z], p, parts.count(p)))
    order = fixed_beam(tuple(types), "CJ")
    if order is None:
        order = beam_search(cj_zones(clean, jerk), "CJ")
    return order, compact_text(order)


def scheme_lines(s):
    """One session's movements as exact sets x reps bullets, beam-ordered."""
    cs = [g for g in CLEAN if sum(s["movements"].get(g, []))]
    hs = [g for g in JERK if sum(s["movements"].get(g, []))]
    pair = None
    if len(cs) == 1 and len(hs) == 1:
        c, h = cs[0], hs[0]
        if all(
            (a > 0) == (b > 0) for a, b in zip(s["movements"][c], s["movements"][h])
        ):
            pair = (c, h)
    out = []
    for g in GROUPS:
        counts = s["movements"].get(g, [])
        if not sum(counts) or (pair and g == pair[1]):
            continue
        if pair and g == pair[0]:
            c, h = pair
            out.append(
                f"- {c}+{h}: "
                f"{best_pair_scheme(tuple(s['movements'][c]), tuple(s['movements'][h]))[1]}"
            )
        else:
            out.append(f"- {g}: {best_scheme(tuple(counts), BIN_GROUP[g])[1]}")
    return out


def _slug(text, seen):
    base = re.sub(r"[^\w -]", "", text.lower()).replace(" ", "-")
    count = seen.get(base, 0)
    seen[base] = count + 1
    return base if count == 0 else f"{base}-{count}"


def toc_entries(headings):
    """GitHub-style (level, title, anchor) for each ## or ### heading."""
    entries = []
    seen: dict = {}
    for line in headings:
        if line.startswith("### "):
            level, title = 3, line[4:]
        elif line.startswith("## "):
            level, title = 2, line[3:]
        else:
            continue
        entries.append((level, title, _slug(title, seen)))
    return entries


def to_markdown(plan):
    lines = [f"# {plan['macro']}", "", f"Annual: {plan['annual']} lifts", ""]
    lines += group_table(plan["groups"]) + [""]
    lines += ["Meso sizes: " + ", ".join(str(m["vol"]) for m in plan["mesos"]), ""]
    body = []
    for m in plan["mesos"]:
        body += [f"## {m['name']} ({m['phase']}) - {m['vol']} lifts", ""]
        body += group_table(m["groups"]) + [""]
        body += ["Week sizes: " + ", ".join(str(w["vol"]) for w in m["weeks"]), ""]
        for wi, w in enumerate(m["weeks"]):
            body += [f"### Week {wi + 1} - {w['vol']} lifts", ""]
            body += week_table(w["groups"], w["bins"]) + [""]
            body += [
                "Day sizes: " + ", ".join(str(s["vol"]) for s in w["sessions"]),
                "",
            ]
            for i, s in enumerate(w["sessions"], 1):
                body += [f"#### Session {i} - {s['vol']} lifts", ""]
                body += scheme_lines(s) + [""]
    contents = ["## Contents", ""]
    for level, title, anchor in toc_entries(body):
        contents.append(("  " if level == 3 else "") + f"- [{title}](#{anchor})")
    contents.append("")
    return "\n".join(lines + contents + body)


def write_outputs(path="outputs"):
    path = Path(path)
    path.mkdir(exist_ok=True)
    for cls in CLASSES:
        (path / f"{cls}.md").write_text(to_markdown(build_plan(cls)))


def main():
    write_outputs()


if __name__ == "__main__":
    main()
