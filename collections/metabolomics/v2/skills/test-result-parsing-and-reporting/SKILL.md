---
name: test-result-parsing-and-reporting
description: Use when when you need to validate that a package's periodic integration test suite (distinct from unit tests) passes as expected, or when you must collect and communicate structured evidence of test outcomes across multiple test cases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - MassQL
  - pytest
  - GitHub Actions
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# test-result-parsing-and-reporting

## Summary

Parse CI workflow test execution logs and artifacts from a GitHub Actions run, then generate structured pass/fail reports (JSON or CSV) documenting overall test suite status and individual test outcomes. This skill is essential for validating package-level integration test results and communicating test health across development teams.

## When to use

When you need to validate that a package's periodic integration test suite (distinct from unit tests) passes as expected, or when you must collect and communicate structured evidence of test outcomes across multiple test cases. Apply this skill after executing a CI workflow such as test-package.yml and need to extract, normalize, and report results in a machine-readable format.

## When NOT to use

- When only unit tests (not package-level integration tests) are being validated — use simpler unit test result reporting instead.
- When the CI workflow has not yet been executed or no test logs are available — first run the workflow before attempting to parse results.
- When you only need to check the CI badge status visually rather than programmatically extract and analyze test details.

## Inputs

- GitHub Actions workflow definition file (YAML, e.g., test-package.yml)
- Workflow execution logs (text or structured format from GitHub Actions API)
- Test runner output (pytest stdout/stderr or equivalent)
- Error logs and stack traces from failed test cases

## Outputs

- Structured test results report (JSON format with test cases, statuses, durations, errors)
- Structured test results report (CSV format with one row per test case)
- Overall test suite status summary (pass count, fail count, error count, total duration)

## How to apply

Clone the repository and inspect the CI workflow definition (e.g., test-package.yml) to identify integration test targets and success criteria. Execute the package-level integration tests specified in the workflow using the appropriate test runner environment (pytest or GitHub Actions runner). Collect structured test results including pass/fail status for each test case, execution time, and error logs from the workflow output or artifact store. Parse these logs into a normalized intermediate representation (e.g., JSON objects with test name, status, duration, and error message fields). Finally, aggregate results and generate a structured report in CSV or JSON format documenting the overall test suite status (pass/fail/error counts) and individual test outcomes, enabling downstream validation and troubleshooting.

## Related tools

- **pytest** (Test runner that executes package integration tests and produces structured output logs)
- **GitHub Actions** (CI environment that runs the test-package.yml workflow and provides logs and artifact storage) — https://github.com/mwang87/MassQueryLanguage
- **MassQL** (Target package being tested; test-package.yml validates package-level integration tests distinct from unit tests) — https://github.com/mwang87/MassQueryLanguage

## Evaluation signals

- Generated report contains all test case names, pass/fail statuses, and execution times with no missing fields.
- Pass/fail counts in the aggregate summary match the count of individual test records in the detailed report.
- Error messages for failed test cases are non-empty and traceable to the original test runner output.
- Report schema is consistent across all test records (e.g., all timestamps in ISO 8601 format, all durations in milliseconds).
- Overall test suite status (pass, fail, or error) matches the logical aggregation of individual test outcomes (e.g., suite fails if any test fails).

## Limitations

- Requires access to CI workflow logs, which may be restricted by repository permissions or GitHub Actions API rate limits.
- Test result parsing depends on consistent log format from the test runner; variations in pytest output format or custom log formatters may break parsing.
- Does not capture flaky or intermittent test failures unless the workflow is re-executed multiple times and results are aggregated across runs.
- Error messages in logs may be truncated or obfuscated if the test runner output exceeds log storage limits.
- Integration test results are specific to the CI environment and may not reproduce identically in local development environments due to differences in dependencies, Python versions, or fixture availability (as noted in the README: 'We currently test massql in python 3.9, but are figuring out other versions if they work or not').

## Evidence

- [other] The MassQL repository includes a periodic package-testing CI workflow (test-package.yml) distinct from unit tests: "The MassQL repository includes a periodic package-testing CI workflow (test-package.yml) distinct from unit tests, as indicated by the badge link in the project documentation."
- [other] Execute the package-level integration tests and collect structured results: "Execute the package-level integration tests specified in test-package.yml using the appropriate test runner (e.g., pytest or GitHub Actions runner environment). 4. Collect structured test results"
- [other] Generate a structured report documenting test outcomes: "Generate a structured pass/fail report (JSON or CSV format) documenting overall test suite status and individual test outcomes."
- [readme] Python version testing and fixture management: "We currently test massql in python 3.9, but are figuring out other versions if they work or not."
- [readme] Test setup requires fetching fixtures and extra dependencies: "To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: `cd tests && sh ./get_data.sh`. You will also want to install the extra requirements for the test suite:"
