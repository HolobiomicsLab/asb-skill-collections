---
name: data-format-conformance-checking
description: Use when you have retrieved a complete set of project JSON documents from a data platform and need to verify that each document's structure, field types, and required properties match a canonical JSON Schema definition (e.g., app/public/schema.json).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - npm
  - JSON Schema validator
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-format-conformance-checking

## Summary

Validate a collection of JSON documents against a published JSON Schema specification to identify structural and type violations. This skill ensures that all deposited data conform to the expected format before downstream processing or publication.

## When to use

Apply this skill when you have retrieved a complete set of project JSON documents from a data platform and need to verify that each document's structure, field types, and required properties match a canonical JSON Schema definition (e.g., app/public/schema.json). Use it as a quality-control step before archiving, integrating with external databases, or claiming conformance to a published specification.

## When NOT to use

- Input JSON documents are already known to be non-standard or intentionally variant from the schema (e.g., legacy data with deprecated fields).
- The JSON Schema definition itself is under active revision and not yet canonicalized.
- Only a small subset of documents needs validation; use manual spot-checking or a lighter-weight tool instead.

## Inputs

- Complete set of project JSON documents (from Paired Omics Data Platform API or web export)
- JSON Schema definition file (e.g., app/public/schema.json)

## Outputs

- Validation report listing project identifier, validation status (pass/fail), and schema violations per document
- Aggregated conformance summary (e.g., count of passing vs. non-conforming projects)

## How to apply

First, retrieve the complete set of project JSON documents from the target platform via API or web interface. Next, load the canonical JSON Schema definition from the published location (e.g., app/public/schema.json in the iomega/paired-data-form repository). Iterate over each retrieved project JSON document and validate its structure and field types against the schema using a JSON Schema validator (e.g., a Node.js JSON Schema validator library). For each validation, record the project identifier, validation status (pass/fail), and any schema violations encountered. Finally, aggregate results to confirm all documents conform or flag non-conforming projects for remediation. The rationale is to detect schema drift early, before data propagates downstream or is published to external archives.

## Related tools

- **npm** (Package manager and test harness for running JSON Schema validators and aggregating validation results in Node.js environment)
- **JSON Schema validator** (Core tool for iterating over project documents and validating structure and field types against the canonical schema definition)

## Evaluation signals

- All project documents in the validation report are marked as pass or fail with explicit status indicators.
- Each non-conforming project is listed with its specific schema violation(s) (e.g., missing required field, incorrect field type).
- Aggregated summary counts match the total number of documents queried and the number flagged for remediation is non-zero only when violations are present.
- Re-running validation after remediating non-conforming projects shows all documents passing.
- Validation report is reproducible and time-stamped, allowing comparison across platform versions or schema updates.

## Limitations

- Schema validation does not detect semantic errors (e.g., logically inconsistent but structurally valid field combinations).
- Validation relies on the canonical schema definition being accurate and up-to-date; if the schema itself contains errors or ambiguities, validation may miss or over-flag violations.
- Large document collections may require optimization to avoid timeouts; batch validation or parallel processing may be necessary.
- URL encoding issues and special characters in field values are not detected by schema validation alone (e.g., spaces in URLs reported as known issue #75).

## Evidence

- [other] research_question: Do all project JSON documents currently deposited in the Paired Omics Data Platform conform to the published JSON Schema specification?: "Do all project JSON documents currently deposited in the Paired Omics Data Platform conform to the published JSON Schema specification?"
- [other] A JSON schema (app/public/schema.json) has been published to formally describe the required format of paired omics data projects stored in the platform.: "A JSON schema (app/public/schema.json) has been published to formally describe the required format of paired omics data projects stored in the platform."
- [other] Query the Paired Omics Data Platform API or web interface to retrieve the complete set of project JSON documents currently published. Load the canonical JSON Schema definition from app/public/schema.json in the iomega/paired-data-form repository. Iterate over each retrieved project JSON document and validate its structure and field types against the schema using a JSON Schema validator.: "Query the Paired Omics Data Platform API or web interface to retrieve the complete set of project JSON documents currently published. Load the canonical JSON Schema definition from"
- [other] Generate a validation report listing each project identifier, validation status (pass/fail), and any schema violations encountered. Aggregate results to confirm all documents conform or flag non-conforming projects for remediation.: "Generate a validation report listing each project identifier, validation status (pass/fail), and any schema violations encountered."
- [readme] The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project.: "The JSON schema (app/public/schema.json) describes the format of an project."
