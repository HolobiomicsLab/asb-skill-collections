---
name: massbank-record-validation
description: Use when you have a collection of MassBank records (in plain-text or structured format) that need to be systematically validated for conformance to MassBank format specification—particularly in a continuous integration context where validation must run on every commit or pull request to maintain.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - MassBank-web Validator
  - MassBank-web
  - GitHub Actions
  - MassBank-data repository
derived_from:
- doi: 10.1002/jms.1777
  title: MassBank
evidence_spans:
- Validator from MassBank-web
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# massbank-record-validation

## Summary

Automated validation of MassBank spectral records against standardized format and content rules using GitHub Actions and the MassBank-web Validator. This skill ensures all records in the MassBank-data repository conform to defined metadata and spectral data standards before publication.

## When to use

Apply this skill when you have a collection of MassBank records (in plain-text or structured format) that need to be systematically validated for conformance to MassBank format specification—particularly in a continuous integration context where validation must run on every commit or pull request to maintain data quality across a shared repository.

## When NOT to use

- Records are already known to conform to MassBank specification and do not require re-validation
- You need to validate records against a custom or non-standard schema different from MassBank's defined format
- Input records are in a non-MassBank format (e.g., mzML, mzXML) that the MassBank Validator does not parse

## Inputs

- MassBank records in plain-text or structured format
- MassBank-data repository commit or pull request
- Individual or batch MassBank record files

## Outputs

- Validation status report (pass/fail per record set)
- Machine-readable validation output (JSON or CSV)
- Validation error/warning messages for failed checks
- GitHub Actions workflow status badge

## How to apply

Trigger the GitHub Actions workflow validate-records.yml in the MassBank-data repository, which invokes the Validator component from MassBank-web against all records. The Validator parses each record's metadata fields (accession, name, formula, mass, spectrum peaks, etc.) according to MassBank format specification, applies validation rules for field presence, data type, value range, and format constraints, and collects validation errors or warnings for each failed rule. The workflow generates a machine-readable validation report (JSON or CSV) with pass/fail outcomes per record set. Monitor validation status via GitHub Actions badges displayed for main and dev branches to verify that all records pass before merging changes.

## Related tools

- **GitHub Actions** (Orchestrates and schedules automated validation workflow (validate-records.yml) on every commit; manages workflow execution environment and artifact collection) — https://github.com/MassBank/MassBank-data
- **MassBank-web Validator** (Implements validation logic (field presence, data type, value range, format constraints) and parses MassBank record metadata and spectral data) — https://github.com/MassBank/MassBank-web/blob/main/MassBank-Project/MassBank-lib/src/main/java/massbank/cli/Validator.java
- **MassBank-data repository** (Central repository containing all MassBank records and GitHub Actions workflow configurations) — https://github.com/MassBank/MassBank-data

## Evaluation signals

- All validation status badges for main and dev branches show passing (green) status
- Validation report lists zero failed checks for all records in the batch
- Machine-readable output (JSON/CSV) contains no error entries or all error counts are zero
- GitHub Actions workflow completes without timeout or fatal errors and produces machine-readable output
- Specific error messages are absent from validation report (or present only for intentionally flagged records)

## Limitations

- The MassBank-web repository is deprecated; the Validator and command-line tools are now maintained in https://github.com/MassBank/MassBank-cli-tools, so validation logic may differ between legacy and current versions
- Validation rules are fixed to MassBank specification and cannot be customized per-record-set without modifying the Validator source code
- GitHub Actions workflow execution may have latency or quota limits depending on repository size and GitHub infrastructure availability

## Evidence

- [readme] uses GitHub Actions to validate the content of all records with the Validator from MassBank-web: "uses GitHub Actions to validate the content of all records with the [Validator](https://github.com/MassBank/MassBank-web/blob/main/MassBank-Project/MassBank-lib/src/main/java/massbank/cli/Validator.ja"
- [other] Validator parses metadata fields and applies format rules: "Parse the record's metadata fields (accession, name, formula, mass, spectrum peaks, etc.) according to MassBank format specification. 3. Apply the validation rules implemented in MassBank-web"
- [other] validation status badges displayed for main and dev branches: "validation status badges displayed for main and dev branches"
- [other] Machine-readable validation output requirement: "Output the validation report in a machine-readable format (JSON or CSV)"
- [readme] MassBank-web is deprecated; validator moved to cli-tools: "This repo is deprecated. Please do not use it! The new MassBank web app is maintained in repo https://github.com/MassBank/MassBank3. The validator and other command line tools are maintained in"
