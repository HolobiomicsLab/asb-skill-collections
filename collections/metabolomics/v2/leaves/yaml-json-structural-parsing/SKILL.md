---
name: yaml-json-structural-parsing
description: Use when you have a versioned workflow definition file (YAML or JSON)
  from a specific release commit and need to verify it conforms to the project's schema
  specification, validate the presence of all required metadata fields (name, version,
  inputs, outputs, steps), and detect syntax errors or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0339
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - manual expert review
  - QC4metabolomics
  - YAML schema validator
  - JSON schema validator
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c07078
  title: qc4metabolomics
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qc4metabolomics
    doi: 10.1021/acs.analchem.4c07078
    title: qc4metabolomics
  dedup_kept_from: coll_qc4metabolomics
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c07078
  all_source_dois:
  - 10.1021/acs.analchem.4c07078
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# yaml-json-structural-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and validate workflow definition files (YAML or JSON) against schema specifications to verify structural integrity, required metadata fields, and type consistency. This skill is essential when reconstructing or auditing versioned workflow components bundled as release assets.

## When to use

You have a versioned workflow definition file (YAML or JSON) from a specific release commit and need to verify it conforms to the project's schema specification, validate the presence of all required metadata fields (name, version, inputs, outputs, steps), and detect syntax errors or undefined references before downstream processing.

## When NOT to use

- The workflow definition file is already known to be schema-compliant and has been recently validated in production.
- You are performing runtime execution of the workflow rather than static structural inspection.
- The file format is neither YAML nor JSON (e.g., plain text, proprietary binary, or custom format without a defined schema).

## Inputs

- Workflow definition file (YAML or JSON format)
- Schema specification document for the target release version
- Commit hash or release tag identifying the version to validate

## Outputs

- Validation report documenting schema compliance
- List of detected structural issues and errors
- Verified workflow component structure with field inventory

## How to apply

Locate the workflow definition file in the target commit (e.g., commit d441874 for v1.0.0). Select a YAML or JSON schema validator appropriate to the release version's specification. Parse the file and validate against the schema, checking for presence and correctness of all required metadata fields (name, version, inputs, outputs, steps). Systematically verify type consistency, reference resolution, and absence of syntax errors across all component declarations. Document all findings in a validation report that details schema compliance status and itemizes any detected structural issues.

## Related tools

- **QC4metabolomics** (Source project implementing QC systems with versioned workflow components; workflow definition file is a primary artifact of this project) — http://stanstrup.github.io/QC4Metabolomics/
- **YAML schema validator** (Parses and validates YAML syntax and structural conformance to version-specific schema)
- **JSON schema validator** (Parses and validates JSON syntax and structural conformance to version-specific schema)

## Evaluation signals

- All required workflow metadata fields (name, version, inputs, outputs, steps) are present and non-empty.
- Schema validator reports zero syntax errors and zero undefined reference warnings.
- Type consistency check passes: all field values match the declared schema types (string, array, object, etc.).
- Component declarations resolve without circular or missing dependencies.
- Validation report confirms full schema compliance for the specified release version.

## Limitations

- Validation detects structural and schema conformance issues only; it does not verify semantic correctness or whether workflow steps will execute successfully.
- Schema validation is version-specific; a file valid for v1.0.0 may not be valid for a different release if the schema evolved.
- Manual expert review may be required to interpret or contextualize validation errors that are structurally valid but semantically suspicious.

## Evidence

- [other] Locate the workflow definition file in the QC4metabolomics repository (commit d441874). Parse the workflow definition using a YAML or JSON schema validator appropriate to v1.0.0 specification.: "Locate the workflow definition file in the QC4metabolomics repository (commit d441874). Parse the workflow definition using a YAML or JSON schema validator appropriate to v1.0.0 specification."
- [other] Validate all required workflow metadata fields (name, version, inputs, outputs, steps). Check for syntax errors, undefined references, and type consistency across component definitions.: "Validate all required workflow metadata fields (name, version, inputs, outputs, steps). Check for syntax errors, undefined references, and type consistency across component definitions."
- [other] Generate a validation report documenting schema compliance and any detected issues.: "Generate a validation report documenting schema compliance and any detected issues."
- [readme] QC systems for metabolomics studies: "QC systems for metabolomics studies"
