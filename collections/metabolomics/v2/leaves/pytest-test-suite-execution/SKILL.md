---
name: pytest-test-suite-execution
description: Use when after installing a package in development mode (e.g., via `pip
  install -e .[dev]`) to verify the package functions as intended, or before submitting
  pull requests to confirm no regressions were introduced by code changes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - pip
  - pytest
  - biosynfoni
  license_tier: open
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- pip install -e .[dev]
- pytest tests/
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic
  research
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni
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

# pytest-test-suite-execution

## Summary

Execute a Python package's complete test suite using pytest to verify functional correctness and identify failures before deployment or contribution. This skill validates that all unit and integration tests pass after installation and development modifications.

## When to use

Apply this skill after installing a package in development mode (e.g., via `pip install -e .[dev]`) to verify the package functions as intended, or before submitting pull requests to confirm no regressions were introduced by code changes.

## When NOT to use

- Package has not been installed in development mode — install via `pip install -e .[dev]` first to ensure editable source is available to tests.
- Test dependencies are not installed — verify dev extras are included in the pip install command.
- You only want to run a subset of tests — use pytest filtering syntax (e.g., `pytest tests/test_module.py::test_function`) instead of the full suite command.

## Inputs

- Package source code directory with tests/ subdirectory
- Installed package with development dependencies (via pip install -e .[dev])
- Test module files (Python files in tests/ directory)

## Outputs

- pytest exit code (0 for all pass, non-zero for failures)
- Test results summary (passed count, failed count, skipped count)
- Detailed failure tracebacks and assertion errors (if applicable)
- Optional coverage report (if pytest-cov plugin is used)

## How to apply

Navigate to the package repository root directory and execute pytest on the tests/ directory using `pytest tests/`. This command discovers and runs all test modules, fixtures, and assertions defined in the test suite. Examine the pytest output for pass/fail counts, specific assertion failures, and coverage metrics. All tests must pass with exit code 0 before the package can be considered functional or ready for merge. If tests fail, review the pytest traceback to identify the failing test name, assertion condition, and the input/output mismatch that caused the failure.

## Related tools

- **pytest** (Test discovery, execution, and reporting framework for running the complete test suite) — https://docs.pytest.org/
- **pip** (Package installer used to install the package and its development dependencies before test execution) — https://pip.pypa.io/
- **biosynfoni** (Example package whose test suite is executed by pytest to validate molecular fingerprint functionality) — https://github.com/lucinamay/biosynfoni

## Examples

```
pytest tests/
```

## Evaluation signals

- pytest exit code is 0 (all tests passed)
- Test summary output shows 0 failed tests and 0 errors
- All test function names listed in output are marked PASSED (not FAILED or SKIPPED)
- No assertion errors or exception tracebacks appear in pytest output
- Execution completes without hanging or timing out

## Limitations

- Test suite must be properly written and discoverable by pytest (tests in tests/ directory with test_*.py naming convention)
- Tests may have platform or environment-specific dependencies (e.g., RDKit availability for biosynfoni) that can cause false failures if not met
- Passing tests do not guarantee the package will function correctly in all use cases — only that defined test cases are satisfied

## Evidence

- [other] Execute the complete test suite using pytest on the tests/ directory with `pytest tests/`. Verify all tests pass and package is functional.: "Execute the complete test suite using pytest on the tests/ directory with `pytest tests/`. Verify all tests pass and package is functional."
- [other] Install the package in development mode using pip with dev dependencies via `pip install -e .[dev]`.: "Install the package in development mode using pip with dev dependencies via `pip install -e .[dev]`."
- [other] Run the following command from the root of the project to install the project for development: "Run the following command from the root of the project to install the project for development"
- [other] You can also run the tests locally with the following command: "You can also run the tests locally with the following command"
- [other] The biosynfoni package has a GitHub Actions CI workflow that runs tests, as indicated by the Tests badge displayed in the repository.: "The biosynfoni package has a GitHub Actions CI workflow that runs tests, as indicated by the Tests badge"
