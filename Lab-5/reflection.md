# Reflection: Lab 5 Static Code Analysis

## 1. Which issues were the easiest to fix and which were the hardest?

The easiest were the mechanical ones: Flake8's blank-line and line-length warnings, Pylint's naming and f-string warnings, and the missing docstrings. Each had one obvious fix. The hardest were the problems the tools only pointed at indirectly. Bandit flagged the `try/except/pass`, but removing it was not enough, because it had been hiding real bugs. The string `"full"` crashed `sum()`, and an empty route would divide by zero. I had to add input validation in `add_trip_log` and handle empty routes in `average_load` so the code stayed correct after the `except` was gone.

## 2. Did the tools report any false positives, and how would you handle them?

Bandit's B311 warning on `random.choice` is arguably a false positive. Picking a driver is not a security decision, so a predictable generator is not a real risk. I switched to `secrets.choice` anyway, since it is a one-line change and leaves no suppression in the code. The other option is a `# nosec B311` comment with a short justification. I would use that when a fix is costly and the risk is clearly absent. A suppression should always carry a reason, so the next reader knows it was a decision and not an oversight.

## 3. How would you integrate static analysis into a real development workflow?

I would run all three tools automatically instead of by hand. A pre-commit hook would catch style and obvious issues before the code is committed, and a CI check on every pull request would block merges that drop the Pylint score or add Bandit findings. Doing it in stages, as in this lab (security first, then quality, then style), also keeps commits easy to review. I would still keep human code review, because the tools missed some bugs in this file.

## 4. What improvements did you see in code quality after the fixes?

The numbers changed clearly. Pylint went from 6.25/10 to 10.00/10, Bandit went from 2 findings to 0, and Flake8 went from 10 findings to 0. The program also became more reliable: before, it crashed with `KeyError: 'R3'` at the end of the run, and now it runs to completion and rejects bad data with a clear message. The code is easier to read as well, with docstrings, consistent naming, files that close properly and no shared mutable default. The main lesson is that a clean report does not prove the code is correct. Some of the worst problems here, such as the crash and the bad passenger counts, were not reported by any tool and only showed up when I ran the program and read the output.
