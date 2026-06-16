---
name: github-actions-workflow-execution
description: Use when you need to validate that a repository's automated build, test, or publish pipeline is functioning correctly on a target branch (e.g., release branch); when you want to confirm that workflow status badges in documentation accurately reflect current execution state;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - GitHub Actions
  - SIRIUS
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans:
- GitHub Actions 'Build and Publish' workflow (distribute.yaml)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
---

# github-actions-workflow-execution

## Summary

Verify that a GitHub Actions workflow (such as Build and Publish) executes successfully on a specified branch by triggering the workflow, monitoring logs, and confirming pass status via the Actions tab and repository badges. This skill ensures CI/CD pipeline health and reproducibility of automated build processes.

## When to use

Apply this skill when you need to validate that a repository's automated build, test, or publish pipeline is functioning correctly on a target branch (e.g., release branch); when you want to confirm that workflow status badges in documentation accurately reflect current execution state; or when troubleshooting CI/CD failures requires inspection of live workflow logs and run history.

## When NOT to use

- Workflow definition file does not exist or is malformed (syntax error) — fix the YAML first.
- Repository is private and you lack read access to the Actions tab — request access or use a different verification method.
- The workflow is intentionally disabled or archived — check the workflow metadata for 'disabled' flags before attempting to trigger.

## Inputs

- GitHub repository URL
- target branch name (e.g., 'release-4-pre')
- workflow definition file (YAML, e.g., .github/workflows/distribute.yaml)

## Outputs

- GitHub Actions run ID
- workflow execution logs (stdout/stderr from build steps)
- final run status ('passed', 'failed', or 'cancelled')
- status badge URL and display state (passing/failing)

## How to apply

Navigate to the target GitHub repository and identify the relevant workflow file (e.g., distribute.yaml in .github/workflows/). Review the workflow trigger conditions to determine whether to create a release tag, push to the target branch, or manually trigger the run. Execute or await the workflow run, then open the Actions tab to monitor logs in real time, watching for errors or warnings that might indicate build failures. Upon completion, verify the run status displays 'passed' in the Actions interface. Finally, cross-reference the repository README or documentation to confirm that any associated status badge (e.g., 'Build and Publish') displays a passing indicator (green badge or 'passing'/'success' label), confirming the workflow is reproducible and the badge is up to date.

## Related tools

- **GitHub Actions** (CI/CD orchestration platform used to define, trigger, and monitor workflow execution; provides logs, status tracking, and badge generation for workflow health.) — https://github.com/features/actions
- **SIRIUS** (Java-based software framework for LC-MS/MS data analysis; the Build and Publish workflow automates compilation, testing, and distribution of SIRIUS binaries across multiple platforms.) — https://github.com/sirius-ms/sirius

## Evaluation signals

- GitHub Actions 'Actions' tab shows a completed run with status 'passed' (indicated by green checkmark) for the specified workflow and branch.
- Workflow run logs contain no errors, fatal exceptions, or 'failed' step indicators; all build and publish steps complete successfully.
- Status badge in the repository README displays green coloring and 'passing' or 'success' label, matching the latest Actions run status.
- Build artifacts (e.g., compiled binaries, release packages) are successfully published to the expected location (GitHub Releases, package registry, etc.) as evidenced by download links or asset listings.
- Re-triggering the workflow on the same branch produces the same 'passed' status, confirming reproducibility.

## Limitations

- Workflow execution may fail silently or with unclear error messages if secrets (API keys, credentials) are misconfigured or missing — examine the 'secrets' context in the workflow definition.
- Status badges are cached and may not update immediately after a workflow completes; refresh the README page to see the latest badge state.
- Network or rate-limiting issues on external services (e.g., package registries, Docker Hub) invoked by the workflow may cause transient failures that do not reflect code quality.
- Workflow logs are retained only for a limited period (typically 90 days on GitHub); historical run information may become unavailable.

## Evidence

- [other] workflow trigger and status verification: "Trigger the 'Build and Publish' workflow by creating a release tag or pushing to the release branch, depending on the workflow trigger conditions specified in distribute.yaml. Monitor the GitHub"
- [readme] workflow configuration and badge display: "Examine the distribute.yaml workflow file in the .github/workflows directory to understand the build and publish pipeline. Inspect the repository README to confirm the build badge displays a passing"
- [readme] status badge in documentation: "[![Build and Publish](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml/badge.svg?branch=release-4-pre)](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml)"
- [readme] repository version and distribution context: "SIRIUS+CSI:FingerID GUI and CLI - Version 6.3.7 (2026-05-23). These versions include the Java Runtime Environment, so there is no need to install Java separately!"
