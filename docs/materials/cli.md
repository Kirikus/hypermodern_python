# click: Command Line Interfaces

Every tool starts with a single, well-chosen command

## What is a CLI

A **Command Line Interface (CLI)** is a program that accepts text commands from the terminal (or shell) and returns text output. Users invoke it with a command name followed by arguments and options, e.g.:

```console
wc -l pyproject.toml
```

CLIs are the foundation of tools, scripts, and utilities.

## Why a dedicated package for argument parsing

Parsing `sys.argv` manually is possible but quickly becomes messy. A dedicated library is strongly recommended because it gives you:

- **Brief, readable code** instead of pages of manual string handling.
- **Automatic `--help` generation** and consistent error messages.
- **Robust handling of edge cases** (quoted values, flags, multiple values, short/long options, etc.).
- **Type conversion and validation** (int, float, paths, enums…).
- **Declarative style** that clearly documents the interface.
- **Maintainability and testing** — the interface is defined once and behaves predictably across releases.

Popular libraries can create a CLI with a few lines of code instead of hundreds.

## Main concepts

- **Argument** — positional value (order matters). Usually required.
- **Option** — named value, introduced with `--option` or `-o`. Usually optional and has a default.
- **Flag** — boolean option (on/off).
- **Command** — the executable function (or sub-command).
- **Group / Subcommand** — organizes related commands (e.g. `git commit`, `git push`).

Full details are in each library’s manual (linked below).

## Comparison: argparse vs click vs typer

Python offers three widely used solutions. All three can create the **exact same CLI** shown below (one positional argument + one option) with the same usage:

```console
python greet.py --help
python greet.py Alice --greeting Hi
```

### [argparse](https://docs.python.org/3/library/argparse.html)

Built-in, zero dependencies, very explicit and powerful. Most control and slight performance improvement (which is important only for very short-lived CLIs).

```python
import argparse

parser = argparse.ArgumentParser(description="Greet someone")
parser.add_argument("name", help="Name to greet")
parser.add_argument("--greeting", default="Hello", help="Greeting prefix")
args = parser.parse_args()

print(f"{args.greeting} {args.name}!")
```

### [click](https://click.palletsprojects.com/)

Decorator-based, excellent for complex CLIs with more-or-less standard behaviours. Supports features like colors and shell completion. CLI declaration is better separated from its logic compared to argparse.

```python
import click

@click.command()
@click.argument("name")
@click.option("--greeting", default="Hello", help="Greeting prefix")
def greet(name: str, greeting: str):
   print(f"{greeting} {name}!")

if __name__ == "__main__":
   greet()
```

### [typer](https://typer.tiangolo.com/)

Built on Click. Uses Python type hints for the shortest possible code while retaining full power. Since type annotations should be present anyway, often is the best out-of-the-box solution, works like magic.

```python
import typer

app = typer.Typer()

@app.command()
def greet(
   name: str,
   greeting: str = typer.Option("Hello", help="Greeting prefix"),
):
   print(f"{greeting} {name}!")

if __name__ == "__main__":
   app()
```

## Testing command line interfaces

Testing CLIs requires special care because execution happens through the shell rather than direct function calls.

### argparse

Since there is no built-in method of testing, you will be making one. Below is, to my knowledge, the best solution (courtesy of [Jürgen Gmach](https://jugmac00.github.io/blog/testing-argparse-applications-the-better-way/)).

Define CLI dunction as `def main(argv=None)` and pass that argument to `ArgumentParser.parse_args(argv)`; call `main` without arguments by default. In tests, pass necessary arguments as a list; this will supersede reading from `sys.argv`.

```python
def main(argv=None):
    parser = argparse.ArgumentParser(description="Greet someone")
    parser.add_argument("name", help="Name to greet")
    parser.add_argument("--greeting", default="Hello", help="Greeting prefix")
    args = parser.parse_args(argv)
    print(f"{args.greeting} {args.name}!")

if __name__ == '__main__':
    sys.exit(main())
```

Then, use [built-in fixtures](https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html) to capture stdout.

```python
def test_greeting(capsys):
    main(["--name", "Jürgen"])
    captured = capsys.readouterr()
    assert captured.out == "Hello Jürgen\n"
```

### click and typer

These packages provide a special class `CLIRunner` for testing purposes, use it.

```python
from click.testing import CliRunner
# or from typer.testing import CliRunner

def test_greeting():
    runner = CliRunner()
    result = runner.invoke(app, ["Alice", "--greeting", "Hi"])
    assert result.exit_code == 0
    assert "Hi Alice!" in result.output
```

For more information, consult relevant sections in the official manuals of [click](https://click.palletsprojects.com/en/stable/testing/) and [typer](https://typer.tiangolo.com/tutorial/testing/) packages.
