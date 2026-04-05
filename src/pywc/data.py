"""Counting data in files without path manipulation."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Self


@dataclass(slots=True, kw_only=True)
class CounterFlags:
    """Using to decide which arguments to report and current reading status.

    Attributes:
        lines (bool): If true, lines statistics are among the statistics used.
        words (bool): If true, words statistics are among the statistics used.
        chars (bool): If true, characters statistics are among the statistics used.
        bytes (bool): If true, bytes statistics are among the statistics used.

    Args:
        lines (bool): If true, lines statistics are among the statistics used.
        words (bool): If true, words statistics are among the statistics used.
        chars (bool): If true, characters statistics are among the statistics used.
        bytes (bool): If true, bytes statistics are among the statistics used.
    """

    lines: bool = True
    words: bool = True
    chars: bool = True
    bytes: bool = True


@dataclass(kw_only=True, slots=True, eq=True)
class FileStats:
    """Statistics for file contests.

    Attributes:
        lines (int): Number of lines in the file.
        words (int): Number of words in the file.
        chars (int): Number of characters in the file.
        bytes (int): Number of bytes in the file.

    Raises:
        ValueError: Some of the arguments are negative or are in descending order.
    """

    lines: int = 0
    words: int = 0
    chars: int = 0
    bytes: int = 0

    def __post_init__(self) -> None: # noqa: D105
        if self.lines < 0 or self.words < 0 or self.chars < 0 or self.bytes < 0:
            msg = "File statistics must be non-negative."
            raise ValueError(msg)
        if not (self.lines <= self.words <= self.chars <= self.bytes):
            msg = "File statistics must be non-descending order."
            raise ValueError(msg)

    def __add__(self, other: Self) -> Self:
        """Calculate total of 2 FileStats objects by adding respective fields.

        Args:
            other (Self): FileStats instance to add.

        Returns:
            Self: new FileStats instance.
        """
        return FileStats(
            lines=self.lines + other.lines,
            words=self.words + other.words,
            chars=self.chars + other.chars,
            bytes=self.bytes + other.bytes,
        )

    @classmethod
    def from_file(cls, file: Path) -> Self:
        """Generate stats for a single file.

        Args:
            file(Path): Path to the file.

        Returns:
            Self: new FileStats instance.
        """
        chunk_size = 2**16  # 64 KB
        lines, words, chars, bytes_read = 0, 0, 0, 0
        in_word = False

        with file.open("br") as f:
            # In case the file is too big to read into memory, only process a chunk at a time
            while chunk := f.read(chunk_size):
                if not chunk:
                    break
                text = chunk.decode("utf-8", errors="ignore")

                bytes_read += len(chunk)
                chars += len(text)

                for b in chunk:
                    if b == ord("\n"):
                        lines += 1
                    if chr(b).isspace():
                        if in_word:
                            words += 1
                            in_word = False
                    else:
                        in_word = True

        # Count last word
        if in_word:
            words += 1

        return cls(
            lines=lines,
            words=words,
            chars=chars,
            bytes=bytes_read,
        )
