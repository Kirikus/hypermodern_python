# sphinx: writing documentation

The best time to write documentation was yesterday. The second best time is now.

## Advantages of writing documentation

Writing documentation helps users understand your code, reduces support requests, and improves code quality by forcing clearer design decisions.

Even in solo projects it pays off: it serves as a reference for your future self, speeds up onboarding if the project grows, and makes refactoring safer because intent is recorded. Even small projects can receive sudden continuation several years later.

Furthermore, documentation can be used by programs such as IDEs, linters and similar tools, or even AI-agents. Once docstrings are written, creating documentation is trivial.

## Main principles of good documentation

Keep it **clear**, **concise**, and **up-to-date**. Structure it logically, use consistent style, and focus on what the reader needs to know rather than implementation details.

See the [Diátaxis framework](https://diataxis.fr/) for a practical way to organise different types of documentation.

## Packages for writing documentation in Python

The two most common tools are:

- [Sphinx](https://www.sphinx-doc.org/) — the standard for Python projects (supports reStructuredText and MyST Markdown, excellent autodoc integration).
- [MkDocs](https://www.mkdocs.org/) — lightweight, Markdown-first, great for simpler sites.

Sphinx is usually preferred when you need API docs from docstrings; MkDocs shines for quick, theme-rich project websites.

Remaining of this page is dedicated to the specifics of using sphinx.

## Configuration

Sphinx traditionally uses a `conf.py` file in the documentation root for all settings (project name, extensions, theme, etc.). This, however, creates a duplication of setting files, since other packages store settings in `pyproject.toml`.

With the [sphinx-pyproject](https://sphinx-pyproject.readthedocs.io/en/latest/) package you can move most configuration (including project metadata) into `pyproject.toml`:

- It reads the standard `[project]` table (name, version, description, etc.).
- Sphinx-specific settings go under `[tool.sphinx-pyproject]`.

You can either:

- Keep a minimal `conf.py` that only contains Python code loading data from `pyproject.toml`.
- Keep most settings in `conf.py` and access `pyproject.toml` only to load data from `[project]` section (this avoids duplication).

## Markup formats: Markdown, reStructuredText and MyST

- **Markdown (.md)** — simple, human-readable, used by MkDocs. Limited for complex cross-references and custom Sphinx roles.
- **reStructuredText (.rst)** — Sphinx’s native format. Very powerful for directives, roles, and autodoc.
- **MyST Markdown** — Markdown + Sphinx features (via myst-parser). Gives you the best of both worlds inside Sphinx.

**When to choose each**:

- Use plain Markdown + MkDocs for small or quick-start projects. There is a reason use see `README.md` everywhere!
- Use reStructuredText for maximum control in large Sphinx sites. Or, actually, don't because...
- Use MyST when you like Markdown syntax but still want full Sphinx power.

Here is the same simple document written in each format (tabs are synchronised via the `sphinx-design` extension; selecting a tab in one place will keep others in sync if you reuse the same `sync` keys elsewhere):

``````{tab-set}
---
sync-group: markup-example
---
`````{tab-item} rst
**reStructuredText**

```rst
Example function
================

This function does something useful.

* Point one
* Point two

.. code-block:: python

   def my_function():
       """Does something useful."""
       pass
```

`````

`````{tab-item} md
**Markdown (MkDocs)**

````markdown
# Example function

This function does something useful.

* Point one
* Point two

```python
def my_function():
    """Does something useful."""
    pass
```
````

`````

`````{tab-item} MyST
**MyST Markdown (Sphinx)**

````markdown
# Example function

This function does something useful.

* Point one
* Point two

```{code-block} python
def my_function():
    """Does something useful."""
    pass
```
````

`````

`````{tab-item} View result

# Example function

This function does something useful.

- Point one
- Point two

```python
def my_function():
    """Does something useful."""
    pass
```

`````

``````

## Directives

Directives are reStructuredText (and MyST) blocks that add special behaviour such as notes, code blocks, images, or tables of contents.

Format of using directives may wary, as well as the specifics of customizing them. Consult manuals or examples when using them. Here are the most common examples of directive formats:

``````{tab-set}
---
sync-group: markup-example
---
`````{tab-item} rst

```rst
.. directive-name:: optional argument
   :option: value

   Content goes here.
```

`````

`````{tab-item} MyST (backtick fence)

````markdown
```{directive-name} optional argument
:option: value

Content goes here.
```
````

`````

`````{tab-item} MyST (colon fence)

```markdown
:::{directive-name} optional argument
:option: value

Content goes here.
:::
```

`````

`````{tab-item} MyST (tilde fence)

```markdown
~~~{directive-name} optional argument
:option: value

Content goes here.
~~~
```

`````
``````

Common examples of directives are: `note`, `warning`, `code-block`, `image`, `toctree`, `todo`.

More features include nested directives, different format of arguments, one-line usage, etc.

Full reference: [Sphinx directives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html) and [MyST directives](https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html).

## toctree

[toctree](https://www.sphinx-doc.org/en/master/usage/quickstart.html#defining-document-structure) is, basically, the most important directive. It will be automatically added to the `index.rst` file during its automatic creation.

This directive builds the navigation tree and table of contents and allows navigation between pages.

Basic usage example:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   installation
   usage
```

This creates links between current page and `intro`, `installation` and `usage` (these pages become children of current page). Note that for other pages copying this information is not necessary, as the whole table of contents tree will be constructed using directive from all pages.

## Automatic documentation from docstrings

Sphinx can automatically generate API reference pages by extracting docstrings from your Python modules, classes, functions, and methods.

This keeps documentation close to the code, keeps them in sync, and reduces duplication.

### Relevant directives and roles

The most commonly used autodoc directives are:

- `automodule` — documents an entire module
- `autoclass` — documents a class (including methods and attributes)
- `autofunction` — documents a single function or method
- `automethod` — documents a method inside a class
- `autoattribute` — documents a class or module attribute

You can control what is included with options like `:members:`, `:undoc-members:`, `:private-members:`, `:special-members:`, and `:inherited-members:`.

Example in reStructuredText/MyST:

```rst
.. autoclass:: mypackage.MyClass
   :members:
   :undoc-members:
```

Full list and options: [Sphinx autodoc extension](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)

### Recommended tool: sphinx-autoapi

For modern projects, [sphinx-autoapi](https://sphinx-autoapi.readthedocs.io/) is often the best choice. It parses your source code directly and generates clean, consistent API documentation.

Advantages:

- Works without executing your code
- Handles complex projects and circular imports better
- Produces more predictable output

Add it to your Sphinx extensions and configure the directories to scan.

### Other options

- [sphinx.ext.autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) (built-in) — classic approach. Requires your package to be importable. Simple but can fail with import errors or complex dependencies.
- [sphinx.ext.autosummary](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html) — generates summary tables and stub pages that can then use autodoc. Good when you want fine control over page layout.
- [sphinx-apidoc](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html) (command-line tool) — generates .rst stub files from your package. Useful for one-time generation but requires manual maintenance.
- [pdoc](https://pdoc.dev/docs/pdoc.html) or [mkdocstrings](https://mkdocstrings.github.io/) — alternatives if you prefer MkDocs instead of Sphinx.

| Tool           | Import required  | Handles complex projects | Output style        | Best for                   |
| -------------- | ---------------- | ------------------------ | ------------------- | -------------------------- |
| sphinx-autoapi | No               | Excellent                | Clean & modern      | Most new Sphinx projects   |
| autodoc        | Yes              | Good                     | Flexible            | Simple packages            |
| autosummary    | Yes              | Good                     | Highly customisable | Projects needing summaries |
| sphinx-apidoc  | No (scans files) | Moderate                 | Basic stubs         | Quick initial setup        |

Start with **sphinx-autoapi** unless you have a specific reason to use the built-in autodoc.
