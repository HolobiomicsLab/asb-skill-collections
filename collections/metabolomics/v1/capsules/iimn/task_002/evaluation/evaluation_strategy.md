# Evaluation Strategy

## Direct Checks

- file_exists: verify that github:mzmine__mzmine repository contains a workflow file at .github/workflows/dev_build_release.yml
- script_runs: trigger or retrieve the most recent execution of dev_build_release.yml workflow from the mzmine/mzmine public repository on GitHub
- output_matches_reference: confirm that the workflow execution status is 'success' or 'passed' (not 'failure', 'cancelled', or 'skipped')
- file_exists: verify that a build artifact (JAR, executable, or release asset) is present in the workflow run artifacts or GitHub Releases associated with the passing build
- value_in_range: confirm that the workflow completion timestamp is within the last 90 days (robust to clock skew; no canonical answer for 'most recent' without explicit configuration)

## Expert Review

- Verify that the build artifact is functional and compatible with the stated JDK 25 and JavaFX 24 requirements listed in the EnrichedIndex
- Assess whether the artifact filename and metadata correctly identify it as an mzmine build product
