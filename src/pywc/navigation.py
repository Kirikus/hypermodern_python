"""Navigate different files and folders."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path

    from pywc.format import FormatterT

from pywc.data import CounterFlags, FileStats


def process_path(
    path: Path,
    flags: CounterFlags,
    *,
    ignored_regexps: Iterable[str] = (),
    formatter: FormatterT | None = None,
) -> FileStats:
    """Recursively process a file or directory and return aggregated FileStats.

    Side effects (printing) are optional and controlled by `formatter`.

    Args:
        path (Path): Path of file or directory to process.
        flags (CounterFlags | None): Optional counter of file flags to use.
        ignored_regexps (Iterable[str]): Regexes to ignore.
        formatter (FormatterT | None): Optional formatter, used to print file contents on IO device.

    Returns:
        FileStats: FileStats instance containing file or aggregated directory statistics.
    """

    def _walk(p: Path) -> FileStats:
        total = FileStats(lines=0, words=0, chars=0, bytes=0)

        if not path.exists():
            return total  # zero value

        if any(path.match(r) for r in ignored_regexps):
            return total  # zero value

        if p.is_file():
            stats = FileStats.from_file(p)

            if formatter:
                formatter(stats, flags, str(p))

            return stats

        if not p.is_dir():  # symlink, broken, etc.
            return total  # zero value

        # Recursive call for directories
        for child in p.iterdir():
            total += _walk(child)

        return total

    return _walk(path)
