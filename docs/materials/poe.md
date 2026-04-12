# poethepoet: defining scripts and tasks

“A short story must have a single mood and every sentence must build towards it.”

## Basic scripts definition in `[project.scripts]`

The `[project.scripts]` section in `pyproject.toml` allows definition of command-line entry points. These become executable commands once the project is installed.

- It turns Python functions into CLI tools that anyone can run after installing your package.
- Maps script to a single python function.
- Follows the standard [PEP 621](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/) for project metadata.

Usage:

```toml
[project.scripts]
hello = "my_package.cli:hello"
run-server = "my_package.server:main"
```

- The key (`hello`) is the command name users will type.
- The value is a string in the form `"module:function"`.

GUI entry points can also be defined with `[project.gui-scripts]`, though this is less common.

For simple one-off scripts without packaging, `uv run my_script.py` can be used directly — no need for `[project.scripts]`.

## Limitations

`[project.scripts]` is limited to defining **installable CLI entry points** — simple mappings from a command name to a Python function. It requires your project to be installed and is best for end-user tools, not internal development workflows. It struggles with:

- Complex commands with arguments, help text, and environment variables.
- Running sequences of tasks (e.g., lint → test → build).
- Running tasks in parallel.
- Conditional logic, custom Python functions, or shell scripts.
- Isolated or multi-Python-version execution.

[Poe the Poet](https://poethepoet.natn.io/index.html) is used for **development and automation tasks**. It is a lightweight task runner designed for Python projects using `uv`. It defines reusable development, build, test, and automation tasks directly in `pyproject.toml` under the `[tool.poe.tasks]` section.

```bash
uv run poe --help
uv run poe <task-name>
```

In a pure `uv` workflow, `uv run` handles basic script execution well, but `poe` provides a centralized, declarative way to manage the full set of repetitive commands developers use every day — without scattering them in Makefiles, shell scripts, or CI files. This complements `uv`: `uv` manages the environment and dependencies, while `poe` orchestrates the tasks inside that environment.

```{note}
Tools like `nox` or `tox` can achieve similar multi-environment testing, but `poe` is lighter, lives entirely in `pyproject.toml`, and integrates more naturally with daily `uv` workflows.
```

## Different types of tasks

Poe supports two main categories: **execution tasks** (run something directly) and **orchestration tasks** (combine other tasks).

### Execution tasks

These run content in a subprocess.

- **cmd** (default for simple strings): A command executed without a shell.\
  Example:

  ```toml
  [tool.poe.tasks]
  lint = "ruff check ."
  ```

- **script**: Calls a Python function (with optional arguments).\
  Example:

  ```toml
  [tool.poe.tasks]
  migrate.script = "my_app.db:migrate"
  ```

- **shell**: Runs a shell script (uses `bash` or similar on POSIX).\
  Useful for complex pipelines or environment-dependent commands.

- **expr**: Evaluates a Python expression and prints the result.

### Orchestration tasks

These control the flow of other tasks.

- **sequence**: Runs tasks one after another (in order).\
  Example:

  ```toml
  [tool.poe.tasks]
  check = ["lint", "test"]
  ```

- **parallel**: Runs tasks simultaneously.

You can also create **ref** tasks (references to other tasks) and combine everything with options like `help`, `args`, `env`, `executor` (for `uv`-specific behavior), and more.
