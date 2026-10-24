# Order 4day-2: permute 4-day canonical SLMS -> SMSL

Lead: 4-day weeks (SLMS) miss a turn by construction. Same multiset, different sequence.

Baseline (stack-1): book score 0.855 | strain 0.99 (exc 147.8 short 0.0) | size 0.92 | rhythm 2.09 | drift -0.12 (pace -0.28)
Trial SMSL: book score 0.852 | strain 1.13 (exc 169.6 short 0.1) | size 0.91 | rhythm 1.96 | drift -0.35 (pace -0.51)

Rhythm improved 2.09 -> 1.96 but strain + drift regressed; net book -0.003.
No test fence hit on edit (pytest not run mid-trial due to budget; reverted tree passes 129/129).
Verdict: REVERTED — idea directionally correct for rhythm, wrong for book. Keep SLMS.
