"""Navigate different files and folders."""

from pathlib import Path

from pywc.logic import FileStats, Mask, pretty_print


def is_ignored(
    file: Path,
    *,
    ignored_extensions: list[str] | None = None,
    ignored_names: list[str] | None = None,
) -> bool:
    """Check if the file matches any of the ignored extensions or directories."""
    ignored_extensions = ignored_extensions or []
    ignored_names = ignored_names or []
    return any(v in file.suffixes for v in ignored_extensions) or any(file.name == v for v in ignored_names)


def process_file(
    file: Path,
    mask: Mask,
    ignored_extensions: [str] = None,
    ignored_names: [str] = None,
) -> FileStats:
    """Calculate stats for a file."""
    if is_ignored(file, ignored_extensions=ignored_extensions, ignored_names=ignored_names):
        return FileStats()
    res = FileStats.count_data(file)
    pretty_print(
        data=res,
        mask=mask,
        name=str(file),
    )
    return res


def process_file_or_dir(
    file: Path,
    mask: Mask,
    ignored_extensions: [str] = None,
    ignored_names: [str] = None,
) -> FileStats:
    """Calculate stats for a file or recursively go into a directory."""
    if not file.exists():
        return FileStats()
    if file.is_file():
        return process_file(
            file,
            mask=mask,
            ignored_extensions=ignored_extensions,
            ignored_names=ignored_names,
        )
    if is_ignored(file, ignored_extensions=ignored_extensions, ignored_names=ignored_names):
        return FileStats()
    total = FileStats()
    for f in file.iterdir():
        total += process_file_or_dir(
            f,
            mask=mask,
            ignored_extensions=ignored_extensions,
            ignored_names=ignored_names,
        )
    return total
