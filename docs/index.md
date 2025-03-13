# PyWC Project example

``` {toctree}
:maxdepth: 2
:hidden:
license.md
reference.md
```

The example project inspired after
[Hypermodern Python](https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769)
article series.
The command-line interface simulates `wc` utility. 

## Performance

``` {eval-rst}
.. plot:: ../plots/performance.py
    :show-source-link:
```

## Installation

To install PyWC,
run this command in your terminal:

``` {code-block} console
   $ pip install pywc
```

## Usage

PyWC usage looks like:

``` {eval-rst}
.. click:: pywc.console:main
   :prog: pywc
```
