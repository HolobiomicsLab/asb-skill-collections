---
name: test-failure-diagnosis-and-logging-analysis
description: Use when you have modified the Scanpy codebase (e.g., added a feature or bugfix) and need to confirm that all unit and integration tests pass before submitting a pull request, or when a CI workflow fails and you need to reproduce the failure locally to diagnose the root cause.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0091
  tools:
  - git
  - pytest
  - Hatch
  - matplotlib
  - Scanpy
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
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

# test-failure-diagnosis-and-logging-analysis

## Summary

Diagnose and analyze test failures in a scientific software suite by executing the full pytest test suite via Hatch, interpreting exit codes and non-skipped test counts, and examining matplotlib plot reference image mismatches via the image_comparer fixture. This skill is essential for validating that CI workflows reproduce correctly and that code changes do not introduce regressions in preprocessing, visualization, clustering, or trajectory inference pipelines.

## When to use

Use this skill when you have modified the Scanpy codebase (e.g., added a feature or bugfix) and need to confirm that all unit and integration tests pass before submitting a pull request, or when a CI workflow fails and you need to reproduce the failure locally to diagnose the root cause. Also apply this skill to verify that custom matplotlib plot reference images in the test suite match expected outputs after changes to visualization code.

## When NOT to use

- You have not yet cloned the repository and set up a local development environment; first perform git clone and Hatch environment initialization.
- You are running only a subset of tests and treating a passing subset run as equivalent to full test suite validation; always run the full suite before finalizing changes.
- The test failure is in a third-party dependency (e.g., numpy, scipy) rather than in Scanpy code itself; consult the dependency's issue tracker or upgrade the dependency version.

## Inputs

- Scanpy repository fork (cloned locally via git)
- Modified source code in scanpy/ directory
- hatch.toml configuration file specifying test environment
- pytest test files in scanpy/tests/ directory
- matplotlib plot reference images (baseline images in test fixtures)

## Outputs

- pytest exit code (0 for success, non-zero for failure)
- count of passed, failed, and skipped tests
- detailed test failure tracebacks and error messages
- image_comparer fixture reports comparing generated plots to reference images
- log output from test run (stdout/stderr)
- confirmation of zero non-skipped test failures

## How to apply

Clone the scverse/scanpy repository and set up a development environment using Hatch by running `hatch test` from the repository root, which automatically creates the Hatch environment defined in hatch.toml with all test dependencies. Execute the full pytest test suite via `hatch test`, which runs all tests in the scanpy/tests directory with the configured pytest settings and reports exit code and test failure counts. Verify the run completes with exit code 0 and zero non-skipped test failures; if failures occur, examine the pytest output for specific test names and error tracebacks. For visualization tests, check that matplotlib plot reference images match expected outputs via the image_comparer fixture—mismatches indicate unintended changes to plot rendering. For faster iteration during development, run a subset of tests using `-k` patterns (e.g., `hatch test -k test_plotting`) or specific test files (e.g., `hatch test test_plotting.py`), but always run the full suite before finalizing a PR.

## Related tools

- **pytest** (Test runner that executes unit and integration tests in scanpy/tests/ and reports failures, error messages, and exit codes)
- **Hatch** (Environment manager that creates isolated test environments from hatch.toml configuration and runs pytest via `hatch test` command)
- **matplotlib** (Plotting library used by Scanpy visualization; matplotlib.testing.setup and image_comparer fixture establish consistent environment for plot reference image comparison)
- **git** (Version control for cloning the Scanpy repository and managing branches during development) — https://github.com/scverse/scanpy
- **Scanpy** (The single-cell analysis toolkit being tested; contains test suite in scanpy/tests/ and source code to be validated) — https://github.com/scverse/scanpy

## Examples

```
hatch test
```

## Evaluation signals

- pytest exit code is 0, indicating no test failures
- Test summary reports zero non-skipped test failures (all failures, if any, are in skipped tests only)
- matplotlib image_comparer fixture confirms generated plots match reference images without significant pixel divergence
- Full test suite run (not just a subset via `-k` pattern) completes without timeout or hanging
- Specific test files related to modified code (e.g., test_plotting.py if visualization changed) show all passing tests

## Limitations

- Image_comparer fixture requires matplotlib reference images to be present and up-to-date; if reference images are missing or outdated, comparison will fail even if the code is correct—regenerate reference images explicitly if intentional plot changes are made.
- Test execution time can be long for the full suite; subset testing via `-k` patterns speeds iteration but does not catch all integration failures, so must be followed by full suite run.
- Some tests may be platform-specific (e.g., rendering or file system behavior) and could fail on certain operating systems or with certain matplotlib backends, even though the code is correct.
- Skipped tests are excluded from the failure count, so a test can be silently skipped (e.g., due to missing optional dependency) without triggering a failure signal.

## Evidence

- [other] Scanpy uses pytest for testing and provides a Hatch environment configuration to execute the test suite via the `hatch test` command.: "Scanpy uses pytest for testing and provides a Hatch environment configuration to execute the test suite via the `hatch test` command."
- [other] Execute the full pytest test suite via `hatch test`, which runs all tests in the scanpy/tests directory with the configured pytest settings.: "Execute the full pytest test suite via `hatch test`, which runs all tests in the scanpy/tests directory with the configured pytest settings."
- [other] Verify the test run completes with exit code 0 and reports zero non-skipped test failures.: "Verify the test run completes with exit code 0 and reports zero non-skipped test failures."
- [other] Check that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture.: "Check that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture."
- [other] We use pytest to test scanpy. To run the tests, simply run `hatch test`: "We use pytest to test scanpy. To run the tests, simply run `hatch test`"
- [other] matplotlib.testing.setup tries to establish a consistent environment for creating plots: "matplotlib.testing.setup tries to establish a consistent environment for creating plots"
