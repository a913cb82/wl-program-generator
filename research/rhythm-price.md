# rhythm-price: price the rhythm term (book 2.09, weight 0.1) — ANALYSIS ONLY

Scorer (`_week_rhythm`, src/wlscore.py): per-week
`total = amplitude + missing + away`, with `amplitude = |hi/lo-2.75|/0.25`
(0.25 contrast miss = 1.0 pt), `missing = possible-turns` (moves < range/10
don't count, zero-moves excluded), `away = |peaks-1|`. Book rhythm = median
of 100 pooled weeks; class rhythm = median of its 20.

## Component table (per-class medians decomposed; audit medians match)

| class | rhythm | median-week recipe | amp | miss | away | where |
|---|---|---|---|---|---|---|
| III | 1.55 | 3-sess `[36,107,36]`-type (10 wks) | ~1.0 | 0 | 0 | contrast stuck ~3.0 vs 2.75 ideal |
| III | — | 4-sess `[45,133,89,44]`-type (8 wks, tot ~1.9-2.2) | ~1.0 | +1 | 0 | up then down-down: turns 1/2 |
| II | 1.55 | identical to III (bit-for-bit) | ~1.0 | +1 on 4-sess | 0 | same |
| I | 3.09 | 5-sess `[87,44,130,87,43]`-type (median band, tot ~3.1) | ~1.1 | +1 | +1 | 2 turns/3 possible, 2 peaks |
| I | — | flat 4-sess, contrast ~1.5 (7 wks, tot 5-6) | ~+5.0 | 0 | +1 | ABOVE median: no median leverage |
| CMS | 3.00 | same bimodal shape as I (median band = 5-sess, tot 2.8-3.1) | ~1.0 | +1 | +1 | same |
| CMS | — | flat 3/4-sess contrast ~1.5 (7 wks, tot 5-6) | ~+5.0 | 0 | +1 | above median |
| MS | 2.96 | 5-sess median band (tot 2.9-3.2) | ~1.0 | +1 | +1 | same 5-sess floor |
| MS | — | S-less flat weeks, contrast ~1.2 (6 wks, tot 6.1-7.2) | ~+6.1 | 0 | 0/1 | above median |
| book | 2.09 | pooled rank 50/51 = 4-sess `[45,133,89,44]`-type | 1.09 | +1 | 0 | III/II/CMS/MS 4-sess cluster (ranks ~47-55 all 2.0-2.2) |

Structural floors (verified by brute force on the scorer): 3-sess floor ≈ amp
(~1.0); 4-sess floor ≈ amp+1 (~2.0) — turns=2 and peaks=1 are jointly
unreachable with 4 distinct vols (alternating `+,-,+` forces an endpoint
second peak); 5-sess floor ≈ amp+2 (~3.0). I's weeks don't touch the book
median at all (all ≤1.4 or ≥2.9).

## Ranked by book-gain-per-effort (weight 0.1: 1.0 rhythm pt = 0.1 score)

1. **Amplitude trim (contrast →2.75):** saves ~1.0/wk everywhere but touches
   ~15 median-band weeks across 4 classes; day-rebalance proved strain cost
   ~4.5x rhythm gain (book 0.902→2.177). Worst ratio. NO.
2. **Resequence 4-sess SLMS→SMSL (missing→away swap):** structural wash
   (saves 1 miss, pays 1 away); order-4day-2 proved net book −0.003 with exc
   147.8→169.6. NO.
3. **Flat-tail fixes (MS S-less skip):** ms-rhythm proved MS 3.00→2.22 but
   book exc +2.3 (147.8→150.1, past the 150 line), book worse — and tails sit
   above the median, so book-median leverage ≈ 0. NO.
4. **5-sess→fewer-days (I/CMS/MS):** cuts class medians, book median untouched
   (median set by 4-sess cluster). Book gain ≈ 0. NO.

## ONE recommended shot (probe, kill-line attached)

**Fold-Thursday probe:** in median-band 4-sess prep/comp weeks of shape
`[45,133,89,44]` (H-M-L taper), move Thursday's dose onto Wednesday as a
back-to-back repeat (`[45,133,66.5,66.5]`, week total + weekly group totals
fixed): the zero Thursday move drops out of `big` (possible 2→1) and the
endpoint peak vanishes (peaks 2→1 in alternating variants). Scorer math:
2.09 (1.09+1+0) → ~0.82 (0.82+0+0). ~10 weeks across III/II/CMS/MS sit in the
2.0-2.2 band; moving 3-4 below the line shifts book median 2.09→~1.9
(book ≈ −0.02) for a one-rule template change — cheapest book-gain-per-effort
of anything priced.
**Strain fence (name it):** Wednesday's session grows ~50% (89→~110+ volume
with Thursday's lifts) — trips per-session movement CAPs → excess, longer
longest-session (size), possible clash/slot; ms-rhythm proved this family
costs +2.3 exc, day-rebalance proved 4.5x strain-vs-rhythm pricing.
**Kill line:** revert unless book exc stays <150 AND strain cost < 2x rhythm
gain. Expect NO-GO; honest prior is that rhythm at weight 0.1 is not worth
chasing vs strain (0.4).
