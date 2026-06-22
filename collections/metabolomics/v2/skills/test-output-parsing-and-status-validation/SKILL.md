---
name: test-output-parsing-and-status-validation
description: Use when you need to verify whether a GitHub Actions workflow badge (e.g., main.yml) accurately reports the CI pipeline's true pass/fail status.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - git
  - RDKit
  - GitHub Actions
derived_from:
- doi: 10.1021/acs.analchem.5c00633
  title: metid
evidence_spans:
- Clone the Met-ID repository
- Powered by RDKit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00633
  all_source_dois:
  - 10.1021/acs.analchem.5c00633
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# test-output-parsing-and-status-validation

## Summary

Parse CI/CD workflow test output logs and validate that the final exit status matches the reported badge status, confirming reproducibility of automated checks. This skill is essential when verifying that a repository's public CI badge accurately reflects the true state of the automated test pipeline.

## When to use

Apply this skill when you need to verify whether a GitHub Actions workflow badge (e.g., main.yml) accurately reports the CI pipeline's true pass/fail status. Use it when reproducing a repository locally or auditing CI/CD integrity—particularly when the badge-reported status differs from observed test failures or when you need to trace root causes of build failures.

## When NOT to use

- The workflow badge is already documented as deprecated or under maintenance—defer to maintainer communication.
- The repository uses a CI system other than GitHub Actions (e.g., Travis CI, CircleCI)—adapt the log parsing and status check to that platform's output format.
- You lack read access to the .github/workflows/ directory or GitHub Actions logs—validation cannot proceed without viewing the workflow definition.

## Inputs

- GitHub repository URL (pbjarterot/Met-ID or equivalent)
- Workflow definition file (.github/workflows/main.yml)
- CI environment specifications (dependencies, Python/Rust/Node versions)
- Local test environment or GitHub Actions API credentials

## Outputs

- Parsed test result summary (pass count, fail count, error details)
- Final CI exit status code (integer)
- Validation report comparing parsed status to badge-reported status
- Error logs and failure stack traces (if applicable)
- Boolean flag indicating badge accuracy

## How to apply

Clone the target repository and inspect the .github/workflows/ configuration file (e.g., main.yml) to identify the CI steps, environment setup, and test commands. Execute the same test suite and dependency installation steps locally or trigger the workflow via GitHub Actions API and monitor its completion. Capture all test output and final exit codes. Parse the output logs to extract test results (pass/fail counts, error messages, assertion failures) and the final exit status code. Compare the parsed exit status against the badge-reported status to validate consistency. Document any discrepancies in exit codes, test counts, or error logs that indicate the badge may be stale or inaccurate.

## Related tools

- **GitHub Actions** (CI/CD platform that executes the workflow, logs test output, and reports final status; use API or web UI to monitor and retrieve test logs) — https://github.com/pbjarterot/Met-ID/actions
- **git** (Clone the repository locally to access .github/workflows/ configuration and prepare the environment for local test execution)
- **RDKit** (Dependency used by Met-ID; ensure correct version is installed during test environment setup, as version mismatches can cause CI failures) — https://www.rdkit.org/

## Examples

```
git clone https://github.com/pbjarterot/Met-ID.git && cd Met-ID && cat .github/workflows/main.yml && cargo test --release 2>&1 | tee test_output.log && grep -E '(test result:|failures:|PASSED|FAILED)' test_output.log
```

## Evaluation signals

- Exit status code from test suite execution is 0 (success) or non-zero (failure), and matches the badge-reported state (passing/failing).
- Test output log contains explicit summary lines (e.g., 'X tests passed, Y tests failed') that can be parsed and validated against expected counts.
- No stale or cached workflow artifacts are present; re-running the workflow produces identical exit codes and error messages.
- Comparison of local test results with GitHub Actions API-reported results shows no discrepancy in exit codes or test counts.
- All documented dependencies (RDKit version, Python version, Rust toolchain) are correctly installed and match the workflow specification.

## Limitations

- Met-ID is under active development; database files may not update automatically when reinstalling newer versions, requiring manual removal from the platform-specific AppData/Library/config folder before re-running CI tests.
- GitHub Actions job logs are ephemeral; retention policies may delete logs older than 90 days, making historical validation of past workflow runs unavailable.
- Local test environment may differ from GitHub Actions runner environment (OS, installed packages, hardware), potentially producing different exit codes or test failures not seen in CI.
- Parsing test output is format-dependent; changes to the test runner's output format (e.g., switching from pytest to a different test framework) require updating log parsing logic.

## Evidence

- [other] Does the Met-ID GitHub repository's CI workflow (main.yml) execute successfully and pass all automated checks as indicated by the badge?: "Does the Met-ID GitHub repository's CI workflow (main.yml) execute successfully and pass all automated checks as indicated by the badge?"
- [other] Inspect the main.yml workflow file in .github/workflows/ to identify the CI steps, environment setup, and test commands.: "Inspect the main.yml workflow file in .github/workflows/ to identify the CI steps, environment setup, and test commands."
- [other] Execute the workflow locally by running the same test suite and dependency installation steps that the CI pipeline defines, or trigger the workflow via GitHub Actions API and monitor its completion.: "Execute the workflow locally by running the same test suite and dependency installation steps that the CI pipeline defines, or trigger the workflow via GitHub Actions API and monitor its completion."
- [other] Capture the final pass/fail exit status and any error logs or test output.: "Capture the final pass/fail exit status and any error logs or test output."
- [readme] ![example workflow](https://github.com/pbjarterot/Met-ID/actions/workflows/main.yml/badge.svg): "![example workflow](https://github.com/pbjarterot/Met-ID/actions/workflows/main.yml/badge.svg)"
- [readme] For some reason, reinstalling newer versions of Met-ID does not update the database files it comes bundled with: "For some reason, reinstalling newer versions of Met-ID does not update the database files it comes bundled with"
