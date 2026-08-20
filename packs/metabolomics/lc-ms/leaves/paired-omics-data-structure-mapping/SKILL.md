---
name: paired-omics-data-structure-mapping
description: Use when when you have a paired omics project document (JSON format) that combines MS/MS mass spectrometry data with genome identifiers, biosynthetic gene cluster information, sample preparation, extraction method, and instrumentation metadata, and you need to verify it conforms to the platform's.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - npm
  - Github
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory
- pull request (https://help.github.com/articles/about-pull-requests/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla_cq
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00724-z
  all_source_dois:
  - 10.1038/s41589-020-00724-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# paired-omics-data-structure-mapping

## Summary

Validate paired omics project documents against a JSON schema to ensure structural compliance and data integrity before storage or submission. This skill enforces format requirements for linking MS/MS mass spectra with genome, biosynthetic gene cluster, and metadata annotations.

## When to use

When you have a paired omics project document (JSON format) that combines MS/MS mass spectrometry data with genome identifiers, biosynthetic gene cluster information, sample preparation, extraction method, and instrumentation metadata, and you need to verify it conforms to the platform's structural and format requirements before uploading or storing it.

## When NOT to use

- Document is already known to be valid and has passed validation in a prior workflow step.
- Data is in a format other than JSON (e.g., CSV, XML, or unstructured text) — requires format conversion first.
- Schema file is unavailable or corrupted — validation cannot proceed without the authoritative schema.

## Inputs

- paired omics project JSON document
- JSON schema file (app/public/schema.json)

## Outputs

- validation report with pass/fail status
- list of schema violations (if any)
- error messages detailing specific constraint violations

## How to apply

Load the paired omics project JSON document and the JSON schema from app/public/schema.json. Apply JSON schema validation using npm test framework to check the document against all schema constraints. Capture validation results including pass/fail status, any schema violations, and error messages. Generate a structured validation report detailing compliance status and specific violations. The schema defines both structural requirements (e.g., required fields linking spectra to genome and gene cluster annotations) and format constraints (e.g., data types, identifier formats). Validation ensures data integrity before the web application stores the project as a file on disk or submits it to Zenodo.

## Related tools

- **npm** (Test framework for running JSON schema validation checks against project documents)
- **Github** (Version control and collaboration platform for managing schema definitions and validation workflows) — https://github.com/iomega/paired-data-form

## Examples

```
npm run test
```

## Evaluation signals

- Validation report explicitly states 'pass' or 'fail' for the entire document against schema constraints.
- All mandatory schema fields (those linking MS/MS spectra, genome, and gene cluster data) are present and correctly formatted.
- Error messages for violations cite specific schema constraints (e.g., required field missing, incorrect data type, invalid identifier format).
- Documents passing validation can be successfully stored as project files on disk or submitted to the web application without structural errors.
- No schema violations are reported for documents that comply with the structural and format requirements defined in app/public/schema.json.

## Limitations

- Validation checks only structural and format compliance; it does not verify semantic correctness (e.g., whether a genome identifier actually exists in GenBank or whether MS/MS spectra are scientifically meaningful).
- Schema version mismatches between the document and app/public/schema.json may cause false positives or false negatives if the schema has been updated without document migration.
- The npm test framework depends on npm dependencies being installed and up-to-date; missing or outdated dependencies may cause validation to fail or produce incomplete results.

## Evidence

- [other] The JSON schema file located at app/public/schema.json that defines the structural and format requirements for paired omics data projects.: "The application uses a JSON schema file located at app/public/schema.json that defines the structural and format requirements for paired omics data projects."
- [other] The workflow for applying JSON schema validation using npm test framework to check documents against all schema constraints.: "Apply JSON schema validation using npm test framework to check the document against all schema constraints."
- [other] Capturing validation results including pass/fail status, schema violations, and error messages.: "Capture validation results including pass/fail status, any schema violations, and error messages."
- [readme] The schema describes the format of a paired omics project document.: "The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project."
- [readme] Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method.: "Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method"
