# pytest: Testing in Python 

Code without tests is a liability disguised as an asset.

## Why write tests

Automated testing is one of the most important practices for building maintainable, reliable, and evolvable software. Well-written tests give developers confidence to refactor and extend code without fear of breaking existing functionality.

Without automated tests, developers are forced to spend time manually testing code when changing it, time after time. Over the timeline of a serious projects, this adds up to more time that would be required to write automated tests.

Furthermore, without tests developers are required to remember proper testing procedures, which takes a mental toll and make long-term maintainability much harder.

## Writing high-quality tests

Excellent tests share several key characteristics:

- Fast to execute (most unit tests should run in milliseconds)
- Independent and isolated from one another
- Deterministic and repeatable
- Easy to read and understand
- Self-documenting through clear, descriptive names
- Free of unnecessary external dependencies
- Automatically verifiable (no manual inspection required)

### Test naming

Choose names that clearly describe the scenario and expected outcome. Good names act as living documentation and make failures immediately understandable.

Examples:

- ``test_empty_input_raises_value_error``
- ``test_valid_user_data_creates_profile_successfully``
- ``test_expired_token_rejected_with_401``

### Test organization

- Place tests in a dedicated ``tests/`` directory
- Mirror the structure of the source code when appropriate
- Group related tests logically within files and subdirectories


## Why pytest?

[pytest](https://docs.pytest.org/en/stable/) has become the standard choice for Python testing due to its simplicity, powerful features, and excellent ecosystem.

While [unittest](https://docs.python.org/3/library/unittest.html) is an alternative, pytest is generally preferred because it is more concise, expressive, and comes with many built-in conveniences.

For code dealing with complex input domains (especially algorithms or mathematical functions), the [hypothesis](https://hypothesis.readthedocs.io/) package can complement pytest by generating diverse test cases automatically, reducing reliance on manually chosen examples.

## Test discovery and basic usage

pytest automatically discovers and runs tests with almost no configuration, as long as certain conventions are being followed:

- Test files must be named ``test_*.py`` or ``*_test.py``
- Test functions must start with ``test_``
- Test classes must start with ``Test`` and contain methods starting with ``test_``

Tests are written using ordinary ``assert`` statements. ``pytest`` enhances these assertions with readable failure messages.

Run all with:
```bash
   uv run pytest
```

## Core pytest features

### Fixtures

In automated testing, every test should run in a **known, consistent, and isolated state**. Without proper setup, tests become fragile, hard to maintain, and unreliable.

Manually repeating setup code (creating objects, connecting to databases, preparing test data, etc.) in every test function leads to:

- Massive code duplication
- Difficulty keeping setups in sync when requirements change
- No automatic cleanup (teardown), which can leave side effects between tests
- Poor separation between *arrange* (setup) and *act/assert* (the actual test logic) steps

[Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) solve these problems. They are declared using a simple function with a special decorator:

```python
@pytest.fixture
def user():
   """Return a test user object."""
   return {"id": 42, "name": "Alice", "email": "alice@example.com"}
```

To use a fixture, simply pass its name as an argument to the test function:

```python
def test_user_has_name(user):
   assert user["name"] == "Alice"
   assert "email" in user
```

### Parametrization

[Parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html) allows running the same test logic against multiple inputs without duplicating code:

```python
@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

Without it, code duplication would occur, leading to the same issues as described above. 


### Marks

[Marks](https://docs.pytest.org/en/stable/how-to/mark.html) let you tag tests for skipping, expected failures, or selective execution (for example, not running tests with ``@pytest.mark.slow`).

Not very useful if you are just starting to write tests, you can get by without using them. 

### Mocking

If code depends on external systems — databases, APIs, file systems, or third-party services - [mocking](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) is used. 

Directly using those systems creates several problems:

- Tests become slow
- Tests may become unreliable due network issues, rate limits, etc.
- Tests require too complex setup or credentials
- You cannot easily test edge cases or error conditions
- Running tests modifies real data or incurs costs
- Failure in a single base class leads to errors across all tests even loosely related to that class. 

**Mocking** solves this by replacing real objects or functions with fake ("mock") versions that simulate the behavior you need.

### Additional plugins

There are [a lot of plugins](https://docs.pytest.org/en/stable/reference/plugin_list.html), but here is a brief list of suggested ones:

- ``pytest-cov`` measures code coverage.
- ``pytest-xdist`` runs tests in parallel.
- ``pytest-sugar`` and ``pytest-clarity`` improve console output.
- ``pytest-randomly`` runs tests in random order.

## Further Reading

- [Official pytest documentation](https://docs.pytest.org/).
- [pytest good integration practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html).
- [CKAN Testing Coding Standards](https://docs.ckan.org/en/latest/contributing/testing.html).
