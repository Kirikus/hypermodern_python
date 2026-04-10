"""Test cases for the data classes necessary for pywc."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

import pytest

from pywc.data import FileStats


class TestFileStats:
    """Tests for pywc.data.FileStats."""

    def test_positional_constructor(self) -> None:
        """Allow only usage with 4 named arguments."""
        with pytest.raises(TypeError, match="takes 1 positional argument but 5 were given"):
            FileStats(1, 2, 3, 4)  # type: ignore  # noqa: PGH003

    def test_positive_constructor(self) -> None:
        """Allow only usage with positive values."""
        with pytest.raises(ValueError):
            FileStats(lines=-1, words=2, chars=3, bytes=4)
        with pytest.raises(ValueError):
            FileStats(lines=1, words=-2, chars=3, bytes=4)
        with pytest.raises(ValueError):
            FileStats(lines=1, words=2, chars=-3, bytes=4)
        with pytest.raises(ValueError):
            FileStats(lines=1, words=2, chars=3, bytes=-4)

    def test_realistic_order_constructor(self) -> None:
        """Allow only usage with non-decreasing order of lines/words/chars/bytes values."""
        with pytest.raises(ValueError):
            FileStats(lines=4, words=3, chars=2, bytes=1)

    def test_add(self) -> None:
        """Add respective fields to create new object."""
        a = FileStats(lines=111, words=222, chars=333, bytes=444)
        b = FileStats(lines=11, words=22, chars=33, bytes=44)
        c = a + b
        assert c.lines == a.lines + b.lines
        assert c.words == a.words + b.words
        assert c.chars == a.chars + b.chars
        assert c.bytes == a.bytes + b.bytes

    def test_from_small_file(self, small_file: Path, small_file_stats: FileStats) -> None:
        """Handle small files."""
        res = FileStats.from_file(small_file)
        assert res.lines == small_file_stats.lines
        assert res.words == small_file_stats.words
        assert res.chars == small_file_stats.chars
        assert res.bytes == small_file_stats.bytes

    def test_from_big_file(self, large_file: Path, large_file_stats: FileStats) -> None:
        """Handle large files."""
        res = FileStats.from_file(large_file)
        assert res.lines == large_file_stats.lines
        assert res.words == large_file_stats.words
        assert res.chars == large_file_stats.chars
        assert res.bytes == large_file_stats.bytes

    def test_chunksize_spaces(self, create_file: Callable[[int, int, int, str | None], Path]) -> None:
        """Handle large files with space around chunk size (before or after)."""
        chunk_size = 2**16
        res = FileStats.from_file(create_file(0, chunk_size, 3 * chunk_size, None))
        assert res.lines == 0
        assert res.words == chunk_size
        assert res.chars == 3 * chunk_size
        res = FileStats.from_file(create_file(1, chunk_size, 3 * chunk_size, None))
        assert res.lines == 1
        assert res.words == chunk_size
        assert res.chars == 3 * chunk_size
