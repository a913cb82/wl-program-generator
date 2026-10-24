# SIZE_WEIGHT nudge probes (research/sizeweight-nudge)

Base: research/stack-1, `SIZE_WEIGHT = {S:1, M:2, L:3}`.
Method: one group at a time, minimal single-step delta, in-process
`wlscore.audit()` per candidate (fresh subprocess each; no shared caches).
Scores are in-process numbers — baseline here is book **0.902**
(strain 1.02, size 0.92, rhythm 2.00); CLI `wlgen audit` reads 0.893 on the
same tree, delta is CPU pace/drift wobble. Comparisons below are all
same-harness, so relative order stands. No `wlscore` edits; no test edits.

## Probe table (book score; lower is better)

| probe | weights (S/M/L) | book | strain | size | rhythm | drift | verdict |
|---|---|---|---|---|---|---|---|
| base | 1 / 2 / 3 | 0.902 | 1.02 | 0.92 | 2.00 | 0.08 | — |
| S+1 | 2 / 2 / 3 | 2.202 | 1.32 | 0.92 | 4.98 | 4.51 | worse (rhythm + drift blow out) |
| S-0.5 | 0.5 / 2 / 3 | 1.963 | 1.25 | 0.93 | 7.40 | 2.21 | worse (rhythm 7.40) |
| M+1 | 1 / 3 / 3 | 1.042 | 1.00 | 0.92 | 2.00 | 0.83 | closest, still worse (drift 0.83) |
| M-1 | 1 / 1 / 3 | 1.268 | 1.01 | 0.91 | 1.17 | 2.37 | worse (drift 2.37) |
| L+1 | 1 / 2 / 4 | 1.332 | 1.02 | 0.94 | 6.00 | 0.20 | worse (rhythm 6.00) |
| L-1 | 1 / 2 / 2 | 2.081 | 1.38 | 0.99 | 3.03 | 4.63 | worse (everything regresses) |

## Verdict: NO-GO — revert all, no src change

Every single-step direction degrades the book. The {1,2,3} split sits on a
local optimum: flattening it (S+1, M+1≈M/L tie, L-1) starves heavy/light
contrast and drift/bad-week terms spike; steepening it (S-0.5, L+1)
over-concentrates volume and rhythm doubles-to-triples. Strain/size barely
move — the loss is all rhythm + drift, i.e. the day-split shares are what
keep weekly contrast and spread in balance.

Per protocol (revert at first flat quality term) no candidate earned a
pytest fence-check; all were rejected on audit numbers alone. `pytest`
baseline stays 128 green untouched. SIZE_WEIGHT left at {1,2,3}.
Do not probe further without a new mechanism (e.g. per-class weights);
uniform moves are exhausted in both directions.
