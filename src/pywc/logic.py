"""Counting data in files and printing it, without path manipulation."""

from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass
class Mask:
    """Decides which arguments to report."""

    line_count: bool = False
    word_count: bool = False
    character_count: bool = False
    byte_count: bool = False


@dataclass(kw_only=True)
class FileStats:
    """File contests counts."""

    line_count: int = 0
    word_count: int = 0
    character_count: int = 0
    byte_count: int = 0

    @classmethod
    def count_data(cls, file: Path) -> Self:
        """Generate stats for a single file."""
        chunk_size = 65536  # 64 KB
        line_count, word_count, character_count, byte_count = 0, 0, 0, 0
        buffer = ""
        end_whitespace = True

        with file.open("br") as f:
            # In case the file is too big to read into memory, only process a chunk at a time
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    # Process the remaining buffer
                    if buffer:
                        word_count += len(buffer.split())
                    break

                byte_count += len(chunk)
                text = chunk.decode("utf-8", errors="ignore")

                line_count += text.count("\n")

                buffer += text
                word_counts_in_buffer = buffer.split()
                if len(word_counts_in_buffer) > 1:
                    word_count += len(word_counts_in_buffer)
                    if end_whitespace or buffer[0].isspace():
                        word_count -= 1
                    buffer = word_counts_in_buffer[-1]
                else:
                    buffer = word_counts_in_buffer[0] if word_counts_in_buffer else ""

                end_whitespace = text[-1].isspace()
                character_count += len(text)

        return cls(
            line_count=line_count + 1,
            word_count=word_count,
            character_count=character_count,
            byte_count=byte_count,
        )

    def __add__(self, other: Self) -> Self:
        """Calculate total of 2 FileStats objects by adding respective fields."""
        return FileStats(
            line_count=self.line_count + other.line_count,
            word_count=self.word_count + other.word_count,
            character_count=self.character_count + other.character_count,
            byte_count=self.byte_count + other.byte_count,
        )


def pretty_print(
    data: FileStats,
    mask: Mask,
    name: str = "total",
) -> None:
    """Format printer for final stats."""
    if not (mask.line_count or mask.word_count or mask.character_count or mask.byte_count):
        raise ValueError(mask)
    print("  ", end="")  # noqa: T201
    if mask.line_count:
        print(f"{data.line_count}\t", end="")  # noqa: T201
    if mask.word_count:
        print(f"{data.word_count}\t", end="")  # noqa: T201
    if mask.character_count:
        print(f"{data.character_count}\t", end="")  # noqa: T201
    if mask.byte_count:
        print(f"{data.byte_count}\t", end="")  # noqa: T201
    print(f"{name}")  # noqa: T201
