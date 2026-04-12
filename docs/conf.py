# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from sphinx_pyproject import SphinxConfig

config = SphinxConfig(
    "../pyproject.toml",
    globalns=globals(),
)
project = config.name
author = config.author
version = config.version

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False
napoleon_attr_annotations = True
napoleon_include_init_with_doc = False

mermaid_init_config = {'startOnLoad': 'true', 'securityLevel': 'loose'}
mermaid_params = ['-p', 'puppeteer-config.json']

# Key setting for dataclasses
autoapi_python_class_content = "both"     # ← Add this line

# Optional but helpful
autoapi_member_order = "bysource"         # Preserves field order from source

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# Moved to pyproject's [tool.sphinx-pyproject]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# Moved to pyproject's [tool.sphinx-pyproject]
