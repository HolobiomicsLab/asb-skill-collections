---
name: batch-record-processing
description: Use when when you have a repository containing hundreds or thousands of structured records (e.g., MassBank records in standardized format) that must be validated for correctness before release or merge.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - GitHub Actions
  - MassBank-web Validator
  - MassBank-cli-tools
derived_from:
- doi: 10.1002/jms.1777
  title: MassBank
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massbank_cq
    doi: 10.1002/jms.1777
    title: MassBank
  dedup_kept_from: coll_massbank_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/jms.1777
  all_source_dois:
  - 10.1002/jms.1777
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-record-processing

## Summary

Automated validation of large collections of structured scientific records (e.g., mass spectrometry metadata) using continuous integration workflows and specialized validators. This skill ensures data consistency and compliance across thousands of records without manual inspection of each entry.

## When to use

When you have a repository containing hundreds or thousands of structured records (e.g., MassBank records in standardized format) that must be validated for correctness before release or merge. Use this skill if you need to catch validation failures early in the development cycle and maintain a visible audit trail (e.g., status badges) of validation outcomes across branches.

## When NOT to use

- Records are already validated in a prior pipeline stage and no schema or format changes have occurred since validation.
- Validation logic is domain-specific and no reusable validator tool exists for your record format.
- Record collection is too small (<10 records) to justify the setup overhead of CI automation.

## Inputs

- Repository containing structured records in standardized format (e.g., MassBank records)
- GitHub Actions workflow configuration file (e.g., validate-records.yml)
- Validator tool or command-line interface (e.g., MassBank-web Validator)

## Outputs

- Validation status report (JSON or CSV format) with pass/fail outcomes per record set
- Validation status badges for main and dev branches
- GitHub Actions workflow logs and execution results

## How to apply

Set up a GitHub Actions workflow (e.g., validate-records.yml) that triggers on pushes and pull requests to your repository. Configure the workflow to invoke a specialized validator tool (such as the MassBank-web Validator) against all records in the repository. Collect validation results for each record and aggregate them by record set. Generate a machine-readable validation report (JSON or CSV format) with pass/fail outcomes. Display validation status badges on main and dev branches to provide real-time visibility into data quality. This approach leverages version control hooks to enforce data integrity as a gate before code merges.

## Related tools

- **GitHub Actions** (Orchestrates the batch validation workflow; triggers validator on all records on pushes/PRs to main and dev branches) — https://github.com/MassBank/MassBank-data
- **MassBank-web Validator** (Command-line tool that validates individual MassBank records against schema and content rules) — https://github.com/MassBank/MassBank-web/blob/main/MassBank-Project/MassBank-lib/src/main/java/massbank/cli/Validator.java
- **MassBank-cli-tools** (Successor repository maintaining the validator and other command-line tools for batch processing) — https://github.com/MassBank/MassBank-cli-tools

## Evaluation signals

- All records in the repository pass validation without errors reported in the workflow log.
- Validation status badges display a 'passing' state for both main and dev branches.
- Machine-readable output report (JSON/CSV) contains records with expected pass/fail counts matching manual spot-checks of known-good and known-bad records.
- Workflow execution time is consistent and proportional to record count (no unexpected timeouts or failures).
- Any record failing validation is flagged with specific error messages that allow root cause diagnosis.

## Limitations

- Validator tool must exist and be callable from CI environment; domain-specific validators may not be available for all record types.
- Workflow setup and maintenance require familiarity with GitHub Actions syntax and CI/CD best practices.
- Validation rules are static at workflow execution time; schema changes require workflow edits and re-deployment.
- MassBank-web repository is deprecated; validator maintenance has moved to MassBank-cli-tools, requiring migration of existing workflows.

## Evidence

- [intro] GitHub Actions validates content with MassBank-web Validator: "uses GitHub Actions to validate the content of all records with the Validator from MassBank-web"
- [readme] Status badges indicate validation on main and dev branches: "MassBank-data validation status * main branch * dev branch"
- [other] Workflow produces structured validation results: "Collect validation results for each record and record set. 4. Generate a validation status report with pass/fail outcomes per record set. 5. Output the validation report in a machine-readable format"
- [readme] Validator moved to maintained repository: "The validator and other command line tools are maintained in https://github.com/MassBank/MassBank-cli-tools"
