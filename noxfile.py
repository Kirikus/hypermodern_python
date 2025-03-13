"""Nox sessions."""

import tempfile
from pathlib import Path

import nox
import nox_poetry
from nox_poetry.sessions import Session

package = "pywc"
nox.options.sessions = "formatter", "linter", "mypy", "pytype", "tests"
locations = "src", "tests", "noxfile.py", "docs/conf.py", "plots"


@nox_poetry.session(python="3.12")
def formatter(session: Session) -> None:
    """Run ruff code formatter."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "format", *args)


@nox_poetry.session(python=["3.12"])
def linter(session: Session) -> None:
    """Lint using ruff."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", "--fix", *args)


@nox_poetry.session(python="3.12")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.TemporaryDirectory() as d, (Path(d) / "constraints.txt").open("w") as constraints:
        session.run(
            "poetry",
            "export",
            "--with=main",
            "--format=constraints.txt",
            "--without-hashes",
            f"--output={constraints.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "scan", f"--file={constraints.name}", "--full-report")


@nox_poetry.session(python=["3.12"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox_poetry.session(python="3.12")
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


@nox_poetry.session(python=["3.12"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--only=main", external=True)
    session.install("coverage[toml]", "pytest", "pytest-cov", "pytest-mock")
    session.run("pytest", *args)


@nox_poetry.session(python=["3.12"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--only=main", external=True)
    session.install("pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox_poetry.session(python=["3.12"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--only=main", external=True)
    session.install("xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox_poetry.session(python="3.12")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox_poetry.session(python="3.12")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", external=True)
    #session.run("poetry", "install", "--only=main", external=True)
    session.install(
        "sphinx",
        "myst-parser",
        "sphinx-autodoc2",
        "sphinx-click",
        "furo",
        "matplotlib",
    )
    session.run("sphinx-build", "docs", "docs/_build")
