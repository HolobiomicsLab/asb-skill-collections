---
name: workflow-status-monitoring
description: Use when you need to verify that a GitHub Actions workflow (such as 'dev_build_release.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  - GitHub Actions
  - GitHub Actions API
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1038/s41467-021-23953-9
  title: iimn
evidence_spans:
- mzmine is an open-source software for mass spectrometry data processing
- JDK version-25-blue
- JavaFX version-24
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iimn
    doi: 10.1038/s41467-021-23953-9
    title: iimn
  dedup_kept_from: coll_iimn
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-021-23953-9
  all_source_dois:
  - 10.1038/s41467-021-23953-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-status-monitoring

## Summary

Monitor the execution status and completion of automated CI/CD workflows (e.g., GitHub Actions) in real time, polling for status updates and verifying successful artifact production. This skill is essential when validating that build pipelines for scientific software (such as mass spectrometry data processing tools) complete without fatal errors and produce expected output artifacts.

## When to use

Apply this skill when you need to verify that a GitHub Actions workflow (such as 'dev_build_release.yml') has successfully executed on a target branch, or when you must confirm that a triggered build produces valid, downloadable artifacts (compiled binaries, JAR files, installer packages) suitable for distribution or testing.

## When NOT to use

- The workflow file does not exist or is not configured in the repository's .github/workflows directory.
- You are monitoring a workflow that has already reached a terminal state and you only need to retrieve cached results (use artifact download instead).
- The repository does not expose GitHub Actions (e.g., private repository without sufficient access permissions).

## Inputs

- GitHub repository URL (e.g., https://github.com/mzmine/mzmine)
- Workflow file path (e.g., .github/workflows/dev_build_release.yml)
- Target branch name (e.g., 'dev', 'main')

## Outputs

- Workflow execution status (success, failure, cancelled, in_progress)
- Build log (full compilation and packaging output)
- Artifact metadata (file names, sizes, checksums, download URLs)
- Artifact integrity report (validation results)

## How to apply

First, access the workflow file in the .github/workflows directory of the target repository (e.g., mzmine/mzmine) and identify the workflow you intend to monitor (e.g., dev_build_release.yml). Trigger the workflow via the GitHub Actions web interface or API, specifying the desired branch (dev, main, or a feature branch). Use the GitHub Actions API to poll the workflow run status at regular intervals until the run reaches a terminal state (success, failure, or cancelled). Retrieve the detailed build log and scan for fatal compilation errors or warnings that indicate incomplete processing. Confirm that all expected artifacts (JAR files, application bundles, platform-specific installers for Windows, macOS, Linux) were generated and are available for download from the workflow run artifacts section. Finally, validate artifact integrity by checking file sizes, extracting archive contents, or computing checksums to ensure the binaries are not corrupted.

## Related tools

- **GitHub Actions** (CI/CD automation platform for triggering and monitoring workflow execution) — https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml
- **GitHub Actions API** (Programmatic polling interface for workflow run status and artifact metadata retrieval) — https://docs.github.com/en/rest/actions
- **JDK 25** (Java compiler and runtime required to build and validate mzmine artifacts)
- **JavaFX 24** (GUI toolkit packaged with mzmine artifacts for cross-platform UI rendering)

## Examples

```
curl -s -H 'Authorization: token <GITHUB_TOKEN>' 'https://api.github.com/repos/mzmine/mzmine/actions/workflows/dev_build_release.yml/runs?branch=dev&status=completed' | jq '.workflow_runs[0] | {status: .status, conclusion: .conclusion, artifacts_url: .artifacts_url}'
```

## Evaluation signals

- Workflow run reaches 'completed' status with conclusion 'success' (not 'failure' or 'cancelled').
- Build log contains no fatal errors or unresolved compilation errors; all compilation steps logged without exception.
- All expected artifacts are present in the workflow run artifacts section (e.g., mzmine_*.deb, mzmine_*.exe, mzmine_*.dmg, mzmine_*.jar) with non-zero file sizes.
- Artifact checksums are consistent when re-downloaded or when computed from extracted contents (e.g., JAR can be unzipped without corruption).
- Artifact platform coverage matches the workflow definition (Windows, macOS, Linux installers/portable versions are all present and distinct).

## Limitations

- Workflow execution time is variable and may be prolonged if the JDK 25 or JavaFX 24 dependencies must be rebuilt; polling intervals should account for typical queue and build durations.
- GitHub Actions API rate limits may apply (60 requests per hour for unauthenticated requests); use authenticated requests and implement exponential backoff for long-running workflows.
- Build artifacts are retained only for a limited time (default 90 days) and may be garbage-collected; this skill does not archive or preserve artifacts beyond the GitHub Actions retention policy.
- The workflow may succeed but produce artifacts with incorrect platform-specific binaries (e.g., a .deb file that is actually a Windows executable); file content validation is essential and not guaranteed by workflow completion status alone.

## Evidence

- [other] Trigger the workflow via GitHub Actions API or web interface with the desired branch (e.g., 'dev' or 'main'). 3. Monitor the workflow execution until completion, polling the GitHub Actions API for status updates.: "Trigger the workflow via GitHub Actions API or web interface with the desired branch (e.g., 'dev' or 'main'). 3. Monitor the workflow execution until completion, polling the GitHub Actions API for"
- [other] Retrieve the build log and verify that all compilation steps completed without fatal errors. 5. Confirm that build artifacts (compiled JAR, application bundles, or installer packages) were generated and are available for download from the workflow run.: "Retrieve the build log and verify that all compilation steps completed without fatal errors. 5. Confirm that build artifacts (compiled JAR, application bundles, or installer packages) were generated"
- [other] The mzmine repository includes a Development Build Release GitHub Actions workflow (dev_build_release.yml) accessible via badge link, indicating CI/CD automation is configured for the project.: "The mzmine repository includes a Development Build Release GitHub Actions workflow (dev_build_release.yml) accessible via badge link, indicating CI/CD automation is configured for the project."
- [readme] mzmine should work on Windows, macOS, and Linux using either the installers or the portable versions. There are **NO** further requirements as mzmine packages a specific Java Virtual Machine.: "mzmine should work on Windows, macOS, and Linux using either the installers or the portable versions. There are **NO** further requirements as mzmine packages a specific Java Virtual Machine."
- [other] Validate artifact integrity by checking file size, checksum, or attempting to extract/inspect contents.: "Validate artifact integrity by checking file size, checksum, or attempting to extract/inspect contents."
