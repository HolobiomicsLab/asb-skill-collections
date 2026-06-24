---
name: molecular-format-conversion
description: Use when when ingesting raw chemical structure data from multiple external
  sources (publications, databases, contributor submissions) that use different molecular
  file formats (SMILES strings, SDF files, or other representations), and you need
  to unify them into a single canonical format before.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - PubChem standardization
  - rcdk
  license_tier: open
derived_from:
- doi: 10.1038/s41592-023-02143-z
  title: RepoRT (retention-time repository)
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_report_retention_time_repository_cq
    doi: 10.1038/s41592-023-02143-z
    title: RepoRT (retention-time repository)
  dedup_kept_from: coll_report_retention_time_repository_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-023-02143-z
  all_source_dois:
  - 10.1038/s41592-023-02143-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-format-conversion

## Summary

Convert raw chemical structures from heterogeneous input formats (SMILES, SDF, or other molecular representations) into a standardized canonical format for downstream processing in retention time prediction and molecular identification workflows. This skill ensures consistent molecular representation across diverse data sources collected into the RepoRT repository.

## When to use

When ingesting raw chemical structure data from multiple external sources (publications, databases, contributor submissions) that use different molecular file formats (SMILES strings, SDF files, or other representations), and you need to unify them into a single canonical format before applying PubChem standardization, calculating molecular descriptors, or building retention time prediction models.

## When NOT to use

- Structures are already in a standardized, canonical format and have passed validation
- Input data contains only molecular properties or descriptors (no structural data)
- Raw structures are malformed or contain unrecoverable syntax errors that prevent parsing

## Inputs

- Raw chemical structures in SMILES format
- Raw chemical structures in SDF format
- Raw chemical structures in other molecular file formats

## Outputs

- Chemical structures in canonical output format
- Validated structures passing format conversion
- Conversion error log (structures that failed conversion)

## How to apply

Load raw chemical structures in their native input format (SMILES, SDF, or other molecular representation). Apply format conversion to translate each structure into a canonical output format suitable for downstream standardization and descriptor calculation. Validate that converted structures maintain chemical validity and retain structural information without loss or corruption during the conversion process. Structures that fail conversion should be flagged and excluded from further analysis. The converted structures are then passed to the PubChem standardization step to normalize representation, remove salts, and canonicalize connectivity before retention time model development.

## Related tools

- **PubChem standardization** (Downstream standardization procedure applied after format conversion to normalize molecular representation, remove salts, and canonicalize connectivity)
- **rcdk** (Post-standardization tool for calculating molecular fingerprints and chemical descriptors from converted and standardized structures)

## Evaluation signals

- All structures successfully convert from input format without syntax or parsing errors
- Converted structures maintain chemical validity and can be read back into molecular software without data loss
- Canonical output format is consistent across all converted structures (e.g., all use the same SMILES canonical rules or SDF variant)
- Structures that could not be converted are logged with diagnostic error messages for manual review
- Downstream PubChem standardization step runs without format-related failures on the converted structures

## Limitations

- Conversion fidelity depends on whether the source format fully encodes all structural features (e.g., stereochemistry, formal charges, isotope labels); lossy formats may degrade chemical information
- Some molecular formats (particularly loosely-defined SMILES variants) may have ambiguous or non-canonical representations that convert differently across tools, leading to standardization artifacts downstream
- No changelog or versioning information is provided for the conversion workflow, so reproducibility may be compromised if conversion tool versions or configuration drift over time

## Evidence

- [other] Load raw chemical structures (SMILES, SDF, or other molecular format) from input dataset: "Load raw chemical structures (SMILES, SDF, or other molecular format) from input dataset."
- [other] Validate standardized structures for chemical validity and retain only structures that pass standardization without error: "Validate standardized structures for chemical validity and retain only structures that pass standardization without error."
- [readme] From the input data structures are standardized using the PubChem standardization: "From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk."
- [other] Export standardized structures to canonical output format: "Export standardized structures to canonical output format."
