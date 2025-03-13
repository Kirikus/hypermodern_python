"""Test cases for the wikipedia module."""

import itertools
from pathlib import Path

import pytest

from pywc.navigation import is_ignored

files = [Path("file.py"), Path("file.tar.gz")]
dirs = [Path(), Path(), Path(".."), Path("tests/")]
paths = [d / f for d, f in itertools.product(dirs, files)] + files + dirs


@pytest.mark.parametrize("file", paths)
def test_ignore_nothing(file: Path) -> None:
    """Return False if no names or extensions are ignored."""
    assert not is_ignored(file)
    assert not is_ignored(file, ignored_extensions=[], ignored_names=[])


@pytest.mark.parametrize("file", paths)
def test_ignore_different_extension(file: Path) -> None:
    """Return False if no names or extensions are ignored."""
    path = Path(str(file))
    extension = path.suffix
    if not extension:
        return
    assert not is_ignored(path)
    assert not is_ignored(path, ignored_extensions=[".a", ".z"]) or extension in [".a", ".z"]
    assert is_ignored(path, ignored_extensions=[extension])
    assert is_ignored(path, ignored_extensions=[".a", extension, ".z"])


@pytest.mark.parametrize("file", paths)
def test_ignore_same_extension(file: Path) -> None:
    """Return True iff that exact extension is present."""
    path = Path(str(file))
    extension = path.suffix
    if not extension:
        return
    assert not is_ignored(path, ignored_extensions=[".a", ".z"]) or extension in [".a", ".z"]
    assert is_ignored(path, ignored_extensions=[extension])
    assert is_ignored(path, ignored_extensions=[".a", extension, ".z"])


@pytest.mark.parametrize("file", paths)
def test_ignore_multiple_extensions(file: Path) -> None:
    """Return True if that exact extension is in the middle, like "file.py.old"."""
    path = Path(str(file))
    extension = path.suffix
    if not extension:
        return
    other = extension + "_"
    assert is_ignored(path.with_name(path.name + other), ignored_extensions=[".a", extension, ".z"])
    assert is_ignored(path.with_name(path.stem + other + path.suffix), ignored_extensions=[".a", extension, ".z"])
