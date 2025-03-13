from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileStats:
    lines: int = 0
    words: int = 0
    characters: int = 0
    bytes: int = 0

    def __add__(self, other):
        return FileStats(
            lines=self.lines + other.lines,
            words=self.words + other.words,
            characters=self.characters + other.characters,
            bytes=self.bytes + other.bytes,
        )


def is_ignored(file_path: str, ext_or_dir_to_ignore: [str]) -> bool:
    """Check if the file matches any of the ignored extensions or directories"""
    return any(file_path.endswith(ext) for ext in ext_or_dir_to_ignore) or any(
        f"\\{dir}\\" in file_path for dir in ext_or_dir_to_ignore
    )


def count_data(
    file: Path,
) -> FileStats:
    """Generate stats for a single file"""
    chunk_size = 65536  # 64 KB
    lines, words, characters, bytes_count = 0, 0, 0, 0
    buffer = ""

    with file.open("br") as f:
        # In case the file is too big to read into memory, only process a chunk at a time
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                # Process the remaining buffer
                if buffer:
                    words += len(buffer.split())
                break

            bytes_count += len(chunk)
            text = chunk.decode("utf-8", errors="ignore")

            lines += text.count("\n")

            buffer += text
            words_in_buffer = buffer.split()
            if len(words_in_buffer) > 1:
                words += len(words_in_buffer) - 1
                buffer = words_in_buffer[-1]
            else:
                buffer = words_in_buffer[0] if words_in_buffer else ""

            characters += len(text)

    return FileStats(lines=lines, words=words, characters=characters, bytes=bytes_count)


def pretty_print(
    data: FileStats,
    args_bytes: bool,
    args_characters: bool,
    args_words: bool,
    args_lines: bool,
    name: str = "total",
) -> None:
    """Format printer for final stats."""
    print("  ", end="")
    if args_lines:
        print(f"{data.lines}\t", end="")
    if args_words:
        print(f"{data.words}\t", end="")
    if args_characters:
        print(f"{data.characters}\t", end="")
    if args_bytes:
        print(f"{data.bytes}\t", end="")
    print(f"{name}")
