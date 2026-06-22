---
name: python-automated-test-execution
description: Use when when contributing code changes to a Python project (fork, feature branch, or pull request) that uses a setup.py-based test suite, before pushing changes to the remote repository or merging into the main branch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MS2Query
  - Python
  - GitHub Actions
  - Python setuptools
  - Sonarcloud
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
- make sure the existing tests still work by running ``python setup.py test``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# python-automated-test-execution

## Summary

Execute Python test suites within continuous integration workflows to verify that code changes do not break existing functionality. This skill ensures software reliability by automating test discovery and execution on each commit or pull request.

## When to use

When contributing code changes to a Python project (fork, feature branch, or pull request) that uses a setup.py-based test suite, before pushing changes to the remote repository or merging into the main branch. Apply this skill to validate that new code or modifications do not introduce regressions in existing test cases.

## When NOT to use

- Input is a compiled binary or pre-built package—test suite must be executed from source.
- Project does not use setup.py or has no defined test suite—use language-specific test runners (pytest, unittest, tox) directly instead.
- Tests require external services or datasets not available in the CI environment—mock or skip integration tests that cannot run in CI.

## Inputs

- Python source code repository with setup.py configuration
- Test suite (pytest, unittest, or custom tests referenced in setup.py)
- Git commit or pull request containing code changes

## Outputs

- Test execution report (console output with pass/fail counts)
- Exit code (0 for all tests passing, non-zero for failures)
- GitHub Actions workflow status (optional: automated badge reflecting test outcome)

## How to apply

Run the test suite using `python setup.py test` from the repository root after making code changes. This command discovers and executes all tests defined in the project's test configuration. Verify that all tests pass (exit code 0) before proceeding with commits or pull requests. In a GitHub Actions workflow context, integrate this step into the CI pipeline by adding a job that runs the same command; the workflow will trigger automatically on push and pull request events and report test results via a status badge. If tests fail, review the error output to identify which test cases are broken and remediate the code changes accordingly. The test execution should be repeatable and deterministic—running the same commit twice should yield the same test results.

## Related tools

- **GitHub Actions** (Orchestrates automated test execution on push and pull request events; reports CI status and generates status badge) — https://github.com/iomega/ms2query/actions/workflows/CI_build.yml
- **Python setuptools** (Provides setup.py test command for discovering and running test suite)
- **Sonarcloud** (Optional static analysis step integrated into CI workflow to scan code quality alongside test execution)

## Examples

```
python setup.py test
```

## Evaluation signals

- Exit code is 0 (all tests passed) after running `python setup.py test`
- GitHub Actions workflow status badge displays 'passing' and links to successful workflow run
- All test case names are listed in console output with PASSED status; no FAILED or ERROR entries
- Test count reported in output matches the expected number of test cases in the project
- Repeated execution of the same commit produces identical test results (determinism check)

## Limitations

- Tests must be self-contained and not require manual environment setup beyond conda/pip dependencies listed in setup.py; external databases or API keys are not available in standard CI environments.
- MS2Query is tested on MacOS, Windows, and Ubuntu for Python 3.9 and 3.10 only—tests may fail on other Python versions or operating systems.
- Test execution time increases with the number of tests; large test suites may exceed CI runner time limits.
- Flaky or non-deterministic tests (e.g., those depending on system clock, network I/O, or random seeds) may pass or fail intermittently despite no code changes.

## Evidence

- [methods] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [other] MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge: "MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge"
- [readme] MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10: "MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10"
- [other] Configure GitHub Actions workflow file to trigger on push and pull request events to the ms2query repository.: "Configure GitHub Actions workflow file to trigger on push and pull request events to the ms2query repository"
- [other] Define a matrix job that runs Python test suite using `python setup.py test` to verify existing tests pass.: "Define a matrix job that runs Python test suite using `python setup.py test` to verify existing tests pass"
