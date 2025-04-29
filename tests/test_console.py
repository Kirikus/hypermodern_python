"""Test cases for the console module."""

from pathlib import Path

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture, MockType

from pywc.console import main
from pywc.logic import FileStats, Mask

MOCK_LINES = 1
MOCK_WORDS = 3
MOCK_CHARACTERS = 13
MOCK_BYTES = 97


@pytest.fixture
def default_mask() -> Mask:
    """Count everything except bytes."""
    return Mask(byte_count=False, character_count=True, word_count=True, line_count=True)


@pytest.fixture
def mock_logic(mocker: MockerFixture) -> MockType:
    """Fixture for mocking internal calls."""
    mock = mocker.patch("pywc.console.process_file_or_dir")
    mock.return_value = FileStats(
        line_count=MOCK_LINES,
        word_count=MOCK_WORDS,
        character_count=MOCK_CHARACTERS,
        byte_count=MOCK_BYTES,
    )
    return mock


@pytest.fixture
def mock_print(mocker: MockerFixture) -> MockType:
    """Fixture for mocking final print."""
    mock = mocker.patch("pywc.console.pretty_print")
    mock.return_value = None
    return mock


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.mark.usefixtures("runner", "mock_logic", "mock_print")
class TestMain:
    """Tests for pywc.console.main."""

    def test_default_args(self, mock_logic: MockType, runner: CliRunner, default_mask: Mask) -> None:
        """Default mask includes everything except bytes, nothing is ignored."""
        result = runner.invoke(main, ["."])
        mock_logic.assert_called_once_with(Path(), mask=default_mask, ignored_extensions=(), ignored_names=())
        assert result.exit_code == 0

    def test_lines_mask(self, mock_logic: MockType, runner: CliRunner) -> None:
        """Accepts --lines argument."""
        result = runner.invoke(main, [".", "--lines"])
        mock_logic.assert_called_once_with(
            Path(),
            mask=Mask(byte_count=False, character_count=False, word_count=False, line_count=True),
            ignored_extensions=(),
            ignored_names=(),
        )
        assert result.exit_code == 0

    def test_words_mask(self, mock_logic: MockType, runner: CliRunner) -> None:
        """Accepts --words argument."""
        result = runner.invoke(main, [".", "--words"])
        mock_logic.assert_called_once_with(
            Path(),
            mask=Mask(byte_count=False, character_count=False, word_count=True, line_count=False),
            ignored_extensions=(),
            ignored_names=(),
        )
        assert result.exit_code == 0

    def test_characters_mask(self, mock_logic: MockType, runner: CliRunner) -> None:
        """Accepts --characters argument."""
        result = runner.invoke(main, [".", "--characters"])
        mock_logic.assert_called_once_with(
            Path(),
            mask=Mask(byte_count=False, character_count=True, word_count=False, line_count=False),
            ignored_extensions=(),
            ignored_names=(),
        )
        assert result.exit_code == 0

    def test_bytes_mask(self, mock_logic: MockType, runner: CliRunner) -> None:
        """Accepts --bytes argument."""
        result = runner.invoke(main, [".", "--bytes"])
        mock_logic.assert_called_once_with(
            Path(),
            mask=Mask(byte_count=True, character_count=False, word_count=False, line_count=False),
            ignored_extensions=(),
            ignored_names=(),
        )
        assert result.exit_code == 0

    def test_ignored_names(self, mock_logic: MockType, runner: CliRunner, default_mask: Mask) -> None:
        """Accepts --ignore-name argument."""
        result = runner.invoke(main, [".", "--ignore-name", "A", "--ignore-name", "B"])
        mock_logic.assert_called()
        mock_logic.assert_called_once_with(Path(), mask=default_mask, ignored_extensions=(), ignored_names=("A", "B"))
        assert result.exit_code == 0

    def test_ignored_extension(self, mock_logic: MockType, runner: CliRunner, default_mask: Mask) -> None:
        """Accepts --ignore-extension argument."""
        result = runner.invoke(main, [".", "--ignore-extension", ".A", "--ignore-extension", ".B"])
        mock_logic.assert_called()
        mock_logic.assert_called_once_with(Path(), mask=default_mask, ignored_extensions=(".A", ".B"), ignored_names=())
        assert result.exit_code == 0

    def test_nonexistent_files(self, runner: CliRunner) -> None:
        """Exit if any of the files does not exist."""
        result = runner.invoke(main, [".", "missing"])
        assert result.exit_code != 0

    def test_iteration(self, mock_logic: MockType, runner: CliRunner) -> None:
        """Iterates over each input argument."""
        files = ["." for _ in range(10)]
        result = runner.invoke(main, files)
        assert mock_logic.call_count == len(files)
        assert result.exit_code == 0

    def test_total_print(self, mock_print: MockType, runner: CliRunner, default_mask: Mask) -> None:
        """Performs summation and performs final print."""
        files = ["." for _ in range(10)]
        result = runner.invoke(main, files)
        mock_print.assert_called_once_with(
            data=FileStats(
                line_count=MOCK_LINES * 10,
                word_count=MOCK_WORDS * 10,
                character_count=MOCK_CHARACTERS * 10,
                byte_count=MOCK_BYTES * 10,
            ),
            mask=default_mask,
            name="total",
        )
        assert result.exit_code == 0
