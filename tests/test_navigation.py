"""Test cases for the wikipedia module."""

import itertools
from pathlib import Path

import pytest
from pytest_mock import MockerFixture, MockType

from pywc.logic import FileStats, Mask
from pywc.navigation import is_ignored, process_file, process_file_or_dir

files = [Path("file.py"), Path("file.tar.gz")]
dirs = [Path(), Path(), Path(".."), Path("tests/")]
paths = [d / f for d, f in itertools.product(dirs, files)] + files + dirs

MOCK_LINES = 1
MOCK_WORDS = 3
MOCK_CHARACTERS = 13
MOCK_BYTES = 97


class TestIsIgnored:
    """Tests for pywc.navigation.is_ignored."""

    @pytest.mark.parametrize("file", paths)
    def test_ignore_nothing(self, file: Path) -> None:
        """Return False if no names or extensions are ignored."""
        assert not is_ignored(file)
        assert not is_ignored(file, ignored_extensions=[], ignored_names=[])

    @pytest.mark.parametrize("file", paths)
    def test_ignore_different_extension(self, file: Path) -> None:
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
    def test_ignore_same_extension(self, file: Path) -> None:
        """Return True iff that exact extension is present."""
        path = Path(str(file))
        extension = path.suffix
        if not extension:
            return
        assert not is_ignored(path, ignored_extensions=[".a", ".z"]) or extension in [".a", ".z"]
        assert is_ignored(path, ignored_extensions=[extension])
        assert is_ignored(path, ignored_extensions=[".a", extension, ".z"])

    @pytest.mark.parametrize("file", paths)
    def test_ignore_multiple_extensions(self, file: Path) -> None:
        """Return True if that exact extension is in the middle, like "file.py.old"."""
        path = Path(str(file))
        extension = path.suffix
        if not extension:
            return
        other = extension + "_"
        assert is_ignored(path.with_name(path.name + other), ignored_extensions=[".a", extension, ".z"])
        assert is_ignored(path.with_name(path.stem + other + path.suffix), ignored_extensions=[".a", extension, ".z"])


@pytest.fixture
def mock_filter(mocker: MockerFixture) -> MockType:
    """Fixture for mocking is_ignored."""
    mock = mocker.patch("pywc.navigation.is_ignored")
    mock.return_value = False
    return mock


@pytest.fixture
def mock_print(mocker: MockerFixture) -> MockType:
    """Fixture for mocking final print."""
    mock = mocker.patch("pywc.navigation.pretty_print")
    mock.return_value = None
    return mock


@pytest.fixture
def mock_count(mocker: MockerFixture) -> MockType:
    """Fixture for mocking internal calls."""
    mock = mocker.patch("pywc.navigation.FileStats.count_data")
    mock.return_value = FileStats(
        line_count=MOCK_LINES,
        word_count=MOCK_WORDS,
        character_count=MOCK_CHARACTERS,
        byte_count=MOCK_BYTES,
    )
    return mock


@pytest.mark.usefixtures("mock_filter", "mock_count", "mock_print")
class TestProcessFile:
    """Tests for pywc.logic.process_file."""

    def test_skip_file(self, mock_filter: MockType, mock_count: MockType, mock_print: MockType) -> None:
        """Return immediately on ignored file."""
        mock_filter.return_value = True
        stats = process_file(Path("file"), Mask())
        assert stats.byte_count == stats.character_count == stats.word_count == stats.line_count == 0
        assert mock_filter.called
        assert not mock_print.called
        assert not mock_count.called

    def test_normal(self, mock_filter: MockType, mock_count: MockType, mock_print: MockType) -> None:
        """After all checks, data is calculated and printed."""
        process_file(Path("file"), Mask())
        assert mock_filter.called
        assert mock_print.called
        assert mock_count.called


class MockedPath:
    """Mock for either a file or a directory with NESTED_COUNT files."""

    NESTED_COUNT = 3

    def __init__(self, mocker: MockerFixture, *, file: bool = True) -> None:
        """
        Construct mock collection with default meaningful returns.

        Boolean argument switches between file and directory mock modes.
        """
        self.mock_exists = mocker.patch("pywc.navigation.Path.exists")
        self.mock_exists.return_value = True
        self.mock_is_file = mocker.patch("pywc.navigation.Path.is_file")
        if file:
            self.mock_is_file.return_value = True
        else:
            self.mock_is_file.side_effect = [False] + [True] * MockedPath.NESTED_COUNT
        self.mock_iterdir = mocker.patch("pywc.navigation.Path.iterdir")
        if file:
            self.mock_iterdir.return_value = None
        else:
            self.mock_iterdir.return_value = [Path("file") for _ in range(MockedPath.NESTED_COUNT)]


@pytest.fixture
def mock_navigation_file(mocker: MockerFixture) -> MockedPath:
    """Return MockedPath for a single file."""
    return MockedPath(mocker, file=True)


@pytest.fixture
def mock_navigation_directory(mocker: MockerFixture) -> MockedPath:
    """Return MockedPath for directory with MockedPath.NESTED_COUNT files."""
    return MockedPath(mocker, file=False)


@pytest.mark.usefixtures("mock_filter", "mock_count", "mock_print")
class TestProcessFileOrDir:
    """Tests for pywc.navigation.process_file_or_dir."""

    def test_file_identified(
        self,
        mock_navigation_file: MockedPath,
        mock_filter: MockType,
        mock_count: MockType,
    ) -> None:
        """Call process_file on a normal file."""
        process_file_or_dir(Path("file"), Mask(byte_count=True))
        assert mock_navigation_file.mock_exists.called
        assert mock_filter.called
        assert mock_count.call_count == 1
        assert not mock_navigation_file.mock_iterdir.called

    def test_missing_directory(
        self,
        mock_navigation_file: MockedPath,
        mock_count: MockType,
        mock_print: MockType,
    ) -> None:
        """Skip processing missing paths, without raising Exceptions."""
        mock_navigation_file.mock_exists.return_value = False
        stats = process_file_or_dir(Path("file"), Mask(byte_count=True))
        assert stats.byte_count == stats.character_count == stats.word_count == stats.line_count == 0
        assert mock_navigation_file.mock_exists.called
        assert not mock_count.called
        assert not mock_print.called
        assert not mock_navigation_file.mock_iterdir.called

    def test_ignored_directory(
        self,
        mock_navigation_directory: MockedPath,
        mock_filter: MockType,
        mock_count: MockType,
    ) -> None:
        """Skip processing ignored paths, without raising Exceptions."""
        mock_filter.return_value = True
        stats = process_file_or_dir(Path("file"), Mask(byte_count=True))
        assert stats.byte_count == stats.character_count == stats.word_count == stats.line_count == 0
        assert mock_filter.called
        assert not mock_count.called
        assert not mock_navigation_directory.mock_iterdir.called

    def test_recursive_process(
        self,
        mock_navigation_directory: MockedPath,
        mock_filter: MockType,
        mock_count: MockType,
    ) -> None:
        """Enter directories and process entities in them one by one."""
        stats = process_file_or_dir(Path("file"), Mask(byte_count=True))
        assert mock_count.call_count == MockedPath.NESTED_COUNT
        assert mock_filter.call_count == 1 + MockedPath.NESTED_COUNT
        assert mock_navigation_directory.mock_exists.call_count == 1 + MockedPath.NESTED_COUNT
        assert mock_navigation_directory.mock_is_file.call_count == 1 + MockedPath.NESTED_COUNT
        assert stats.byte_count == MOCK_BYTES * MockedPath.NESTED_COUNT
        assert stats.character_count == MOCK_CHARACTERS * MockedPath.NESTED_COUNT
        assert stats.word_count == MOCK_WORDS * MockedPath.NESTED_COUNT
        assert stats.line_count == MOCK_LINES * MockedPath.NESTED_COUNT
