---
name: metadata-field-validation
description: Use when you have received new or updated MassBank records (in plain-text or structured format) that must be integrated into the MassBank-data repository and you need to ensure they conform to the MassBank format specification before acceptance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  tools:
  - MassBank-web Validator
  - GitHub Actions
  - MassBank-cli-tools
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-field-validation

## Summary

Automated validation of structured metadata records against a defined schema and rule set to ensure content conformance before integration into a curated repository. This skill enforces data type, format, presence, and value-range constraints across all fields in a record.

## When to use

Apply this skill when you have received new or updated MassBank records (in plain-text or structured format) that must be integrated into the MassBank-data repository and you need to ensure they conform to the MassBank format specification before acceptance. Use it as part of a continuous integration workflow to catch validation failures early.

## When NOT to use

- Records that are already pre-validated and archived in Zenodo or a stable release
- Ad-hoc exploratory analysis where schema enforcement is not required
- Raw spectral data before metadata extraction and structuring

## Inputs

- MassBank record file (plain-text or structured format)
- MassBank record string
- Record metadata fields (accession, name, formula, mass, spectrum peaks)

## Outputs

- Validation report with passed and failed checks
- Specific error messages for each failed rule
- Validation status badge (pass/fail) for CI workflow

## How to apply

Load a MassBank record from an input file or string and parse its metadata fields (accession, name, formula, mass, spectrum peaks, etc.) according to the MassBank format specification. Apply the validation rules implemented in MassBank-web Validator.java, which check field presence, data type, value range, and format constraints. Collect validation errors or warnings for each failed rule. Generate a validation report listing passed and failed checks with specific error messages. Use GitHub Actions to invoke validation automatically on every commit or pull request to main and dev branches.

## Related tools

- **MassBank-web Validator** (Implements field presence, data type, value range, and format constraint rules; invoked by GitHub Actions) — https://github.com/MassBank/MassBank-web/blob/main/MassBank-Project/MassBank-lib/src/main/java/massbank/cli/Validator.java
- **GitHub Actions** (Orchestrates automated validation workflow on commits and pull requests to main and dev branches) — https://github.com/MassBank/MassBank-data/actions/workflows/validate-records.yml
- **MassBank-cli-tools** (Successor to MassBank-web; maintains validator and command-line tools for record validation) — https://github.com/MassBank/MassBank-cli-tools

## Evaluation signals

- All required metadata fields are present in the record
- Field values conform to specified data types and format constraints
- Numeric values (mass, m/z, intensity) fall within acceptable ranges
- Validation report shows zero errors (warnings may be acceptable)
- CI workflow badge shows passing status on the main and dev branches

## Limitations

- The MassBank-web repository is deprecated; validators are now maintained in MassBank-cli-tools, which may have different rule sets or invocation patterns
- No changelog is available to track changes to validation rules over time
- Validation rules are enforced at the syntax and schema level but do not assess biological or chemical accuracy of record content

## Evidence

- [other] Parse the record's metadata fields (accession, name, formula, mass, spectrum peaks, etc.) according to MassBank format specification.: "Parse the record's metadata fields (accession, name, formula, mass, spectrum peaks, etc.) according to MassBank format specification."
- [other] Apply the validation rules implemented in MassBank-web Validator.java (field presence, data type, value range, format constraints).: "Apply the validation rules implemented in MassBank-web Validator.java (field presence, data type, value range, format constraints)."
- [other] Collect validation errors or warnings for each failed rule. Generate a validation report listing passed and failed checks with specific error messages.: "Collect validation errors or warnings for each failed rule. Generate a validation report listing passed and failed checks with specific error messages."
- [readme] uses GitHub Actions to validate the content of all records with the Validator from MassBank-web: "uses GitHub Actions to validate the content of all records with the Validator from MassBank-web"
- [readme] ***This repo is deprecated. Please do not use it! The new MassBank web app is maintained in repo https://github.com/MassBank/MassBank3. The validator and other command line tools are maintained in https://github.com/MassBank/MassBank-cli-tools***: "The validator and other command line tools are maintained in https://github.com/MassBank/MassBank-cli-tools"
