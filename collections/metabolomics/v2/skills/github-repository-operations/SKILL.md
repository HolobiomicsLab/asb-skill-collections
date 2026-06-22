---
name: github-repository-operations
description: Use when when you need to verify that a software package (such as MassQL) passes its periodic integration test suite as indicated by CI workflow badges in the project documentation, or when you must reproduce pass/fail results for package-testing workflows distinct from unit tests to establish.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MassQL
  - GitHub Actions
  - pytest
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

# github-repository-operations

## Summary

Execute and validate automated CI/CD workflows (e.g., unit tests, integration tests, package-level tests) defined in GitHub Actions to verify software reliability and reproducibility. This skill is essential for confirming that a repository's test suite passes consistently and generating structured reports of test outcomes.

## When to use

When you need to verify that a software package (such as MassQL) passes its periodic integration test suite as indicated by CI workflow badges in the project documentation, or when you must reproduce pass/fail results for package-testing workflows distinct from unit tests to establish confidence in a tool's stability.

## When NOT to use

- The CI workflow definition file does not exist or is not accessible in the repository.
- Test fixtures cannot be obtained (e.g., get_data.sh is unavailable or broken) and the workflow cannot proceed without them.
- The goal is to modify the CI workflow itself rather than to execute it and collect results.

## Inputs

- GitHub repository URL (e.g., mwang87/MassQueryLanguage)
- CI workflow definition file (YAML, e.g., test-package.yml)
- Test fixture data (if required and not bundled in repo)
- Python environment with test dependencies (requirements_test.txt or equivalent)

## Outputs

- Pass/fail test results (structured JSON or CSV report)
- Individual test case outcomes with execution times and error logs
- Overall test suite status summary
- CI workflow badge status (pass/fail indicator)

## How to apply

Clone the target GitHub repository, then locate and inspect the CI workflow definition file (e.g., test-package.yml for package-level integration tests or test-unit.yml for unit tests). Parse the workflow to identify test targets, success criteria, and required fixtures or dependencies. Set up the test environment according to the workflow specification (e.g., install test requirements via pip install -r requirements_test.txt, fetch test data fixtures via shell scripts). Execute the test runner invoked by the workflow (pytest, unittest, or GitHub Actions runner environment), collect structured results including pass/fail status, execution time, and error logs for each test case, and generate a structured report (JSON or CSV format) documenting overall test suite status and individual test outcomes.

## Related tools

- **GitHub Actions** (CI/CD platform that defines and executes test workflows (test-package.yml, test-unit.yml) on repository commits) — https://github.com/mwang87/MassQueryLanguage
- **pytest** (Python test runner used to execute unit and integration tests specified in the workflow)
- **MassQL** (The target software package being tested; its Python API and command-line tool are validated by the CI workflows) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
cd /path/to/MassQueryLanguage && cd tests && sh ./get_data.sh && pip install -r ../requirements_test.txt && pytest -v
```

## Evaluation signals

- All test cases in the workflow complete execution with documented pass/fail status (no hanging or timeout failures).
- Pass/fail results match the CI badge status displayed in the repository README.
- Structured output file (JSON or CSV) contains non-empty test records with scan IDs, timestamps, and error messages for failed tests.
- Test fixtures are successfully fetched and available before test execution begins (verify get_data.sh completion).
- Error logs for failed tests include actionable diagnostic information (stack traces, assertion messages) enabling root-cause analysis.

## Limitations

- Test fixtures may not be bundled with the git repository and must be downloaded via shell script (get_data.sh); network failures or broken links will halt execution.
- The Python environment must match the version constraints specified in the workflow (e.g., MassQL is tested on Python 3.9 and 'are figuring out other versions if they work or not').
- The test suite requires additional dependencies (requirements_test.txt) that may conflict with the primary package dependencies or have external system requirements.
- CI workflow definitions are repository-specific; the execution method and success criteria vary across projects and may require manual inspection of the .yml file to identify test targets.

## Evidence

- [other] Does the MassQL package pass its periodic integration test suite as indicated by the test-package.yml CI workflow?: "Does the MassQL package pass its periodic integration test suite as indicated by the test-package.yml CI workflow?"
- [other] The MassQL repository includes a periodic package-testing CI workflow (test-package.yml) distinct from unit tests, as indicated by the badge link in the project documentation.: "The MassQL repository includes a periodic package-testing CI workflow (test-package.yml) distinct from unit tests, as indicated by the badge link in the project documentation."
- [other] Inspect and parse the test-package.yml CI workflow definition to identify integration test targets and success criteria. Execute the package-level integration tests specified in test-package.yml using the appropriate test runner: "Inspect and parse the test-package.yml CI workflow definition to identify integration test targets and success criteria. Execute the package-level integration tests specified in test-package.yml"
- [readme] To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: cd tests && sh ./get_data.sh: "To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: cd tests && sh ./get_data.sh"
- [readme] You will also want to install the extra requirements for the test suite: pip install -r requirements_test.txt: "You will also want to install the extra requirements for the test suite: pip install -r requirements_test.txt"
