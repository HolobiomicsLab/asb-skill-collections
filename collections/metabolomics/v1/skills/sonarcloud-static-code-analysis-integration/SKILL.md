---
name: sonarcloud-static-code-analysis-integration
description: Use when when you have a GitHub-hosted Python project (or other supported language) with an existing test suite and want to gate code contributions on multiple quality dimensions beyond unit tests—specifically when you need automated reporting of code coverage, technical debt, security issues, and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - MS2Query
  - GitHub Actions
  - Sonarcloud
  - Python (setup.py)
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
---

# sonarcloud-static-code-analysis-integration

## Summary

Integrate Sonarcloud static analysis into a GitHub Actions continuous integration workflow to automatically scan code quality, security metrics, and coverage on every pull request and push event. This skill ensures that quality gates are evaluated alongside build and test execution, producing automated quality reports and CI status badges.

## When to use

When you have a GitHub-hosted Python project (or other supported language) with an existing test suite and want to gate code contributions on multiple quality dimensions beyond unit tests—specifically when you need automated reporting of code coverage, technical debt, security issues, and code smells on every PR without manual review.

## When NOT to use

- Project is not hosted on GitHub or does not use GitHub Actions—Sonarcloud integration is specific to GitHub workflows.
- Test suite does not exist or cannot be reliably executed in CI—Sonarcloud complements but does not replace automated testing.
- Organization policy prohibits third-party SaaS code analysis or has air-gapped infrastructure—Sonarcloud requires outbound connectivity.

## Inputs

- GitHub repository with source code (Python or other Sonarcloud-supported language)
- Existing test suite executable via CI (e.g., setup.py with test command)
- GitHub Actions workflow configuration file (YAML)
- Sonarcloud project token or authentication credentials

## Outputs

- GitHub Actions workflow status badge (passing/failing)
- Sonarcloud quality report (CSV or JSON) with code coverage %, technical debt, quality gate status
- Pull request annotations linking to quality findings
- CI/CD execution logs showing all workflow steps (build, test, analysis)

## How to apply

Create or update a GitHub Actions workflow file (e.g., CI_build.yml) that triggers on push and pull request events to your repository. Define a job matrix that executes your existing test suite (e.g., `python setup.py test` for Python projects) to ensure backward compatibility. Add a Sonarcloud analysis step to the workflow that scans the codebase and reports metrics such as code coverage, technical debt, and quality gate status. Execute the complete workflow on a test commit or pull request to validate job execution order and confirm that the Sonarcloud quality report is generated and linked to the pull request. Document the Sonarcloud quality report output, including code coverage percentages, identified technical debt, and whether quality gates passed or failed, to establish a baseline for future contributions.

## Related tools

- **GitHub Actions** (CI/CD orchestration platform that executes workflow jobs on repository events (push, pull request)) — https://github.com/iomega/ms2query
- **Sonarcloud** (Static analysis and code quality scanning service that evaluates code coverage, security, technical debt, and quality gates)
- **Python (setup.py)** (Test execution framework used to run existing test suite in the workflow)

## Examples

```
# In .github/workflows/CI_build.yml, configure the workflow to run tests and Sonarcloud analysis:
# - name: Run tests
#   run: python setup.py test
# - name: Sonarcloud scan
#   uses: SonarSource/sonarcloud-github-action@master
#   env:
#     GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
#     SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## Evaluation signals

- GitHub Workflow Status badge displays a passing or failing state and links to the CI_build.yml workflow execution.
- Sonarcloud analysis step completes without errors and produces a quality report accessible from the pull request or repository dashboard.
- Code coverage metric is captured and reported (e.g., percentage of lines covered by tests).
- Quality gates are evaluated and reported (pass/fail) for defined thresholds (e.g., code smells, security hotspots, technical debt ratio).
- Workflow logs show all three stages (build, test, analysis) executing in sequence with expected output for each step.

## Limitations

- Sonarcloud requires a valid project token and internet connectivity; air-gapped or offline repositories cannot use this service.
- Quality gate thresholds must be explicitly configured in Sonarcloud; default gates may not align with project-specific standards.
- Analysis time and cost scale with codebase size; very large monorepos may incur higher Sonarcloud SaaS costs or longer workflow execution times.
- Static analysis cannot detect runtime issues, logic errors, or architectural problems—it complements but does not replace functional testing.

## Evidence

- [other] MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud: "MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge that reflects the combined outcome of"
- [other] Configure GitHub Actions workflow file to trigger on push and pull request events: "Configure GitHub Actions workflow file to trigger on push and pull request events to the ms2query repository."
- [other] Define a matrix job that runs Python test suite using python setup.py test: "Define a matrix job that runs Python test suite using `python setup.py test` to verify existing tests pass."
- [other] Integrate Sonarcloud static analysis step into the workflow to scan code quality and security metrics: "Integrate Sonarcloud static analysis step into the workflow to scan code quality and security metrics."
- [other] Retrieve and document the Sonarcloud quality report output showing code coverage, technical debt, and quality gates status: "Retrieve and document the Sonarcloud quality report output showing code coverage, technical debt, and quality gates status."
- [readme] GitHub Workflow Status badge reflecting combined outcome of build, test, and static analysis: "[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/iomega/ms2query/CI_build.yml)](https://github.com/iomega/ms2query/actions/workflows/CI_build.yml)"
