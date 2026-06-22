---
name: ci-status-badge-deployment
description: Use when you have configured a GitHub Actions workflow that executes build, test, and quality checks, and you want to embed a machine-readable, auto-updating badge in your repository README to signal pipeline status at a glance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - MS2Query
  - GitHub Actions
  - Sonarcloud
  - shields.io
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

# CI Status Badge Deployment

## Summary

Generate and deploy a GitHub Workflow Status badge that reflects the combined outcome of automated build, test, and static analysis checks in a continuous integration pipeline. This skill visually communicates pipeline health to repository users and contributors.

## When to use

Apply this skill when you have configured a GitHub Actions workflow that executes build, test, and quality checks, and you want to embed a machine-readable, auto-updating badge in your repository README to signal pipeline status at a glance. Use it after Sonarcloud or other CI quality gates are integrated into your workflow file.

## When NOT to use

- Workflow file does not yet exist or has not been committed to the repository—badge will show an error state until the workflow is accessible.
- Repository is private and the workflow runs on private runners without public status exposure—badge may not render correctly.
- You are building a status indicator for a tool that does not use GitHub Actions (e.g., GitLab CI, Jenkins, CircleCI)—use platform-specific badge services instead.

## Inputs

- GitHub repository with GitHub Actions workflows configured
- GitHub Actions workflow file (YAML) with defined jobs and steps
- Workflow name or filename (e.g., CI_build.yml)
- Repository owner and name

## Outputs

- GitHub Workflow Status badge (shield.io SVG image)
- Badge markdown code for embedding in README
- Auto-updating CI status indicator visible in repository documentation

## How to apply

Create a GitHub Actions workflow file (e.g., CI_build.yml) that triggers on push and pull request events, define job steps for build/test execution and static analysis integration, then reference the workflow in a GitHub Workflow Status badge URL using the format `https://img.shields.io/github/actions/workflow/status/<owner>/<repo>/<workflow-filename>`. The badge will automatically update to reflect the latest workflow run status (success, failure, or in-progress). Place the badge markdown in your README to display current CI status. The badge acts as a living document that requires no manual updates—GitHub Actions automatically refreshes it based on workflow execution results.

## Related tools

- **GitHub Actions** (Orchestrates continuous integration workflow execution; workflow status is the source of truth for badge rendering) — https://github.com/features/actions
- **Sonarcloud** (Executes static code analysis and quality gates within the workflow; results feed into the overall CI status)
- **shields.io** (Generates and hosts the status badge SVG image based on GitHub Actions workflow status queries) — https://shields.io
- **MS2Query** (Example project using GitHub Actions workflow with Sonarcloud integration and CI status badge) — https://github.com/iomega/ms2query

## Examples

```
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/iomega/ms2query/CI_build.yml)](https://github.com/iomega/ms2query/actions/workflows/CI_build.yml)
```

## Evaluation signals

- Badge markdown renders without 404 or 'workflow not found' errors in the README.
- Badge SVG image updates to reflect the status of the most recent workflow run (green for success, red for failure, yellow for in-progress).
- Clicking the badge URL navigates to the GitHub Actions workflow run history page.
- Workflow file (CI_build.yml) exists in the repository and contains at least one job with a defined trigger event.
- Badge is visible in the rendered README on GitHub; status changes correlate with new workflow executions within 1–2 minutes.

## Limitations

- Badge status reflects only the latest workflow run; historical or per-branch status requires additional dashboards or custom query parameters.
- Private repositories may not expose workflow status publicly; badge will fail or show a generic error unless explicitly configured for public visibility.
- Workflow file must be committed to the default branch; badge URLs referencing workflows on feature branches may not resolve correctly.
- Sonarcloud or other quality gate failures are reflected in the badge only if the workflow is configured to fail on those checks; warnings alone will not affect the overall badge status.
- Badge URL is static and must be manually placed in README; no automatic badge generation or discovery is performed.

## Evidence

- [other] MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge that reflects the combined outcome of build, test, and static analysis checks.: "MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge that reflects the combined outcome of"
- [other] Configure GitHub Actions workflow file to trigger on push and pull request events to the ms2query repository.: "Configure GitHub Actions workflow file to trigger on push and pull request events to the ms2query repository."
- [readme] [![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/iomega/ms2query/CI_build.yml)](https://github.com/iomega/ms2query/actions/workflows/CI_build.yml): "[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/iomega/ms2query/CI_build.yml)](https://github.com/iomega/ms2query/actions/workflows/CI_build.yml)"
- [other] Integrate Sonarcloud static analysis step into the workflow to scan code quality and security metrics.: "Integrate Sonarcloud static analysis step into the workflow to scan code quality and security metrics."
- [other] Retrieve and document the Sonarcloud quality report output showing code coverage, technical debt, and quality gates status.: "Retrieve and document the Sonarcloud quality report output showing code coverage, technical debt, and quality gates status."
