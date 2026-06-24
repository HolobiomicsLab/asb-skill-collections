---
name: qc-workflow-component-inspection
description: Use when you have acquired a versioned QC workflow definition file (YAML
  or JSON) from a metabolomics QC system release (e.g., v1.0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - manual expert review
  - QC4Metabolomics
  license_tier: restricted
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

# qc-workflow-component-inspection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Reconstruct and validate the structural integrity of QC workflow component definitions bundled in metabolomics software releases. This skill verifies schema compliance, field presence, and type consistency across workflow metadata and step declarations.

## When to use

Apply this skill when you have acquired a versioned QC workflow definition file (YAML or JSON) from a metabolomics QC system release (e.g., v1.0.0) and need to verify that all required workflow metadata fields (name, version, inputs, outputs, steps) are present, properly structured, and type-consistent before downstream integration or execution.

## When NOT to use

- The workflow definition is already validated and integrated into a running pipeline.
- You lack the schema specification or validation rules for the target release version.

## Inputs

- workflow definition file (YAML or JSON format)
- v1.0.0 schema specification or validation rules
- commit reference or repository snapshot

## Outputs

- parsed workflow component structure
- validation report (schema compliance, errors, warnings)
- structured metadata fields (name, version, inputs, outputs, steps)

## How to apply

Locate the workflow definition file in the target repository commit. Parse the file using a YAML or JSON schema validator appropriate to the declared v1.0.0 specification. Verify presence of all required qc_workflow_component fields and validate that metadata (name, version, inputs, outputs, steps) conform to expected types and structure. Scan for syntax errors, undefined references, and type mismatches across component definitions. Generate a validation report documenting schema compliance and any detected structural issues.

## Related tools

- **QC4Metabolomics** (source repository containing workflow component definitions for metabolomics QC systems) — http://stanstrup.github.io/QC4Metabolomics/

## Evaluation signals

- All required workflow metadata fields are present and non-null
- No syntax errors or undefined references detected in the parsed structure
- Field types (string, list, dict) match the schema specification
- qc_workflow_component declaration is structurally valid according to v1.0.0 rules
- Validation report documents zero critical schema violations

## Limitations

- Validation scope is limited to structural and type consistency; runtime behavior or execution errors are not detected by this inspection alone.
- Schema validation depends on availability of the exact v1.0.0 specification; mismatched or missing schema definitions will reduce validation fidelity.
- Manual expert review may be required to interpret validation warnings or detect domain-specific semantic errors beyond schema conformance.

## Evidence

- [other] What is the structure and composition of the QC workflow definition file declared in commit d441874 for the v1.0.0 release of QC4metabolomics?: "the structure and composition of the QC workflow definition file declared in commit d441874 for the v1.0.0 release"
- [other] 1. Locate the workflow definition file in the QC4metabolomics repository (commit d441874). 2. Parse the workflow definition using a YAML or JSON schema validator appropriate to v1.0.0 specification. 3. Verify presence and structural integrity of the qc_workflow_component declaration. 4. Validate all required workflow metadata fields (name, version, inputs, outputs, steps). 5. Check for syntax errors, undefined references, and type consistency across component definitions. 6. Generate a validation report documenting schema compliance and any detected issues.: "Validate all required workflow metadata fields (name, version, inputs, outputs, steps). 5. Check for syntax errors, undefined references, and type consistency across component definitions. 6."
- [readme] QC systems for metabolomics studies: "QC systems for metabolomics studies"
