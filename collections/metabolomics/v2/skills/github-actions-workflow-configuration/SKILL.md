---
name: github-actions-workflow-configuration
description: Use when when you have a Python package repository on GitHub and need to automatically verify that pull requests and commits pass unit tests and meet code quality standards before merge.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  tools:
  - MS2Query
  - GitHub
  - GitHub Actions
  - Sonarcloud
  - Python
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
- use the search functionality [here](https://github.com/iomega/ms2query/issues)
- fork the repository to your own Github profile and create your own feature branch off of the latest master commit
- A GitHub action will run which will publish the new version to [pypi](https://pypi.org/project/ms2query/)
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
---

# GitHub Actions Workflow Configuration

## Summary

Configure and validate a GitHub Actions continuous integration (CI) workflow that automates build, test, and static code analysis on pull requests and commits. This skill integrates Python test execution with Sonarcloud quality gates to produce automated quality reports and CI status badges.

## When to use

When you have a Python package repository on GitHub and need to automatically verify that pull requests and commits pass unit tests and meet code quality standards before merge. Specifically useful when you want to combine test execution with static analysis metrics (code coverage, technical debt, security flags) in a single automated workflow.

## When NOT to use

- Repository is not on GitHub or does not use GitHub Actions as CI platform
- Python package does not have an existing test suite or test runner configured
- Project does not have or cannot obtain Sonarcloud integration (e.g., private/closed-source restrictions)

## Inputs

- Python package with test suite (setup.py with test target)
- GitHub repository with write access
- Sonarcloud organization token and project credentials

## Outputs

- GitHub Actions workflow file (CI_build.yml)
- GitHub Workflow Status badge
- Sonarcloud quality report (code coverage, technical debt, quality gates status)

## How to apply

Create a GitHub Actions workflow file (e.g., CI_build.yml) that triggers on push and pull_request events. Define a matrix job that runs the project's Python test suite using `python setup.py test` to verify existing tests pass. Integrate a Sonarcloud analysis step into the workflow to scan code quality and security metrics on the same event. Execute the workflow on a test commit or pull request to validate job execution. Retrieve the Sonarcloud quality report output, which will show code coverage, technical debt metrics, and quality gate pass/fail status. The workflow will automatically generate and display a GitHub Workflow Status badge reflecting the combined outcome of build, test, and static analysis checks.

## Related tools

- **GitHub Actions** (Workflow automation platform that executes CI jobs on trigger events (push, pull_request)) — https://github.com/iomega/ms2query
- **Sonarcloud** (Static code analysis service that scans code quality, security vulnerabilities, coverage, and enforces quality gates)
- **Python** (Test suite execution via setup.py test command to validate unit tests before merge)
- **MS2Query** (Example project demonstrating CI workflow integration with GitHub Actions and Sonarcloud) — https://github.com/iomega/ms2query

## Examples

```
ms2query --help
# Or in a GitHub Actions workflow step:
- name: Run tests
  run: python setup.py test
```

## Evaluation signals

- Workflow file (CI_build.yml) exists in .github/workflows/ and syntax is valid YAML
- Workflow triggers successfully on pull request and push events to the repository
- Python test suite completes without errors and reports pass/fail status in workflow logs
- Sonarcloud analysis step executes and produces a quality report with code coverage and debt metrics visible in GitHub PR checks
- GitHub Workflow Status badge appears in README and reflects current CI state (pass/fail/pending)

## Limitations

- Sonarcloud free tier has limits on analysis frequency and may not support all project sizes; large repositories may require paid plan
- Workflow execution time depends on test suite complexity; large test suites may extend CI feedback loop and increase GitHub Actions usage costs
- Quality gate thresholds and metrics are configurable in Sonarcloud but must be validated against project requirements; default gates may be too strict or lenient
- Requires Sonarcloud account and token setup; misconfigured credentials will cause analysis step to fail silently or fail loudly without clear error messaging

## Evidence

- [other] MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge that reflects the combined outcome of build, test, and static analysis checks.: "MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge"
- [other] Configure GitHub Actions workflow file to trigger on push and pull request events to the ms2query repository. Define a matrix job that runs Python test suite using `python setup.py test` to verify existing tests pass. Integrate Sonarcloud static analysis step into the workflow to scan code quality and security metrics.: "Configure GitHub Actions workflow file to trigger on push and pull request events to the ms2query repository. Define a matrix job that runs Python test suite using `python setup.py test` to verify"
- [other] Execute the complete workflow on a test commit or pull request to validate job execution and generate CI status badge. Retrieve and document the Sonarcloud quality report output showing code coverage, technical debt, and quality gates status.: "Execute the complete workflow on a test commit or pull request to validate job execution and generate CI status badge. Retrieve and document the Sonarcloud quality report output showing code"
- [readme] [![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/iomega/ms2query/CI_build.yml)](https://github.com/iomega/ms2query/actions/workflows/CI_build.yml): "[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/iomega/ms2query/CI_build.yml)]"
- [methods] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
