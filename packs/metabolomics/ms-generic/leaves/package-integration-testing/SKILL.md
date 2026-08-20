---
name: package-integration-testing
description: Use when you need to verify that a Python package (or similar installable software) passes its declared integration test suite as a prerequisite to trusting its reliability in production or downstream analysis. Specifically, apply it when you observe a periodic testing CI workflow badge (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3960
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MassQL
  - pytest
  - GitHub Actions
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1038/s41592-025-02785-1
  title: MassQL
evidence_spans:
- The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massql
    doi: 10.1038/s41592-025-02785-1
    title: MassQL
  dedup_kept_from: coll_massql
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02785-1
  all_source_dois:
  - 10.1038/s41592-025-02785-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# package-integration-testing

## Summary

Execute and reproduce a software package's periodic integration test suite to verify end-to-end functionality beyond unit tests. This skill validates that the packaged tool works correctly across its full workflow and dependencies in a realistic deployment environment.

## When to use

Use this skill when you need to verify that a Python package (or similar installable software) passes its declared integration test suite as a prerequisite to trusting its reliability in production or downstream analysis. Specifically, apply it when you observe a periodic testing CI workflow badge (e.g., test-package.yml) in project documentation but have not yet confirmed the current pass/fail status, or when reproducing published results that depend on the package.

## When NOT to use

- The package has only unit tests and no separate periodic integration test workflow is defined or documented.
- You only need to validate unit test coverage, not end-to-end package functionality.
- The package is not installable via standard package managers (pip, conda) or has no declared test suite.

## Inputs

- GitHub repository URL (mwang87/MassQueryLanguage or equivalent)
- CI workflow definition file (test-package.yml or equivalent YAML)
- Test fixtures and data (downloaded via helper scripts if not bundled)
- Test requirements file (requirements_test.txt)
- Package source code and setup configuration (setup.py, pyproject.toml)

## Outputs

- Structured test results (JSON or CSV format)
- Pass/fail status for each test case
- Test execution logs and error messages
- Overall integration test suite status report
- Execution time and resource usage metrics

## How to apply

Clone the source repository and inspect the CI workflow definition (e.g., test-package.yml) to identify integration test targets, success criteria, and test runner configuration. Install the package and any test dependencies specified in requirements files (e.g., requirements_test.txt). Execute the test suite using the declared test runner (typically pytest or GitHub Actions environment) and collect structured results including pass/fail status, execution time, and error logs for each test case. Generate a structured report (JSON or CSV) that documents overall suite status and individual test outcomes. Verify that all test cases pass and that execution time and resource usage are within acceptable ranges for the deployment context.

## Related tools

- **MassQL** (Package under test; provides Python API (msql_engine.process_query) and command-line interface (massql CLI) that integration tests validate) — https://github.com/mwang87/MassQueryLanguage
- **pytest** (Test runner for executing integration test suite and collecting results)
- **GitHub Actions** (CI/CD platform that executes the test-package.yml workflow and reports pass/fail status via badge)

## Examples

```
cd tests && sh ./get_data.sh && pip install -r requirements_test.txt && pytest
```

## Evaluation signals

- All test cases in the integration test suite report PASS status with no FAIL or ERROR outcomes.
- Test execution completes without exceptions or unhandled errors in logs.
- Structured report file is generated with valid JSON or CSV schema containing scan-level and suite-level results.
- Execution time for the full integration test suite falls within historical or documented acceptable range (e.g., under 30 minutes).
- CI workflow badge (test-package.yml) on repository README displays a passing status after test execution.

## Limitations

- Integration tests may depend on external data or network resources (e.g., mass spectrometry data fixtures) that must be downloaded separately via helper scripts (get_data.sh); network failures or data unavailability will cause tests to skip or fail.
- Test results are specific to the Python version and dependencies specified in the test environment (e.g., 'We currently test massql in python 3.9'); results may differ if run on untested Python versions or with conflicting dependency versions.
- Integration tests validate the package API and CLI but do not necessarily cover all possible user workflows, edge cases, or performance at scale; passing tests do not guarantee correctness for all downstream use cases.
- No changelog is publicly available in the repository, making it difficult to correlate test results with specific bug fixes or feature changes between versions.

## Evidence

- [other] The MassQL repository includes a periodic package-testing CI workflow (test-package.yml) distinct from unit tests: "periodic package-testing CI workflow (test-package.yml) distinct from unit tests, as indicated by the badge link in the project documentation"
- [other] Execute the package-level integration tests using the appropriate test runner: "Execute the package-level integration tests specified in test-package.yml using the appropriate test runner (e.g., pytest or GitHub Actions runner environment)"
- [other] Collect structured test results including pass/fail status and error logs: "Collect structured test results including pass/fail status for each test case, execution time, and error logs"
- [readme] Test fixtures must be fetched before running the test suite: "To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: cd tests && sh ./get_data.sh"
- [readme] MassQL is tested in Python 3.9 with additional test requirements: "We currently test massql in python 3.9, but are figuring out other versions if they work or not. You will also want to install the extra requirements for the test suite: pip install -r"
- [readme] Periodic testing badge indicates package-level integration test status: "[![Periodic Testing of Package](https://github.com/mwang87/MassQueryLanguage/actions/workflows/test-package.yml/badge.svg)]"
