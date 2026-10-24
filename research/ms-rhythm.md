# ms-rhythm: repair the MS-only M+0.5 rhythm regression — NO-GO (killed on strain)

## Diagnosis
- The M+0.5 weights moved 6 MS weeks onto S-less shapes (4x LMLM, 2x MLM).
  With M=2.5 their contrast sits near 1.2 (vs the 2.75 rhythm ideal), so those
  weeks score ~6-7 and drag the MS median 2.10 -> 3.00. They win variants
  because heavier M days strand fewer sub-minimum doses.
- Other classes untouched (III 1.55 / II 1.55 / I 3.09 / CMS 3.09 bit-identical).

## Attempted repair (reverted, not in tree)
- `variants_for(cls, n)`: MS skips S-less patterns (MLM, LMLM); all other
  classes keep the shared table bit-for-bit. TDD test `test_ms_skips_sless_variants`.
- Effect: MS rhythm 3.00 -> 2.22 (all six ~6-7 weeks fall to ~2.0-2.3),
  MS exc 43.3 -> 45.5, book exc 147.8 -> 150.1, book 0.851 -> 0.877.

## Verdict
NO-GO — killed on the pre-set line: book exc 150.1 climbs past 150, so the
trade is not worth it. Tree reverted to stack-1 (129/129 green). The S-less
shapes are load-bearing for the strain win; rhythm repair needs an approach
that does not move dose mass back onto S days (e.g. peak-placement within
kept variants, not variant swaps).
