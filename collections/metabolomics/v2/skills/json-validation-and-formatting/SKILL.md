---
name: json-validation-and-formatting
description: Use when after enriching a project JSON document with external metadata
  (e.g., organism names, genome identifiers) or before writing enriched JSON to disk.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3500
  tools:
  - npm
  - paired-data-form
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or
  `app/` directory
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# json-validation-and-formatting

## Summary

Validate and ensure well-formedness of JSON project documents against a schema before storage or submission. This skill detects structural errors, missing required fields, and data type mismatches that would break downstream data integration and search indexing.

## When to use

Apply this skill after enriching a project JSON document with external metadata (e.g., organism names, genome identifiers) or before writing enriched JSON to disk. Use it when project JSON files will be indexed into Elasticsearch, submitted programmatically via OpenAPI, or stored in the paired-data-form platform's file system.

## When NOT to use

- The project JSON has already been validated and stored in the platform's data directory.
- You are performing exploratory data analysis on raw, unstructured omics metadata before deciding on a project schema.

## Inputs

- Enriched project JSON document (in-memory object or file)
- JSON schema definition (app/public/schema.json)

## Outputs

- Validation status (pass/fail with error details)
- Well-formed, schema-compliant project JSON file ready for storage or submission

## How to apply

Parse the enriched project JSON document and validate it against the canonical JSON schema located at app/public/schema.json. Check that all required fields are present, that field values conform to their declared types (string, number, array, object), and that nested structures match the schema hierarchy. If validation fails, report specific field paths and error messages before writing to disk. After successful validation, ensure the JSON is properly formatted (consistent indentation, no trailing commas) before persisting. This prevents malformed documents from breaking Elasticsearch indexing or API submissions.

## Related tools

- **npm** (Run test suite (npm run test) to verify JSON validation logic in api/ and app/ directories) — https://www.npmjs.com/
- **paired-data-form** (Source of canonical JSON schema (app/public/schema.json) and web service that stores and indexes validated project JSON) — https://github.com/iomega/paired-data-form

## Evaluation signals

- Validated JSON matches all field names and types defined in app/public/schema.json
- No schema validation errors are reported; all required fields are present and populated
- Enriched document contains both original genome identifier and newly populated organism name fields without duplication or conflicting values
- JSON is syntactically well-formed (parses without errors, no trailing commas, proper nesting)
- Downstream Elasticsearch indexing or API submission of the validated JSON succeeds without schema-related failures

## Limitations

- The skill validates structural conformance to schema but does not verify semantic correctness (e.g., whether a fetched organism name is actually valid for the genome identifier used).
- Documentation on field descriptions and requirements is incomplete (issue #76), making it difficult to infer constraints beyond the schema structure.
- Schema validation does not detect spaces in URLs or other URL format issues (issue #75)—additional domain-specific validation may be needed.
- The skill operates on complete project JSON documents; it does not validate incremental updates or partial enrichment steps.

## Evidence

- [other] Validate that the enriched JSON is well-formed and contains both the original genome identifier and the newly populated organism name.: "Validate that the enriched JSON is well-formed and contains both the original genome identifier and the newly populated organism name."
- [readme] The JSON schema (app/public/schema.json) describes the format of an project.: "The JSON schema (app/public/schema.json) describes the format of an project."
- [readme] The web service stores each project as a file on disk. The application offers full text search functionality via web services using an elastic search (v7.6.2) index.: "The web service stores each project as a file on disk. The application offers full text search functionality via web services using an elastic search (v7.6.2) index."
- [other] make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory: "make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory"
