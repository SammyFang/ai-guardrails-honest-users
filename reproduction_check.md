# Publication reproduction check

Checked on November 10, 2026, on Windows with Python 3.13.5 and the pinned numerical/plotting packages.

The release folder started without original data or an original notebook. `python run.py --current-env` downloaded all three official sources, verified their SHA256 hashes and completed with exit code 0.

- Independent implementation: **5,032 checks passed**; maximum absolute numeric discrepancy `2.220446049250313e-16`.
- Original saved notebook counts: **4 of 4 matched** (1,341 / 1,193 / 1,288 / 1,155).
- The primary estimate and confidence limits match the frozen analysis: `0.030674390968508613`, `[0.021316102198455138, 0.04047831253713607]` on the probability scale.
- The rates/interval figures were generated from `tables/effects.csv` and visually checked for labels, units, confidence intervals and clipping.
- The tracked-file audit excludes original data, individual-level derived records, original notebooks, article PDFs, credentials, environment folders and per-person numeric audit rows.

This verifies the released analysis implementation and limited saved-count reproduction. It does not reproduce historical API generations or every original regression, and it does not validate causal psychological mechanisms.
