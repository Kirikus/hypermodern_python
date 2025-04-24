"""Test cases for the wikipedia module."""

import platform
from pathlib import Path

import pytest

from pywc.logic import FileStats, Mask, pretty_print


@pytest.fixture
def file_stats() -> FileStats:
    """Realistically-looking file stats."""
    return FileStats(line_count=111, word_count=222, character_count=333, byte_count=444)


def test_print_empty(file_stats: FileStats) -> None:
    """Raise on empty mask."""
    with pytest.raises(ValueError, match="Mask.*False.*False.*False.*False"):
        pretty_print(file_stats, Mask())


def test_print_singles(capfd: pytest.LogCaptureFixture, file_stats: FileStats) -> None:
    """Print correct number and only it."""
    pretty_print(file_stats, Mask(line_count=True))
    assert f"{file_stats.line_count}" in capfd.readouterr()[0]
    pretty_print(file_stats, Mask(word_count=True))
    assert f"{file_stats.word_count}" in capfd.readouterr()[0]
    pretty_print(file_stats, Mask(character_count=True))
    assert f"{file_stats.character_count}" in capfd.readouterr()[0]
    pretty_print(file_stats, Mask(byte_count=True))
    assert f"{file_stats.byte_count}" in capfd.readouterr()[0]


def test_print_name(capfd: pytest.LogCaptureFixture, file_stats: FileStats) -> None:
    """Append filename to the message."""
    pretty_print(file_stats, Mask(line_count=True), "test_name")
    assert capfd.readouterr()[0].rstrip().endswith("test_name")


def test_print_default_name(capfd: pytest.LogCaptureFixture, file_stats: FileStats) -> None:
    """Print "total" in the absence of filename."""
    pretty_print(file_stats, Mask(line_count=True))
    assert capfd.readouterr()[0].rstrip().endswith("total")


def test_stats_positional_constructor() -> None:
    """Allow only usage with 4 named arguments."""
    FileStats()
    with pytest.raises(TypeError, match="takes 1 positional argument but 5 were given"):
        FileStats(1, 2, 3, 4)


def tess_stats_add() -> None:
    """Add respective fields to create new object."""
    a = FileStats(line_count=111, word_count=222, character_count=333, byte_count=444)
    b = FileStats(line_count=11, word_count=22, character_count=33, byte_count=44)
    c = a + b
    assert c.line_count == a.line_count + b.line_count
    assert c.word_count == a.word_count + b.word_count
    assert c.character_count == a.character_count + b.character_count
    assert c.byte_count == a.byte_count + b.byte_count


@pytest.fixture
def file(request: [int, int, int], tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Temporary file with [0] lines, [1] words and [2] characters."""
    lines, words, characters = request.param
    path = tmp_path_factory.mktemp("data") / "file"
    with path.open("w") as f:
        f.write("L\n" * (lines - 1))
        f.write("L")
        f.write(" W" * (words - lines))
        chars_per_line = 3 if platform.system() == "Windows" else 2
        f.write("c" * (characters - chars_per_line * (lines - 1) - 1 - 2 * (words - lines)))
    return path


few_lines = 11
few_words = 22
few_chars = 77


@pytest.mark.parametrize("file", [[few_lines, few_words, few_chars]], indirect=["file"])
def test_stats_creation(file: Path) -> None:
    """Create stats based on file stats."""
    res = FileStats.count_data(file)
    assert res.line_count == few_lines
    assert res.word_count == few_words
    assert res.character_count == few_chars
    assert res.byte_count == few_chars


many_lines = 77777
many_words = 88888
many_chars = 999999


@pytest.mark.parametrize("file", [[many_lines, many_words, many_chars]], indirect=["file"])
def test_stats_creation_big_file(file: Path) -> None:
    """Handle large files."""
    res = FileStats.count_data(file)
    assert res.line_count == many_lines
    assert res.word_count == many_words
    assert res.character_count == many_chars
    assert res.byte_count == many_chars
