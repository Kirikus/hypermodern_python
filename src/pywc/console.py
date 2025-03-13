"""Command-line interface."""

import os
from pathlib import Path

import click

from pywc.wc import FileStats, count_data, is_ignored, pretty_print

from . import __version__


def process_file(
    file: Path,
    args_bytes: bool,
    args_characters: bool,
    args_words: bool,
    args_lines: bool,
    ext_or_dir_to_ignore: [str],
) -> FileStats:
    if is_ignored(file, ext_or_dir_to_ignore):
        return FileStats
    assert file.is_file()
    res = count_data(file)
    pretty_print(
        data=res,
        args_bytes=args_bytes,
        args_characters=args_characters,
        args_words=args_words,
        args_lines=args_lines,
        name=str(file),
    )
    return res


def process_file_or_dir(
    file: Path,
    args_bytes: bool,
    args_characters: bool,
    args_words: bool,
    args_lines: bool,
    ext_or_dir_to_ignore: [str],
) -> FileStats:
    if file.is_file():
        return process_file(file, args_bytes, args_characters, args_words, args_lines, ext_or_dir_to_ignore)
    total = FileStats()
    for f in file.iterdir():
        total += process_file_or_dir(f, args_bytes, args_characters, args_words, args_lines, ext_or_dir_to_ignore)
    return total


@click.command()
@click.version_option(version=__version__)
@click.option("-c", "--args_bytes", is_flag=True, help="Count bytes")
@click.option("-m", "--args_characters", is_flag=True, help="Count characters")
@click.option("-w", "--args_words", is_flag=True, help="Count words")
@click.option("-l", "--args_lines", is_flag=True, help="Count lines")
@click.option(
    "-i",
    "--args_ignore-extensions",
    multiple=True,
    type=str,
    help="List of file extensions to ignore",
)
@click.argument(
    "args_input_files_or_dirs",
    nargs=-1,
    type=click.Path(exists=True),
)
def main(
    args_input_files_or_dirs: [Path],
    args_bytes: bool,
    args_characters: bool,
    args_words: bool,
    args_lines: bool,
    args_ignore_extensions: [str],
):
    """
    Python version of wd command with limited functionality

    ARGS_INPUT_FILES_OR_DIRS - Path to the input file(s) and/or dir(s)
    """
    # default mode when no flags are chosen
    if not (args_bytes or args_lines or args_characters or args_words):
        args_characters = args_words = args_lines = True

    total = FileStats()
    # compute stats for all file(s) / dir(s) passed as input
    for file_or_directory in args_input_files_or_dirs:
        total += process_file_or_dir(
            Path(file_or_directory),
            args_bytes=args_bytes,
            args_characters=args_characters,
            args_words=args_words,
            args_lines=args_lines,
            ext_or_dir_to_ignore=args_ignore_extensions,
        )
    pretty_print(
        data=total,
        args_bytes=args_bytes,
        args_characters=args_characters,
        args_words=args_words,
        args_lines=args_lines,
        name="total",
    )


if __name__ == "__main__":
    main()
