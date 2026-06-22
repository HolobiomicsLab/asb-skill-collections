---
name: ci-cd-pipeline-monitoring
description: Use when you need to verify that a GitHub Actions workflow (such as a Build and Publish pipeline) executes successfully on a specific branch (e.g., release branch) and produces a passing build status.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - GitHub Actions
  - distribute.yaml
  - SIRIUS
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
---

# CI/CD Pipeline Monitoring

## Summary

Monitor and verify the execution status of continuous integration/continuous deployment (CI/CD) workflows in GitHub Actions, particularly for build and publish pipelines, to ensure successful builds and artifact publication. This skill is essential for validating that automated build processes complete without failures and produce passing status indicators.

## When to use

Apply this skill when you need to verify that a GitHub Actions workflow (such as a Build and Publish pipeline) executes successfully on a specific branch (e.g., release branch) and produces a passing build status. Use it when establishing confidence in automated build reproducibility, validating release readiness, or troubleshooting workflow failures in a repository's continuous deployment process.

## When NOT to use

- When you only need to inspect workflow configuration syntax without executing the pipeline; use static YAML linting instead.
- When monitoring local builds or non-GitHub CI systems; this skill is specific to GitHub Actions.
- When the workflow is already known to be broken and you are designing fixes rather than validating current status.

## Inputs

- GitHub repository URL (sirius-ms/sirius)
- Workflow configuration file (distribute.yaml)
- Target branch name (e.g., release-4-pre)
- Trigger event (release tag creation or push event)

## Outputs

- Workflow run status (passed/failed)
- GitHub Actions run logs and execution trace
- Status badge URL and display state
- Build artifact availability confirmation

## How to apply

Navigate to the target repository on GitHub and locate the release or target branch. Examine the workflow configuration file (e.g., distribute.yaml) in the .github/workflows directory to understand the pipeline's triggers and build steps. Trigger the workflow by creating a release tag or pushing code to the monitored branch, depending on the workflow's configured event triggers. Monitor the GitHub Actions run tab in real-time, reviewing logs for any failures, warnings, or unexpected behavior. Verify that the final workflow run status displays 'passed' or 'success'. Confirm that the repository's README includes a status badge (generated from the workflow) displaying the passing status with green coloring, which serves as a public indicator of build health.

## Related tools

- **GitHub Actions** (CI/CD execution environment where workflows are defined, triggered, and monitored; provides real-time logs and run status tracking.) — https://github.com/sirius-ms/sirius
- **distribute.yaml** (Workflow definition file that specifies build, test, and publish steps; configures triggers and job dependencies.) — https://github.com/sirius-ms/sirius/blob/release-4-pre/.github/workflows/distribute.yaml
- **SIRIUS** (The Java-based software framework being built and published by the CI/CD pipeline.) — https://github.com/sirius-ms/sirius

## Evaluation signals

- Workflow run status in the GitHub Actions tab displays 'passed' or 'success' (not 'failed' or 'cancelled').
- Status badge in the repository README renders with green coloring and 'passing' or 'success' label, matching the badge URL parameter (e.g., branch=release-4-pre).
- Build logs contain no ERROR or FATAL level messages; warnings may be present but do not block job completion.
- Expected build artifacts (e.g., compiled binaries, release packages) are available or indexed after successful workflow completion.
- Workflow execution time is within expected range and no timeout errors occur during job stages.

## Limitations

- GitHub Actions status badge reflects the most recent workflow run; historical failures may not be visible in the badge unless the workflow is re-triggered.
- Workflow logs are retained by GitHub for 90 days; older runs may not be available for inspection.
- Status badge caching in external documentation (e.g., README snapshots) may lag behind actual workflow status by minutes.
- Private repositories or workflows with restricted access may not display readable status badges or logs to all users.

## Evidence

- [other] Examine the distribute.yaml workflow file in the .github/workflows directory to understand the build and publish pipeline.: "Examine the distribute.yaml workflow file in the .github/workflows directory to understand the build and publish pipeline."
- [other] Trigger the 'Build and Publish' workflow by creating a release tag or pushing to the release branch, depending on the workflow trigger conditions specified in distribute.yaml.: "Trigger the 'Build and Publish' workflow by creating a release tag or pushing to the release branch, depending on the workflow trigger conditions specified in distribute.yaml."
- [other] Monitor the GitHub Actions run until completion, tracking logs for any failures or warnings.: "Monitor the GitHub Actions run until completion, tracking logs for any failures or warnings."
- [other] Verify that the workflow run status shows 'passed' in the Actions tab.: "Verify that the workflow run status shows 'passed' in the Actions tab."
- [other] Inspect the repository README to confirm the build badge displays a passing status (typically indicated by 'passing' or 'success' label and green coloring).: "Inspect the repository README to confirm the build badge displays a passing status (typically indicated by 'passing' or 'success' label and green coloring)."
- [readme] [![Build and Publish](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml/badge.svg?branch=release-4-pre)](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml): "[![Build and Publish](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml/badge.svg?branch=release-4-pre)]"
