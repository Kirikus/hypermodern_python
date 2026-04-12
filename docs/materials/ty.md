# ty: Type Checking

## Typing in python

Python is natively a **dynamically typed** language. This signifies that types are associated with objects at runtime rather than with variable names during a compilation phase. While this provides immense flexibility and rapid prototyping speed, it can lead to "type errors" that only surface when the code is executed.

To mitigate these risks, [PEP 484](https://peps.python.org/pep-0484/) introduced **type hints**. These are optional annotations that allow the intended type of variables, function parameters, and return values to be specified. However, these hints are ignored by the Python interpreter; their primary purpose is to be consumed by external tools known as **type checkers**.

## Static and dynamic type checking

A fundamental distinction must be made between when and how types are verified:

- **Static type checking**: Types are analyzed **before** the code is run. Tools examine the source code to identify potential mismatches between the provided annotations and the actual logic. This process is similar to the compilation checks found in languages like Java or C++.
- **Dynamic type checking**: Types are verified **during** execution. If a function expects an integer but receives a string, an error is raised at the exact moment the operation is attempted. While Python naturally throws exception, this happens because of missing methods and similar issues, not because of type mismatch during function call.

## Advantages

The adoption of static type checking is driven by several long-term benefits:

- **Early bug detection**: Logic errors, such as passing a `None` value to a function that cannot handle it, are caught during development rather than in production logs.
- **Enhanced documentation**: Type hints serve as a form of "living documentation" that remains in sync with the code. The intent of a function is made clear without needing to read through its internal implementation.
- **Improved tooling**: IDEs leverage type information to provide superior autocompletion, more accurate refactoring tools, and immediate visual feedback on errors.
- **Scalability**: In large codebases with multiple contributors, types provide a safety net that allows for more confident refactoring and easier onboarding of new developers.

## Tradeoffs

While beneficial, the introduction of type checking is not without its costs:

- **Increased boilerplate**: Additional syntax must be written, which feels overly verbose for simple scripts.
- **Learning curve**: Mastery of advanced typing concepts (such as Generics, Protocols, or TypeVars) requires a time investment.
- **Tooling overhead**: Type checkers must be integrated into development environments and CI/CD pipelines, adding a layer of complexity to the workflow.
- **False positives**: Static analysis is not perfect; occasionally, valid Python code may be flagged as an error, requiring the use of `# type: ignore` comments or explicit casts.

## Available packages

Several mature tools exist within the ecosystem, each with distinct strengths:

- **[ty](https://docs.astral.sh/ty/)**: Created by [Astral](https://astral.sh) (the developers of `uv` and `ruff`), this is a next-generation type checker written in Rust. It aims for extreme performance—targeting speeds 10x to 100x faster than existing tools—and provides a unified experience for users of the Astral toolchain.
- **[mypy](https://mypy.readthedocs.io/en/stable/)**: The "grandfather" of Python type checkers and the official reference implementation. It is highly configurable and has a vast ecosystem of plugins.
- **[pyright](https://microsoft.github.io/pyright/)**: Developed by Microsoft, this checker is written in TypeScript and is significantly faster than mypy. It powers the [Pylance](https://visualstudio.com) extension in VS Code.
- **[pyre](https://pyre-check.org/)**: A performant checker from Meta designed for massive codebases, featuring advanced security analysis (taint analysis).
- **[pytype](https://google.github.io/pytype/)**: Developed by Google, it is unique because it can infer types even in code that lacks annotations.

**Pyright** remains the best starting point due to its seamless integration with VS Code. However, for development speed **ty** is the recommended choice (despite being a beta version at the time of writing), especially when used alongside `uv`. **mypy** is the preferred industry staple for its level of plugin support and strict adherence to the reference standard.

## Advanced concepts

As codebases grow in complexity, advanced typing features are required. Those often help with handling circular dependencies, simplifying complex signatures, and defining flexible interfaces.

### Indicating type support with py.typed

When a library is distributed, a mechanism is required to inform type checkers that it contains valid type annotations. Without this, tools like `mypy` or `pyright` may ignore the internal hints and treat the library as untyped.

The `py.typed` file is a **marker file** introduced by [PEP 561](https://peps.python.org/pep-0561/). Its presence signals to static analysis tools that the package maintainer has provided type information that should be used during the type-checking process of any downstream code.

- **Create for libraries**: This file is essential if a package is intended to be used as a dependency by other developers. It ensures that users of the library receive accurate type hints and error reporting in their own environments.
- **Do not create for applications**: For standalone applications that are not imported by other projects, a `py.typed` file is generally unnecessary. The type checker already has access to the source code it is analyzing directly.
- **Content**: The file is typically **empty**. Its mere existence is the relevant signal to the tooling.
- **Location**: It must be placed in the **root of the package** (the same directory containing the `__init__.py` file). If a package contains sub-packages, the marker at the top level applies recursively to all of them.

### Imports under TYPE_CHECKING

Circular imports frequently occur when two modules need to reference each other's types for annotations. The `TYPE_CHECKING` constant from the `typing` module is used to resolve this.

- **Behavior**: It is evaluated as `True` by static type checkers but remains `False` at runtime.
- **Usage**: Imports needed strictly for type hints are placed inside an `if TYPE_CHECKING:` block. This prevents the Python interpreter from executing those imports during normal program runs, thus avoiding circularity.
- **Forward References**: When using this pattern, types from the guarded import must be referenced as strings (e.g., `def func(obj: "ClassName"):`) unless `from __future__ import annotations` is used at the top of the file. Can be used out of the box for python starting from 3.14.

### Type aliases

Type aliases allow a complex type expression to be assigned a simpler, more descriptive name, enhancing readability.

- **Modern Syntax (Python 3.12+)**: The `type` keyword is the preferred method for declaring aliases (e.g., `type Point = tuple[float, float]`). It provides lazy evaluation and clearer differentiation from standard variable assignments.
- **Legacy Syntax**: In older versions, aliases were created via simple assignment, often annotated with `TypeAlias` to assist checkers (e.g., `Point: TypeAlias = tuple[float, float]`).
- **Generics**: Aliases can be generic, allowing them to represent a family of types.

### Subtyping with protocols

While standard inheritance (Nominal Subtyping) requires a class to explicitly inherit from a base class, **Protocols** enable "Static Duck Typing".

- **Definition**: A [Protocol](https://typing.python.org/en/latest/spec/protocol.html) defines a set of required methods and attributes.
- **Compatibility**: Any class that implements those required members is automatically considered a subtype of the protocol, even without an explicit inheritance relationship.
- **Comparison with ABCs**: Unlike [Abstract Base Classes (ABCs)](https://docs.python.org/3/library/abc.html), protocols do not require explicit registration or inheritance, making them ideal for typing third-party libraries that cannot be modified.

### Distinguishing types with NewType

The [NewType](https://docs.python.org/3/library/typing.html#newtype) helper is used to create distinct types that the checker treats as separate, even if they share the same underlying representation.

- **Example**: Creating a `UserId` type from an `int` ensures that a standard integer cannot be accidentally passed to a function expecting a verified `UserId`, preventing logic errors with zero runtime performance cost.

## Further reading

- [Official python typing documentation](https://docs.python.org/3/library/typing.html)
- [Typing.python.org: the community typing portal](https://typing.python.org/)
