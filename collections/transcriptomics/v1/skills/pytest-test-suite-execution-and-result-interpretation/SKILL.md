---
name: pytest-test-suite-execution-and-result-interpretation
description: Use when after forking and cloning a repository (e.g., scverse/scanpy) to verify that the development environment is correctly configured, or after implementing a feature or bugfix to ensure no regressions were introduced.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pytest
  - git
  - Hatch
  - matplotlib
  - Scanpy
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- We use pytest to test scanpy. To run the tests, simply run `hatch test`
- This section of the docs covers our practices for working with git on our codebase
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scanpy
    doi: 10.1186/s13059-017-1382-0
    title: scanpy
  dedup_kept_from: coll_scanpy
schema_version: 0.2.0
---

# pytest-test-suite-execution-and-result-interpretation

## Summary

Execute a pytest test suite via Hatch to validate code correctness and identify test failures in a development environment. This skill ensures CI/CD reproducibility by running all configured tests and interpreting exit codes and failure reports.

## When to use

After forking and cloning a repository (e.g., scverse/scanpy) to verify that the development environment is correctly configured, or after implementing a feature or bugfix to ensure no regressions were introduced. Use this skill whenever you need to reproduce the CI workflow locally or validate that a code change does not break existing functionality.

## When NOT to use

- When the development environment is not yet created or Hatch is not installed — first ensure Hatch is available and hatch.toml exists in the repository root.
- When only a subset of tests is needed and the full test suite would be prohibitively slow — use `-k` pattern matching or specify individual test files instead of running the full suite.
- When testing against a specific older version of a dependency that conflicts with the Hatch environment specification — use a manual virtual environment or a custom pytest invocation instead.

## Inputs

- cloned repository with hatch.toml configuration
- pytest test suite in scanpy/tests directory
- matplotlib reference images (for plot comparison tests)

## Outputs

- test execution report with pass/fail counts
- exit code (0 for success, non-zero for failure)
- pytest log with detailed failure messages and tracebacks
- image comparison results (for plot-based tests)

## How to apply

Clone the repository and navigate to the root directory. Invoke `hatch test` to automatically create the predefined Hatch environment specified in hatch.toml and execute the full pytest test suite on all tests in the scanpy/tests directory with the configured pytest settings. Monitor the exit code (0 indicates all non-skipped tests passed). Inspect the test output for failure counts and error messages. For rapid iteration during development, run a subset of tests using `-k` patterns or specific test file names (e.g., `hatch test test_plotting.py`). For visual regression testing, verify that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture. A test run is considered successful when it completes with exit code 0 and reports zero non-skipped test failures.

## Related tools

- **pytest** (Test framework that discovers and executes unit and integration tests; configured via pytest settings in hatch.toml)
- **Hatch** (Project environment and dependency manager that creates isolated Python environments and provides the `hatch test` command to run the test suite with predefined configuration)
- **git** (Version control tool used to clone the repository and manage branches during development)
- **matplotlib** (Plotting library; its image_comparer fixture validates that generated plots match reference images)
- **Scanpy** (The target package being tested; test suite validates preprocessing, visualization, clustering, trajectory inference, and differential expression functionality) — https://github.com/scverse/scanpy

## Examples

```
hatch test
```

## Evaluation signals

- Test execution completes with exit code 0 and reports zero non-skipped test failures.
- All test files in the scanpy/tests directory are discovered and executed by pytest without import or collection errors.
- Custom matplotlib plot reference images generated during test execution match the expected outputs as verified by the image_comparer fixture.
- No unexpected warnings or deprecation notices appear in the test output that would indicate breaking changes in dependencies.
- Optional: subset tests using `-k` patterns execute faster and still report correct pass/fail status for the filtered test set.

## Limitations

- The test suite execution time may be substantial for large codebases; use `-k` pattern matching or individual test files for faster feedback during rapid development iteration.
- Image comparison tests (matplotlib plots) are sensitive to font rendering, backend configuration, and system-level graphics settings; the image_comparer fixture may produce false negatives on different operating systems or graphics environments.
- Exit code 0 confirms that tests passed but does not guarantee code correctness or comprehensive coverage; review test coverage reports and manually validate critical functionality.
- Hatch environment isolation may mask dependency conflicts that would appear in production environments; consider running tests in multiple isolated environments or with different dependency versions for robustness.

## Evidence

- [other] Scanpy uses pytest for testing and provides a Hatch environment configuration to execute the test suite via the `hatch test` command.: "Scanpy uses pytest for testing and provides a Hatch environment configuration to execute the test suite via the `hatch test` command."
- [other] Execute the full pytest test suite via `hatch test`, which runs all tests in the scanpy/tests directory with the configured pytest settings.: "Execute the full pytest test suite via `hatch test`, which runs all tests in the scanpy/tests directory with the configured pytest settings."
- [other] Verify the test run completes with exit code 0 and reports zero non-skipped test failures.: "Verify the test run completes with exit code 0 and reports zero non-skipped test failures."
- [other] Run a subset of tests using `-k` patterns or specific test files (e.g., `hatch test test_plotting.py`) for faster iteration during development.: "Run a subset of tests using `-k` patterns or specific test files (e.g., `hatch test test_plotting.py`) for faster iteration during development."
- [other] Check that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture.: "Check that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture."
- [other] We use pytest to test scanpy. To run the tests, simply run `hatch test`: "We use pytest to test scanpy. To run the tests, simply run `hatch test`"
- [other] Create a development environment using Hatch by running `hatch test` from the repository root, which automatically creates the predefined Hatch environment specified in hatch.toml.: "Create a development environment using Hatch by running `hatch test` from the repository root, which automatically creates the predefined Hatch environment specified in hatch.toml."
