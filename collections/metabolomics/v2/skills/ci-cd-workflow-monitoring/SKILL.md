---
name: ci-cd-workflow-monitoring
description: Use when when you need to verify that a continuous integration pipeline for a scientific software project (e.g., mzmine) completes successfully, produces expected build artifacts, or fails in a reproducible manner.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CI/CD Workflow Monitoring

## Summary

Monitor and verify the status of automated GitHub Actions workflows to ensure reproducibility of build artifacts and identify failures in development release pipelines. This skill documents workflow execution logs, build outcomes, and artifact availability for continuous integration transparency.

## When to use

When you need to verify that a continuous integration pipeline for a scientific software project (e.g., mzmine) completes successfully, produces expected build artifacts, or fails in a reproducible manner. Use this skill when assessing whether development builds reflect the current state of the repository's master branch or when troubleshooting broken CI pipelines.

## When NOT to use

- The workflow configuration file itself does not exist or is inaccessible (use repository file inspection instead).
- You are debugging local build failures that do not involve the remote GitHub Actions pipeline (use local build and logging inspection).
- The workflow has not yet run or there are no historical runs to analyze (wait for the first run or manually trigger if allowed).

## Inputs

- GitHub Actions workflow URL (string)
- Target repository name (string, e.g., 'mzmine/mzmine')
- Workflow filename (string, e.g., 'dev_build_release.yml')

## Outputs

- Structured workflow status report (JSON or plain text)
- Build artifact links (URLs to .deb, .exe, .dmg, or portable archives)
- Execution log excerpts (text)
- Timestamp of last successful/failed run (ISO 8601 datetime)
- Error messages or build failure details (text)

## How to apply

Access the GitHub Actions workflow URL for the target repository (e.g., https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml). Retrieve the most recent workflow run and examine its status badge and execution logs. Document the pass/fail outcome, any error messages, and links to produced artifacts (e.g., portable installers or .deb packages for Windows, macOS, and Linux). Record results in a structured report file with timestamp, workflow status, artifact links, and JDK/JavaFX version compatibility notes. Cross-reference the README's stated requirements (e.g., 'JDK version 23 or newer') against the workflow's actual environment to identify configuration mismatches.

## Related tools

- **GitHub Actions** (Continuous integration platform that executes the dev_build_release.yml workflow and provides workflow run history, logs, and artifact storage.) — https://github.com/mzmine/mzmine
- **mzmine** (Target software project whose CI/CD pipeline is monitored; produces mass spectrometry data processing binaries across multiple platforms.) — https://github.com/mzmine/mzmine
- **JDK 25** (Java Development Kit required by the mzmine build process; version compatibility verified in workflow execution.)
- **JavaFX 24** (GUI framework bundled with mzmine; version compatibility verified in workflow status and README.)

## Examples

```
curl -s https://api.github.com/repos/mzmine/mzmine/actions/workflows/dev_build_release.yml/runs?per_page=1 | jq '.workflow_runs[0] | {status, conclusion, created_at, artifacts_url}'
```

## Evaluation signals

- Workflow run status badge shows 'passing' or 'failing' state consistently with the latest run details.
- Artifact links in the workflow output resolve and point to valid, non-expired download URLs (e.g., .deb, .exe, .dmg files).
- Build artifacts exist for all documented platform targets (Windows, macOS, Linux) or documented absences are explained in logs.
- Timestamps of artifact generation match the workflow run completion time (within expected jitter).
- Error messages or build failure logs contain actionable information (e.g., JDK version mismatch, missing dependencies, compilation errors) that can be cross-referenced against the README's build requirements.

## Limitations

- Workflow status is only as current as the last push to the repository; manual runs or scheduled builds may be configured outside the repository README.
- Artifact links may expire or be pruned by GitHub's retention policies; archived reports are needed for historical reproducibility audits.
- Workflow logs do not capture all runtime dependencies (e.g., system libraries on Linux); platform-specific installation issues may not surface in CI logs.
- No changelog is provided in the repository README, so workflow failures cannot be directly correlated to recent code changes without additional git history inspection.

## Evidence

- [other] A development build release workflow is configured and accessible at the mzmine/mzmine repository GitHub Actions, as indicated by the presence of the dev_build_release.yml workflow badge linking to the workflow runs.: "A development build release workflow is configured and accessible at the mzmine/mzmine repository GitHub Actions, as indicated by the presence of the dev_build_release.yml workflow badge linking to"
- [other] Retrieve the most recent workflow run status and execution logs. Document the pass/fail outcome and any build artifacts or error messages produced. Record results in a structured report file with timestamp, workflow status, and artifact links.: "Retrieve the most recent workflow run status and execution logs. Document the pass/fail outcome and any build artifacts or error messages produced. Record results in a structured report file with"
- [readme] mzmine development requires Java Development Kit (JDK) version 23 or newer (http://jdk.java.net).: "mzmine development requires Java Development Kit (JDK) version 23 or newer (http://jdk.java.net)."
- [readme] Releases are split into stable releases and the latest development build which reflects the current state of the master branch and is meant for testing purposes. Download options include portable versions and installers for the Window, macOS, and Linux.: "Releases are split into stable releases and the latest development build which reflects the current state of the master branch and is meant for testing purposes. Download options include portable"
- [readme] mzmine should work on Windows, macOS, and Linux using either the installers or the portable versions. There are NO further requirements as mzmine packages a specific Java Virtual Machine.: "mzmine should work on Windows, macOS, and Linux using either the installers or the portable versions. There are NO further requirements as mzmine packages a specific Java Virtual Machine."
