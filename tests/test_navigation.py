"""Test cases for the Path navigation code necessary for pywc."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pywc.data import CounterFlags, FileStats
from pywc.format import FormatterT
from pywc.navigation import process_path


@pytest.fixture
def formatter_mock() -> FormatterT:
    """Stub for formatter calls, used to calculate calls to it."""
    return MagicMock(spec=FormatterT)


def symlink_fails() -> bool:
    """True if current platform does not support symlinks."""
    d = Path("symlink_test_dir")
    d.mkdir()
    (link, target) = d / "link", d / "target"
    try:
        target.write_text("target")
        link.symlink_to(target)
        assert link.read_text() == "target"
        link.unlink()
        target.unlink()
    except OSError:
        link.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        d.rmdir()
        return True
    return False


SYMLINK_FAILS = symlink_fails()


class TestProcessPath:
    """Tests for pywc.navigation.process_path function."""

    def test_stats_small_file(self, small_file: Path, small_file_stats: FileStats) -> None:
        """Process a single file returns correct stats."""
        result = process_path(small_file, CounterFlags())
        assert result == small_file_stats

    def test_stats_large_file(self, large_file: Path, large_file_stats: FileStats) -> None:
        """Process a single file returns correct stats."""
        result = process_path(large_file, CounterFlags())
        assert result == large_file_stats

    def test_non_existent_path_is_zero(self) -> None:
        """Non-existent path returns zero FileStats."""
        result = process_path(Path("/non/existent/path"), CounterFlags())
        assert result == FileStats(lines=0, words=0, chars=0, bytes=0)  # zero value

    def test_empty_directory_is_zero(self, tmp_path: Path) -> None:
        """Empty directory returns zero stats."""
        result = process_path(tmp_path, CounterFlags())
        assert result == FileStats(lines=0, words=0, chars=0, bytes=0)

    def test_ignored_file_is_zero(self, small_file: Path) -> None:
        """Files matching any ignored regexp are skipped (return zero stats)."""
        result = process_path(
            small_file,
            CounterFlags(),
            ignored_regexps=["*mal*"],
        )
        assert result == FileStats(lines=0, words=0, chars=0, bytes=0)

    def test_ignored_directory_is_zero(self, tmp_path: Path) -> None:
        """Directories matching ignored regex are skipped entirely."""
        dir_path = tmp_path / "ignored_dir"
        dir_path.mkdir()
        (dir_path / "test.txt").write_text("content")

        result = process_path(
            tmp_path,
            CounterFlags(),
            ignored_regexps=[r"*ignored_dir*"],
        )

        # Should ignore the whole directory → zero stats
        assert result == FileStats(lines=0, words=0, chars=0, bytes=0)

    def test_directory_with_multiple_files(
        self,
        tmp_path: Path,
    ) -> None:
        """Processing a directory aggregates stats from all files recursively."""
        # Setup test directory structure
        file1 = tmp_path / "file1.txt"
        file1.write_text("hello")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        file2 = subdir / "file2.txt"
        file2.write_text("world")

        assert process_path(tmp_path, CounterFlags()) == process_path(file1, CounterFlags()) + process_path(
            file2, CounterFlags()
        )

    def test_calls_formatter_for_each_file(
        self,
        tmp_path: Path,
        formatter_mock: FormatterT,
    ) -> None:
        """Formatter is called once per processed file (not for directories)."""
        # Create a small directory with 2 files
        dir_path = tmp_path / "testdir"
        dir_path.mkdir()
        (dir_path / "a.txt").write_text("a")
        (dir_path / "b.txt").write_text("b")

        process_path(dir_path, CounterFlags(), formatter=formatter_mock)

        assert formatter_mock.call_count == 2  # noqa:PLR2004

    def test_does_not_call_formatter_on_ignored_files(self, small_file: Path, formatter_mock: FormatterT) -> None:
        """Formatter is not called for files that match ignored_regexps."""
        process_path(
            small_file,
            CounterFlags(),
            ignored_regexps=["*"],
            formatter=formatter_mock,
        )

        formatter_mock.assert_not_called()

    @pytest.mark.skipif(SYMLINK_FAILS, reason="Symlinks are unsupported")
    def test_symlink_to_file(self, small_file: Path, small_file_stats: FileStats, tmp_path: Path) -> None:
        """Symlinks to files should be followed and processed."""
        symlink = tmp_path / "link_to_small.txt"
        symlink.symlink_to(small_file)

        result = process_path(symlink, CounterFlags())
        assert result == small_file_stats

    @pytest.mark.skipif(SYMLINK_FAILS, reason="Symlinks are unsupported")
    def test_broken_symlink(self, tmp_path: Path) -> None:
        """Broken symlinks should return zero stats (as per current implementation)."""
        broken = tmp_path / "broken_link"
        broken.symlink_to("/non/existent/target")

        result = process_path(broken, CounterFlags())
        assert result == FileStats(lines=0, words=0, chars=0, bytes=0)
