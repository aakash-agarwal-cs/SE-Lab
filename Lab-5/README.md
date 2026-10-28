# Lab 5: Static Code Analysis

Static analysis of `shuttle_system.py` (Campus Shuttle Timetable & Fleet Tracker) using Pylint, Bandit and Flake8. The fixes were made in three commits, one per tool.

## Contents

- `shuttle_system.py`: the cleaned script
- `before/`: Pylint, Bandit and Flake8 reports on the original code
- `after/`: the same reports after the fixes
- `issues.md`: table of the issues found and how each was fixed
- `reflection.md`: reflection answers

## Results

| Tool | Before | After |
| ---- | ------ | ----- |
| Bandit | 2 issues (Low) | 0 |
| Pylint | 6.25 / 10 | 10.00 / 10 |
| Flake8 | 10 issues | 0 |

## Run

```
python shuttle_system.py
```
