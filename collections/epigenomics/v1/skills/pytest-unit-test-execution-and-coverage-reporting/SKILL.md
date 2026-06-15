---
name: pytest-unit-test-execution-and-coverage-reporting
description: Use when after implementing or modifying Python library functions (such as utility functions in cooltools.lib subpackages) to verify correctness and identify gaps in test coverage before merging changes or releasing code.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0769
  tools:
  - pytest
  - pytest-cov
  - pytest-flake8
  - flake8
  - conda
  - Python
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans:
- We use [pytest](https://docs.pytest.org/en/latest) as our unit testing framework
- We use [pytest](https://docs.pytest.org/en/latest) as our unit testing framework with the `pytest-cov` extension
- pytest-cov` extension to check code coverage and `pytest-flake8` to check code style
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

# pytest-unit-test-execution-and-coverage-reporting

## Summary

Execute unit tests on a Python package using pytest, measure code coverage with pytest-cov, and report both functional correctness and coverage metrics. This skill verifies that library functions behave as expected and identifies untested code paths.

## When to use

Apply this skill after implementing or modifying Python library functions (such as utility functions in cooltools.lib subpackages) to verify correctness and identify gaps in test coverage before merging changes or releasing code.

## When NOT to use

- Package contains no unit tests or test infrastructure—establish test files first before running pytest.
- Testing integration behavior or end-to-end workflows requiring external dependencies, data files, or services—use integration test frameworks or fixtures instead.
- Code coverage is not a project requirement or concern—pytest can still execute tests, but the -cov extension adds overhead unnecessary in purely pass/fail scenarios.

## Inputs

- Python package source code with unit tests
- pytest configuration file (pytest.ini or setup.cfg with [tool:pytest] section, optional)
- Test files following pytest naming conventions (test_*.py or *_test.py)

## Outputs

- Unit test execution report (PASSED/FAILED status per test)
- Code coverage percentage and per-file coverage metrics
- Coverage report showing line-by-line execution status

## How to apply

Navigate to the root of the repository and run `pytest` with the `pytest-cov` extension to execute all unit tests and simultaneously measure code coverage. The framework will discover and execute all test files matching standard naming conventions (test_*.py or *_test.py), report pass/fail status for each test, and generate a coverage report showing which lines and branches were executed during testing. Examine the coverage output to identify functions or code paths not yet covered by tests, and use those results to guide additional test writing before considering the test suite complete.

## Related tools

- **pytest** (Core unit testing framework that discovers, executes, and reports on test outcomes) — https://docs.pytest.org/en/latest
- **pytest-cov** (pytest extension that measures and reports code coverage during test execution) — https://pytest-cov.readthedocs.io/
- **pytest-flake8** (pytest plugin that enforces code style standards alongside unit test execution) — https://github.com/tholo/pytest-flake8
- **Python** (Language runtime in which tests and source code are written and executed)

## Examples

```
cd /path/to/cooltools && pip install -e . && pytest --cov=cooltools.lib --cov-report=term-report
```

## Evaluation signals

- All tests execute without collection errors (test discovery succeeds on all test_*.py files)
- pytest reports PASSED status for expected unit tests and FAILED status only for intentionally broken tests
- Coverage report shows ≥80% line coverage for core library functions; any uncovered lines are documented as intentional or edge cases
- No import errors or import-time failures when pytest loads test modules and the library under test
- Coverage metrics are reproducible across multiple test runs with the same source code and test suite

## Limitations

- pytest-cov measures line coverage but does not guarantee branch coverage; conditional logic may be only partially exercised.
- High code coverage (e.g., 90%+) does not guarantee functional correctness—tests must have appropriate assertions and test meaningful code paths.
- pytest-cov execution time scales with number and complexity of tests; large test suites may require parallelization or selective test runs.
- Coverage reports do not capture dynamically executed code (e.g., code loaded via importlib or eval) and may underestimate true execution in such cases.
- pytest-flake8 integration checks style but does not replace human code review for design and maintainability issues.

## Evidence

- [other] pytest as unit testing framework: "We use [pytest](https://docs.pytest.org/en/latest) as our unit testing framework"
- [other] pytest-cov for code coverage measurement: "with the `pytest-cov` extension to check code coverage"
- [other] pytest-flake8 for style enforcement: "and `pytest-flake8` to check code style"
- [other] Running pytest from repository root: "you can just `cd` to the root of your repository and run `pytest`"
- [other] Development mode installation for testing: "install in "editable" (i.e. development) mode using the `-e` option"
