from pathlib import Path

import numpy as np


def is_ignored(file_path: str, ext_or_dir_to_ignore: [str]) -> bool:
    """Check if the file matches any of the ignored extensions or directories"""
    return any(file_path.endswith(ext) for ext in ext_or_dir_to_ignore) or any(
        f"\\{dir}\\" in file_path for dir in ext_or_dir_to_ignore
    )


def count_data(
    file: Path,
    file_name: str,
    optional_flags: int,
    args_bytes: bool,
    args_characters: bool,
    args_words: bool,
    args_lines: bool,
) -> [int]:
    """Generate stats for a single file"""
    res = ()  # init empty tuple for result
    chunk_size = 65536  # 64 KB
    lines, words, characters, bytes_count = 0, 0, 0, 0
    buffer = ""

    print("  ", end="")

    # In case the file is too big to read into memory, only process a chunk at a time
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            # Process the remaining buffer
            if buffer:
                words += len(buffer.split())
            break

        bytes_count += len(chunk)
        text = chunk.decode("utf-8", errors="ignore")

        if args_lines or optional_flags == 0:
            lines += text.count("\n")

        if args_words or optional_flags == 0:
            buffer += text
            words_in_buffer = buffer.split()
            if len(words_in_buffer) > 1:
                words += len(words_in_buffer) - 1
                buffer = words_in_buffer[-1]
            else:
                buffer = words_in_buffer[0] if words_in_buffer else ""

        if args_characters:
            characters += len(text)

    if args_lines:
        print(f"{lines}\t", end="")
        res += (lines,)

    if args_words:
        print(f"{words}\t", end="")
        res += (words,)

    if args_characters:
        print(f"{characters}\t", end="")
        res += (characters,)

    if args_bytes:
        print(f"{bytes_count}\t", end="")
        res += (bytes_count,)

    # if no optional args are specified, print line count, word count, and bytes
    if optional_flags == 0:
        print(f"{lines}\t{words}\t{bytes_count}\t{file_name}")
        return lines, words, bytes_count

    # o.w., return the tuple containing the stats we computed
    else:
        print(file_name)
        return res


def pretty_print(
    arr: np.ndarray,
    optional_flags: int,
    args_bytes: bool,
    args_characters: bool,
    args_words: bool,
    args_lines: bool,
) -> None:
    """Format printer for final stats."""

    print("  ", end="")
    for elem in arr:
        print(f"{int(elem)}\t", end="")
    print("total")

    print("  ", end="")

    if optional_flags == 0:
        print("lines\twords\tbytes")

    if args_lines:
        print("lines\t", end="")

    if args_words:
        print("words\t", end="")

    if args_characters:
        print("chars\t", end="")

    if args_bytes:
        print("bytes\t", end="")
