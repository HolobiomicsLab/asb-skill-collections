---
name: whitespace-character-detection
description: Use when validating project JSON documents against the platform's schema (app/public/schema.json) and you need to ensure all URL-type fields conform to URL syntax rules. Specifically, use it when the schema designates certain fields as URL type (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3473
  tools:
  - npm
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00724-z
  all_source_dois:
  - 10.1038/s41589-020-00724-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# whitespace-character-detection

## Summary

Detect and flag URL fields in project JSON documents that contain whitespace characters (spaces, tabs, newlines), which are invalid in URLs and prevent proper data validation. This skill applies schema-based field validation to identify problematic URLs before they are stored or transmitted.

## When to use

Apply this skill when validating project JSON documents against the platform's schema (app/public/schema.json) and you need to ensure all URL-type fields conform to URL syntax rules. Specifically, use it when the schema designates certain fields as URL type (e.g., project URLs, reference links, data repository links) and you want to detect malformed URLs that contain whitespace before they cause downstream issues.

## When NOT to use

- Input JSON does not use the platform schema or does not define URL-type fields explicitly — the skill requires schema metadata to identify which fields to validate
- URLs have already been pre-processed or normalized to remove whitespace — validation would be redundant
- The goal is to fix malformed URLs rather than report them — this skill detects problems but does not auto-correct

## Inputs

- Project JSON document conforming to app/public/schema.json
- JSON schema definition (app/public/schema.json) with field type annotations

## Outputs

- Validation report listing flagged URLs with field name, offending URL value, and warning message
- Structured record of whitespace violations and their locations within the document

## How to apply

Load a project JSON document from the platform and identify all fields designated as URL type in the schema. Iterate through each URL field and check for the presence of whitespace characters (spaces, tabs, newlines). For each URL containing whitespace, record the field name, the offending URL value, and generate a warning message. Compile validation results into a report listing all flagged URLs and their locations within the document. The rationale is that URLs are space-sensitive tokens; any embedded whitespace breaks URL parsing and transmission, so early detection prevents silent data corruption.

## Related tools

- **npm** (Build and test framework used to run validation tests and verify whitespace detection logic)

## Evaluation signals

- All URL-type fields from the schema are checked; no designated URL field is skipped
- Every URL containing spaces, tabs, or newlines is flagged in the validation report with correct field name and location
- No false positives: non-URL fields are not validated, and URLs without whitespace are not flagged
- Validation report is properly structured and human-readable, listing field name, offending value, and warning message for each violation
- Existing test suite still passes after implementation (npm run test in api/ and/or app/ directory)

## Limitations

- The skill depends on the schema correctly marking all URL fields; if the schema is incomplete or mislabels fields, some malformed URLs may be missed
- Detection is syntactic only — it identifies whitespace presence but does not validate whether the URL is otherwise well-formed (e.g., correct protocol, valid domain structure)
- The skill reports violations but does not automatically correct them; human intervention or a separate correction step is required to fix the URLs
- The GitHub issue #75 notes that spaces in URLs were not being properly handled, indicating that user education or UI-level validation may also be needed alongside this detection step

## Evidence

- [other] The platform stores paired omics data projects using a JSON schema format (app/public/schema.json) that defines project structure, which serves as the basis for implementing field-level validation rules including URL format constraints.: "JSON schema format (app/public/schema.json) that defines project structure, which serves as the basis for implementing field-level validation rules including URL format constraints"
- [other] Identify all fields designated as URL type in the schema (e.g., project URLs, reference links, data repository links). Iterate through each URL field and check for the presence of whitespace characters (spaces, tabs, newlines).: "Identify all fields designated as URL type in the schema (e.g., project URLs, reference links, data repository links). Iterate through each URL field and check for the presence of whitespace"
- [other] For each URL containing whitespace, record the field name, the offending URL value, and generate a warning message. Compile validation results into a report listing all flagged URLs and their locations within the document.: "record the field name, the offending URL value, and generate a warning message. Compile validation results into a report listing all flagged URLs and their locations within the document"
- [discussion] Warning to not include spaces in urls ([#75]: "Spaces in URLs not properly handled [section=discussion; evidence='Warning to not include spaces in urls ([#75]']"
- [other] make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory: "make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory"
