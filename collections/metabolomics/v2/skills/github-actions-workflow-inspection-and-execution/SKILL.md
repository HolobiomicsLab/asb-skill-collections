---
name: github-actions-workflow-inspection-and-execution
description: Use when a GitHub repository displays a CI workflow badge (e.g., passing/failing status in README) and you need to verify that the reported status is accurate, reproduce the CI environment locally, or debug workflow failures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0769
  tools:
  - git
  - GitHub Actions
  - RDKit
derived_from:
- doi: 10.1021/acs.analchem.5c00633
  title: metid
evidence_spans:
- Clone the Met-ID repository
- GitHub Actions CI workflow (main.yml)
- Powered by RDKit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00633
  all_source_dois:
  - 10.1021/acs.analchem.5c00633
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# GitHub Actions Workflow Inspection and Execution

## Summary

Inspect and locally reproduce a GitHub Actions CI workflow by examining the main.yml configuration file and executing the same test suite and dependency installation steps to verify that the workflow passes and matches the reported badge status. This skill validates the integrity of automated CI pipelines and confirms reproducibility of build artifacts.

## When to use

Use this skill when a GitHub repository displays a CI workflow badge (e.g., passing/failing status in README) and you need to verify that the reported status is accurate, reproduce the CI environment locally, or debug workflow failures. Apply it as part of dependency auditing, build validation, or when assessing the reliability of automated checks before integrating code.

## When NOT to use

- The repository does not display a CI badge or does not use GitHub Actions; use generic repository health inspection instead.
- You only need to verify that the repository has a workflow file; use lightweight YAML schema validation instead of full execution.
- The workflow requires access to private secrets, API keys, or cloud credentials not available in your local environment; consider manual code review or staged CI re-runs instead.

## Inputs

- GitHub repository URL (e.g., https://github.com/pbjarterot/Met-ID)
- Workflow YAML file (.github/workflows/main.yml)
- Repository source code and dependency manifests (e.g., Cargo.toml, requirements.txt, package.json)

## Outputs

- Workflow execution exit status (pass/fail)
- Test output and error logs from local execution
- Comparison report of badge-reported status vs. reproduced status
- Documented discrepancies, environment conditions, and debugging artifacts

## How to apply

Clone the target repository (e.g., pbjarterot/Met-ID) and navigate to the .github/workflows/ directory to locate the main workflow file (main.yml). Inspect the workflow YAML to identify all CI steps, environment setup (Python/Rust/dependency versions), and test commands. Replicate the workflow environment locally by installing declared dependencies and running the test suite with identical commands. Monitor the exit status and capture logs or test output. Compare the final pass/fail result and any error messages against the badge-reported status. If they diverge, document the discrepancy and inspect environment variables, secrets, or OS-specific conditions that may differ between CI and local execution.

## Related tools

- **git** (Clone the repository and access workflow files from version control) — https://git-scm.com/
- **GitHub Actions** (Execute and monitor CI workflow via GitHub's automation platform; trigger workflows via API and capture completion status) — https://github.com/pbjarterot/Met-ID/actions
- **RDKit** (Dependency checked in workflow; may be required for test suite execution) — https://www.rdkit.org/

## Examples

```
git clone https://github.com/pbjarterot/Met-ID && cd Met-ID && cat .github/workflows/main.yml && git clone https://github.com/pbjarterot/Met-ID && cd Met-ID && cargo build && cargo test
```

## Evaluation signals

- Local test execution produces the same exit code (pass/fail) as the CI badge status.
- No uncaught exceptions or segmentation faults during dependency installation and test execution.
- Test output matches or is semantically equivalent to CI logs (assertions passed, coverage thresholds met).
- Workflow YAML is valid and all declared steps execute without missing tools or environment variables.
- Exit codes and error messages are logged and reviewed to identify environment-specific gaps (OS version, Python/Rust version, missing optional dependencies).

## Limitations

- Private secrets and API credentials used in the workflow may not be accessible locally; some workflow steps may be skipped or fail in local execution.
- OS-specific workflow branches (macOS, Linux, Windows) may not execute identically on a different host platform; platform coverage must be explicitly tested.
- Scheduled triggers, event-based conditions (on pull_request, on push to specific branches), or matrix strategies in the workflow may not apply during local execution; a full reproduction may require GitHub Actions API triggers.
- The repository README notes that Met-ID is under active development and database file updates may not propagate correctly across reinstalls, which could affect test reproducibility if database fixtures are part of the CI suite.

## Evidence

- [other] The Met-ID repository displays a GitHub Actions workflow badge linked to main.yml, indicating the presence of automated CI pipeline execution tracking.: "The Met-ID repository displays a GitHub Actions workflow badge linked to main.yml, indicating the presence of automated CI pipeline execution tracking."
- [other] Workflow inspection and local reproduction steps: "1. Clone the pbjarterot/Met-ID repository from GitHub using git. 2. Inspect the main.yml workflow file in .github/workflows/ to identify the CI steps, environment setup, and test commands. 3. Execute"
- [readme] Tool dependencies used in CI/CD: "[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/pbjarterot/Met-ID/actions)"
- [readme] Multiple programming languages and frameworks in the codebase: "[![Rust](https://img.shields.io/badge/rust-%23000000.svg?style=for-the-badge&logo=rust&logoColor=white)](https://www.rust-lang.org/) [![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.sv"
- [readme] Development status and potential reproducibility issues: "Met-ID is under development. For some reason, reinstalling newer versions of Met-ID does not update the database files it comes bundled with and as such the database files will have to removed"
