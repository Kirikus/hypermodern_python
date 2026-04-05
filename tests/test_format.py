"""Tests for string format of FileStats objects."""

import pytest

from pywc.data import CounterFlags, FileStats
from pywc.format import format_automatic


class TestFormatAutomatic:
    """Tests for format_automatic, which implies non-human readable format w/o dimensions (like Kb)."""

    def test_raises_value_error_when_no_flags_enabled(self, small_file: FileStats) -> None:
        """Should raise ValueError if no output fields are requested."""
        no_flags = CounterFlags(lines=False, words=False, chars=False, bytes=False)

        with pytest.raises(ValueError) as exc_info:
            format_automatic(small_file, no_flags)

        assert exc_info.value.args[0] is no_flags

    @pytest.mark.parametrize("name", ["file.txt", "very_long_filename_that_should_be_truncated_in_display.txt"])
    def test_name_formatting(self, name: str, small_file_stats: FileStats, full_counter_flags: CounterFlags) -> None:
        """Name should be left-aligned if provided."""
        result = format_automatic(small_file_stats, full_counter_flags, name=name)
        assert result.startswith(name)

    def test_only_lines(self, small_file_stats: FileStats) -> None:
        """Contain only lines count."""
        result = format_automatic(small_file_stats, CounterFlags(lines=True, words=False, chars=False, bytes=False))
        assert result == str(small_file_stats.lines)

    def test_only_words(self, small_file_stats: FileStats) -> None:
        """Contain only words count."""
        result = format_automatic(small_file_stats, CounterFlags(lines=False, words=True, chars=False, bytes=False))
        assert result == str(small_file_stats.words)

    def test_only_chars(self, small_file_stats: FileStats) -> None:
        """Contain only chars count."""
        result = format_automatic(small_file_stats, CounterFlags(lines=False, words=False, chars=True, bytes=False))
        assert result == str(small_file_stats.chars)

    def test_only_bytes(self, small_file_stats: FileStats) -> None:
        """Contain only bytes count."""
        result = format_automatic(small_file_stats, CounterFlags(lines=False, words=False, chars=False, bytes=True))
        assert result == str(small_file_stats.bytes)

    @pytest.mark.parametrize(
        "name", [" file.txt", "file txt", "file.txt ", " very long filename with spaces everywhere "]
    )
    def test_name_with_spaces(self, name: str, small_file_stats: FileStats) -> None:
        """Names with spaces should still be formatted to 20 chars."""
        flags = CounterFlags(lines=True)
        result = format_automatic(small_file_stats, flags, name=name)

        assert result.startswith(name)  # left aligned, padded to 20

    def test_output_contains_only_expected_parts(
        self, small_file_stats: FileStats, full_counter_flags: CounterFlags
    ) -> None:
        """Smoke test: output should only contain name + enabled numeric fields."""
        result = format_automatic(small_file_stats, full_counter_flags, name="name")

        assert result.startswith("name")
        assert result.endswith(str(small_file_stats.bytes))

        parts = result.split()
        assert len(parts) == 5  # noqa:PLR2004
        assert parts[0] == "name"
        assert parts[1] == str(small_file_stats.lines)
        assert parts[2] == str(small_file_stats.words)
        assert parts[3] == str(small_file_stats.chars)
        assert parts[4] == str(small_file_stats.bytes)

    def test_empty_name_vs_no_name(self, small_file_stats: FileStats, full_counter_flags: CounterFlags) -> None:
        """Passing name='' should behave same as not passing name (or name=None)."""
        result1 = format_automatic(small_file_stats, full_counter_flags, name="")
        result2 = format_automatic(small_file_stats, full_counter_flags)

        assert result1 == result2
