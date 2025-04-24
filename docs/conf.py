"""Sphinx configuration."""

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.append(str((Path("..") / "src").resolve()))

project = "PyWC"
author = "Dmitry Derbyshev"
copyright = f"{datetime.now(tz=timezone.utc).year}, {author}"  # noqa: A001
extensions = [
    "matplotlib.sphinxext.plot_directive",
    "myst_parser",
    "autodoc2",
    "sphinx.ext.napoleon",
    "sphinx_click",
]
html_static_path = ["_static"]
html_theme = "furo"
myst_enable_extensions = [
    "colon_fence",
]
autodoc2_packages = [
    {
        "path": "../src/pywc",
        "auto_mode": False,
    },
]
autodoc2_render_plugin = "myst"
