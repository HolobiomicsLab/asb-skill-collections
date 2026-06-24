---
name: pytest-output-interpretation
description: Use when after running `pytest tests/` on a Python package (especially
  one with dev extras installed), you need to determine if the full test suite passed,
  identify which tests failed, and extract error messages or stack traces for debugging.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pip
  - pytest
  - Python
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
  - build: coll_biosynfoni_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni_cq
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

# pytest-output-interpretation

## Summary

Interpret pytest test execution output to determine whether a Python package's bundled test suite passes or fails, and extract diagnostic information from the test report. This skill is essential for validating package correctness and identifying test failures during development or continuous integration workflows.

## When to use

After running `pytest tests/` on a Python package (especially one with dev extras installed), you need to determine if the full test suite passed, identify which tests failed, and extract error messages or stack traces for debugging. Use this skill when you have concrete pytest console output or a test report file and need to synthesize a pass/fail verdict and diagnostic summary.

## When NOT to use

- The test suite has not yet been run; you need to execute `pytest` first.
- You are trying to modify or write new tests rather than interpret existing results.
- The output is from a different test runner (e.g., unittest, nose, tox) — this skill is pytest-specific.

## Inputs

- pytest console output (stdout/stderr)
- pytest test report file (e.g., JUnit XML, JSON, or terminal summary)
- test result summary line from pytest

## Outputs

- pass/fail verdict (boolean or enum)
- total test count (integer)
- passed test count (integer)
- failed test count (integer)
- skipped test count (integer)
- list of failed test names and error messages (structured)
- diagnostic summary (string)

## How to apply

Execute the test suite using `pytest tests/` from the package root (after installing in development mode with `pip install -e .[dev]`), then parse the final summary line and any FAILED markers in the output. Look for the summary statement that reports the total number of passed, failed, skipped, or errored tests (e.g., '42 passed', '2 failed'). If the exit code is 0 and the summary shows no failures, the test suite passed. If failures or errors are reported, read the FAILED section and the traceback for each failing test to extract the assertion error or exception type. Record the specific test names, error messages, and any relevant stack trace context to guide remediation. The test pass/fail status directly validates package correctness and reproducibility.

## Related tools

- **pytest** (test runner; executes the bundled test suite and produces structured output with pass/fail status and failure diagnostics) — https://pytest.readthedocs.io/
- **pip** (package manager; installs the package in development mode with test dependencies before pytest execution) — https://pip.pypa.io/
- **Python** (runtime environment; executes pytest and the test suite) — https://www.python.org/

## Examples

```
pytest tests/
```

## Evaluation signals

- Exit code is 0 (success) or non-zero (failure) — the process exit code reliably indicates pass/fail
- The final pytest summary line is present and parseable (e.g., 'X passed', 'X failed', 'X error') — absence suggests incomplete output
- All test node IDs in the FAILED section match patterns in the tests/ directory (tests/test_*.py::TestClass::test_method) — validates test identification
- Error messages and stack traces are present for each failed test and contain recognizable Python exception types (AssertionError, ImportError, etc.) — confirms diagnostic completeness
- Test counts are consistent: passed + failed + skipped ≤ total tests run — validates internal consistency of the report

## Limitations

- pytest output format may vary by version, verbosity flag, or plugin configuration (e.g., `-v`, `-vv`, `--tb=short`), requiring robust parsing.
- Flaky or nondeterministic tests may pass or fail on successive runs, making a single test run an unreliable validator of package state.
- Pytest may be interrupted or killed before completion, producing truncated output that cannot be fully interpreted.
- Conditional test skips (marked with `@pytest.mark.skip` or platform/dependency conditions) mean the absence of a test result does not imply failure.

## Evidence

- [other] The biosynfoni repository displays a Tests badge linked to a GitHub Actions workflow (test-biosynfoni.yml) that validates the package's test suite status.: "The biosynfoni repository displays a Tests badge linked to a GitHub Actions workflow (test-biosynfoni.yml) that validates the package's test suite status."
- [other] Run the full test suite using pytest on the tests/ directory (pytest tests/). Verify that all tests pass and report the test outcome.: "Run the full test suite using pytest on the tests/ directory (pytest tests/). Verify that all tests pass and report the test outcome."
- [other] Install the package in editable/development mode using pip with the dev extras (pip install -e .[dev]).: "Install the package in editable/development mode using pip with the dev extras (pip install -e .[dev])."
- [other] You can also run the tests locally with the following command: pytest tests/: "You can also run the tests locally with the following command: pytest tests/"
