---
name: chemical-structure-standardization
description: Use when when you have raw molecular structures in SMILES or SDF format that must be prepared as input to a descriptor-based classifier (e.g., BitterPredict).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - BitterPredict
  - RDKit
  - BitterPredict.m
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bittermass
    doi: 10.1021/acs.jafc.3c09767
    title: bittermass
  dedup_kept_from: coll_bittermass
schema_version: 0.2.0
---

# chemical-structure-standardization

## Summary

Parse and validate raw molecular structures in SMILES or SDF format, converting them into canonicalized representations suitable for descriptor calculation and chemical informatics pipelines. This skill ensures structural integrity before downstream analysis.

## When to use

When you have raw molecular structures in SMILES or SDF format that must be prepared as input to a descriptor-based classifier (e.g., BitterPredict). Apply this skill when the source structures have not yet been validated for syntax errors or canonicalized, and you need to feed clean structures into a cheminformatics parser for descriptor generation.

## When NOT to use

- Input structures are already in pre-computed descriptor format (CSV/Excel) — descriptor calculation is not needed.
- Descriptor preparation workflow is already documented and enforced upstream; only apply if structures lack validation or canonicalization.
- The analysis goal does not require descriptor-based machine learning classification (e.g., structure visualization or 2D similarity search may not require full canonicalization).

## Inputs

- SMILES format molecular structure strings
- SDF (Structure Data Format) files containing molecular structures

## Outputs

- Validated and canonicalized molecular structure representations (as Python RDKit mol objects or equivalent canonical SMILES)
- QC report indicating number of structures validated, rejected, or corrected

## How to apply

Load raw molecular structures from SMILES or SDF files into a cheminformatics parser such as RDKit. Validate the syntax of each molecular representation to detect and reject malformed structures. Canonicalize valid structures to a standard form to ensure consistency across the dataset. Document rejection or correction of any structures that fail validation. Pass the validated and canonicalized structure set to the next workflow step (descriptor calculation). The rationale is that molecular descriptors depend on correct structural interpretation; invalid or non-canonical input will produce unreliable or non-comparable descriptor values, compromising downstream classification.

## Related tools

- **RDKit** (Cheminformatics parser for validating molecular structure syntax and canonicalizing SMILES/SDF representations)
- **BitterPredict.m** (Downstream classifier that consumes descriptor tables derived from standardized molecular structures) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- All input SMILES/SDF strings parse without errors in the cheminformatics parser; any that raise exceptions are logged.
- Canonicalized SMILES output is deterministic: re-parsing the same structure yields identical canonical form.
- No loss of molecular connectivity or stereochemistry during validation and canonicalization; structure graphs remain equivalent.
- Output structures pass a round-trip test: canonical SMILES → mol object → canonical SMILES yields identical strings.
- QC report confirms 100% of structures were processed (either validated or documented as rejected); no silent failures.

## Limitations

- SMILES and SDF parsers assume standard chemical notation; non-standard or proprietary formats may fail silently or produce incorrect interpretations.
- Canonicalization is parser-specific (RDKit vs. other engines may produce different canonical forms); ensure consistency across the pipeline.
- Highly unusual or hypothetical structures (e.g., very large molecules, exotic bond types) may not be supported by the parser.
- README notes that 'full code will be available upon publication'; implementation details and edge case handling are not yet publicly documented.

## Evidence

- [other] Load raw molecular structures in SMILES or SDF format. 2. Parse and validate molecular structure syntax using a cheminformatics parser (e.g., RDKit).: "Load raw molecular structures in SMILES or SDF format. 2. Parse and validate molecular structure syntax using a cheminformatics parser (e.g., RDKit)."
- [other] BitterPredict.m accepts CSV or Excel files containing pre-computed molecular descriptors as input, which must be prepared prior to classification: "BitterPredict.m accepts CSV or Excel files containing pre-computed molecular descriptors as input, which must be prepared prior to classification"
- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules"
