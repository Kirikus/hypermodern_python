# ruff: Python Linting and Formatting

Clean code isn’t written once — it is maintained every day.

## Why Use Formatters and Linters?

**Linters** analyze your code for potential errors, style violations, bugs, and best-practice issues.
They help maintain code quality and catch problems early.

**Formatters** automatically rewrite your code to follow consistent style rules (spacing, quotes, line length, etc.).
They eliminate debates about "how it should look" and make diffs cleaner.

**Key difference**:

- Linter → tells you what's wrong (and can often auto-fix it)
- Formatter → silently makes the code look correct

Using both together dramatically improves code readability and maintainability with almost zero manual effort.

Often tools feature integration with IDE, CI/CD and githooks.

## Ruff – The Modern Python Tool

[Ruff](https://docs.astral.sh/ruff/) is a fast Python linter and formatter written in Rust.

**Why Ruff is usually the best choice**:

- Extremely fast (often 10–100× faster than alternatives like Flake8 + Black + isort)
- Single tool that replaces many others: Flake8, PyFlakes, pycodestyle, pydocstyle, isort, pyupgrade, autoflake, etc.
- Actively maintained with very frequent updates
- Excellent VS Code / PyCharm / Neovim integration
- Can run as a pre-commit hook or in CI with almost no overhead

For most projects in 2026, Ruff is the recommended default.

## Setup and Configuration

Ruff is configured in ``pyproject.toml`` (recommended), ``ruff.toml``, or ``.ruff.toml``.

Basic recommended structure:

```toml
    [tool.ruff]
    target-version = "py314"
    line-length = 120
    indent-width = 4
    exclude = ["docs"]

    [tool.ruff.format]
    indent-style = "space"
    quote-style = "double"

    [tool.ruff.lint]
    select = ["ALL"]
    ignore = [
        "AIR", "COM812", "COM819", "DJ", "E111", "E114", "E117",
        "FAST", "FIX", "G", "INT", "LOG",
        "Q000", "Q001", "Q002", "Q003", "Q004",
        "W191",
        # Add more ignores as needed for your project
    ]

    fixable = ["ALL"]

    # Docstring convention (automatically deselects incompatible D rules)
    pydocstyle.convention = "google"
```

Per-file overrides are supported and very useful:

```toml
    [tool.ruff.lint.per-file-ignores]
    "tests/*.py" = [
        "S101",    # asserts are fine in tests
        "INP001",  # implicit namespace package
        "PT011",   # broad pytest.raises(Exception)
    ]
```
See the full configuration guide:
https://docs.astral.sh/ruff/configuration/

## Choosing a Good Rule Set

MMy personal recommendation for a starting point is ``select = ["ALL"]`` combined with a small, project-specific ``ignore`` list.

**Tips for choosing rules**:

- Start broad (`ALL`) and selectively disable categories or individual rules you don't need.
- Disable entire categories when the framework/tool is not used (e.g. ``DJ`` for Django, ``FAST`` for FastAPI, ``AIR`` for Airflow).
- Keep ``FIX`` disabled if you want to allow TODO/FIXME comments.
- Use ``pydocstyle.convention = "google"`` (or ``"numpy"`` / ``"pep257"``) for consistent docstrings.
- Review ignored rules periodically — many rules become useful as the project matures.

Formatter-specific considerations:
https://docs.astral.sh/ruff/formatter/

## Other File Types

Ruff also supports linting and formatting for Jupyter notebooks, but many projects benefit from dedicated tools for configuration files.

**Recommendation**: Use [pyproject-fmt](https://pyproject-fmt.readthedocs.io/en/latest/) to keep your ``pyproject.toml`` clean and consistently formatted.

## Stricter linting of docstrings

### Why ruff does not enforce full documentation in docstrings

Ruff provides style and convention checks for docstrings via its ``D`` rules (pydocstyle) and a growing set of ``DOC`` rules inspired by pydoclint. It deliberately limits full content enforcement to keep rules practical and avoid excessive noise on simple functions or during gradual adoption.

The main reasons are:
- Focus on widely accepted conventions (PEP 257, Google, NumPy, Sphinx styles) rather than exhaustive project-specific completeness.
- Maintaining speed and lightness of the core linter; deep content checks are better handled by dedicated tools.
- Allowing teams to start with style before adding strictness.

### What ruff enforces

Ruff's ``D`` rules cover:

- Presence of docstrings on public modules, classes, functions, and methods (with configurable exceptions).
- Formatting and structure: summary line, blank lines, indentation, section ordering, and style-specific conventions (google, numpy, pep257).

Ruff also includes partial ``DOC`` rules (in preview or recent additions) that overlap with pydoclint, such as checks for missing or extraneous parameters, returns, yields, and exceptions in some cases.

However, ruff does not have the full set of pydoclint checks. It misses several detailed validations around argument matching, class attributes, parsing edge cases, and stricter consistency between docstring and implementation.

### Enforcing complete documentation using pydoclint

For strict verification that docstrings fully and accurately document arguments, returns, yields, raises, class attributes, etc., and that they match the actual code, use [pydoclint](https://jsh9.github.io/pydoclint/https://jsh9.github.io/pydoclint/).

pydoclint is a fast docstring linter focused on content completeness for NumPy, Google, and Sphinx styles. It catches issues like undocumented parameters, extra documented items not in the signature, mismatched returns/yields, and more.

Key features include checks for:
- Argument sections matching function signature.
- Return, yield, and raise sections.
- Class docstrings and attributes.
- Parsing and style-specific violations.

[Configuration options](https://jsh9.github.io/pydoclint/config_options.html) allow for different degree of strictness for checks.

Recommended workflow:
1. Use ruff for style, presence, and basic structure via ``D`` rules.
2. Add pydoclint for full content enforcement in CI or pre-commit.
3. Start lenient (e.g., skip short docstrings) and tighten gradually.

This combination gives speed and broad coverage from ruff plus depth from pydoclint.

## Further Reading

- [Ruff documentation](https://docs.astral.sh/ruff/).
- [Rules reference](https://docs.astral.sh/ruff/rules/).
- [Configuration options](https://docs.astral.sh/ruff/configuration/).
- [Pre-commit integration](https://github.com/astral-sh/ruff-pre-commit).
- [Editor integration](https://docs.astral.sh/ruff/editors/).