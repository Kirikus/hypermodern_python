#!/usr/bin/env python3
"""Simple Scour SVG optimizer.

Usage:
    uv run python scour-cli.py file1.svg [file2.svg ...]

Behavior:
    - Overwrites each input file with its optimized version (in-place)
    - By default: removes comments, metadata, unused IDs, empty elements, etc.
    - Pretty-formatted output (human-readable, 2-space indent)
"""

import sys
from pathlib import Path

import click

try:
    from scour.scour import parse_args, start
except ImportError:
    click.echo("Error: 'scour' is not installed.", err=True)
    click.echo("Run: uv pip install scour", err=True)
    sys.exit(1)


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True, dir_okay=False))
def cli(files: list[Path]) -> None:
    """Simple Scour SVG optimizer wrapper for inplace formatting."""
    if not files:
        click.echo("Usage: scour-cli.py <svg_file1> [svg_file2 ...]")
        click.echo("       Each file will be overwritten with an optimized version.")
        sys.exit(1)

    # Default scour options - clean + pretty output
    default_args = [
        "--enable-comment-stripping",
        "--enable-id-stripping",
        "--shorten-ids",
        "--remove-metadata",
        "--remove-descriptive-elements",
        "--enable-viewboxing",
        "--strip-xml-prolog",
        "--nindent=2",
        "--quiet",
    ]

    options = parse_args(default_args)

    for file_path in files:
        p = Path(file_path)
        p_tmp = p.parent / (p.stem + "_tmp" + p.suffix)

        with p.open("r") as input_file, p_tmp.open("wb") as output_file:
            start(options, input_file, output_file)
        p_tmp.replace(p)


if __name__ == "__main__":
    cli()
