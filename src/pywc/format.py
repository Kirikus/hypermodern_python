"""Formatting collected file statistics."""

from collections.abc import Callable

from pywc.data import CounterFlags, FileStats

FormatterT = Callable[[FileStats, CounterFlags, str | None], str]


def format_automatic(counts: FileStats, flags: CounterFlags, name: str | None = None) -> str:
    """Format printer for stats, non-human readable format w/o dimensions (like Kb).

    Arguments:
        counts (FileStats): calculated file statistics with relevant counts.
        flags (CounterFlags): which file statistics should be printed.
        name (str | None): name of the file, appended to the beginning if present.

    Returns:
        str: Name, followed by line, word, character and byte counts, according to the flags and name fields.

    Raises:
        ValueError: if all flags are false, so nothing is added to the format string.
    """
    if not (flags.lines or flags.words or flags.chars or flags.bytes):
        raise ValueError(flags)
    components = []
    if name:
        components.append(f"{name:<20s}")
    if flags.lines:
        components.append(f"{counts.lines:7d}")
    if flags.words:
        components.append(f"{counts.words:7d}")
    if flags.chars:
        components.append(f"{counts.chars:7d}")
    if flags.bytes:
        components.append(f"{counts.bytes:7d}")

    if name:
        # name could start with a whitespace character, which must be preserved
        return " ".join(components).rstrip()
    return " ".join(components).strip()


def formatter_wrapper_print(formatter: FormatterT) -> FormatterT:
    def wrapped(stats: FileStats, flags: CounterFlags, name: str | None = None) -> str:
        ret = formatter(stats, flags, name)
        print(ret)  # noqa: T201
        return ret

    return wrapped
