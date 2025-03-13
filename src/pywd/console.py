"""Command-line interface."""

import os
from pathlib import Path

import click
import numpy as np

from pywd.wd import count_data, is_ignored, pretty_print

from . import __version__


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
    type=click.Path(exists=True),
)
def main(
    args_input_files_or_dirs: Path,
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
    # Count how many optional flags were passed out of -c, -l, -w, and -m (ignore -i)
    optional_flags = sum([args_bytes, args_lines, args_words, args_characters])

    ### Process each input file
    # if no optional flags are passed, we compute line count, word count, and byte count, by default
    init_arr_size = 3 if optional_flags == 0 else optional_flags

    # initialize array to keep track of totals
    total = np.zeros(init_arr_size)

    # compute stats for all file(s) / dir(s) passed as input
    for file_or_directory in args_input_files_or_dirs:
        # if input is a file, process directly
        if os.path.isfile(file_or_directory):
            if not is_ignored(
                file_path=file_or_directory, ext_or_dir_to_ignore=args_ignore_extensions
            ):
                try:
                    # read file in binary mode
                    with open(file_or_directory, "rb") as file:
                        total += np.array(
                            count_data(
                                file=file,
                                file_name=file_or_directory,
                                args_bytes=args_bytes,
                                args_characters=args_characters,
                                args_words=args_words,
                                args_lines=args_lines,
                                optional_flags=optional_flags,
                            )
                        )
                # skip files we don't have permission to read
                except PermissionError:
                    continue
        # o.w., if input is a directory, process every file within that dir
        elif os.path.isdir(file_or_directory):
            for root, _, files in os.walk(file_or_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not is_ignored(
                        file_path=file_path, ext_or_dir_to_ignore=args_ignore_extensions
                    ):
                        try:
                            # read file in binary mode
                            with open(file_path, "rb") as file:
                                total += np.array(
                                    count_data(
                                        file=file,
                                        file_name=file_path,
                                        args_bytes=args_bytes,
                                        args_characters=args_characters,
                                        args_words=args_words,
                                        args_lines=args_lines,
                                        optional_flags=optional_flags,
                                    )
                                )
                        # skip files we don't have permission to read
                        except PermissionError:
                            continue
        else:
            raise ValueError(f'"{file_or_directory}" is not a valid file / dir type.')

    pretty_print(
        args_bytes=args_bytes,
        args_characters=args_characters,
        args_words=args_words,
        args_lines=args_lines,
        arr=total,
        optional_flags=optional_flags,
    )


if __name__ == "__main__":
    main()
