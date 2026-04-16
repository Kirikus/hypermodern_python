"""Command-lines interface."""

from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING

import click

from pywc.data import CounterFlags, FileStats
from pywc.format import format_automatic, formatter_wrapper_print
from pywc.navigation import process_path

if TYPE_CHECKING:
    from collections.abc import Iterable


@click.command()
@click.version_option(version=version("pywc_hypermodern"))
@click.option("-c", "--bytes", "byte_count", is_flag=True, help="Count bytes")
@click.option("-m", "--characters", "chars", is_flag=True, help="Count characters")
@click.option("-w", "--words", "words", is_flag=True, help="Count words")
@click.option("-l", "--lines", "lines", is_flag=True, help="Count lines")
@click.option(
    "--ignore-extension",
    "ignored_extensions",
    multiple=True,
    type=str,
    help="List of file extensions to ignore",
)
@click.option(
    "--ignore-name",
    "ignored_names",
    multiple=True,
    type=str,
    help="List of file or directory names to ignore",
)
@click.option(
    "--ignore-regexp",
    "ignored_regexps",
    multiple=True,
    type=str,
    help="List of regexps to ignore",
)
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(exists=True),
)
def main(  # noqa: PLR0913
    paths: Iterable[Path],
    *,
    byte_count: bool,
    chars: bool,
    words: bool,
    lines: bool,
    ignored_extensions: Iterable[str],
    ignored_names: Iterable[str],
    ignored_regexps: Iterable[str],
) -> None:
    """Python version of wc command with limited functionality.

    Prints wc information of files and directories (recursively) specified in PATHS.
    """  # noqa: DOC101, DOC103
    # default mode when no flags are chosen
    if not (byte_count or lines or chars or words):
        chars = words = lines = True
    flags = CounterFlags(bytes=byte_count, lines=lines, chars=chars, words=words)

    formatter = formatter_wrapper_print(format_automatic)

    total = FileStats(lines=0, chars=0, words=0, bytes=0)
    # compute stats for all file(s) / dir(s) passed as input
    for file_or_directory in paths:
        try:
            # extensions are reformed to *.ext form
            ignored_extensions = (
                [f"{ext}" for ext in ignored_extensions if ext.startswith("*.")]
                + [f"*{ext}" for ext in ignored_extensions if ext.startswith(".")]
                + [f"*.{ext}" for ext in ignored_extensions if not ext.startswith("*.") and not ext.startswith(".")]
            )

            total += process_path(
                Path(file_or_directory),
                flags,
                ignored_regexps=[*ignored_names, *ignored_extensions, *ignored_regexps],
                formatter=formatter,
            )
        except PermissionError:
            print(f"{file_or_directory} - Permission denied")  # noqa: T201
    formatter(total, flags, "TOTAL:")


if __name__ == "__main__":  # pragma: no cover
    main()
