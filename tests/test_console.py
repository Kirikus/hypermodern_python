"""Tests for CLI of pywc package."""

from importlib.metadata import version
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest
from click.testing import CliRunner

from pywc.console import main
from pywc.format import FormatterT
from pywc.navigation import process_path

if TYPE_CHECKING:
    from unittest.mock import Mock

    from pytest_mock import MockerFixture

    from pywc.data import CounterFlags, FileStats


@pytest.fixture
def runner() -> CliRunner:
    """Standard click runner fixture."""
    return CliRunner()


@pytest.fixture
def mock_formatter(mocker: MockerFixture) -> Mock:
    """Mocking side effects of main function, formatter function.

    Returns wrapped function mock instead of decorator.
    """
    m = mocker.patch("pywc.console.formatter_wrapper_print")
    m.return_value = mocker.Mock(spec=FormatterT)
    return m.return_value


@pytest.fixture
def mock_process_path(mocker: MockerFixture, small_file_stats: FileStats) -> Mock:
    """Mocking side effects of main function, process_path function."""
    m = mocker.patch("pywc.console.process_path")
    m.return_value = small_file_stats
    return m


@pytest.fixture
def mock_flags(mocker: MockerFixture) -> Mock:
    """Mocking side effects of main function, CounterFlags class."""
    return mocker.patch("pywc.console.CounterFlags")


@pytest.fixture
def mocked(
    mock_formatter: FormatterT, mock_process_path: type(process_path), mock_flags: CounterFlags
) -> SimpleNamespace:
    """Namespace object containing all the mocks for convenient access in tests."""
    return SimpleNamespace(mock_flags=mock_flags, mock_process_path=mock_process_path, mock_formatter=mock_formatter)


class TestConsole:
    """Tests for main, CLI interface written with click."""

    def test_main_without_arguments_returns_0(self, runner: CliRunner) -> None:
        """Main runs without arguments."""
        result = runner.invoke(main, [])
        assert result.exit_code == 0

    def test_main_no_args_calls_counterflags_with_default_flags(
        self, runner: CliRunner, mocked: SimpleNamespace
    ) -> None:
        """Main has every flag set to True except for bytes."""
        runner.invoke(main, [])
        mocked.mock_flags.assert_called_once_with(
            bytes=False,
            lines=True,
            chars=True,
            words=True,
        )

    @pytest.mark.parametrize(
        ("flag_arg", "expected_flag"),
        [
            (["-c"], "bytes"),
            (["--bytes"], "bytes"),
            (["-m"], "chars"),
            (["--characters"], "chars"),
            (["-w"], "words"),
            (["--words"], "words"),
            (["-l"], "lines"),
            (["--lines"], "lines"),
        ],
    )
    def test_individual_flag_sets_corresponding_counterflag(
        self, runner: CliRunner, flag_arg: [str], expected_flag: str, mocked: SimpleNamespace
    ) -> None:
        """Check long and short form of all flags."""
        runner.invoke(main, flag_arg)
        kwargs = mocked.mock_flags.mock_calls[0].kwargs
        assert kwargs[expected_flag] == True  # noqa: E712
        kwargs[expected_flag] = False
        assert all(x == False for x in kwargs.values())  # noqa: E712

    def test_main_no_args_calls_formatter_once_with_total_case_insensitive(
        self, runner: CliRunner, mocked: SimpleNamespace
    ) -> None:
        """Main prints some total value, formatter is called with total in its args."""
        runner.invoke(main)
        assert mocked.mock_formatter.call_count == 1
        name = mocked.mock_formatter.mock_calls[0].args[-1]
        assert name.lower().startswith("total")  # first arg to formatter_wrapper_print

    def test_main_has_help_option(self, runner: CliRunner) -> None:
        """Help option should be built-in from click."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0

    def test_main_has_version_option(self, runner: CliRunner) -> None:
        """Version option has correct value."""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert version("pywc") in result.output

    def test_main_calls_process_path_for_each_provided_path(
        self, runner: CliRunner, mocked: SimpleNamespace, small_file: Path, mocker: MockerFixture
    ) -> None:
        """There is no protection from duplicates, so we can just call main on the same file twice."""
        paths = [small_file, small_file]
        paths = list(map(str, paths))
        runner.invoke(main, paths)
        assert mocked.mock_process_path.call_count == len(paths)
        expected_calls = [mocker.call(Path(p), mocker.ANY, ignored_regexps=[], formatter=mocker.ANY) for p in paths]
        mocked.mock_process_path.assert_has_calls(expected_calls, any_order=False)

    @pytest.mark.parametrize(
        ("ignored_args", "expected_regexps"),
        [
            (["--ignore-name", ".git"], [".git"]),
            (["--ignore-name", ".git", "--ignore-name", "src"], [".git", "src"]),
            (["--ignore-extension", "py"], ["*.py"]),
            (["--ignore-extension", ".py"], ["*.py"]),
            (["--ignore-extension", ".py", "--ignore-extension", "pyc"], ["*.py", "*.pyc"]),
            (["--ignore-regexp", "test*.py"], [r"test*.py"]),
            (["--ignore-regexp", "test*.py", "--ignore-regexp", "test_*.py"], ["test*.py", "test_*.py"]),
            (
                [
                    "--ignore-name",
                    ".git",
                    "--ignore-name",
                    "src",
                    "--ignore-extension",
                    ".py",
                    "--ignore-extension",
                    "pyc",
                    "--ignore-regexp",
                    "test*.py",
                    "--ignore-regexp",
                    "test_*.py",
                ],
                [".git", "src", "*.py", "*.pyc", "test*.py", "test_*.py"],
            ),
        ],
    )
    def test_ignored_arguments_are_passed_to_process_path_as_regexps(
        self,
        runner: CliRunner,
        ignored_args: [str],
        expected_regexps: [str],
        mocked: SimpleNamespace,
        small_file: Path,
    ) -> None:
        """Ignored names and regexes are set as is, extensions are prefixed with '*.', like *.py example."""
        runner.invoke(main, [*ignored_args, str(small_file)])

        mocked.mock_process_path.assert_called()
        call_kwargs = mocked.mock_process_path.call_args[1]
        assert call_kwargs["ignored_regexps"] == expected_regexps

    def test_main_accumulates_total_and_passes_to_final_formatter(
        self, runner: CliRunner, mocked: SimpleNamespace, small_file: Path, small_file_stats: FileStats
    ) -> None:
        """Scanning same file twice print double statistics in total."""
        runner.invoke(main, [str(small_file), str(small_file)])

        assert mocked.mock_formatter.call_count == 1
        stats = mocked.mock_formatter.mock_calls[0].args[0]

        assert stats.lines == 2 * small_file_stats.lines
        assert stats.words == 2 * small_file_stats.words
        assert stats.chars == 2 * small_file_stats.chars
