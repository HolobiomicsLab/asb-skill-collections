---
name: github-actions-artifact-retrieval
description: Use when you need to verify that a GitHub Actions workflow (such as a
  development build release pipeline) has completed successfully, capture its build
  artifacts (installers, portable binaries, or packages), and document the workflow
  run metadata.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  - GitHub Actions
  license_tier: open
derived_from:
- doi: 10.1038/s41587-023-01690-2
  title: mzmine3
evidence_spans:
- mzmine is an open-source software for mass spectrometry data processing
- JDK version-25-blue
- JavaFX version-24
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzmine3
    doi: 10.1038/s41587-023-01690-2
    title: mzmine3
  dedup_kept_from: coll_mzmine3
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-023-01690-2
  all_source_dois:
  - 10.1038/s41587-023-01690-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# github-actions-artifact-retrieval

## Summary

Retrieve and document build artifacts and workflow execution logs from a GitHub Actions CI/CD pipeline to verify successful completion and capture deliverables. This skill is essential when validating that automated build workflows produce expected outputs and to capture version-specific binaries for distribution or testing.

## When to use

Apply this skill when you need to verify that a GitHub Actions workflow (such as a development build release pipeline) has completed successfully, capture its build artifacts (installers, portable binaries, or packages), and document the workflow run metadata. Use it specifically when the research question asks whether a CI workflow completes without failure and produces usable build outputs.

## When NOT to use

- The GitHub Actions workflow does not exist or the repository is private and you lack access.
- You need to test the downloaded artifact itself (e.g., install and run mzmine); artifact retrieval only documents presence and links, not functional correctness.
- The workflow is manually triggered and no recent runs are available.

## Inputs

- GitHub repository URL (owner/repo format)
- GitHub Actions workflow file path (.yml filename)
- GitHub Actions run ID or 'latest' run indicator

## Outputs

- Workflow run status (pass/fail)
- Structured report file (CSV or JSON) with timestamp, status, and artifact metadata
- Build artifact links (downloadable URLs for binaries, installers, packages)
- Execution logs or error message extracts

## How to apply

Navigate to the GitHub Actions workflow page for the target repository and workflow file (e.g., https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml). Retrieve the most recent workflow run and examine its status indicator and execution logs. For each run, document the pass/fail outcome, timestamp, and any error messages in the logs. Extract and record links to build artifacts produced by the workflow (e.g., .deb installers, portable archives). Create a structured report with columns for workflow status, artifact links, timestamps, and error context. Verify successful completion by checking that the workflow badge displays 'passing' status and that artifact downloads are accessible.

## Related tools

- **GitHub Actions** (CI/CD platform hosting the workflow runs and artifact storage; provides workflow status badges and run logs) — https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml
- **mzmine** (Target software project; the dev_build_release.yml workflow builds and releases development binaries of mzmine) — https://github.com/mzmine/mzmine

## Evaluation signals

- Workflow run badge linked in README displays 'passing' status and links to the workflow page.
- Structured report file contains valid timestamp, status value (pass or fail), and non-empty artifact URL list.
- For passing runs, artifact links are accessible and point to downloadable files matching expected naming patterns (e.g., mzmine_*.deb, mzmine_*.dmg, mzmine_*.exe for multi-platform releases).
- Execution logs retrieved from the run show no Java/Gradle build errors or artifact upload failures.
- Report documents the JDK version (25) and JavaFX version (24) used in the workflow, confirming environment context.

## Limitations

- GitHub Actions workflows may fail silently or with incomplete error messages in logs; logs may not capture root causes (e.g., network issues, dependency unavailability).
- Artifact storage is time-limited; older runs' artifacts may be expired or deleted by GitHub retention policies.
- Private repositories or workflows with restricted visibility will not be accessible without authentication.
- The presence of a workflow badge and run logs does not guarantee the downloaded artifacts are functional or compatible with target operating systems; functional testing requires installation and execution.

## Evidence

- [other] Access the GitHub Actions workflow page at https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml. Retrieve the most recent workflow run status and execution logs. Document the pass/fail outcome and any build artifacts or error messages produced.: "Access the GitHub Actions workflow page at https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml. Retrieve the most recent workflow run status and execution logs. Document the"
- [other] A development build release workflow is configured and accessible at the mzmine/mzmine repository GitHub Actions, as indicated by the presence of the dev_build_release.yml workflow badge linking to the workflow runs.: "A development build release workflow is configured and accessible at the mzmine/mzmine repository GitHub Actions, as indicated by the presence of the dev_build_release.yml workflow badge linking to"
- [readme] [![Development Build Release](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml/badge.svg)](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml): "[![Development Build Release](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml/badge.svg)](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml)"
- [readme] Releases are split into stable releases and the latest development build which reflects the current state of the master branch and is meant for testing purposes. Download options include portable versions and installers for the Window, macOS, and Linux.: "Releases are split into stable releases and the latest development build which reflects the current state of the master branch and is meant for testing purposes. Download options include portable"
- [other] Record results in a structured report file with timestamp, workflow status, and artifact links.: "Record results in a structured report file with timestamp, workflow status, and artifact links."
