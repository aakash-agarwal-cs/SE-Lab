# Issues found in `shuttle_system.py`

Line numbers refer to the original file. Severity order: Bandit (security), Pylint (quality), Flake8 (style), then bugs no tool reported.

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| Try/except/pass (B110) | Security (Bandit, Low) | 29-30 | Errors in `average_load` were silently swallowed, which hid the `"full"` data bug and dropped R3 from the "Underused" result. | Removed the try/except. Bad data is now rejected when it is added, and `average_load` handles empty routes explicitly. |
| Weak PRNG (B311) | Security (Bandit, Low) | 35 | `random.choice` is not suitable for security-sensitive selection. | Replaced with `secrets.choice`, so the finding is fixed without a `# nosec` suppression. |
| Bare `except` (W0702 / E722) | Bug / Style | 29 | Catches every exception, including `KeyboardInterrupt`, and hides real bugs. | Removed along with the B110 fix (the same line caused both findings). |
| Mutable default argument (W0102) | Bug | 11 | `logs=[]` is created once and shared across every call, so logs leak between calls. | Default changed to `None`; a new list is created inside the function. |
| Unvalidated passenger counts | Bug (no tool flagged) | 49-50 | `-6` and `"full"` were accepted as trip data. `sum()` then crashed on the string, and the negative value skewed averages. | `add_trip_log` raises `ValueError` for non-integer or negative counts. `main` catches it and reports the skipped entry. |
| Division by zero on empty route | Bug (no tool flagged) | 21 | `average_load` divides by `len(trips)`, which is 0 for a route with no trips. | Returns `0.0` when there are no trips, so an empty route counts as under-used. |
| `KeyError: 'R3'` crash | Bug (no tool flagged) | 55-58 | `main` removes R3 and then calls `average_load("R3")`. Looking up an unknown route also crashed. | `main` checks that the route exists before looking it up and prints a message otherwise. |
| `global` statement (W0603) | Quality (Pylint) | 38 | `sync_fleet_data` rebinds the module-level `routes`. | Updates `routes` in place with `clear()` and `update()`, so no `global` is needed. |
| `open()` without `with` or encoding (R1732, W1514) | Quality (Pylint) | 39, 42 | File handles were not closed on error, the read handle was never closed, and the default encoding is platform-dependent. | Used `with open(..., encoding="utf-8")` and `json.dump` / `json.load`. |
| Function name `assignDriver` (C0103) | Style (Pylint) | 33 | Not snake_case. | Renamed to `assign_driver` and updated the caller. |
| Unused argument `route_id` (W0613) | Quality (Pylint) | 33 | The argument was never used. | `assign_driver` now checks that the route exists before assigning. |
| `%` formatting (C0209) | Style (Pylint) | 13 | Old-style string formatting. | Converted to an f-string. |
| Missing docstrings (C0114, C0116) | Documentation (Pylint) | 1, 11, 16, 19, 23, 33, 37, 45 | No module or function docstrings. | Added a one-line docstring to the module and to every function. |
| Missing blank lines (E302, E305) | Style (Flake8) | 11, 16, 19, 23, 33, 37, 45, 60 | PEP 8 requires two blank lines around top-level definitions. | Added the blank lines. `main()` now sits under an `if __name__ == "__main__":` guard. |
| Line too long (E501) | Style (Flake8) | 13 | 82 characters, over the 79 limit. | Shortened the line. |

## Results

| Tool | Before | After |
| ---- | ------ | ----- |
| Bandit | 2 issues (Low) | 0 |
| Pylint | 6.25 / 10 | 10.00 / 10 |
| Flake8 | 10 issues | 0 |
