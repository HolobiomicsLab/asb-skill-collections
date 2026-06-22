---
name: url-format-constraint-checking
description: Use when ingesting or validating project JSON documents against a schema (such as app/public/schema.json in the Pairing Omics Data Platform) that designates certain fields as URL type (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3674
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
---

# url-format-constraint-checking

## Summary

Validate URL fields in JSON project documents by detecting and flagging embedded whitespace characters that violate URL syntax. This skill ensures data quality in omics platforms that store structured project metadata with URL references.

## When to use

Apply this skill when ingesting or validating project JSON documents against a schema (such as app/public/schema.json in the Pairing Omics Data Platform) that designates certain fields as URL type (e.g., project URLs, reference links, data repository links) and you need to flag invalid entries before storage or publication.

## When NOT to use

- Input documents that have already passed upstream URL validation (to avoid redundant checks)
- URL fields that are intentionally permitted to contain encoded whitespace (%20 sequences) — this skill detects literal whitespace only, not properly encoded equivalents

## Inputs

- project JSON document (e.g., output from web form submission or programmatic API call)
- JSON schema file defining field types and constraints (e.g., app/public/schema.json)

## Outputs

- validation report listing flagged URLs with field names, offending values, and document locations
- warning/error messages for each URL containing whitespace

## How to apply

Load a project JSON document and cross-reference it against the platform's JSON schema to identify all fields designated as URL type. Iterate through each URL field value and check for the presence of whitespace characters (spaces, tabs, newlines), which are invalid in URLs according to RFC 3986. For each URL containing whitespace, record the field name, the offending URL value, and the location within the document. Compile validation results into a report listing all flagged URLs and their field paths. This prevents silent data corruption and supports data quality assurance workflows, as documented in the platform's issue tracking where spaces in URLs have been flagged as a known problem.

## Related tools

- **npm** (test runner and build tool for executing validation logic in api/ and app/ directories using npm run test commands)

## Evaluation signals

- All URL-type fields from the JSON schema are checked (coverage = 100% of designated URL fields)
- Every whitespace character (space, tab, newline) present in any URL field is detected and reported
- Flagged URLs are accompanied by correct field path and original value (no truncation or encoding)
- Validation report is machine-readable and can be consumed downstream (e.g., by CI/CD pipelines or review workflows)
- No false positives on properly formatted URLs without whitespace

## Limitations

- Detects only literal whitespace characters; does not validate other URL format constraints (e.g., invalid characters, malformed schemes, domain syntax)
- Requires that the input document is valid JSON and that the schema file is present and correctly formatted
- Does not validate that URLs are reachable or that linked resources exist; scope is syntactic only

## Evidence

- [other] Identify all fields designated as URL type in the schema (e.g., project URLs, reference links, data repository links): "Identify all fields designated as URL type in the schema (e.g., project URLs, reference links, data repository links)."
- [other] check for the presence of whitespace characters (spaces, tabs, newlines): "Iterate through each URL field and check for the presence of whitespace characters (spaces, tabs, newlines)."
- [other] The platform stores paired omics data projects using a JSON schema format (app/public/schema.json) that defines project structure, which serves as the basis for implementing field-level validation rules including URL format constraints.: "The platform stores paired omics data projects using a JSON schema format (app/public/schema.json) that defines project structure, which serves as the basis for implementing field-level validation"
- [discussion] Warning to not include spaces in urls: "Spaces in URLs not properly handled [section=discussion; evidence='Warning to not include spaces in urls ([#75]']"
- [readme] The JSON schema (app/public/schema.json) describes the format of an project.: "The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project."
