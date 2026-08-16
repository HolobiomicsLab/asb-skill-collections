---
name: test-suite-execution-and-validation
description: Use when when you have cloned or obtained a Python package repository
  and need to verify that the package can be installed from source and that its test
  suite passes without errors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - pip
  - pytest
  - black
  license_tier: open
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- pip install -e .[dev]
- pytest tests/
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni_2_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# test-suite-execution-and-validation

## Summary

Execute a Python package's pytest test suite locally to validate that the package installs correctly and all automated tests pass. This skill confirms reproducibility of the software environment and integration of dependencies.

## When to use

When you have cloned or obtained a Python package repository and need to verify that the package can be installed from source and that its test suite passes without errors. Use this skill after a development installation to detect regressions or dependency issues before deployment or contribution submission.

## When NOT to use

- Package has no test suite or tests/ directory is empty—validation cannot be performed.
- Development dependencies are not installable (e.g., due to system library conflicts or unavailable wheels for your Python version)—resolve environment issues first.
- You are testing a pre-built/wheel-installed package rather than a development clone—use the package's installed test runner or integration tests instead.

## Inputs

- Python package repository (source directory)
- pyproject.toml or setup.py with [dev] extras defined
- tests/ directory containing pytest test files

## Outputs

- Test execution report (pass/fail for each test)
- Exit code (0 for all pass, non-zero for failures)
- stdout/stderr logs with failure details and stack traces

## How to apply

First, navigate to the package repository root directory. Install the package in editable mode with development dependencies using `pip install -e .[dev]`, which ensures test fixtures and development tools (like pytest) are available. Then execute the full test suite using `pytest tests/` from the root directory. The test suite will report pass/fail status for each test; all tests must pass without errors or warnings (unless explicitly marked as expected failures). If any tests fail, inspect the error output to diagnose missing dependencies, incompatible versions, or code defects. Code formatting should also be validated against the project's style guide (e.g., Black) before test execution to catch style violations early.

## Related tools

- **pytest** (Test discovery, execution, and result reporting for the package test suite) — https://docs.pytest.org
- **pip** (Package installation in editable mode with development dependencies) — https://pip.pypa.io
- **black** (Optional code style validation before running tests to catch formatting violations) — https://github.com/psf/black

## Examples

```
pip install -e .[dev] && pytest tests/
```

## Evaluation signals

- pytest reports 'passed' count equal to total test count with exit code 0
- No import errors or missing module exceptions during test collection phase
- All test assertions complete without AttributeError, ValueError, or ImportError
- Execution time is reasonable (no indefinite hangs or timeouts)
- stdout shows reproducible and deterministic results across repeated runs

## Limitations

- Test suite may not cover all code paths or edge cases; passing tests do not guarantee the package is production-ready.
- Tests may pass on the development machine but fail in different environments (e.g., different OS, Python micro-version, or system libraries).
- Development dependencies must be installable; if a transitive dependency is broken or unavailable, tests cannot run.
- No changelog was found in the biosynfoni repository, so test coverage history and known issues are not documented.

## Evidence

- [other] Execute the test suite using pytest tests/ to confirm all tests pass.: "Execute the test suite using pytest tests/ to confirm all tests pass."
- [other] Install the package in editable mode with development dependencies using pip install -e .[dev].: "Install the package in editable mode with development dependencies using pip install -e .[dev]."
- [readme] You can also run the tests locally with the following command: pytest tests/: "You can also run the tests locally with the following command: pytest tests/"
- [readme] Please use `black` to format your code before submitting a pull request: "Please use `black` to format your code before submitting a pull request"
