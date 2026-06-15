---
name: editable-development-mode-installation-and-verification
description: Use when when you are developing or contributing to a Python package (like cooltools) and need to test changes to utility functions, library integrations, or API implementations without reinstalling the package after each modification. Apply this when you must verify that a new function (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3071
  tools:
  - flake8
  - conda
  - pip
  - pytest
  - pytest-cov
  - pytest-flake8
  - Sphinx
  - black
  - cooler
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans:
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

# editable-development-mode-installation-and-verification

## Summary

Install a Python package in editable (development) mode and verify correctness through import, unit testing, code coverage, style linting, and documentation generation. This workflow enables rapid iteration on package code while ensuring all components remain functional and compliant.

## When to use

When you are developing or contributing to a Python package (like cooltools) and need to test changes to utility functions, library integrations, or API implementations without reinstalling the package after each modification. Apply this when you must verify that a new function (e.g., adaptive_coarsegrain) is correctly exposed in the package namespace, passes all unit tests, meets code style standards, and is properly documented.

## When NOT to use

- Package is already installed in production mode and users should not modify source code; use standard installation (`pip install package_name`) instead.
- You are running a pre-compiled or binary package with no Python source; editable mode requires a setuptools-compatible source tree.
- Development environment lacks build tools (gcc, Make, Sphinx) or permission to modify the installation directory; fall back to virtual environment isolation or containerization.

## Inputs

- Git repository containing Python package source code (e.g., open2c/cooltools)
- Python environment with pip and build tools available
- Package setup.py or pyproject.toml with dependency specifications

## Outputs

- Installed package in editable mode with symlink to source directory
- Unit test execution report (passed/failed counts, coverage metrics)
- Code style lint report (flake8 compliance check)
- Built Sphinx HTML documentation with API reference
- Confirmation that target function/utility is importable and callable

## How to apply

Begin by cloning the target repository and installing it in editable mode using `pip install -e .` from the repository root; this creates a symlink to the development directory so changes are immediately reflected without reinstallation. Next, import the function or module of interest in a Python session to confirm it is callable and accessible from the intended namespace (e.g., `from cooltools.lib import adaptive_coarsegrain`). Then run the full pytest suite with `pytest` to execute unit tests and verify behavioral correctness. Extend pytest with the `pytest-cov` extension to measure code coverage and ensure the new code paths are exercised; also run `pytest-flake8` to enforce code style compliance using flake8 linting rules. Finally, build the Sphinx documentation using `make docs` and inspect the generated API reference to confirm the function appears with its docstring and signature intact. Success is indicated when all tests pass, coverage is satisfactory, no style violations are reported, and the function is discoverable in the built documentation.

## Related tools

- **pip** (Install package in editable mode with -e flag; manages Python dependencies and package path setup) — https://pip.pypa.io/en/latest/
- **pytest** (Execute unit tests to verify function behavior and catch regressions) — https://docs.pytest.org/en/latest
- **pytest-cov** (Measure code coverage during test execution to ensure new functions are exercised) — https://github.com/pytest-dev/pytest-cov
- **pytest-flake8** (Run flake8 linting as part of pytest suite to enforce PEP 8 code style compliance) — https://github.com/tholo/pytest-flake8
- **flake8** (Automatically lint code and maintain code style according to PEP 8 standards) — http://flake8.pycqa.org/en/latest/
- **Sphinx** (Build HTML documentation from Numpy-style docstrings and render API reference for verification) — http://www.sphinx-doc.org/en/stable
- **black** (Optional code formatter to ensure consistent formatting before testing) — https://github.com/psf/black
- **cooler** (Upstream library for .cool file format handling; may be a dependency of cooltools.lib) — https://github.com/open2c/cooler

## Examples

```
cd /path/to/cooltools && pip install -e . && python -c "from cooltools.lib import adaptive_coarsegrain; print(adaptive_coarsegrain)" && pytest && pytest --cov=cooltools.lib && make docs
```

## Evaluation signals

- Function is successfully imported without ImportError from the expected namespace (e.g., `from cooltools.lib import adaptive_coarsegrain`)
- All unit tests pass (exit code 0 from pytest); no test failures or errors reported
- Code coverage for the new/modified module meets project threshold (typically ≥80%); coverage report shows the function's code paths are exercised
- No flake8 style violations in the modified or new code; pytest-flake8 completes without warnings in the target module
- Function signature, docstring, and description appear in the built Sphinx HTML documentation under the appropriate API section (e.g., cooltools.lib)

## Limitations

- Editable mode requires a source tree with a valid setup.py or pyproject.toml; will fail on pre-built or binary-only distributions.
- Documentation build requires Sphinx and configured conf.py; may fail if the project's docs directory is incomplete or dependencies are missing.
- Code coverage measurement depends on test suite comprehensiveness; high coverage does not guarantee correctness, only that code paths are executed.
- Style checking with flake8 enforces syntactic conventions (line length, indentation, naming) but does not validate logic or algorithmic correctness.
- Function must be explicitly exposed in the module's __init__.py or public API for import verification to succeed; internal utility functions may not be discoverable in the intended namespace.

## Evidence

- [other] install in "editable" (i.e. development) mode using the `-e` option: "install in "editable" (i.e. development) mode using the `-e` option"
- [other] pytest and code coverage checking via pytest-cov extension: "We use [pytest](https://docs.pytest.org/en/latest) as our unit testing framework with the `pytest-cov` extension"
- [other] flake8 and pytest-flake8 for code style enforcement: "We use [pytest](https://docs.pytest.org/en/latest) as our unit testing framework with the `pytest-cov` extension to check code coverage and `pytest-flake8` to check code style"
- [other] Sphinx documentation generation and API reference: "We use [Numpy style docstrings](https://numpydoc.readthedocs.io/en/latest/format.html>) and [Sphinx](http://www.sphinx-doc.org/en/stable) to document this library"
- [other] pytest execution from repository root: "you can just `cd` to the root of your repository and run `pytest`"
- [other] Sphinx documentation build command: "To build the documentation: `make docs`"
