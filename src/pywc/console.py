"""Command-line_count interface."""

from pathlib import Path

import click

from pywc.logic import FileStats, Mask, pretty_print
from pywc.navigation import process_file_or_dir

from . import __version__


@click.command()
@click.version_option(version=__version__)
@click.option("-c", "--bytes", "byte_count", is_flag=True, help="Count bytes")
@click.option("-m", "--characters", "character_count", is_flag=True, help="Count characters")
@click.option("-w", "--words", "word_count", is_flag=True, help="Count words")
@click.option("-l", "--lines", "line_count", is_flag=True, help="Count lines")
@click.option(
    "-i",
    "--ignore-extension",
    "ignored_extensions",
    multiple=True,
    type=str,
    help="List of file extensions to ignore",
)
@click.option(
    "-I",
    "--ignore-name",
    "ignored_names",
    multiple=True,
    type=str,
    help="List of file extensions to ignore",
)
@click.argument(
    "input_files_or_dirs",
    nargs=-1,
    type=click.Path(exists=True),
)
def main(  # noqa: PLR0913
    input_files_or_dirs: [Path],
    *,
    byte_count: bool,
    character_count: bool,
    word_count: bool,
    line_count: bool,
    ignored_extensions: [str],
    ignored_names: [str],
) -> None:
    """
    Python version of wd command with limited functionality.

    ARGS_INPUT_FILES_OR_DIRS - Path to the input file(s) and/or dir(s)
    """
    # default mode when no flags are chosen
    if not (byte_count or line_count or character_count or word_count):
        character_count = word_count = line_count = True
    mask = Mask(byte_count=byte_count, line_count=line_count, character_count=character_count, word_count=word_count)

    total = FileStats()
    # compute stats for all file(s) / dir(s) passed as input
    for file_or_directory in input_files_or_dirs:
        total += process_file_or_dir(
            Path(file_or_directory),
            mask=mask,
            ignored_extensions=ignored_extensions,
            ignored_names=ignored_names,
        )
    pretty_print(
        data=total,
        mask=mask,
        name="total",
    )


if __name__ == "__main__":  # pragma: no cover
    main()
