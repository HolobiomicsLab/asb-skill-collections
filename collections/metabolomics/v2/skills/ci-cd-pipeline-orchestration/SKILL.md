---
name: ci-cd-pipeline-orchestration
description: Use when you need to automate testing and quality checks on code changes—specifically when pull requests or commits are made to a repository and you want to verify that builds succeed, test suites pass, and code quality metrics meet project standards before merging.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MS2Query
  - GitHub Actions
  - Sonarcloud
  - Python setuptools
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
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

# CI/CD Pipeline Orchestration

## Summary

Design and deploy automated continuous integration and continuous deployment (CI/CD) pipelines using GitHub Actions to orchestrate build, test, and static analysis workflows. This skill ensures code quality and deployment reliability by integrating multiple validation stages into a single triggerable workflow.

## When to use

Apply this skill when you need to automate testing and quality checks on code changes—specifically when pull requests or commits are made to a repository and you want to verify that builds succeed, test suites pass, and code quality metrics meet project standards before merging.

## When NOT to use

- The repository has no automated tests or you are unwilling to maintain test coverage as code evolves.
- Your project does not use GitHub or GitHub Actions (different CI/CD platform required).
- Static analysis or build validation is not a project requirement or organizational standard.

## Inputs

- GitHub repository with source code
- GitHub Actions workflow configuration file (YAML)
- Python test suite or equivalent build/test command
- Static analysis tool credentials (e.g., Sonarcloud token)
- Pull requests or commits to trigger the workflow

## Outputs

- GitHub Workflow Status badge (reflecting combined build, test, and analysis outcome)
- Sonarcloud quality report (code coverage, technical debt, quality gate status)
- Test execution logs and pass/fail summary
- CI status visible in pull request checks
- Automated quality metrics documented in workflow run artifacts

## How to apply

Create a GitHub Actions workflow file (e.g., CI_build.yml) that triggers on push and pull request events. Define a matrix job to execute the test suite (e.g., `python setup.py test` for Python projects) to verify existing tests pass. Integrate a static analysis step (e.g., Sonarcloud) to scan code quality and security metrics. Execute the workflow on a test commit or pull request to validate job execution. Monitor and document the generated quality report output (code coverage, technical debt, quality gate status) and link the workflow status badge to your README to communicate CI health. Use the combined outcome of build, test, and static analysis checks to determine whether the pull request meets the project's quality bar.

## Related tools

- **GitHub Actions** (Orchestrates workflow execution on push/pull request events, defines job matrix for test parallelization, manages build and test step execution) — https://github.com/iomega/ms2query
- **Sonarcloud** (Performs static code analysis to scan quality metrics, security issues, and code coverage; produces quality gate pass/fail status integrated into CI workflow)
- **Python setuptools** (Executes test suite via `python setup.py test` command within CI workflow to validate existing tests pass)

## Examples

```
# In your GitHub repository, create .github/workflows/CI_build.yml with:
on:
  push:
    branches: [master]
  pull_request:
strategy:
  matrix:
    python-version: [3.9, 3.10]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: python setup.py test
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
```

## Evaluation signals

- GitHub Workflow Status badge displays green (passing) after successful execution of build, test, and static analysis stages.
- Sonarcloud quality gates pass and report shows code coverage, technical debt, and security metrics within acceptable ranges.
- All test cases in the test suite execute without failure when triggered by pull request or commit.
- Pull request checks clearly show CI status before merge, blocking merge if any workflow stage fails.
- Workflow run logs contain clear evidence of job execution steps, test output, and static analysis report generation without errors.

## Limitations

- MS2Query test suite is limited to Python 3.9 and 3.10; workflow validation depends on testing only these versions.
- Static analysis via Sonarcloud requires valid credentials and network access; workflow will fail if service is unavailable or credentials are misconfigured.
- CI workflow does not perform peak picking or clustering of MS2 spectra; preprocessing (e.g., via MZMine) must be handled separately before or after CI validation.
- Matrix job testing is platform-specific (MacOS, Windows, Ubuntu); cross-platform validation requires explicit matrix configuration in workflow.

## Evidence

- [other] Configure GitHub Actions workflow file to trigger on push and pull request events to the ms2query repository.: "Configure GitHub Actions workflow file to trigger on push and pull request events to the ms2query repository."
- [other] Define a matrix job that runs Python test suite using `python setup.py test` to verify existing tests pass.: "Define a matrix job that runs Python test suite using `python setup.py test` to verify existing tests pass."
- [other] Integrate Sonarcloud static analysis step into the workflow to scan code quality and security metrics.: "Integrate Sonarcloud static analysis step into the workflow to scan code quality and security metrics."
- [other] MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge that reflects the combined outcome of build, test, and static analysis checks.: "MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge that reflects the combined outcome of"
- [readme] MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10: "MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10"
- [readme] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
