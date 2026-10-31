#!/bin/bash
# Scored exam for round exc-size-2 (orchestrator only). Run in a clean tree.
# Prints one summary block vs baseline 8940c00. Close calls: rerun back-to-back.
set -u
cd /home/abrai/projects/wl-program-generator
echo "=== gate ==="
.venv/bin/python -m pytest tests/ -q -p no:cacheprovider 2>&1 | tail -1
echo "=== build + audit ==="
.venv/bin/python - <<'PY'
import os, sys; sys.path.insert(0,'src')
t0 = os.times()
from wlgen import build_plan
for cls in ('III','II','I','CMS','MS'):
    build_plan(cls)
t1 = os.times()
print('CPU user+sys: %.2f' % ((t1.user-t0.user)+(t1.system-t0.system)))
PY
.venv/bin/python -m wlgen >/dev/null 2>&1
.venv/bin/python -m wlgen audit 2>&1 | grep -E "^(III|II|I|CMS|MS|book)"
echo "=== room ==="
.venv/bin/python - <<'PY'
import json
def norm(r): return r if isinstance(r, list) else [r]
for cls in ('III','II','I','CMS','MS'):
    prog = json.load(open('outputs/%s.json'%cls))
    cx = tot = pullfuse = 0; mar = 0; solo_hi = solo_tot = 0; longest = 0
    for s in prog['sessions']:
        for slot in s['slots']:
            n = sum(x if isinstance(x,int) else sum(x) for _,r in slot['seq'] for x in norm(r))
            longest = max(longest, len(slot['seq']))
            tot += n
            if '+' in slot['movement']:
                cx += n
                if 'Pull' in slot['movement']: pullfuse += n
            else:
                if slot['movement'] == 'SnPull':
                    for z,r in slot['seq']:
                        solo_tot += r
                        if z >= 90: solo_hi += r
            if len(slot['seq']) > 13: mar += 1
    print('%s share %.1f%% pullfuse %d mar %d longest %d solo %d/%d' % (cls, 100*cx/tot, pullfuse, mar, longest, solo_hi, solo_tot))
PY
echo "=== baseline 8940c00: exc 9.0/10.0/35.4/42.6/93.3 book 190.3; longest 24/26/33/26/28; mar 22/11/23/30/44; instr 9421; rhythm 5.22; soft 84; solo 34/34 I/CMS; fusion 897/895/1666; share 35.2/35.2/45.0; CPU 2.95; suite 211 ==="
