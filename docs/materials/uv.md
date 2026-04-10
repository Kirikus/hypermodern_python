# uv: Modern Package/Project Manager

uv makes Python development significantly faster and more pleasant.

## What is a Package/Project Manager

A **package manager** is a tool that automates the process of installing, upgrading, configuring, and removing software packages (libraries and dependencies) for a programming language. In the Python ecosystem, it handles downloading packages from repositories like [PyPI](https://pypi.org/), resolving version conflicts between dependencies, and ensuring that the correct versions are installed.

A **project manager** goes further: it helps manage an entire Python project by handling:

- Project metadata (name, version, description, etc.)
- Dependency declarations
- Virtual environment creation and management
- Reproducible installs via lockfiles
- Running scripts or commands in the project's isolated environment

Modern project managers (like uv, Poetry, or Hatch) typically use a ``pyproject.toml`` file as the central configuration and generate a lockfile (e.g., ``uv.lock``) for exact, reproducible dependency versions.

## Why use uv over pip

[pip](https://pip.pypa.io/) is the traditional package installer that comes bundled with Python. While reliable and widely used, it has limitations in speed, dependency resolution, and workflow integration.

**uv** (developed by Astral) is an extremely fast Python package and project manager written in Rust. It aims to replace multiple tools at once: pip, pip-tools, venv/virtualenv, pyenv, and more.

Key advantages of uv over plain pip include:

- **Blazing speed**: uv is often 10–100× faster than pip for installations and dependency resolution thanks to its Rust implementation and smart caching.
- **All-in-one tool**: It manages Python interpreters, virtual environments, projects, and scripts without needing separate tools.
- **Better project workflow**: Uses ``pyproject.toml`` + lockfile for reproducible environments, automatic syncing, and clean dependency management.
- **Efficient caching**: Global cache reduces disk usage and avoids re-downloading the same packages repeatedly.
- **No pre-installed Python required**: uv can download and manage Python versions itself (see below).

For simple one-off scripts, ``pip`` is still fine. For anything resembling a real project or when speed and reproducibility matter, uv provides a much smoother and faster experience.

## How to set up a Python interpreter using uv

uv does **not** require a pre-installed Python interpreter at all. You can install and use uv first, then let it handle Python versions.

To get started with uv, follow the official installation instructions:

- [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

Once uv is installed, you can:

- List available Python versions: ``uv python list``
- Install a specific Python version (e.g., 3.12): ``uv python install 3.12``
- Set a default Python version for your projects

For a new project, uv will automatically detect or install the required Python version specified in ``pyproject.toml`` (via the ``requires-python`` field or a ``.python-version`` file).

See the official guide for more details:

- [Installing and managing Python versions with uv](https://docs.astral.sh/uv/guides/install-python/)

## How to use uv — Basic commands

uv works best with **projects**. Start a new project with:

```console
uv init myproject
cd myproject
```

This creates a ``pyproject.toml`` file and sets up the basic project structure.

### Adding and removing dependencies

- Add a package (production dependency):

```console
     uv add requests
```

- Add a development-only dependency (e.g., for testing):

```console
     uv add --dev pytest
```

- Remove a dependency:

```console
     uv remove requests
```

These commands update ``pyproject.toml`` and the ``uv.lock`` lockfile automatically.

### Syncing the environment

To install or update the project's dependencies into the virtual environment:

```console
   uv sync
```

``uv sync`` creates/updates the virtual environment and installs exactly the packages listed in the lockfile (exact mode by default, removing extraneous packages).

### Running commands or scripts

Use ``uv run`` to execute commands or scripts inside the project's managed virtual environment:

```console
   uv run python script.py          # Run a script
   uv run pytest                    # Run tests
   uv run ruff check .              # Run a linter
```

``uv run`` automatically ensures the environment is synced before running the command.

For more advanced usage, explore the full documentation:

- [uv CLI Reference](https://docs.astral.sh/uv/reference/cli/)
- [uv Concepts — Projects](https://docs.astral.sh/uv/concepts/projects/)
- [Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)

## Additional Resources

- [Official uv Documentation](https://docs.astral.sh/uv/)
- [uv Features Overview](https://docs.astral.sh/uv/getting-started/features/)
- [uv vs. traditional tools](https://docs.astral.sh/uv/getting-started/features/#comparison-with-other-tools)
