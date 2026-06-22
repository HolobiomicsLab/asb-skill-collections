---
name: validation-report-generation
description: Use when when you have loaded a project JSON document from the Pairing Omics Data Platform and need to identify and document constraint violations (such as whitespace in URL fields) defined in the JSON schema.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - npm
  - JSON schema validator (implied by app/public/schema.json)
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
  - build: coll_massbank_cq
    doi: 10.1002/jms.1777
    title: MassBank
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

# validation-report-generation

## Summary

Generate structured validation reports that document detected anomalies in project JSON documents by iterating through schema-defined fields, checking for constraint violations, and compiling results into a comprehensive report listing flagged items and their locations.

## When to use

When you have loaded a project JSON document from the Pairing Omics Data Platform and need to identify and document constraint violations (such as whitespace in URL fields) defined in the JSON schema. Use this skill when systematic reporting of field-level validation issues is required for quality assurance, user feedback, or data curation workflows.

## When NOT to use

- When you need to auto-correct violations rather than report them — this skill documents issues without modifying the source data.
- When validation constraints are not yet defined in the schema — the skill depends on schema field type metadata.
- When you need real-time streaming validation of incoming data rather than batch validation of stored documents.

## Inputs

- project JSON document (conforming to app/public/schema.json structure)
- JSON schema definition with field type and constraint annotations

## Outputs

- validation report (structured list of flagged fields with violation details)
- warning messages indexed by field name and document location

## How to apply

Load the project JSON document and the schema definition (app/public/schema.json) that describes field types and constraints. Iterate through each field in the JSON document that corresponds to a URL type in the schema. For each URL field, apply the validation constraint (e.g., check for whitespace characters including spaces, tabs, and newlines). When a violation is detected, record the field name, the offending value, and generate a descriptive warning message. Compile all flagged items into a structured report that lists each violation with its location within the document hierarchy, enabling downstream processes or human reviewers to assess and remediate issues.

## Related tools

- **npm** (test runner and package manager for validating that existing tests still pass after schema or validation logic changes)
- **JSON schema validator (implied by app/public/schema.json)** (defines field types, constraints, and structure against which validation rules are evaluated) — https://github.com/iomega/paired-data-form

## Evaluation signals

- All URL fields in the schema are checked; no schema-defined URL fields are skipped in the report.
- For each reported violation, the field name, offending value, and location path in the JSON document are present and accurate.
- Whitespace detection correctly identifies spaces, tabs, newlines, and other whitespace characters per the constraint definition.
- The report is deterministic and reproducible — running the validation on the same input document produces an identical report.
- The warning message format is consistent and provides sufficient context for a user or curator to locate and understand each issue.

## Limitations

- The skill detects only constraints that are explicitly defined in the schema; undocumented or implicit constraints cannot be validated.
- Whitespace detection is character-level and does not apply semantic or context-aware rules (e.g., distinguishing structural whitespace from content whitespace).
- The skill operates on static documents and does not validate dynamic constraints such as referential integrity across multiple project files.
- As noted in GitHub issue #75, the platform has historically lacked robust URL validation, meaning some projects may contain numerous violations.

## Evidence

- [other] The platform stores paired omics data projects using a JSON schema format (app/public/schema.json) that defines project structure, which serves as the basis for implementing field-level validation rules including URL format constraints.: "The platform stores paired omics data projects using a JSON schema format (app/public/schema.json) that defines project structure, which serves as the basis for implementing field-level validation"
- [other] Iterate through each URL field and check for the presence of whitespace characters (spaces, tabs, newlines). For each URL containing whitespace, record the field name, the offending URL value, and generate a warning message. Compile validation results into a report listing all flagged URLs and their locations within the document.: "For each URL containing whitespace, record the field name, the offending URL value, and generate a warning message. Compile validation results into a report listing all flagged URLs and their"
- [readme] The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project.: "The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project."
- [discussion] Warning to not include spaces in urls ([#75]: "Warning to not include spaces in urls ([#75]"
