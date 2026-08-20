---
name: schema-compliance-testing
description: Use when when uploading or ingesting a new paired omics project JSON
  document into the Pairing Omics Data Platform, or when programmatically submitting
  projects via the OpenAPI interface. Apply this skill before persisting the document
  to disk or indexing it for search.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0091
  tools:
  - npm
  - Github
  - GitHub
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or
  `app/` directory
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

# schema-compliance-testing

## Summary

Validate paired omics project documents against a JSON schema to ensure structural and format compliance before storage or submission. This skill detects schema violations early, preventing corrupted or malformed data from entering the platform.

## When to use

When uploading or ingesting a new paired omics project JSON document into the Pairing Omics Data Platform, or when programmatically submitting projects via the OpenAPI interface. Apply this skill before persisting the document to disk or indexing it for search.

## When NOT to use

- Document has already been validated and stored in the platform database
- Raw mass spectrometry or genomic data files (use file format validation instead)
- Legacy projects in older schema versions without migration to current schema

## Inputs

- Paired omics project JSON document (user-submitted or programmatic)
- JSON schema definition (app/public/schema.json)

## Outputs

- Validation pass/fail status
- Structured validation report with violation details
- Error messages and schema constraint violations (if any)
- Compliance status document

## How to apply

Load the paired omics project JSON document and the canonical JSON schema from app/public/schema.json. Apply JSON schema validation using the npm test framework (npm run test in the app/ or api/ directory) to check the document against all schema constraints, including structural requirements, field types, and format specifications. Capture validation results including pass/fail status, any schema violations, and detailed error messages. Generate a structured validation report documenting compliance status and listing specific violations (e.g., missing required fields, incorrect data types, value constraint breaches). Reject documents with violations and provide actionable error output to the submitter.

## Related tools

- **npm** (Execute JSON schema validation tests via npm run test command) — https://www.npmjs.com/
- **GitHub** (Host schema definition and validation test suite; track validation test failures via CI/CD workflow) — https://github.com/iomega/paired-data-form

## Examples

```
npm run test
```

## Evaluation signals

- Validation returns pass status for conformant documents with no schema violations reported
- Validation correctly identifies and reports specific schema violations (missing required fields, wrong data types, invalid values) in non-conformant documents
- Error messages in validation report are actionable and point to exact field or constraint that failed
- npm test suite runs successfully and all existing schema compliance tests pass without regression
- Documents that pass validation can be successfully stored and retrieved from the platform

## Limitations

- Schema validation only checks structural and format compliance; it does not validate semantic correctness (e.g., whether a GenBank identifier actually exists or whether MS/MS spectra and genome truly pair biologically)
- JSON schema validation does not perform cross-document or historical consistency checks
- Validation errors may require schema updates if the platform evolves to support new paired omics data types or formats

## Evidence

- [other] The application uses a JSON schema file located at app/public/schema.json that defines the structural and format requirements for paired omics data projects.: "The application uses a JSON schema file located at app/public/schema.json that defines the structural and format requirements for paired omics data projects."
- [other] Apply JSON schema validation using npm test framework to check the document against all schema constraints.: "Apply JSON schema validation using npm test framework to check the document against all schema constraints."
- [other] Capture validation results including pass/fail status, any schema violations, and error messages.: "Capture validation results including pass/fail status, any schema violations, and error messages."
- [readme] The JSON schema (app/public/schema.json) describes the format of an project.: "The JSON schema (app/public/schema.json) describes the format of an project."
- [readme] make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory: "make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory"
