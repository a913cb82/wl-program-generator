import os
import re
from concurrent.futures import ProcessPoolExecutor
from functools import cache
from html import escape
from math import gcd
from pathlib import Path

from wlconfig import (
    BALLAST,
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
    COMPLEXITY_COST,
    DAY,
    EPS,
    FAN,
    FINISH_SCAN,
    FREE_SLOTS,
    GAP,
    GROUPS,
    MACRO,
    MIN_DOSE,
    PAIR_REF,
    PAIRED_GROUPS,
    PAIRS,
    PATTERNS,
    REPS,
    SCHEDULES,
    SIZE_WEIGHT,
    STRAY_COST,
    TOL,
    VARIANTS,
    WARMUP_COST,
    slot_singles,
    token_parts,
)


def expand(slots):
    out: list = [()]
    for alts, lo, hi, optional in slots:
        choices = [*alts, *([None] if optional else [])]
        out = [o + (c,) for o in out for c in choices]
    return out


PAIR_SET = {frozenset(p) for p in PAIRS}
PAIR_BY_SET = {frozenset(p): p for p in PAIRS}


def _slot_tables():
    singles: dict = {}
    complexes: dict = {}
    for si, slot in enumerate(DAY):
        for tok in slot[0]:
            parts = token_parts(tok)
            if len(parts) == 1:
                singles.setdefault(parts[0], set()).add(si)
            else:
                complexes.setdefault(frozenset(parts), set()).add(si)
    return singles, complexes


SINGLE_SLOTS, COMPLEX_SLOTS = _slot_tables()


def map_zone_index(zlo, group):
    """Member bin index for a reference zone label.

    Exact when the label exists in the member's zones; below-range labels map
    to the member's lowest bin (paired pulls ride the classic's low zones),
    above-range to its highest, otherwise to the nearest bin.
    """
    zones = BIN_ZONES[BIN_GROUP[group]]
    if zlo in zones:
        return zones.index(zlo)
    if zlo <= zones[0]:
        return 0
    if zlo >= zones[-1]:
        return len(zones) - 1
    return min(range(len(zones)), key=lambda i: abs(zones[i] - zlo))


@cache
def is_matchable(groups):
    """True when every hosted group can take a template slot, with listed
    A+X complexes sharing one slot.

    Co-hosted pairs need not render jointly: unpaired groups keep their own
    sets (separate bullets), so overlapping triples only need distinct-slot
    sharing here. Designated pairs are chosen later by detect_pairs."""
    groups = set(groups)
    if not groups:
        return True
    if any(g not in SINGLE_SLOTS and all(g not in p for p in PAIR_SET) for g in groups):
        return False

    def rec(remaining, used):
        if not remaining:
            return True
        g = next(iter(remaining))
        rest = set(remaining)
        rest.discard(g)
        for si in SINGLE_SLOTS.get(g, ()):
            if si not in used and rec(rest, used | {si}):
                return True
        for h in list(rest):
            key = frozenset((g, h))
            if key not in PAIR_SET:
                continue
            for si in COMPLEX_SLOTS.get(key, ()):
                if si not in used:
                    rest2 = set(rest)
                    rest2.discard(h)
                    if rec(rest2, used | {si}):
                        return True
        return False

    return rec(groups, set())


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
    m = _ipf(tuple(tuple(r) for r in prior), tuple(rows), tuple(cols), iters)
    return None if m is None else [list(r) for r in m]


@cache
def _ipf(prior, rows, cols, iters):
    nr = len(rows)
    m = [[float(x) for x in row] for row in prior]
    rng = range(nr)
    for it in range(iters):
        for i in rng:
            row = m[i]
            s = sum(row)
            if s:
                f = rows[i]
                m[i] = [x * f / s for x in row]
        for j, col in enumerate(zip(*m)):
            s = sum(col)
            if s:
                factor = cols[j] / s
                for row in m:
                    row[j] *= factor
        if it % 10 == 9:
            ok = True
            for i in rng:
                if abs(sum(m[i]) - rows[i]) >= 1e-6:
                    ok = False
                    break
            if ok:
                for j, col in enumerate(zip(*m)):
                    if abs(sum(col) - cols[j]) >= 1e-6:
                        ok = False
                        break
            if ok:
                return tuple(tuple(r) for r in m)
    return None


def feasible(prior, rows, cols):
    """True when the margins fit the support: an exact max-flow check."""
    return _feasible(tuple(tuple(r) for r in prior), tuple(rows), tuple(cols))


@cache
def _feasible(prior, rows, cols):
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
        head = 0
        while head < len(queue) and parent[sink] is None:
            u = queue[head]
            head += 1
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
    if not feasible(prior, rows, cols):
        return None
    m = ipf(prior, rows, cols)
    if m is None:
        return None
    nr, nc = len(rows), len(cols)
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
    diff = [cols[j] - sum(out[i][j] for i in range(nr)) for j in range(nc)]
    for _ in range(sum(abs(d) for d in diff) // 2 + 1):
        # Single swaps can stall when only a chain of moves frees a unit
        # (e.g. a sparse support after dose pruning). Augment along a path
        # from an over column to an under one; each augmentation fixes two
        # units of column drift while keeping every row sum exact.
        diff = [cols[j] - sum(out[i][j] for i in range(nr)) for j in range(nc)]
        if not any(diff):
            break
        parent: dict = {}
        queue = [j for j, d in enumerate(diff) if d < 0]
        for j in queue:
            parent[j] = None
        target = None
        head = 0
        while head < len(queue) and target is None:
            j = queue[head]
            head += 1
            for i in range(nr):
                if out[i][j] <= 0:
                    continue
                for k in range(nc):
                    if prior[i][k] <= 0 or k in parent:
                        continue
                    parent[k] = (j, i)
                    if diff[k] > 0:
                        target = k
                        break
                    queue.append(k)
                if target is not None:
                    break
        if target is None:
            break
        k = target
        while parent[k] is not None:
            j, i = parent[k]
            out[i][j] -= 1
            out[i][k] += 1
            k = j
    if any(sum(out[i]) != rows[i] for i in range(nr)):
        return None
    if any(sum(out[i][j] for i in range(nr)) != cols[j] for j in range(nc)):
        return None
    return out


def prune_doses(support, rows, cols, groups=None):
    """Drop cells below a usable dose where the margins stay feasible.

    With groups (one name per row), a drop must also keep the session's
    hosted set slot-matchable: pruning a pair partner must not strand the
    other half in a slot clash (e.g. SnPull left alone with ClPull)."""
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
            if groups is not None:
                hosted = {groups[ii] for ii in range(len(rows)) if p[ii][j] > 0}
                hosted.discard(groups[i])
                if not slot_match(hosted):
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
    slot), then drop cells below a usable dose.

    Stranded sub-minimum cells are banned and the hosted sets re-resolved,
    so the matrix holds 0 or >= MIN_DOSE per cell wherever the margins
    allow it; the least-stranded matrix wins. Rows whose weekly total is
    itself below the minimum cannot be placed legally and are left for
    the weekly repair."""
    idx = {g: i for i, g in enumerate(GROUPS)}
    base = [row[:] for row in prior]
    banned: set[tuple[int, int]] = set()
    best = None
    best_key = None
    for _ in range(20):
        trial = [row[:] for row in base]
        for i, j in banned:
            trial[i][j] = 0
        support = resolve_slots(trial, rows, cols, idx, [0], limit=2000)
        if support is None:
            break
        p = prune_doses(support, rows, cols, GROUPS)
        m = fit(p, rows, cols) if p is not None else None
        if m is None:
            break
        key = sum(
            1
            for i in range(len(rows))
            for j in range(len(cols))
            if 0 < m[i][j] < MIN_DOSE
        )
        if best_key is None or key < best_key:
            best, best_key = m, key
        if key == 0:
            break
        target = next(
            (
                (i, j)
                for i in range(len(rows))
                for j in range(len(cols))
                if 0 < m[i][j] < MIN_DOSE and rows[i] >= MIN_DOSE
            ),
            None,
        )
        if target is None:
            break
        banned.add(target)
    return best


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
    live = tuple(live)
    return _session_options(live, tuple(weight[g] for g in live))


@cache
def _session_options(live, weights):
    opts = []
    weight = dict(zip(live, weights))

    def rec(k, chosen):
        if k == len(live):
            if is_matchable(frozenset(chosen)):
                opts.append(tuple(chosen))
            return
        g = live[k]
        rec(k + 1, chosen)
        rec(k + 1, chosen + [g])

    rec(0, [])
    opts.sort(key=lambda groups: -sum(weight[g] for g in groups))
    return tuple(opts)


def slot_match(groups):
    """True when every group can take a distinct template slot (listed
    complexes may share one)."""
    groups = set(groups)
    return is_matchable(frozenset(groups))


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
        live = [g for g in slot_singles(slot) if targets[g] > 0]
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
    free = {g for slot in FREE_SLOTS for g in slot_singles(slot)}
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
    m is zone-major: m[zone][session].

    A gap the week cannot fill is left alone: when a zone holds fewer
    units than the sessions spanning it (below and above, or just above
    for the base), no swap can give every spanning session that zone, so
    trying only churns mass between days."""
    nz, ns = len(m), len(m[0])
    base = next((z for z in range(nz) if any(m[z])), nz)
    if base == nz:
        return m
    weekcount = [sum(m[z]) for z in range(nz)]

    def spanning(z):
        n = 0
        for s in range(ns):
            above = any(m[zz][s] for zz in range(z + 1, nz))
            if not above:
                continue
            if z == base or any(m[zz][s] for zz in range(base, z)):
                n += 1
        return n

    def raw_gaps(s):
        used = [z for z in range(base, nz) if m[z][s]]
        if not used:
            return []
        return [z for z in range(used[0], used[-1] + 1) if not m[z][s]]

    def fill(s, z):
        """Fill session s's gap at z, strictly reducing the total gap
        count. Every candidate move is simulated first and applied only
        when s gains no new gap and nobody else does either; a lone
        pigeonholed gap can strand a two-way swap, so a three-cycle
        (holder -> s -> middleman -> holder) is tried next."""
        pre = [len(raw_gaps(t)) for t in range(ns)]

        def ok(touched):
            post = {t: len(raw_gaps(t)) for t in touched}
            if post[s] >= pre[s]:
                return False
            return all(post[t] <= pre[t] for t in touched if t != s)

        def take(give, recv):
            for zz, ss, delta in give:
                m[zz][ss] += delta
            for zz, ss, delta in recv:
                m[zz][ss] += delta

        def untake(give, recv):
            for zz, ss, delta in give:
                m[zz][ss] -= delta
            for zz, ss, delta in recv:
                m[zz][ss] -= delta

        # two-way: s takes z from d, d takes an upper v back
        for v in range(z + 1, nz):
            if not m[v][s]:
                continue
            for d in range(ns):
                if d == s or not m[z][d]:
                    continue
                give = [(z, s, 1), (v, d, 1)]
                recv = [(z, d, -1), (v, s, -1)]
                take(give, recv)
                good = ok((s, d))
                if not good:
                    untake(give, recv)
                else:
                    return True
        # three-cycle: a holder h with nothing above z hands z to s,
        # s hands its top v on to a middleman d2, d2 hands a lower w
        # it can spare back to h. Nobody gains a new gap by construction
        # (h and s trade their tops down, d2 keeps every zone it holds).
        top = max(zz for zz in range(z + 1, nz) if m[zz][s])
        for h in range(ns):
            if h == s or not m[z][h]:
                continue
            if any(m[zz][h] for zz in range(z + 1, nz)):
                continue
            for d2 in range(ns):
                if d2 == s or d2 == h:
                    continue
                for w in range(base, z):
                    if m[w][d2] < 2:
                        continue
                    give = [(z, s, 1), (top, d2, 1), (w, h, 1)]
                    recv = [(z, h, -1), (top, s, -1), (w, d2, -1)]
                    take(give, recv)
                    good = ok((s, h, d2))
                    if not good:
                        untake(give, recv)
                    else:
                        return True
        return False

    def pass_once():
        changed = False
        for s in range(ns):
            stuck = set()
            while True:
                nxt = next(
                    (
                        z
                        for z in range(base, nz)
                        if z not in stuck
                        and m[z][s] == 0
                        and any(m[zz][s] for zz in range(z + 1, nz))
                        and weekcount[z] >= spanning(z)
                    ),
                    None,
                )
                if nxt is None:
                    break
                if fill(s, nxt):
                    changed = True
                else:
                    stuck.add(nxt)
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


def count_dose_violations(sessions):
    """Unpaired (group, session) cells holding 1-5 lifts."""
    n = 0
    for s in sessions:
        paired_here = {g for a, b in s.get("pairs", {}) for g in (a, b)}
        for g, counts in s["movements"].items():
            if g in paired_here:
                continue
            if 0 < sum(counts) < MIN_DOSE:
                n += 1
    return n


def repair_week_doses(week_groups, nominals):
    """Fold sub-minimum weekly group totals into sibling weeks.

    A weekly total of 1-5 lifts cannot be placed legally in any session
    split, so it forces a session violation downstream. Set it to the
    nearest placeable dose (0 or 6), completing the 4-cycle with a second
    group so meso totals and week volumes stay exact. Every landing must
    also stay inside its nominal week band, so the repair never breaks
    the weekly shape; every move strictly reduces the stranded count, so
    this terminates."""
    rows = [[wg[g] for wg in week_groups] for g in GROUPS]
    nr, nc = len(rows), len(rows[0])

    def dose_ok(v):
        return v == 0 or v >= MIN_DOSE

    def band_ok(i, j, v):
        n = nominals[j][GROUPS[i]]
        slack = 2 if GROUPS[i] in PAIRED_GROUPS else 0
        return abs(v - n) <= max(1, round(TOL * n)) + slack

    for _ in range(nr * nc):
        target = next(
            ((i, j) for i in range(nr) for j in range(nc) if 0 < rows[i][j] < MIN_DOSE),
            None,
        )
        if target is None:
            for i, g in enumerate(GROUPS):
                for j, wg in enumerate(week_groups):
                    wg[g] = rows[i][j]
            return True
        i, j = target
        for t in (0, MIN_DOSE):
            d = t - rows[i][j]
            if d == 0 or not band_ok(i, j, t):
                continue
            for j2 in range(nc):
                if j2 == j or not dose_ok(rows[i][j2] - d):
                    continue
                if not band_ok(i, j2, rows[i][j2] - d):
                    continue
                for i2 in range(nr):
                    if i2 == i:
                        continue
                    if not dose_ok(rows[i2][j2] + d):
                        continue
                    if not dose_ok(rows[i2][j] - d):
                        continue
                    if not band_ok(i2, j2, rows[i2][j2] + d):
                        continue
                    if not band_ok(i2, j, rows[i2][j] - d):
                        continue
                    rows[i][j] += d
                    rows[i][j2] -= d
                    rows[i2][j2] += d
                    rows[i2][j] -= d
                    break
                else:
                    continue
                break
            else:
                continue
            break
    return False


def week_sessions(vol, targets, nom, cls, mi, wi, prev_last=None):
    """First session-size variant the week can host: the cap-driven day count
    first, source variants in table order, canonical (first) pattern preferred.

    Weeks whose first feasible variant strands sub-minimum doses try the
    remaining variants and keep the least-stranded; violation-free weeks
    are unaffected."""
    best = None
    best_key = None
    variants = [
        (n, pattern) for n in range(len(sessions(vol)), 7) for pattern in VARIANTS[n]
    ]
    for idx, (n, pattern) in enumerate(variants):
        vols, session_list = day_split(vol, pattern)
        if max(vols) > CAP and n != 6:
            continue
        attempt = dict(targets)
        try:
            planned = plan_sessions(session_list, attempt, nom, cls, mi, wi, prev_last)
        except ValueError:
            continue
        v = count_dose_violations(planned)
        if v == 0:
            targets.clear()
            targets.update(attempt)
            return planned
        key = (v, idx)
        if best_key is None or key < best_key:
            best_key, best = key, (planned, attempt)
    if best is None:
        raise ValueError("week has no feasible session-size variant")
    targets.clear()
    targets.update(best[1])
    return best[0]


@cache
def week_units(cls, mi, wi, t, ref="Clean"):
    """Paired units in the heavy, mid and light ratio tiers.

    Tiers follow the reference member's zones (the classic lift limits the
    complex), so mixed pairs share the classic's heavy/mid/light split."""
    lo = BIN_ZONES[BIN_GROUP[ref]]
    counts = week_bin_lifts(cls, mi, wi, ref, t)
    return (
        sum(c for c, z in zip(counts, lo) if z >= 90),
        sum(c for c, z in zip(counts, lo) if z == 80),
        sum(c for c, z in zip(counts, lo) if z < 80),
    )


def pair_options(c, h, cls, mi, wi, ref="Clean"):
    """Legal tier schedules for one session, closest to (c, h) first."""
    out = []
    for t in range(max(1, (c + h) // 5 - 2), (c + h) // 2 + 2):
        heavy, mid, light = week_units(cls, mi, wi, t, ref)
        for rh, rm, rl in SCHEDULES:
            ac = rh[0] * heavy + rm[0] * mid + rl[0] * light
            aj = rh[1] * heavy + rm[1] * mid + rl[1] * light
            out.append((abs(ac - c) + abs(aj - h), -(ac + aj), ac, aj, t, (rh, rm, rl)))
    out.sort()
    return out


def cover_session(hosted):
    """Pairing + slot assignment covering every hosted group, or None.

    Listed pairs share their complex slot (preferred, so complexes render),
    the rest take distinct single slots. Groups volume-first, pairs before
    singles, both in sorted order: deterministic."""
    hosted = sorted(hosted, key=lambda g: (-hosted[g], g))
    names = list(hosted)

    def rec(names, used, pairs):
        if not names:
            return list(pairs)
        g = names[0]
        rest = names[1:]
        for k, h in enumerate(rest):
            key = frozenset((g, h))
            if key not in PAIR_SET:
                continue
            for si in sorted(COMPLEX_SLOTS.get(key, ())):
                if si not in used:
                    a, b = PAIR_BY_SET[key]
                    out = rec(rest[:k] + rest[k + 1 :], used | {si}, pairs + [(a, b)])
                    if out is not None:
                        return out
        for si in sorted(SINGLE_SLOTS.get(g, ())):
            if si not in used:
                out = rec(rest, used | {si}, pairs)
                if out is not None:
                    return out
        return None

    return rec(names, set(), [])


def detect_pairs(moved, idx, vols):
    """Slot-consistent A+X pairs per session. The fit guarantees a cover
    exists; when none is found the session stays unpaired (separate sets)."""
    found: dict = {}
    for j in range(len(vols)):
        hosted = {g for g in GROUPS if moved[idx[g]][j] > 0}
        cover = cover_session({g: moved[idx[g]][j] for g in hosted})
        if cover:
            found[j] = cover
    return found


def pair_fit(moved, vols, targets, nom, prior, cls, mi, wi):
    """Snap every session hosting a listed A+X pair to one small ratio,
    then refit the other groups. Week targets flex to what was planned."""
    idx = {g: i for i, g in enumerate(GROUPS)}
    detected = detect_pairs(moved, idx, vols)
    if not detected:
        return moved, {}
    instances = [
        (j, a, b, PAIR_REF[(a, b)]) for j, picks in detected.items() for a, b in picks
    ]
    # The refit only moves never-paired groups: every pairable row is frozen
    # (snapped where paired, as-fit elsewhere), so the refit cannot strand
    # a new unsnapped co-hosted pair in one session.
    free = [i for i, g in enumerate(GROUPS) if g in BALLAST]
    lo = [nom[GROUPS[i]] - max(1, round(TOL * nom[GROUPS[i]])) for i in free]
    hi = [nom[GROUPS[i]] + max(1, round(TOL * nom[GROUPS[i]])) for i in free]
    prior = prior or session_prior(targets, len(vols))

    def snap(combo):
        work = [row[:] for row in moved]
        pairs: dict = {}
        for (j, a, b, ref), (_, _, ac, aj, t, sched) in zip(instances, combo):
            work[idx[a]][j] = ac
            work[idx[b]][j] = aj
            pairs.setdefault(j, []).append((a, b, ac, aj, t, sched, ref))
        return work, pairs

    def band_excess(work):
        return sum(
            max(0, abs(sum(work[idx[g]]) - nom[g]) - max(1, round(TOL * nom[g])))
            for g in PAIRED_GROUPS
        )

    per_opts = [
        pair_options(moved[idx[a]][j], moved[idx[b]][j], cls, mi, wi, ref)[:6]
        for j, a, b, ref in instances
    ]
    # A snapped pair occupies its complex slot, and every frozen (unsnapped
    # but hosted) pairable cell keeps its single slot, so the refit may not
    # host other singles needing those slots in the same session (e.g. no
    # lone Squat alongside a frozen ClPull in slot 2).
    occupied: dict = {}
    for j, a, b, _ref in instances:
        slots = COMPLEX_SLOTS.get(frozenset((a, b)), set())
        if slots:
            occupied.setdefault(j, set()).add(sorted(slots)[0])
    # Hill-climb the snap choice: start from the closest option per paired
    # session, then flip single sessions while the week total nears its
    # band. Product order would starve wide weeks (6^12 combos); climbing
    # evaluates hundreds, not billions. Candidates sort by (band excess,
    # session overflow, snap distance); strict takes the first in-band
    # refit, relaxed retries the cheapest excess first. Session overflow
    # is scored (not just filtered) so the climb walks away from snaps
    # that burst a day's volume.
    CAP_EVALS = 20000
    CAP_REFITS = 200
    tried_refits = 0

    def vols_ok(work):
        return not any(
            sum(work[idx[g]][j] for g in PAIRED_GROUPS) > vols[j]
            for j in range(len(vols))
        )

    def combo_key(idxs):
        work, _ = snap(tuple(per_opts[i][k] for i, k in enumerate(idxs)))
        dist = sum(per_opts[i][k][0] for i, k in enumerate(idxs))
        overflow = sum(
            max(0, sum(work[idx[g]][j] for g in PAIRED_GROUPS) - vols[j])
            for j in range(len(vols))
        )
        return (band_excess(work), overflow, dist)

    start = tuple(0 for _ in instances)
    seen_keys = {start}
    scored = [(combo_key(start), start)]
    evals = 1
    cur, cur_score = start, scored[0][0]
    while evals < CAP_EVALS:
        stepped = None
        for i in range(len(instances)):
            for k in range(len(per_opts[i])):
                if k == cur[i]:
                    continue
                nxt = cur[:i] + (k,) + cur[i + 1 :]
                if nxt in seen_keys:
                    continue
                seen_keys.add(nxt)
                evals += 1
                score = combo_key(nxt)
                scored.append((score, nxt))
                if score < cur_score:
                    stepped = (nxt, score)
                    break
                if evals >= CAP_EVALS:
                    break
            if stepped is not None or evals >= CAP_EVALS:
                break
        if stepped is None:
            break
        cur, cur_score = stepped
    scored.sort(key=lambda t: t[0])
    ordered = []
    seen_work = set()
    for _, idxs in scored:
        combo = tuple(per_opts[i][k] for i, k in enumerate(idxs))
        work, pairs = snap(combo)
        if not vols_ok(work):
            continue
        key = tuple(sum(work[idx[g]]) for g in sorted(PAIRED_GROUPS))
        if key in seen_work:
            continue
        seen_work.add(key)
        ordered.append((work, pairs))
        if len(ordered) >= CAP_REFITS * 2:
            break

    def refit(work, pairs):
        nonlocal tried_refits
        tried_refits += 1
        if tried_refits > CAP_REFITS:
            return None
        delta = sum(sum(work[idx[g]]) for g in PAIRED_GROUPS) - sum(
            targets[g] for g in PAIRED_GROUPS
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
            return None
        fixed = [0] * len(GROUPS)
        for i, v in zip(free, rows):
            fixed[i] = v
        cols = [
            vols[j] - sum(work[idx[g]][j] for g in PAIRED_GROUPS)
            for j in range(len(vols))
        ]
        block = [row[:] for row in prior]
        for g in PAIRED_GROUPS:
            block[idx[g]] = [0.0] * len(vols)
        designated = {}
        for jj, plist in pairs.items():
            designated[jj] = {g for a, b, *_ in plist for g in (a, b)}
        for i in free:
            g = GROUPS[i]
            need_slots = SINGLE_SLOTS.get(g, set())
            if not need_slots:
                continue
            for j in range(len(vols)):
                occ = set(occupied.get(j, ()))
                for h in PAIRED_GROUPS:
                    if work[idx[h]][j] > 0 and h not in designated.get(j, set()):
                        occ |= SINGLE_SLOTS.get(h, set())
                if need_slots <= occ:
                    block[i][j] = 0.0
        base = [row[:] for row in block]
        banned: set[tuple[int, int]] = set()
        best = None
        best_key = None
        for _ in range(20):
            trial = [row[:] for row in base]
            for i, j in banned:
                trial[i][j] = 0
            support = resolve_slots(trial, fixed, cols, idx, [0], limit=2000)
            if support is None:
                break
            pruned = prune_doses(support, fixed, cols)
            rest = fit(pruned, fixed, cols) if pruned is not None else None
            if rest is None:
                break
            key = sum(
                1
                for i in range(len(fixed))
                for j in range(len(cols))
                if 0 < rest[i][j] < MIN_DOSE
            )
            if best_key is None or key < best_key:
                best, best_key = rest, key
            if key == 0:
                break
            target = next(
                (
                    (i, j)
                    for i in range(len(fixed))
                    for j in range(len(cols))
                    if 0 < rest[i][j] < MIN_DOSE and fixed[i] >= MIN_DOSE
                ),
                None,
            )
            if target is None:
                break
            banned.add(target)
        if best is None:
            return None
        rest = best
        for i in free:
            for j in range(len(vols)):
                work[i][j] = rest[i][j]
        for i, g in enumerate(GROUPS):
            targets[g] = sum(work[i])
        return work

    for strict in (True, False):
        for work, pairs in ordered:
            if strict and band_excess(work):
                continue
            if refit(work, pairs) is not None:
                return work, pairs
            if tried_refits >= CAP_REFITS:
                break
    return None, None


def pair_zones(cls, mi, wi, pairs):
    """One zone list per movement from the pair's shared unit blocks.

    Units of one reference-zone family split across that family's paired
    sessions with a flat prior (so every complex carries its own warmup
    ramp) and contiguous profiles; each member counts its share in its own
    bins (below-range reference zones land in the member's lowest bin). The
    tier schedule fixes each reference zone's ratio; the actual totals are
    returned too, so the ballast groups can absorb any rounding difference.
    Reference-zone vectors are also returned for rendering."""
    by_bin: dict = {}
    for j, plist in pairs.items():
        for a, b, _ac, _aj, t, sched, ref in plist:
            by_bin.setdefault(BIN_GROUP[ref], []).append((j, a, b, t, sched, ref))
    out = {}
    actual = {}
    refdata = {}
    for bt, items in by_bin.items():
        ref0 = items[0][5]
        units = [it[3] for it in items]
        counts = week_bin_lifts(cls, mi, wi, ref0, sum(units))
        top = max((z for z, c in enumerate(counts) if c), default=0)
        counts = counts[: top + 1]
        nS = len(items)
        # Base floor: every paired session touches the week's base zone when
        # the week holds enough (one per session with units to place), low
        # zones first, so small proportional shares never round to zero and
        # strand a lone top without its warmup base. The remainder still
        # fits exactly, and adding base units cannot open a gap.
        base = next((z for z, c in enumerate(counts) if c), None)
        floored = [u >= 1 for u in units]
        res = [[0] * len(counts) for _ in range(nS)]
        if base is not None and counts[base] >= sum(floored):
            for k in range(nS):
                if floored[k]:
                    res[k][base] = 1
        rem_counts = [
            counts[z] - sum(res[k][z] for k in range(nS)) for z in range(len(counts))
        ]
        rem_units = [units[k] - sum(res[k]) for k in range(nS)]
        m_rem = fit([[1.0] * nS for _ in rem_counts], rem_counts, rem_units)
        close_ramps(m_rem)
        m = [[m_rem[z][k] + res[k][z] for k in range(nS)] for z in range(len(counts))]
        lo = BIN_ZONES[bt]
        nz_full = len(BIN_ZONES[bt])
        for k, (j, a, b, _t, (rh, rm, rl), ref) in enumerate(items):
            ratios = [
                rh if lo[z] >= 90 else rm if lo[z] == 80 else rl
                for z in range(len(counts))
            ]
            ra = [r[0] * m[z][k] for z, r in enumerate(ratios)]
            rb = [r[1] * m[z][k] for z, r in enumerate(ratios)]
            va = [0] * len(BIN_ZONES[BIN_GROUP[a]])
            vb = [0] * len(BIN_ZONES[BIN_GROUP[b]])
            for z in range(len(counts)):
                va[map_zone_index(lo[z], a)] += ra[z]
                vb[map_zone_index(lo[z], b)] += rb[z]
            out[(j, a)] = va
            out[(j, b)] = vb
            actual[(j, a, b)] = (sum(va), sum(vb))
            full_a = ra + [0] * (nz_full - len(ra))
            full_b = rb + [0] * (nz_full - len(rb))
            refdata[(j, a, b)] = (ref, full_a, full_b)
    return out, actual, refdata


def consolidate_doses(moved, pairs):
    """Fold sub-minimum unpaired session doses into sibling sessions.

    Every (group, session) cell must hold 0 or >= MIN_DOSE lifts, but the
    fitters strand 1-5 lifts where margins force them. Move a stranded
    dose into another session hosting the same group, completing the
    4-cycle with a second group so weekly totals and session sizes stay
    exact. Paired cells are frozen (their zone splits are assigned); a
    session's hosted set may only gain slot-matchable groups. Every move
    strictly reduces the stranded count, so this terminates."""
    nr, nc = len(moved), len(moved[0])
    designated = {}
    for j, plist in pairs.items():
        designated[j] = {g for a, b, *_ in plist for g in (a, b)}

    def dose_ok(v):
        return v == 0 or v >= MIN_DOSE

    def hosted(j):
        return {GROUPS[i] for i in range(nr) if moved[i][j] > 0}

    def free_cell(i, j):
        return moved[i][j] == 0 or GROUPS[i] not in designated.get(j, set())

    for _ in range(nr * nc):
        target = next(
            (
                (i, j)
                for i in range(nr)
                for j in range(nc)
                if 0 < moved[i][j] < MIN_DOSE and free_cell(i, j)
            ),
            None,
        )
        if target is None:
            return True
        i, j = target
        v = moved[i][j]
        for j2 in range(nc):
            if j2 == j or not free_cell(i, j2):
                continue
            if not dose_ok(moved[i][j2] + v):
                continue
            for i2 in range(nr):
                if i2 == i or not free_cell(i2, j) or not free_cell(i2, j2):
                    continue
                if not dose_ok(moved[i2][j2] - v):
                    continue
                if moved[i2][j] + v < MIN_DOSE:
                    continue
                moved[i][j] -= v
                moved[i][j2] += v
                moved[i2][j] += v
                moved[i2][j2] -= v
                if slot_match(hosted(j)) and slot_match(hosted(j2)):
                    break
                moved[i][j] += v
                moved[i][j2] -= v
                moved[i2][j] -= v
                moved[i2][j2] += v
            else:
                continue
            break
    return False


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
        s["pairs"] = {}
    paired, actual, refdata = pair_zones(cls, mi, wi, pairs) if pairs else ({}, {}, {})
    idx = {g: i for i, g in enumerate(GROUPS)}
    for j, plist in pairs.items():
        paired_here = {g for a, b, *_ in plist for g in (a, b)}
        free = [i for i, g in enumerate(GROUPS) if g not in paired_here]
        for a, b, _ac, _aj, t, (rh, rm, rl), ref in plist:
            tc, ta = moved[idx[a]][j], moved[idx[b]][j]
            ac, aj = actual[(j, a, b)]
            need = tc + ta - ac - aj
            pool = sum(moved[i][j] for i in free)
            if (need > 0 and pool == 0) or (need < 0 and pool < -need):
                # Unabsorbable drift (near-pair-only session): split this
                # session's own units instead. Totals match the snap exactly
                # by construction, and big-t sessions keep a broad ramp.
                lo = BIN_ZONES[BIN_GROUP[ref]]
                wbl = week_bin_lifts(cls, mi, wi, ref, t)
                ratios = [
                    rh if lo[z] >= 90 else rm if lo[z] == 80 else rl
                    for z in range(len(lo))
                ]
                ra = [r[0] * w for r, w in zip(ratios, wbl)]
                rb = [r[1] * w for r, w in zip(ratios, wbl)]
                va = [0] * len(BIN_ZONES[BIN_GROUP[a]])
                vb = [0] * len(BIN_ZONES[BIN_GROUP[b]])
                for z in range(len(lo)):
                    va[map_zone_index(lo[z], a)] += ra[z]
                    vb[map_zone_index(lo[z], b)] += rb[z]
                paired[(j, a)] = va
                paired[(j, b)] = vb
                actual[(j, a, b)] = (sum(va), sum(vb))
                refdata[(j, a, b)] = (ref, list(ra), list(rb))
                continue
            moved[idx[a]][j] = ac
            moved[idx[b]][j] = aj

            def absorb_ok(i, delta):
                v = moved[i][j] + delta
                return v == 0 or v >= MIN_DOSE

            while need > 0:
                here = [i for i in free if moved[i][j] > 0]
                safe = [i for i in here if absorb_ok(i, 1)]
                i = max(
                    safe or here,
                    key=lambda i: (
                        nom[GROUPS[i]]
                        + max(1, round(TOL * nom[GROUPS[i]]))
                        - sum(moved[i])
                    ),
                    default=None,
                )
                if i is None:
                    break
                moved[i][j] += 1
                need -= 1
            while need < 0:
                here = [i for i in free if moved[i][j] > 0]
                safe = [i for i in here if absorb_ok(i, -1)]
                i = max(
                    safe or here,
                    key=lambda i: (
                        sum(moved[i])
                        - nom[GROUPS[i]]
                        + max(1, round(TOL * nom[GROUPS[i]]))
                    ),
                    default=None,
                )
                if i is None:
                    break
                moved[i][j] -= 1
                need += 1
    consolidate_doses(moved, pairs)
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
            # Ramp repair: every active session shows a dose in each zone
            # below its top that the week holds in force. Zone 0 is owed
            # when the week holds one per active session (this split's
            # base plus paired sessions' base lifts); higher zones when
            # the full week holds twice the active count (the test's
            # dose-per-session-plus-spare bar for all-single doses). The
            # moved unit comes from the lowest zone holding 2+ (else the
            # top, which can only drop), so no session gaps; totals stay
            # exact with no drift (1:1 lifts).
            paired_at: dict = {}
            for (jj, gg), va in paired.items():
                if gg == g:
                    for x, c in enumerate(va):
                        paired_at[x] = paired_at.get(x, 0) + c
            full = [
                (counts[x] if x < len(counts) else 0) + paired_at.get(x, 0)
                for x in range(nz)
            ]
            have0 = full[0] if full else 0
            if have0 >= len(active):
                for z in zones:
                    used = [x for x in range(len(z)) if z[x]]
                    if not used or used[0] == 0:
                        continue
                    if len(used) == 1:
                        # lone zone: move the whole block to the base
                        z[0] = z[used[0]]
                        z[used[0]] = 0
                    elif any(z[x] >= 2 for x in used):
                        # spare rep: reinforce the base, lowest spare first
                        src = next(x for x in used if z[x] >= 2)
                        z[src] -= 1
                        z[0] += 1
                    else:
                        # all singletons: shift the block down to the base
                        b = used[0]
                        block = [z[x] for x in used]
                        for x in used:
                            z[x] = 0
                        for off, c in enumerate(block):
                            z[off] = c
            for z in zones:
                top = max((x for x in range(len(z)) if z[x]), default=None)
                if top is None:
                    continue
                for x in range(top - 1, 0, -1):
                    if z[x] or full[x] < 2 * len(active):
                        continue
                    src = next(
                        (y for y in range(x + 1, len(z)) if z[y] >= 2),
                        max(y for y in range(len(z)) if z[y]),
                    )
                    z[src] -= 1
                    z[x] += 1
            for j, z in zip(active, zones):
                session_list[j]["movements"][g] = z + [0] * (nz - len(z))
        for j in range(len(vols)):
            if (j, g) in paired:
                z = paired[(j, g)]
                session_list[j]["movements"][g] = z + [0] * (nz - len(z))
    for (j, a, b), (ref, va, vb) in refdata.items():
        session_list[j]["pairs"][(a, b)] = (ref, tuple(va), tuple(vb))
    for s in session_list:
        hosted = {g for g, z in s["movements"].items() if sum(z)}
        if not slot_match(hosted):
            raise ValueError("week has no session mix that hosts every group")
        if sum(sum(z) for z in s["movements"].values()) != s["vol"]:
            raise ValueError("week has no session mix that hosts every group")
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
        week_groups = []
        for wi, (wv, nom) in enumerate(zip(week_vols, nominal)):
            tail = {g: sum(n[g] for n in nominal[wi:]) for g in GROUPS}
            remaining = {g: targets[g] - planned[g] for g in GROUPS}
            week_groups.append(
                dict(
                    zip(
                        GROUPS,
                        spread(
                            [nom[g] for g in GROUPS],
                            [remaining[g] for g in GROUPS],
                            [tail[g] for g in GROUPS],
                        ),
                    )
                )
            )
            for g in GROUPS:
                planned[g] += week_groups[-1][g]
        repair_week_doses(week_groups, nominal)
        weeks = []
        for wi, (wv, nom) in enumerate(zip(week_vols, nominal)):
            groups = week_groups[wi]
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


def _th(label, colspan=1):
    span = f' colspan="{colspan}"' if colspan > 1 else ""
    return f'<th scope="col"{span}>{label}</th>'


def _rowh(label, rowspan=1):
    span = f' rowspan="{rowspan}"' if rowspan > 1 else ""
    return f'<th scope="row"{span}>{label}</th>'


def _num(value, cls=""):
    if not value:
        return f'<td class="{cls}"></td>' if cls else "<td></td>"
    return (
        f'<td class="num {cls}">{value}</td>'
        if cls
        else f'<td class="num">{value}</td>'
    )


def group_table(groups):
    """Group totals table."""
    rows = [f"<tr>{_rowh(g)}{_num(v)}</tr>" for g, v in groups.items() if v]
    return (
        '<table class="data">\n<thead><tr>'
        + _th("Group")
        + _th("Lifts")
        + "</tr></thead>\n<tbody>\n"
        + "\n".join(rows)
        + "\n</tbody>\n</table>"
    )


def fill(n, reps):
    """Exact rep split: fewest sets, then largest smallest and largest set."""
    if not n:
        return []
    return list(_fill(n, tuple(sorted(set(reps) | {1}, reverse=True))))


@cache
def _fill(n, reps):
    if not n:
        return ()
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
    return tuple(best[1])


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


def pair_fill(a, b, zlo, a_group="Clean", b_group="Jerk"):
    """Complex sets for an A+X zone; each side capped by its own rep table.

        zlo is the reference (classic) zone label; sides lifting below/above their
        own range use their lowest/highest bin's cap. The tightest side wins, so
    e.g. SnPull+Snatch 3+3 is legal at 70%: correct for Snatch, low for SnPull."""
    m = gcd(a, b)
    p, q = a // m, b // m
    za = BIN_ZONES[BIN_GROUP[a_group]][map_zone_index(zlo, a_group)]
    zb = BIN_ZONES[BIN_GROUP[b_group]][map_zone_index(zlo, b_group)]
    cap_a = max(REPS[BIN_GROUP[a_group]][za])
    cap_b = max(REPS[BIN_GROUP[b_group]][zb])
    kmax = max(1, min(cap_a // p, cap_b // q))
    return [(k * p, k * q) for k in fill(m, tuple(range(kmax, 0, -1)))]


def atom_total(value):
    return value if isinstance(value, int) else value[0] + value[1]


def atom_text(value):
    return str(value) if isinstance(value, int) else f"{value[0]}+{value[1]}"


def pref_min(family, zlo):
    """Smallest useful set size: 1 is the fallback, not a target."""
    sizes = REPS[family][zlo]
    return min((s for s in sizes if s > 1), default=1)


def stray(seq, family):
    # Sets smaller than the zone minimum are stray volume. The first
    # touch of a zone is the warm-up ramp and stays free.
    total = 0
    seen = set()
    for zlo, value in seq:
        if zlo in seen:
            size = max(value) if isinstance(value, tuple) else value
            total += max(0, pref_min(family, zlo) - size)
        else:
            seen.add(zlo)
    return total


def warmup(seq):
    """Warm-up cost of climbing out of a zone having done less than two
    reps there: one rep is a touch, a double is a start. Climbs into a
    zone already visited are free, so drops and waves cost nothing."""
    runs: list = []
    for zlo, value in seq:
        reps = atom_total(value)
        if runs and runs[-1][0] == zlo:
            runs[-1][1] += reps
        else:
            runs.append([zlo, reps])
    total = 0
    seen = set()
    for i, (zlo, reps) in enumerate(runs):
        seen.add(zlo)
        if i + 1 < len(runs) and runs[i + 1][0] > zlo and runs[i + 1][0] not in seen:
            total += 1 if reps < 2 else 0
    return total


def complexity(seq):
    """Things the athlete must remember, counted off the rendered items:
    every set-group and every ×N suffix. A wave's body counts once plus
    its own ×N, so compression reads as fewer instructions."""
    items = _parse(tuple(seq))[2]

    def things(items):
        total = 0
        for item in items:
            if item[0] == "wave":
                total += 1 + things(item[2])
            else:
                total += len(item[2]) + sum(1 for _, c in item[2] if c > 1)
        return total

    return things(items)


@cache
def scheme_cost(seq, family):
    stray_ = stray(seq, family)
    warmup_ = warmup(seq)
    cx = complexity(seq)
    cost = STRAY_COST * stray_ + WARMUP_COST * warmup_ + COMPLEXITY_COST * cx
    return cost, stray_, warmup_, cx


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


@cache
def _render_html(items):
    """One HTML phrase per item: zone-over-reps fractions, sets as a ×N suffix."""
    out = []
    for item in items:
        if item[0] == "wave":
            inner = " ".join(_render_html(item[2]))
            out.append(
                f'<span class="wave"><span class="pl">(</span>{inner}'
                f'<span class="pr">)</span><span class="rep">×{item[1]}</span></span>'
            )
        else:
            _, zlo, pairs = item
            if all(count == 1 for _, count in pairs):
                # Every rep count is a single set, so one fraction carries
                # them all (80%/3,2) instead of repeating the zone.
                reps = ",".join(atom_text(value) for value, _ in pairs)
                frac = (
                    f'<span class="frac"><span class="zone">{zlo}%</span>'
                    f'<span class="reps">{reps}</span></span>'
                )
                out.append(f'<span class="dose">{frac}</span>')
                continue
            parts = []
            for value, count in pairs:
                frac = (
                    f'<span class="frac"><span class="zone">{zlo}%</span>'
                    f'<span class="reps">{atom_text(value)}</span></span>'
                )
                if count > 1:
                    frac += f'<span class="sets">×{count}</span>'
                parts.append(f'<span class="dose">{frac}</span>')
            out.append(" ".join(parts))
    return tuple(out)


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
    if prev_zone is None or zone < prev_zone:
        return True
    if isinstance(value, tuple) and isinstance(prev_value, tuple):
        # Complexes: each member's per-set reps must hold flat or fall.
        # A flat complex total is not enough (1+2 -> 2+1 keeps 3 but
        # raises one side).
        return not any(v > p for v, p in zip(value, prev_value))
    return not (atom_total(value) > atom_total(prev_value))


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


def pair_choices(a_ref, b_ref, a_group, b_group, ref_group):
    """A+X zones for the beam search: size is the shared unit count, value
    is the complex. Zones and tiers follow the reference member."""
    lo = BIN_ZONES[BIN_GROUP[ref_group]]
    out = []
    for z, (a, b) in enumerate(zip(a_ref, b_ref)):
        if not (a or b):
            continue
        m = gcd(a, b)
        p, q = a // m, b // m
        za = BIN_ZONES[BIN_GROUP[a_group]][map_zone_index(lo[z], a_group)]
        zb = BIN_ZONES[BIN_GROUP[b_group]][map_zone_index(lo[z], b_group)]
        cap_a = max(REPS[BIN_GROUP[a_group]][za])
        cap_b = max(REPS[BIN_GROUP[b_group]][zb])
        kmax = max(1, min(cap_a // p, cap_b // q))
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
        1,
        (),
    )
    beam: list = [start]
    finished: list = []

    def key(state):
        _caps, _lz, _lv, _seen, _rl, below, warmup, sfx, _cc, prefix = state
        guide = _guide(prefix) + sfx
        return (
            STRAY_COST * below
            + WARMUP_COST * warmup
            + COMPLEXITY_COST * guide
            + len(prefix),
            guide,
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
            warmup,
            sfx,
            cur_count,
            prefix,
        ) in beam:
            if not any(caps):
                guide = _guide(prefix) + sfx
                finished.append(
                    (
                        STRAY_COST * below
                        + WARMUP_COST * warmup
                        + COMPLEXITY_COST * guide,
                        guide,
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
                    # first touch is the warm-up ramp, exactly as stray() counts
                    short = (
                        0
                        if zone not in seen
                        else max(0, pref_min(family, zone) - amount)
                    )
                    new_below = below + short
                    new_warmup, new_run_len = warmup, run_len
                    new_sfx, new_count = sfx, cur_count
                    if last_zone is not None and zone == last_zone:
                        new_run_len = run_len + 1
                        if value == last_value:
                            if cur_count == 1:
                                new_sfx = sfx + 1
                            new_count = cur_count + 1
                        else:
                            new_count = 1
                    else:
                        new_count = 1
                        if (
                            last_zone is not None
                            and zone > last_zone
                            and zone not in seen
                        ):
                            new_warmup = warmup + (1 if run_len < 2 else 0)
                        new_run_len = amount
                    nxt.append(
                        (
                            tuple(new_caps),
                            zone,
                            value,
                            new_seen,
                            new_run_len,
                            new_below,
                            new_warmup,
                            new_sfx,
                            new_count,
                            prefix + ((zone, value),),
                        )
                    )
        alive = []
        for state in nxt:
            caps, _lz, _lv, seen, _rl, _below, _warmup, _sfx, _cc, _prefix = state
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
        base = tuple(ordered)
    else:
        # The running estimate cannot see wave compression, so rescore the
        # cheapest survivors under the true cost before choosing.
        ranked = sorted(finished, key=lambda i: (i[0], i[1]))[:FINISH_SCAN]
        best = None
        for _approx, _things, prefix in ranked:
            cost, _, _, cx = scheme_cost(prefix, family)
            text = compact_text(prefix)
            pick = (cost, cx, len(prefix), len(text), text)
            if best is None or pick < best[0]:
                best = (pick, prefix)
        assert best is not None
        base = best[1]
    base_cost, _, _, base_cx = scheme_cost(base, family)
    base_rank = (base_cost, base_cx, len(base), len(compact_text(base)))
    for seed in seed_orders(zones):
        cost, _, _, cx = scheme_cost(seed, family)
        seed_pick = (cost, cx, len(seed), len(compact_text(seed)))
        if seed_pick < base_rank:
            base, base_rank = seed, seed_pick
    return base


@cache
def _guide(seq):
    """Pruning guide only: fewest phrases. A repeated wave adds no phrase
    for its count, so the beam can rank compression cheaply; the score
    itself is complexity(). Global memo keeps it fast across prefixes."""
    if not seq:
        return 0
    n = len(seq)
    best = 1 + _guide(seq[1:])
    j = 1
    while j < n and seq[j] == seq[0]:
        j += 1
    best = min(best, 1 + _guide(seq[j:]))
    for p in range(2, n // 2 + 1):
        if seq[p] != seq[0]:
            continue
        unit = seq[:p]
        k = 1
        while (k + 1) * p <= n and seq[k * p : (k + 1) * p] == unit:
            k += 1
        if k >= 2:
            best = min(best, _guide(unit) + _guide(seq[k * p :]))
    return best


def seed_orders(zones):
    """Deterministic candidate orders the joint beam misses.

    Work-set spine (doubles where the zone holds them, flat-or-fall),
    then either grouped bulk or a top-pair wave. The top is flushed
    first, then the lower zones climb from the bottom, so the bulk
    ramps up instead of fading down. Every step is checked against
    _transition_ok and zone totals must match exactly; invalid seeds are
    dropped. Pure (no RNG), so beam_search stays @cache-safe."""
    present = tuple(z for z, _, _ in zones)
    if not present:
        return ()
    sizes = {z: [s for s, _ in ch] for z, _, ch in zones}
    values = {z: {s: v for s, v in ch} for z, _, ch in zones}
    out = []
    for waved in (False, True):
        seq = []
        seen: set = set()
        rem = {z: c for z, c, _ in zones}
        last_zone, last_value = None, None
        prev_size = 2
        ok = True

        def emit(z, size):
            nonlocal last_zone, last_value, ok
            if not ok:
                return
            v = values[z][size]
            if not _transition_ok(
                last_zone, last_value, z, v, frozenset(seen), present
            ):
                ok = False
                return
            seen.add(z)
            last_zone, last_value = z, v
            seq.append((z, v))
            rem[z] -= size

        for z, _, ch in zones:
            want = min(2, rem[z], prev_size)
            size = max(s for s in sizes[z] if s <= want)
            # Take the whole zone as one work set rather than opening with a
            # double and stranding a crumb below the useful size.
            useful = min((s for s in sizes[z] if s > 1), default=1)
            if size < rem[z] < useful + size and rem[z] in sizes[z]:
                size = rem[z]
            emit(z, size)
            prev_size = size
        top = present[-1]
        below = present[-2] if len(present) >= 2 else None
        crumbs = {
            z
            for z in present
            if 0 < rem[z] < min((s for s in sizes[z] if s > 1), default=1)
        }
        s = 2
        if (
            waved
            and below is not None
            and s in sizes[top]
            and s in sizes[below]
            and rem[top] >= s
            and rem[below] >= s
        ):
            for _ in range(rem[top] % s):
                emit(top, 1)
            while ok and rem[top] >= s and rem[below] >= s:
                emit(below, s)
                if ok:
                    emit(top, s)
        cap = None
        if ok and rem[top] > 0:
            arrival = next(k for k, v in values[top].items() if v == last_value)
            for size in sorted(
                fill(rem[top], tuple(s for s in sizes[top] if s <= arrival)),
                reverse=True,
            ):
                emit(top, size)
        for z in sorted(present):
            if z == top or not ok or rem[z] <= 0:
                continue
            if z in crumbs:
                continue
            if cap is None:
                allowed = tuple(sizes[z])
            else:
                allowed = tuple(s for s in sizes[z] if s <= cap)
            parts = sorted(fill(rem[z], allowed), reverse=True)
            for size in parts:
                emit(z, size)
            if parts:
                cap = parts[-1]
        # Crumbs go last, heaviest first. A zone whose lock has been used
        # up leaves a set below the useful size; running it with the bulk
        # would cap every later zone at that size, so it drops in as a
        # back-off instead, where a fall costs nothing.
        for z in sorted(crumbs, reverse=True):
            if ok and rem[z] > 0:
                emit(z, rem[z])
        if ok and all(r == 0 for r in rem.values()) and seq:
            tup = tuple(seq)
            if tup not in out:
                out.append(tup)
    return tuple(out)


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
        1,
        (),
    )
    beam: list = [start]
    finished: list = []

    def key(state):
        _rem, _lz, _lv, _seen, _rl, below, warmup, sfx, _cc, prefix = state
        guide = _guide(prefix) + sfx
        return (
            STRAY_COST * below
            + WARMUP_COST * warmup
            + COMPLEXITY_COST * guide
            + len(prefix),
            guide,
        )

    while beam:
        nxt = []
        for (
            rem,
            last_zone,
            last_value,
            seen,
            run_len,
            below,
            warmup,
            sfx,
            cur_count,
            prefix,
        ) in beam:
            if not any(rem):
                guide = _guide(prefix) + sfx
                finished.append(
                    (
                        STRAY_COST * below
                        + WARMUP_COST * warmup
                        + COMPLEXITY_COST * guide,
                        guide,
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
                short = (
                    0 if zone not in seen else max(0, pref_min(family, zone) - amount)
                )
                new_below = below + short
                new_warmup, new_run_len = warmup, run_len
                new_sfx, new_count = sfx, cur_count
                if last_zone is not None and zone == last_zone:
                    new_run_len = run_len + 1
                    if value == last_value:
                        if cur_count == 1:
                            new_sfx = sfx + 1
                        new_count = cur_count + 1
                    else:
                        new_count = 1
                else:
                    new_count = 1
                    if last_zone is not None and zone > last_zone and zone not in seen:
                        new_warmup = warmup + (1 if run_len < 2 else 0)
                    new_run_len = amount
                nxt.append(
                    (
                        tuple(new_rem),
                        zone,
                        value,
                        new_seen,
                        new_run_len,
                        new_below,
                        new_warmup,
                        new_sfx,
                        new_count,
                        prefix + ((zone, value),),
                    )
                )
        alive = []
        for state in nxt:
            rem, _lz, _lv, seen, _rl, _below, _warmup, _sfx, _cc, _prefix = state
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
    ranked = sorted(finished, key=lambda i: (i[0], i[1]))[:FINISH_SCAN]
    best = None
    for _approx, _things, prefix in ranked:
        cost, _, _, cx = scheme_cost(prefix, family)
        text = compact_text(prefix)
        rank = (cost, cx, len(prefix), len(text), text)
        if best is None or rank < best[0]:
            best = (rank, prefix)
    assert best is not None
    return best[1]


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
def best_pair_scheme(
    a_counts, b_counts, a_group="Clean", b_group="Jerk", ref_group="Clean"
):
    """Preferred complex fill first, joint search only when it cannot order.

    Counts are reference-zone vectors (both sides share the reference zones);
    each side is capped by its own rep table at its mapped zone."""
    lo = BIN_ZONES[BIN_GROUP[ref_group]]
    types = []
    for z, (a, b) in enumerate(zip(a_counts, b_counts)):
        if not (a or b):
            continue
        parts = pair_fill(a, b, lo[z], a_group, b_group)
        for p in sorted(set(parts)):
            types.append((lo[z], p, parts.count(p)))
    order = fixed_beam(tuple(types), BIN_GROUP[ref_group])
    if order is None:
        order = beam_search(
            pair_choices(a_counts, b_counts, a_group, b_group, ref_group),
            BIN_GROUP[ref_group],
        )
    return order, compact_text(order)


def scheme_entries(s):
    """One (movement, atom seq) per slot, DAY-slot ordered.

    Stored pairs (from planning) render jointly from their reference-zone
    vectors; sessions built by hand fall back to auto-detecting same-zone
    pairs with aligned support."""
    stored = dict(s.get("pairs", {}))
    used: set = {g for p in stored for g in p}
    detected: dict = {}
    for a, b in PAIRS:
        if a in used or b in used:
            continue
        if BIN_GROUP[a] != BIN_GROUP[b]:
            continue
        if not (sum(s["movements"].get(a, [])) and sum(s["movements"].get(b, []))):
            continue
        if all(
            (x > 0) == (y > 0) for x, y in zip(s["movements"][a], s["movements"][b])
        ):
            detected[(a, b)] = (
                PAIR_REF[(a, b)],
                tuple(s["movements"][a]),
                tuple(s["movements"][b]),
            )
            used.update((a, b))
    pairs = {**stored, **detected}
    first_of = {a: (a, b) for a, b in pairs}
    second_of = {b: (a, b) for a, b in pairs}
    entries = []
    for order, g in enumerate(GROUPS):
        counts = s["movements"].get(g, [])
        if not sum(counts) or g in second_of:
            continue
        if g in first_of:
            a, b = first_of[g]
            ref, va, vb = pairs[(a, b)]
            slots = COMPLEX_SLOTS.get(frozenset((a, b)), ())
            seq = best_pair_scheme(tuple(va), tuple(vb), a, b, ref)[0]
            text = f"{a}+{b}"
        else:
            slots = SINGLE_SLOTS.get(g, ())
            seq = best_scheme(tuple(counts), BIN_GROUP[g])[0]
            text = g
        entries.append((sorted(slots)[0] if slots else len(DAY), order, text, seq))
    entries.sort(key=lambda entry: (entry[0], entry[1]))
    return [(text, seq) for _, _, text, seq in entries]


def _slug(text, seen):
    base = re.sub(r"[^\w -]", "", text.lower()).replace(" ", "-")
    count = seen.get(base, 0)
    seen[base] = count + 1
    return base if count == 0 else f"{base}-{count}"


def toc_entries(headings):
    """(level, title, anchor) with duplicate-title disambiguation."""
    entries = []
    seen: dict = {}
    for level, title in headings:
        entries.append((level, title, _slug(title, seen)))
    return entries


def micro_table(mesos):
    """All microcycles in one table: weeks as columns, one row per
    group total, group zone, and group ARI."""
    top = ["<thead><tr><th></th>"]
    for mi, m in enumerate(mesos):
        n = len(m["weeks"])
        span = f' colspan="{n}"' if n > 1 else ""
        cls = ' class="meso"' if mi else ""
        top[0] += f'<th scope="col"{span}{cls}>{escape(m["name"])} ({m["phase"]})</th>'
    top[0] += "</tr>"
    weeks = [
        (mi, wi, w) for mi, m in enumerate(mesos) for wi, w in enumerate(m["weeks"])
    ]
    week_cells = [_th("Group")]
    for mi, wi, w in weeks:
        cls = ' class="meso"' if mi and not wi else ""
        week_cells.append(f'<th scope="col"{cls}>W{wi + 1} · {w["vol"]}</th>')
    top.append("<tr>" + "".join(week_cells) + "</tr>")
    top.append("</thead>")
    rows = []
    for g in GROUPS:
        totals = [w["groups"].get(g, 0) for _, _, w in weeks]
        if not any(totals):
            continue
        firsts = [bool(mi and not wi) for mi, wi, _ in weeks]
        lo = BIN_ZONES[BIN_GROUP[g]]
        rows.append(
            '<tr class="grp">'
            + _rowh(g)
            + "".join(
                _num(v, "meso") if first else _num(v)
                for v, first in zip(totals, firsts)
            )
            + "</tr>"
        )
        for zi, z in enumerate(lo):
            cells = []
            for (_, _, w), total, first in zip(weeks, totals, firsts):
                counts = w["bins"].get(g)
                v = counts[zi] if total and counts else 0
                cells.append(_num(v, "meso") if first else _num(v))
            rows.append("<tr>" + _rowh(f"{z}%") + "".join(cells) + "</tr>")
        acells = []
        for (_, _, w), total, first in zip(weeks, totals, firsts):
            counts = w["bins"].get(g)
            v = f"{ari(counts, lo) / total:.1f}" if total and counts else 0
            acells.append(_num(v, "meso") if first else _num(v))
        rows.append("<tr>" + _rowh("ARI") + "".join(acells) + "</tr>")
    return (
        '<table class="micro">\n'
        + "\n".join(top)
        + "\n<tbody>\n"
        + "\n".join(rows)
        + "\n</tbody>\n</table>"
    )


def meso_table(mesos):
    """One group row with a volume column per mesocycle."""
    names = [f"{m['name']} ({m['phase']})" for m in mesos]
    head = (
        "<thead><tr>" + _th("Group") + "".join(_th(n) for n in names) + "</tr></thead>"
    )
    rows = []
    for g in GROUPS:
        if any(m["groups"].get(g, 0) for m in mesos):
            cells = "".join(_num(m["groups"].get(g, 0)) for m in mesos)
            rows.append(f"<tr>{_rowh(g)}{cells}</tr>")
    return (
        '<table class="data">\n'
        + head
        + "\n<tbody>\n"
        + "\n".join(rows)
        + "\n</tbody>\n</table>"
    )


def training_table(meso):
    """One mesocycle's sessions: weeks across, slots down.

    Two columns per week: movement name, then its scheme (zone over
    reps, fraction-style). Each movement slot in each session gets one
    row; the session number spans its slot rows."""
    weeks = meso["weeks"]
    parts = []
    for wi in range(len(weeks)):
        cls = ' class="wk"' if wi else ""
        parts.append(f'<th scope="col" colspan="2"{cls}>Week {wi + 1}</th>')
    head = "<thead><tr><th></th>" + "".join(parts) + "</tr></thead>"
    body = []
    rows = max(len(w["sessions"]) for w in weeks)
    for si in range(rows):
        present = [w for w in weeks if si < len(w["sessions"])]
        slots = max(
            [len(scheme_entries(w["sessions"][si])) for w in present], default=0
        )
        for k in range(slots):
            cells = []
            for wi, w in enumerate(weeks):
                gap = '<td class="wk"></td>' if wi else "<td></td>"
                if si >= len(w["sessions"]):
                    cells += [gap, "<td></td>"]
                    continue
                entries = scheme_entries(w["sessions"][si])
                if k >= len(entries):
                    cells += [gap, "<td></td>"]
                    continue
                movement, seq = entries[k]
                phrases = " ".join(
                    f'<span class="phrase">{p}</span>'
                    for p in _render_html(_parse(tuple(seq))[2])
                )
                move_cls = "move wk" if wi else "move"
                cells += [
                    f'<td class="{move_cls}">{escape(movement)}</td>',
                    f'<td class="scheme">{phrases}</td>',
                ]
            first = f'<th scope="row" rowspan="{slots}">{si + 1}</th>' if k == 0 else ""
            tag = '<tr class="sess">' if k == 0 else "<tr>"
            body.append(tag + first + "".join(cells) + "</tr>")
    return (
        '<table class="plan">\n'
        + head
        + "\n<tbody>\n"
        + "\n".join(body)
        + "\n</tbody>\n</table>"
    )


STYLE = """
:root {
  --bg: #f3f4f6;
  --card: #ffffff;
  --ink: #27272a;
  --muted: #71717a;
  --line: #e4e4e7;
  --strong: #71717a;
  --accent: #9a3412;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.55;
}
main { max-width: 80rem; margin: 0 auto; padding: 1.5rem 1.5rem 4rem; }
header h1 { font-size: 2.2rem; letter-spacing: -0.01em; margin: 0 0 1rem; }
section > h1 { font-size: 1.8rem; margin: 2.5rem 0 1rem; padding-top: 1rem; border-top: 2px solid var(--line); }
h2 { font-size: 1.35rem; margin: 2rem 0 0.75rem; }
h3 { font-size: 1.1rem; margin: 1.5rem 0 0.5rem; }
h4 { font-size: 1rem; margin: 1.25rem 0 0.5rem; }
nav.toc { background: var(--card); border: 1px solid var(--line); border-radius: 0.75rem; padding: 1rem 1.5rem; }
nav.toc h2 { margin: 0 0 0.5rem; font-size: 1.1rem; }
nav.toc ul { margin: 0.25rem 0; padding-left: 1.25rem; }
nav.toc a { color: var(--accent); text-decoration: none; }
nav.toc a:hover { text-decoration: underline; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; background: var(--card); margin: 0.5rem 0 1.5rem; box-shadow: 0 1px 2px rgb(0 0 0 / 0.06); font-variant-numeric: tabular-nums; }
th, td { border: 1px solid var(--line); padding: 0.3rem 0.65rem; vertical-align: top; }
thead th { text-align: center; background: #fafafa; }
tbody th[scope="row"] { text-align: left; background: #fafafa; white-space: nowrap; }
td.num { text-align: right; }
tbody tr:nth-child(even) { background: #fafafa; }
p.sizes { color: var(--muted); margin: 0.25rem 0 1rem; }
td.move { white-space: nowrap; font-weight: 600; }
td.scheme { min-width: 10rem; white-space: nowrap; }
table.plan { width: 100%; }
table.plan tr.sess > td, table.plan tr.sess > th { border-top: 2px solid var(--strong); }
table.plan .wk { border-left: 2px solid var(--strong); }
table.micro { width: 100%; }
table.micro tr.grp > td, table.micro tr.grp > th { border-top: 2px solid var(--strong); }
table.micro .meso { border-left: 2px solid var(--strong); }
table.micro th, table.micro td { white-space: nowrap; }
.frac { display: inline-flex; flex-direction: column; text-align: center; margin: 0.1em 0.25em; }
.frac .zone { border-bottom: 1.5px solid currentColor; padding: 0 0.4em; font-weight: 600; }
.frac .reps { padding: 0 0.4em; }
.sets { font-weight: 600; }
.rep { font-weight: 600; }
.dose, .wave { display: inline-flex; align-items: center; vertical-align: middle; }
.pl, .pr { font-size: 2.2em; line-height: 1; font-weight: 300; }
"""


def toc_tree(entries):
    """Nest (level, title, anchor) entries into [title, anchor, children] trees."""
    root: list = []
    stack = [(0, root)]
    for level, title, anchor in entries:
        while stack[-1][0] >= level:
            stack.pop()
        node = [title, anchor, []]
        stack[-1][1].append(node)
        stack.append((level, node[2]))
    return root


def toc_list(nodes):
    """Nested <ul> table of contents for toc_tree output."""
    parts = ["<ul>"]
    for title, anchor, children in nodes:
        parts.append(f'<li><a href="#{anchor}">{escape(title)}</a>')
        if children:
            parts.append(toc_list(children))
        parts.append("</li>")
    parts.append("</ul>")
    return "".join(parts)


def to_html(plan):
    headings: list = [
        (1, "Volumes"),
        (2, "Macrocycle"),
        (2, "Mesocycles"),
        (2, "Microcycles"),
        (1, "Training Plan"),
    ]
    for m in plan["mesos"]:
        headings.append((2, f"{m['name']} ({m['phase']})"))
    anchors = iter(anchor for _, _, anchor in toc_entries(headings))
    body = ["<section>", f'<h1 id="{next(anchors)}">Volumes</h1>']
    body.append(f'<h2 id="{next(anchors)}">Macrocycle</h2>')
    body.append(group_table(plan["groups"]))
    body.append(
        '<p class="sizes">Meso sizes: '
        + ", ".join(str(m["vol"]) for m in plan["mesos"])
        + "</p>"
    )
    body.append(f'<h2 id="{next(anchors)}">Mesocycles</h2>')
    body.append(meso_table(plan["mesos"]))
    for m in plan["mesos"]:
        body.append(
            f'<p class="sizes">{escape(m["name"])} ({m["phase"]}) - Week sizes: '
            + ", ".join(str(w["vol"]) for w in m["weeks"])
            + "</p>"
        )
    body.append(f'<h2 id="{next(anchors)}">Microcycles</h2>')
    body.append('<div class="scroll">' + micro_table(plan["mesos"]) + "</div>")
    body.append("</section>")
    body.append("<section>")
    body.append(f'<h1 id="{next(anchors)}">Training Plan</h1>')
    for m in plan["mesos"]:
        title = f"{m['name']} ({m['phase']})"
        body.append(f'<h2 id="{next(anchors)}">{escape(title)}</h2>')
        body.append('<div class="scroll">' + training_table(m) + "</div>")
    body.append("</section>")
    toc = [
        '<nav class="toc">',
        "<h2>Contents</h2>",
        toc_list(toc_tree([e for e in toc_entries(headings) if e[0] <= 2])),
        "</nav>",
    ]
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        f"<title>{escape(plan['macro'])}</title>\n<style>{STYLE}</style>\n"
        "</head>\n<body>\n<main>\n"
        f"<header><h1>{escape(plan['macro'])}</h1></header>\n"
        + "\n".join(toc)
        + "\n"
        + "\n".join(body)
        + "\n</main>\n</body>\n</html>\n"
    )


def _render_class(cls):
    """One class end to end: independent of every other class."""
    return cls, to_html(build_plan(cls))


def write_outputs(path="outputs", jobs=None):
    """Write one HTML file per class. Classes share no state, so they run in
    parallel; results are collected by class name to keep output identical."""
    path = Path(path)
    path.mkdir(exist_ok=True)
    if jobs is None:
        jobs = min(len(CLASSES), os.cpu_count() or 1)
    pages: dict = {}
    if jobs > 1 and len(CLASSES) > 1:
        try:
            with ProcessPoolExecutor(max_workers=jobs) as pool:
                for cls, html in pool.map(_render_class, list(CLASSES)):
                    pages[cls] = html
        except (OSError, RuntimeError, ImportError, ValueError):
            pages = {}  # no usable process pool here; fall back to serial
    if not pages:
        for cls in CLASSES:
            pages[cls] = to_html(build_plan(cls))
    for cls in CLASSES:
        (path / f"{cls}.html").write_text(pages[cls])


def main():
    jobs = int(os.environ.get("WLGEN_JOBS", "0")) or None
    write_outputs(jobs=jobs)


if __name__ == "__main__":
    main()
