---
name: python-package-api-interface-design
description: Use when you are building or refactoring a scientific Python library and need to decide how to organize and expose utility functions (e.g., adaptive coarse-graining, filtering, analysis routines) so that end users can import and call them reliably.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Python
  - flake8
  - conda
  - pytest
  - pytest-cov
  - pytest-flake8
  - black
  - autopep8
  - Sphinx
  - cooler
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans:
- enabling high-resolution Hi-C analysis in Python
- We use [flake8](http://flake8.pycqa.org/en/latest/) to automatically lint the code
- we recommend using [conda](https://docs.conda.io/en/latest/miniconda.html)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cooltools
    doi: 10.1371/journal.pcbi.1012067
    title: cooltools
  dedup_kept_from: coll_cooltools
schema_version: 0.2.0
---

# Python Package API Interface Design

## Summary

Design and document a well-structured Python package API that exposes utility functions through organized subpackages (e.g., cooltools.lib) with clear imports, stable interfaces, and comprehensive Sphinx documentation. This skill ensures that scientific computation libraries are discoverable, testable, and maintainable across versions.

## When to use

You are building or refactoring a scientific Python library and need to decide how to organize and expose utility functions (e.g., adaptive coarse-graining, filtering, analysis routines) so that end users can import and call them reliably. Use this skill when you have a set of related functions that should live in a logical subpackage (lib, utils, analysis) and you want to document the API surface, enforce code quality, and validate that the interface works as intended.

## When NOT to use

- Your package is a single-file script or does not need to expose a public API to other projects.
- You are working with unstable, experimental code that is not ready for external consumption (the article notes: 'New functionality for smoothing P(s) and derivatives (API is not yet stable)').
- Your primary goal is rapid prototyping; formal API design and documentation overhead may not justify the effort until the library is stabilized.

## Inputs

- Python source files with utility functions (e.g., .py modules)
- Package structure with __init__.py files defining public exports
- Docstrings in Numpy or similar parseable format
- Configuration files (setup.py, setup.cfg, pyproject.toml, Sphinx conf.py)

## Outputs

- Organized subpackage (e.g., cooltools.lib) with importable public API
- Sphinx-generated HTML API reference documentation
- pytest unit test suite confirming importability and function behavior
- Code coverage and style reports (pytest-cov, pytest-flake8 output)
- Formatted source code passing black or autopep8 checks

## How to apply

Organize utility functions into a dedicated subpackage (e.g., cooltools.lib) with explicit __init__.py imports that expose the public API. Write each function with Numpy-style docstrings so that Sphinx can automatically generate API reference documentation. Install the package in editable (development) mode using `pip install -e .` to allow rapid testing of changes. Run pytest with code-coverage extensions (pytest-cov) and style checks (pytest-flake8, flake8) to ensure functions meet quality standards. Apply a code formatter like black or autopep8 to maintain consistent style. Build the Sphinx documentation locally with `make docs` and verify that the function appears in the API reference with correct signatures and docstrings. Confirm via pytest that the function is importable from the intended path (e.g., `from cooltools.lib import adaptive_coarsegrain`) and behaves as expected in unit tests.

## Related tools

- **pytest** (Unit testing framework to verify that functions are callable and behave correctly after import) — https://docs.pytest.org/en/latest
- **pytest-cov** (Measure code coverage of unit tests to ensure critical API paths are exercised) — https://docs.pytest.org/en/latest
- **pytest-flake8** (Enforce code style and lint standards on the API and supporting code) — https://docs.pytest.org/en/latest
- **flake8** (Automatically lint code to maintain consistent style across the package) — http://flake8.pycqa.org/en/latest/
- **black** (Code formatter to ensure consistent, uncompromising formatting of package source) — https://github.com/psf/black
- **autopep8** (Automated formatter to conform code to PEP 8 style guide) — https://github.com/hhatto/autopep8
- **Sphinx** (Documentation generator that parses Numpy-style docstrings and produces HTML API reference) — http://www.sphinx-doc.org/en/stable
- **cooler** (Underlying data format and utilities for storing and manipulating Hi-C contact matrices) — https://github.com/open2c/cooler

## Examples

```
cd /path/to/cooltools && pip install -e . && python -c "from cooltools.lib import adaptive_coarsegrain; print(adaptive_coarsegrain.__doc__)" && pytest cooltools/lib/tests/ -v --cov=cooltools.lib && make docs
```

## Evaluation signals

- Function is successfully imported from the target subpackage path (e.g., `from cooltools.lib import adaptive_coarsegrain`) without ImportError.
- Sphinx documentation build completes without warnings and function appears in the generated API reference with correct signature and docstring.
- pytest runs to completion with no import or execution errors; unit test suite confirms the function produces expected outputs for standard inputs.
- Code coverage report shows that the public API code paths are exercised by unit tests (target: >80% coverage for critical paths).
- flake8 and black validation pass with no style or lint errors on the API module and its tests.

## Limitations

- API stability requires forward planning; once the public API is released and used by external code, breaking changes incur migration burden (the article notes that smoothing functionality has 'API is not yet stable').
- Sphinx documentation generation requires correct setup of conf.py and consistent docstring format; inconsistent or missing docstrings will result in incomplete or malformed API documentation.
- pytest coverage does not guarantee correctness—high coverage of a buggy function still passes; manual code review and integration testing with real Hi-C data are necessary to validate scientific correctness.
- Style enforcement via black and flake8 is cosmetic; it does not prevent logical errors or performance issues in the implemented functions.

## Evidence

- [other] We use pytest as our unit testing framework with the pytest-cov extension to check code coverage and pytest-flake8 to check code style: "We use [pytest](https://docs.pytest.org/en/latest) as our unit testing framework with the `pytest-cov` extension to check code coverage and `pytest-flake8` to check code style"
- [other] Install in editable development mode using pip install -e . for local development and testing: "install in "editable" (i.e. development) mode using the `-e` option"
- [other] Use Numpy style docstrings and Sphinx to document the library and generate API reference: "We use [Numpy style docstrings](https://numpydoc.readthedocs.io/en/latest/format.html>) and [Sphinx](http://www.sphinx-doc.org/en/stable) to document this library"
- [other] Build documentation locally using make docs and verify the function appears in the API reference: "To build the documentation: `make docs`"
- [discussion] New functionality may have unstable API that is not yet ready for public consumption: "New functionality for smoothing P(s) and derivatives (API is not yet stable)"
- [other] Use code formatters like black or autopep8 to maintain consistent code style: "You can use a code formatter like [black](https://github.com/psf/black) or [autopep8](https://github.com/hhatto/autopep8)"
