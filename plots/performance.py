"""Plot time required to wc a directory with N files with total size S."""

import tempfile
from pathlib import Path
from timeit import timeit

import numpy as np
from matplotlib import pyplot as plt

from pywc.logic import Mask
from pywc.navigation import process_file_or_dir

sizes = np.logspace(10, 20, base=2, num=11, dtype=int)
files = np.logspace(0, 10, base=2, num=11, dtype=int)
times = np.empty_like(sizes)
for f in files:
    times = []
    for s in sizes:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            for i in range(f):
                file = path / f"{i}.file"
                position = s // f
                with file.open("w") as io:
                    io.seek(position - 1)
                    io.write(" ")
            time = timeit(
                """process_file_or_dir(
                    path, mask=Mask(byte_count=True, character_count=True, word_count=True, line_count=True),
                ),""",
                globals={"process_file_or_dir": process_file_or_dir, "Mask": Mask, "path": path},
                number=10,
            )
            times.append(time)

    # the histogram of the data
    plt.plot(sizes, times, label=f"{f} files")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Total size, bytes")
plt.ylabel("Time, s")
plt.title("Performance of `pywc` on directory with files of similar size")
plt.grid(visible=True)
plt.legend()
plt.show()
