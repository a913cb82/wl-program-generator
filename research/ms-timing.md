# MS timing: left-rotate each meso's week volumes by one

## Change
`src/wlgen.py`, in `build_plan`, right after `week_vols = allocate(vol, split)`:

```python
if cls == "MS":
    week_vols = week_vols[1:] + week_vols[:1]
```

MS only. Peak week moves one slot earlier in every meso; same shapes, new
order. Everything downstream (sessions, chains, spills) rebuilds
deterministically from the rotated volumes.

## Result (`.venv/bin/wlgen audit`)
- book: score 0.832 -> 0.827, exc 144.7 -> 142.5, strain 0.96 -> 0.95
- MS: strain 0.28 -> 0.27 (exc 42.5 -> 40.3), rhythm 2.96 -> 2.91, size/instr 2026 -> 2003
- other classes byte-identical (III/II/I/CMS untouched)
- tests: 136 -> 138 passed (new `tests/test_ms_timing.py`: volume preserved,
  deterministic); golden updates confined to MS week order
  (`test_day_patterns` MS exception map, `test_html` W1 290 -> 387,
  `test_book_numbers` exc/instr/slots)

## Gate: KEEP
- book improved (0.827 < 0.841), exc 142.5 <= 144.7
- zero failures (138 passed)
- MS rhythm 2.91 within [2.80, 3.01]

## Bet outcome
Same shapes in a different order moved rhythm (2.96 -> 2.91) and pace as
predicted; strain-led improvement carried the book. No wlscore change.
