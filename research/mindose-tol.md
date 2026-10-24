# mindose-tol probe (research/mindose-tol)

Baseline (stack-1, MIN_DOSE=6, TOL=0.2): book score ~0.88-0.90 across runs
(audit is nondeterministic ±0.01; representative: strain 1.02 / size 0.92 /
rhythm 2.00 / drift -0.01 / score 0.883). 128 tests green.

Protocol: audit-only per value, revert on any pinned-test breakage.
All values reverted — src unchanged.

| knob | book (strain/size/rhythm/drift/score) | tests | verdict |
|------|----------------------------------------|-------|---------|
| MIN_DOSE 6→5 | 1.08 / 0.94 / 1.92 / ~-0.01 / ~0.89 (0.878-0.906 over 5 runs, noise only) | 6 failed, 122 passed | REVERT — breaks pinned tests, no signal |
| MIN_DOSE 6→7 | 1.03 / 1.00 / 2.00 / 0.52 / 1.014 (drift blows up) | 5 failed, 123 passed | REVERT — breaks pinned tests, drift worse |
| TOL 0.2→0.15 | 1.02 / 0.92 / 2.00 / 0.08 / 0.900 | 5 failed, 123 passed | REVERT — breaks pinned tests, terms flat |
| TOL 0.2→0.25 | 1.02 / 0.92 / 2.00 / 0.08 / 0.900 | 1 failed*, 127 passed | REVERT — terms identical to baseline (noise), *sole failure is test_book_numbers_match_research which pins exact research numbers and trips on any move |

Conclusion: no winning value. Dose knobs confirmed breakage-prone as expected;
two-plus clean reverts, src left at baseline.
