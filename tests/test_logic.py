"""Test cases for the wikipedia module."""

from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from pywc.logic import FileStats, Mask, pretty_print

MockedFile = (Path, MockerFixture)


@pytest.fixture
def mock_file(request: [int, int, int], mocker: MockerFixture) -> MockedFile:
    """Temporary file with [0] lines, [1] words and [2] characters."""
    lines, words, characters = request.param
    data = (
        b"L\n" * (lines - 1)
        + b"L"
        + b" W" * (words - lines)
        + b"c" * (characters - 2 * (lines - 1) - 1 - 2 * (words - lines))
    )
    return Path("file"), mocker.mock_open(read_data=data)


@pytest.fixture
def file_stats() -> FileStats:
    """Realistically-looking file stats."""
    return FileStats(line_count=111, word_count=222, character_count=333, byte_count=444)


class TestPrettyPrint:
    """Tests for pywc.logic.pretty_print."""

    def test_empty_mask(self, file_stats: FileStats) -> None:
        """Raise on empty mask."""
        with pytest.raises(ValueError, match="Mask.*False.*False.*False.*False"):
            pretty_print(file_stats, Mask())

    def test_single_bit_mask(self, capfd: pytest.LogCaptureFixture, file_stats: FileStats) -> None:
        """Print correct number and only it."""
        pretty_print(file_stats, Mask(line_count=True))
        out = capfd.readouterr()[0]
        assert f"{file_stats.line_count}" in out
        assert f"{file_stats.word_count}" not in out
        assert f"{file_stats.character_count}" not in out
        assert f"{file_stats.byte_count}" not in out

        pretty_print(file_stats, Mask(word_count=True))
        out = capfd.readouterr()[0]
        assert f"{file_stats.line_count}" not in out
        assert f"{file_stats.word_count}" in out
        assert f"{file_stats.character_count}" not in out
        assert f"{file_stats.byte_count}" not in out

        pretty_print(file_stats, Mask(character_count=True))
        out = capfd.readouterr()[0]
        assert f"{file_stats.line_count}" not in out
        assert f"{file_stats.word_count}" not in out
        assert f"{file_stats.character_count}" in out
        assert f"{file_stats.byte_count}" not in out

        pretty_print(file_stats, Mask(byte_count=True))
        out = capfd.readouterr()[0]
        assert f"{file_stats.line_count}" not in out
        assert f"{file_stats.word_count}" not in out
        assert f"{file_stats.character_count}" not in out
        assert f"{file_stats.byte_count}" in out

    def test_append_name(self, capfd: pytest.LogCaptureFixture, file_stats: FileStats) -> None:
        """Append filename to the message."""
        pretty_print(file_stats, Mask(line_count=True), "test_name")
        assert capfd.readouterr()[0].rstrip().endswith("test_name")

    def test_default_name(self, capfd: pytest.LogCaptureFixture, file_stats: FileStats) -> None:
        """Print "total" in the absence of filename."""
        pretty_print(file_stats, Mask(line_count=True))
        assert capfd.readouterr()[0].rstrip().endswith("total")


class TestFileStats:
    """Tests for pywc.logic.FileStats."""

    few_lines = 11
    few_words = 22
    few_characters = 99
    many_lines = 77777
    many_words = 88888
    many_characters = 999999

    def test_stats_positional_constructor(self) -> None:
        """Allow only usage with 4 named arguments."""
        FileStats()
        with pytest.raises(TypeError, match="takes 1 positional argument but 5 were given"):
            FileStats(1, 2, 3, 4)

    def test_add(self) -> None:
        """Add respective fields to create new object."""
        a = FileStats(line_count=111, word_count=222, character_count=333, byte_count=444)
        b = FileStats(line_count=11, word_count=22, character_count=33, byte_count=44)
        c = a + b
        assert c.line_count == a.line_count + b.line_count
        assert c.word_count == a.word_count + b.word_count
        assert c.character_count == a.character_count + b.character_count
        assert c.byte_count == a.byte_count + b.byte_count

    @pytest.mark.parametrize("mock_file", [[few_lines, few_words, few_characters]], indirect=["mock_file"])
    def test_count_data(self, mocker: MockerFixture, mock_file: MockedFile) -> None:
        """Create stats based on file stats."""
        name, mock = mock_file
        mocker.patch("pathlib.Path.open", mock)
        res = FileStats.count_data(name)
        assert res.line_count == TestFileStats.few_lines
        assert res.word_count == TestFileStats.few_words
        assert res.character_count == TestFileStats.few_characters
        assert res.byte_count == TestFileStats.few_characters

    @pytest.mark.parametrize("mock_file", [[many_lines, many_words, many_characters]], indirect=["mock_file"])
    def test_stats_creation_big_file(self, mocker: MockerFixture, mock_file: MockedFile) -> None:
        """Handle large files."""
        name, mock = mock_file
        mocker.patch("pathlib.Path.open", mock)
        res = FileStats.count_data(name)
        assert res.line_count == TestFileStats.many_lines
        assert res.word_count == TestFileStats.many_words
        assert res.character_count == TestFileStats.many_characters
        assert res.byte_count == TestFileStats.many_characters
