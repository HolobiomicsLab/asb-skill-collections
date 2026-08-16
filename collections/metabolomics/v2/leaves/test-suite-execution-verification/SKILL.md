---
name: test-suite-execution-verification
description: Use when when you have cloned or obtained a Python package repository
  and need to confirm that the codebase's tests pass before integration, contribution,
  or deployment. Particularly relevant when the repository advertises a Tests badge
  linked to a CI/CD workflow (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_0605
  tools:
  - pip
  - pytest
  - GitHub Actions
  license_tier: open
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- pip install -e .[dev]
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

# test-suite-execution-verification

## Summary

Execute a Python package's bundled test suite using pytest to verify functional correctness and reproducibility of the implementation. This skill validates that all unit and integration tests pass after development installation, confirming the package meets its own quality gates.

## When to use

When you have cloned or obtained a Python package repository and need to confirm that the codebase's tests pass before integration, contribution, or deployment. Particularly relevant when the repository advertises a Tests badge linked to a CI/CD workflow (e.g., GitHub Actions), indicating a maintained test suite that serves as the source of truth for package health.

## When NOT to use

- The package does not ship with a tests/ directory or test suite.
- You are running tests in a production environment where side effects (e.g., file I/O, network calls) are undesirable.
- The package's CI workflow is known to be broken or disabled, and local test failure is expected.

## Inputs

- Python package repository (cloned or obtained)
- pyproject.toml or setup.py with dev extras defined
- tests/ directory containing pytest-discoverable test modules

## Outputs

- pytest test report (console output or JUnit XML)
- Pass/fail status for each test
- Exit code (0 for all pass, >0 for failures)

## How to apply

First, install the package in editable/development mode using pip with any dev extras (e.g., `pip install -e .[dev]`), which ensures test dependencies are available. Then execute the full test suite by running `pytest tests/` from the repository root, which will discover and run all test modules. Inspect the pytest output to verify that all tests pass (exit code 0) and that no failures, errors, or skipped tests indicate regressions. If the repository uses a CI workflow badge, cross-check the local test results against the badge status to ensure parity; discrepancies may indicate environment or dependency version mismatches.

## Related tools

- **pytest** (Test discovery and execution framework; runs all test modules in tests/ directory and reports pass/fail status) — https://docs.pytest.org
- **pip** (Package installer; installs the package in editable mode with dev dependencies to enable test execution) — https://pip.pypa.io
- **GitHub Actions** (CI/CD workflow engine; maintains the Tests badge and workflow file (test-biosynfoni.yml) that defines the reference test execution) — https://github.com/lucinamay/biosynfoni/actions/workflows/test-biosynfoni.yml

## Examples

```
pip install -e .[dev] && pytest tests/
```

## Evaluation signals

- pytest exit code is 0, indicating all tests passed without failures or errors.
- All test modules in tests/ are discovered and executed (pytest summary line shows test count > 0).
- No test output contains FAILED, ERROR, or SKIPPED markers for critical tests.
- Local test results align with the status of the repository's Tests badge in its README.
- Test execution completes without unhandled exceptions or import errors in the package under test.

## Limitations

- Test suite execution depends on correct installation of all dev dependencies; missing or incompatible versions will cause test failures unrelated to code correctness.
- Local environment (Python version, OS, installed libraries) may differ from the CI environment, leading to false negatives or false positives.
- Tests may depend on external resources (network, databases) not available in all environments; network tests may be skipped or fail in isolated networks.
- Test suite completeness is not guaranteed; passing tests do not prove absence of bugs, only that bundled tests pass.

## Evidence

- [other] Does the biosynfoni package pass its bundled test suite when installed and executed with pytest?: "Does the biosynfoni package pass its bundled test suite when installed and executed with pytest?"
- [other] Install the package in editable/development mode using pip with the dev extras (pip install -e .[dev]). Run the full test suite using pytest on the tests/ directory (pytest tests/).: "Install the package in editable/development mode using pip with the dev extras (pip install -e .[dev]). Run the full test suite using pytest on the tests/ directory (pytest tests/)."
- [other] The biosynfoni repository displays a Tests badge linked to a GitHub Actions workflow (test-biosynfoni.yml) that validates the package's test suite status.: "The biosynfoni repository displays a Tests badge linked to a GitHub Actions workflow (test-biosynfoni.yml) that validates the package's test suite status."
- [readme] You can also run the tests locally with the following command: pytest tests/: "You can also run the tests locally with the following command: pytest tests/"
- [readme] Run the following command from the root of the project to install the project for development: "Run the following command from the root of the project to install the project for development"
