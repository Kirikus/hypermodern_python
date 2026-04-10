"""Common fixture definitions."""

from collections.abc import Callable
from pathlib import Path

import pytest

from pywc.data import CounterFlags, FileStats

PathFactoryT = Callable[[int, int, int, str | None], Path]
CreateFileT = Callable[
    [int, int, int, str | None],  # lines, words, chars, filename=None
    Path,
]


@pytest.fixture
def create_file(tmp_path: Path) -> CreateFileT:
    """Factory that creates a temporary file with exact line/word/char counts.

    Assumes 1 byte/character.
    """

    def _create(
        lines: int,
        words: int,
        chars: int,
        filename: str | None = None,
    ) -> Path:
        if not filename:
            filename = f"{lines}_{words}_chars.txt"
        file = tmp_path / filename
        assert words >= lines
        assert chars > words * 2
        if lines > 0:
            data = b"L\n" * (lines - 1) + b"L" + b" W" * (words - lines) + b"c" * (chars - 2 * words) + b"\n"
        else:
            data = b" W" * words + b"c" * (chars - 2 * words)
        file.write_bytes(data)

        assert file.read_text().count("\n") == lines
        assert len(file.read_text().split()) == words
        assert len(file.read_text()) == chars
        assert len(file.read_bytes()) == chars

        return file

    return _create


@pytest.fixture
def large_file_stats() -> FileStats:
    """FileStats for Larger file with exact line/word/char counts."""
    many_lines = 77777
    many_words = 88888
    many_characters = 999999
    many_bytes = many_characters
    return FileStats(lines=many_lines, words=many_words, chars=many_characters, bytes=many_bytes)


@pytest.fixture
def large_file(create_file: PathFactoryT, large_file_stats: FileStats) -> Path:
    """Larger file with exact line/word/char counts."""
    return create_file(large_file_stats.lines, large_file_stats.words, large_file_stats.chars, "large")


@pytest.fixture
def small_file_stats() -> FileStats:
    """FileStats for smaller file with exact line/word/char counts."""
    few_lines = 11
    few_words = 22
    few_characters = 99
    few_bytes = few_characters
    return FileStats(lines=few_lines, words=few_words, chars=few_characters, bytes=few_bytes)


@pytest.fixture
def small_file(create_file: PathFactoryT, small_file_stats: FileStats) -> Path:
    """Smaller file with exact line/word/char counts."""
    return create_file(small_file_stats.lines, small_file_stats.words, small_file_stats.chars, "small")


@pytest.fixture
def full_counter_flags() -> CounterFlags:
    """All fields set to true."""
    return CounterFlags(lines=True, words=True, chars=True, bytes=True)
