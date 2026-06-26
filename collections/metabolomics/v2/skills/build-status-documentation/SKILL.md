---
name: build-status-documentation
description: Use when when you need to validate that a development build release workflow
  (such as dev_build_release.yml for a mass spectrometry data processing project)
  executes without failure and generates artifacts for downstream testing or distribution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  - GitHub Actions
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# build-status-documentation

## Summary

Systematically access, retrieve, and document the execution status and artifacts of a GitHub Actions workflow to establish reproducibility and traceability of automated build pipelines. This skill verifies that continuous integration workflows complete successfully and produce expected outputs.

## When to use

When you need to validate that a development build release workflow (such as dev_build_release.yml for a mass spectrometry data processing project) executes without failure and generates artifacts for downstream testing or distribution. Apply this skill when establishing baseline reproducibility, troubleshooting build failures, or tracking artifact availability across workflow runs.

## When NOT to use

- The build workflow has not been configured or does not exist in the repository — use version control inspection or project setup steps instead.
- You only need to verify static badge status without inspecting logs — badge display alone does not capture transient failures, flaky tests, or partial artifact production.
- The workflow is private or access credentials are unavailable — documentation requires authenticated access to GitHub Actions.

## Inputs

- GitHub Actions workflow run URL (e.g., https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml)
- Repository README or .github/workflows/*.yml file containing workflow definition and badge metadata
- Target workflow run identifier (branch, tag, or most recent run)

## Outputs

- Structured status report file (timestamp, workflow status: pass/fail, JDK and runtime version metadata)
- Build artifact links and file names (e.g., portable installers, .deb files for Linux)
- Error messages and build logs (full log or summary excerpt)
- Workflow execution time and resource utilization metadata (if logged)

## How to apply

Navigate to the GitHub Actions workflow page for the target repository and workflow file (e.g., https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml). Retrieve the most recent workflow run by examining the run history and execution logs. Document the pass/fail outcome, capture any error messages or warnings, and record artifact names and download links if the build succeeded. Record all results—including timestamp, workflow status, JDK version (e.g., JDK 25), runtime dependencies (e.g., JavaFX 24), and artifact locations—in a structured report file. Cross-reference the workflow badge displayed in the repository README to confirm visual status representation matches log evidence.

## Related tools

- **mzmine** (Target application whose development build release workflow is being documented; requires JDK 25 and JavaFX 24 for successful compilation) — https://github.com/mzmine/mzmine
- **JDK 25** (Java Development Kit version required by mzmine build system; version constraint must be logged in workflow documentation)
- **JavaFX 24** (GUI framework dependency for mzmine; version and availability must be verified in build artifacts and logs)
- **GitHub Actions** (CI/CD platform hosting and executing the dev_build_release.yml workflow; provides run history, logs, and artifact storage) — https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml

## Examples

```
curl -s https://api.github.com/repos/mzmine/mzmine/actions/workflows/dev_build_release.yml/runs | jq '.workflow_runs[0] | {status, conclusion, created_at, artifacts_url}'
```

## Evaluation signals

- Workflow run shows ✓ status on GitHub Actions page and matches the badge state displayed in the repository README.
- Build artifacts are present in the release or artifacts store (e.g., mzmine_*.deb for Linux, portable installers for Windows/macOS) and are downloadable.
- Execution logs contain no unhandled exceptions, unresolved dependency errors, or JDK/JavaFX version mismatches.
- Documented timestamp, JDK version (25), and JavaFX version (24) match the build environment specified in the workflow file and badge metadata.
- Report file structure is consistent across multiple workflow runs (same schema, field presence, artifact naming convention).

## Limitations

- Workflow status documentation captures a point-in-time snapshot; repeated runs or branch changes may alter artifact availability and status without retroactive warning.
- Private workflows or repositories may be inaccessible without GitHub authentication; public badge display does not guarantee log access.
- Build artifacts are typically retained for a finite time window (GitHub Actions default is 90 days); older workflow runs may have expired artifacts despite passing status.
- No changelog is available in the repository, limiting correlation between workflow success and feature/fix content in the build.

## Evidence

- [readme] dev_build_release.yml workflow badge linking to workflow runs indicates presence of configured CI pipeline: "[![Development Build Release](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml/badge.svg)](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml)"
- [readme] JDK and JavaFX versions are explicitly specified in workflow badge metadata: "![Static Badge](https://img.shields.io/badge/JDK%20version-25-blue) ![Static Badge](https://img.shields.io/badge/JavaFX%20version-24-%2391219c)"
- [readme] Development build reflects current state of master branch and is available as a release artifact: "the [latest development build](https://github.com/mzmine/mzmine3/releases/tag/Development-release) which reflects the current state of the master branch and is meant for testing purposes"
- [readme] Build artifacts include portable versions and platform-specific installers distributed through GitHub Releases: "Download options include portable versions and installers for the Window, macOS, and Linux."
- [other] Task definition specifies structured report output with timestamp, workflow status, and artifact links: "Record results in a structured report file with timestamp, workflow status, and artifact links."
