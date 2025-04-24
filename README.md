[![Tests](https://github.com/Kirikus/hypermodern_python/workflows/Tests/badge.svg)](https://github.com/Kirikus/hypermodern_python/actions?workflow=Tests)
[![Coverage Status](https://coveralls.io/repos/github/Kirikus/hypermodern_python/badge.svg?branch=main)](https://coveralls.io/github/Kirikus/hypermodern_python?branch=main)

# PyWC Project example

The example project inspired after
[Hypermodern Python](https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769)
article series.
The command-line interface simulates `wc` utility. 

Used as IITP Python teaching material, as a semester project example.

# Usage

Firstly, install python. Recommended method is pyenv (or pyenv-win for Windows).

This project uses poetry as its package manager. Install it, following official [guide](https://python-poetry.org/docs/#installation).
Read "Getting started" for basic usage.

Then, install nox and nox-poetry. These packages are used not only for test automation, but also for providing end users with run-commands.
Run `nox --list` for the list of sessions, and run specific ones with `nox -s SESSION`.

Information about the PyWC program can be obtained by building the docs, which can be done by running `nox -s docs`.

# Grading

For students of IITP course, final grade will be dependent upon completing similar project.
Following grading criteria are used ($G$ is the final grade):

$$ G = 1 + C + T + I + D + E $$

Scoring for different categories:

 - $C$ for code quality
    - Possible scores
       - -1 - full absence of desired functionality (ex.: used code from other project)
       - 1 - code has some functionality and is perfectly readable, or vice versa - if code has full functionality, but lacks readability
       - 2 - code has full functionality and is readable
    - Code readability is measured via `ruff` and visually
    - Code functionality is demostrated at final class via CLI (and tests, if present)
 - $T$ for tests
    - Possible scores
       - -1 - full absence of tests or their extremely poor quality
       - 0 - tests are present only nominally
       - 1 - tests are extensive, but not full: coverage is absent or is below 90%
       - 2 - 90% and above coverage 
    - Failing tests **are** still considered and can improve final score
 - $I$ for integration
    - Possible scores
       - -1 - neither `poetry` or `nox` are used
       - 0 - `poetry` is used, `pyproject.toml` has modern syntax
       - 1 - additionally, `nox` is used for some session targets
       - 2 - all session targets are implemented
	- Other package management systems may be used
    - Required sessions: tests, linting, documentation, typechecks (naming may vary)
 - $D$ for documentation
    - Possible scores
       - -1 - No documentation is present, or README is missing
       - 0 - `sphinx` is used, "Reference" section is created automatically
       - 1 - Examples (with plots) and formulas are included in the documentation
       - 2 - Performance metrics (with plots) are included in the documentation
    - Documentation style is also considered during grading
 - $E$ for extra grade
   - Score from 0 to 3, with *rare* exceptions
   - Given for completing extra homework and/or performing well in classes
   - Extra homework is given during semester, individual scores may vary