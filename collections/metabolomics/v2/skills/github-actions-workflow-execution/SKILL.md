---
name: github-actions-workflow-execution
description: Use when you have a GitHub repository containing scientific records (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - GitHub Actions
  - MassBank-web Validator
  - MassBank-data repository
derived_from:
- doi: 10.1002/jms.1777
  title: MassBank
evidence_spans:
- uses GitHub Actions to validate the content of all records
- uses GitHub Actions to validate the content of all records with the [Validator]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  - build: coll_massbank_cq
    doi: 10.1002/jms.1777
    title: MassBank
  dedup_kept_from: coll_massbank_cq
schema_version: 0.2.0
---

# github-actions-workflow-execution

## Summary

Execute automated validation workflows on a GitHub repository using GitHub Actions to test all records against a validator tool, generating pass/fail status reports. This skill enables continuous integration of quality control for scientific data repositories by triggering scheduled or event-driven validation jobs that persist results as machine-readable outputs and status badges.

## When to use

You have a GitHub repository containing scientific records (e.g., mass spectrometry data, chemical records, genomic datasets) that require systematic validation against a schema or reference validator, and you want to automate this validation on every commit or branch update without manual intervention.

## When NOT to use

- Validator tool is computationally prohibitive or exceeds GitHub Actions job time/resource limits for the number of records
- Records are stored outside the GitHub repository (e.g., in a separate database) and cannot be accessed by the workflow runner
- Validation results must be generated interactively or require manual review steps that cannot be scripted in a workflow

## Inputs

- GitHub repository with scientific records (MassBank records in .txt or similar format)
- Validator tool or CLI application (e.g., MassBank-web Validator class)
- GitHub Actions workflow definition file (.yml in .github/workflows/)
- Branch name(s) or trigger event configuration

## Outputs

- Validation status report (JSON or CSV format) with pass/fail outcomes per record set
- GitHub Actions workflow run logs and execution summary
- Validation status badge SVG/URL for embedding in README or documentation
- Per-record validation result details (errors, warnings, schema violations)

## How to apply

Set up a GitHub Actions workflow file (e.g., validate-records.yml) in the .github/workflows directory that invokes your validator tool (in this case, the MassBank-web Validator) against all records in the repository. Configure the workflow to run on pushes to specified branches (main, dev) or on a schedule. The workflow collects validation results for each record and record set, then outputs results in a machine-readable format (JSON or CSV). Display validation status via GitHub Actions workflow badges linked to the workflow runs page, allowing stakeholders to see pass/fail status at a glance. Monitor the workflow execution logs to debug validation failures and iterate on record corrections.

## Related tools

- **GitHub Actions** (Orchestrates workflow execution, triggers validation on branch pushes, manages job environment and logs) — https://github.com/features/actions
- **MassBank-web Validator** (Validates content and schema compliance of all MassBank records; invoked by the workflow against each record) — https://github.com/MassBank/MassBank-web
- **MassBank-data repository** (Source repository containing all records to be validated; hosts the workflow definition) — https://github.com/MassBank/MassBank-data

## Evaluation signals

- Workflow file (.github/workflows/validate-records.yml) exists and is syntactically valid YAML
- Workflow execution completes without runner errors; logs show validator invocation on all records
- Validation status badges display correct pass/fail state and link to corresponding branch workflow runs
- Output report (JSON/CSV) contains an entry for every record in the repository; no records are skipped
- Pass/fail outcomes in the report align with independent manual validation or match expected schema constraints

## Limitations

- GitHub Actions has job timeout limits (~6 hours) that may prevent validation of extremely large repositories
- Validator tool must be accessible from the GitHub-hosted runner environment; private or non-public validators may require additional authentication setup
- Workflow badge status reflects only the most recent workflow run; historical validation trends require separate archival or dashboard integration
- MassBank-web repository is deprecated; new validator maintenance has moved to https://github.com/MassBank/MassBank-cli-tools

## Evidence

- [intro] GitHub Actions to validate the content of all records: "uses GitHub Actions to validate the content of all records with the Validator from MassBank-web"
- [readme] Validation workflow and status outputs: "uses GitHub Actions to validate the content of all records with the [Validator](https://github.com/MassBank/MassBank-web/blob/main/MassBank-Project/MassBank-lib/src/main/java/massbank/cli/Validator.ja"
- [readme] Status badges displayed for branches: "* main branch [![Main Validation Status](https://github.com/MassBank/MassBank-data/actions/workflows/validate-records.yml/badge.svg?branch=main)]"
- [other] Machine-readable output format requirement: "Output the validation report in a machine-readable format (JSON or CSV)"
