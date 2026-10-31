# Lab 6: Code and Branch Coverage Analysis

**Module under test:** `hospital_triage_priority.py` (hospital triage acuity scoring + oxygen manifold monitoring)

| File | Purpose |
|------|---------|
| `hospital_triage_priority.py` | Application code |
| `test_hospital_triage.py` | Starter test (1 test, 47% line / 43% branch) |
| `CodeCoverageTest_hospital_triage_priority.py` | Tests for **line coverage** (100%) |
| `BranchCoverageTest_hospital_triage_priority.py` | Tests for **branch coverage** (100%) |
| `screenshots/` | Terminal output screenshots |

## Commands

```bash
pip install coverage pytest

# Code (line) coverage
coverage run -m pytest CodeCoverageTest_hospital_triage_priority.py
coverage report -m

# Branch coverage
coverage run --branch -m pytest BranchCoverageTest_hospital_triage_priority.py
coverage report -m
```

## Results

| Stage | Line coverage | Branch coverage |
|-------|---------------|-----------------|
| Starter test | 47% | 43% |
| Code coverage tests (14 tests) | **100%** | - |
| Branch coverage tests (33 tests) | - | **100%** |
