
# beam-seed-2

No keeper. All three seed probes reverted (see agent reply for table):

- V1 drop waved seed: winners change (instr 9289->9290). Out of scope.
- V2 swap order: quality bit-identical, pace +0.24 — but breaks the
  seed-order unit test (`test_seed_bulk_climbs_after_big_drop`).
- V3 waved seed only: winners change (instr 9289->9287), pace worse.

Beam seeds stay as-is. No commit on the branch (clean at 37767da).
