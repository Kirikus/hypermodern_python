"""Nox sessions."""

import tempfile
from typing import Any

import nox
from nox.sessions import Session

from pathlib import Path


package = "hypermodern_python"
nox.options.sessions = "lint", "safety", "mypy", "pytype", "tests"
locations = "src", "tests", "noxfile.py", "docs/conf.py"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.

    """
    with tempfile.TemporaryDirectory() as d:
        with (Path(d) / "constraints.txt").open("w") as constraints:
            session.run(
                "poetry",
                "export",
                "--with=dev",
                # "--without-hashes",
                "--format=constraints.txt",
                f"--output={constraints.name}",
                external=True,
            )
            session.install(f"--constraint={constraints.name}", "--use-deprecated=legacy-resolver", *args, **kwargs)


@nox.session(python="3.12")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=["3.12"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python="3.12")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.TemporaryDirectory() as d:
        with (Path(d) / "constraints.txt").open("w") as constraints:
            session.run(
                "poetry",
                "export",
                "--with=main",
                "--format=constraints.txt",
                "--without-hashes",
                f"--output={constraints.name}",
                external=True,
            )
            install_with_constraints(session, "safety")
            session.run("safety", "check", f"--file={constraints.name}", "--full-report")


@nox.session(python=["3.12"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python="3.12")
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=["3.12"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--only=main", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock")
    session.run("pytest", *args)


@nox.session(python=["3.12"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--only=main", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python=["3.12"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--only=main", external=True)
    install_with_constraints(session, "xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python="3.12")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python="3.12")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--only=main", external=True)
    install_with_constraints(session, "sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")
