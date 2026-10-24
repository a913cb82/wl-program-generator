# sched-lock (I SnPull+Other Snatch light-tier ratio lock) — NOT LANDED (budget)

Lead: densest excess cell I Other Snatch @70% pairs, ~7.3 exc / 10 sessions.
Planned move: forbid 1:1 SnPull:Snatch ratio below 80% for CLASS I ONLY,
SnPull+Other Snatch pair only (force pull-heavy 2:1/3:1 at 70%).

Status: 5-min budget expired during recon/baseline. No src/tests change.
Reverted outputs/ noise; tree clean apart from this note.

Baseline (book): score ~0.84, strain 0.96 (exc 144.7), 132 green (pytest).
Target-cell/partner/pair-count fence not measured — needs next session.
Fence on revert: partner-group exc rise > half target-cell fall, or paired
sessions grow → revert.

Next: TDD test on SCHEDULES/allowed_ratios scoping (I-only, pair-only,
light-tier-only), then audit target vs partner cells before/after.
