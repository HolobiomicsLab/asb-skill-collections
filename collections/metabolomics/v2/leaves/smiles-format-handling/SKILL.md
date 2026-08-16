---
name: smiles-format-handling
description: Use when when you have molecular structures in proprietary or non-standard
  formats (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2275
  tools:
  - rcdk
  - PubChem standardization
  license_tier: open
derived_from:
- doi: 10.1038/s41592-023-02143-z
  title: RepoRT (retention-time repository)
evidence_spans:
- molecular fingerprints and chemical descriptors are calculated using rcdk
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

# SMILES format handling

## Summary

Convert molecular structures to and from SMILES (Simplified Molecular Input Line Entry System) format to enable standardized input for fingerprint and descriptor calculation pipelines. SMILES is the canonical string representation used by RepoRT for molecular structure interchange.

## When to use

When you have molecular structures in proprietary or non-standard formats (e.g., SDF, MOL files) and need to submit them to a standardized retention time prediction or chemical descriptor pipeline that expects SMILES strings, or when you need to export computed molecular properties alongside standardized structure representations.

## When NOT to use

- Input structures are already in a standardized format (e.g., canonicalized SMILES with InChI metadata) ready for direct descriptor calculation—skip to rcdk fingerprint/descriptor step.
- You require 3D coordinate information or stereochemistry that goes beyond SMILES line notation; use 3D SDF or PDB formats instead.
- Structures contain exotic or non-organic chemistry not well-represented in standard SMILES notation (e.g., organometallic complexes, polymers).

## Inputs

- SMILES strings (single-line format)
- SDF files containing molecular structures
- Molecule identifiers (e.g., InChI keys, compound names)

## Outputs

- Standardized SMILES strings (PubChem-normalized)
- CSV/TSV table with molecule IDs, SMILES, fingerprints, and descriptors
- Validated structure representations for downstream analysis

## How to apply

Load molecular structure data in SMILES format or convert existing structure files (SDF) to SMILES strings using a chemistry toolkit. Pass SMILES strings as the primary input to downstream standardization steps. After PubChem standardization and descriptor calculation using rcdk, export the standardized structures back to SMILES format alongside computed fingerprints and descriptors in a single table (CSV/TSV) with molecule identifiers as rows and SMILES as one of the descriptor columns. Validate that SMILES strings remain valid and unique after any transformations by checking roundtrip conversion (structure → SMILES → structure) and confirming no malformed characters are present.

## Related tools

- **PubChem standardization** (Normalizes SMILES-encoded structures to canonical form before descriptor calculation)
- **rcdk** (Accepts standardized SMILES input to calculate molecular fingerprints and chemical descriptors)

## Evaluation signals

- All input SMILES strings parse successfully without syntax errors (no missing brackets, invalid atoms, or malformed charge specifications).
- Output SMILES strings remain constant length or are properly canonicalized after PubChem standardization (indicating no loss of structural information).
- Molecule identifiers map 1:1 to rows in the output CSV/TSV table with no duplicates or missing entries.
- Roundtrip validation: convert SMILES → structure → SMILES and verify the output SMILES matches the input (accounting for canonicalization rules).
- All export headers are present and columns contain expected data types (SMILES as string, fingerprints as binary/bit vectors, descriptors as numeric).

## Limitations

- SMILES notation does not preserve 3D stereochemistry or conformational information; explicit 3D coordinate data will be lost.
- Some rare or complex chemical structures (polycyclic cages, metal complexes) may not be fully representable in standard SMILES and may require manual curation or alternative formats.
- SMILES canonicalization is dependent on the specific algorithm and toolkit used; different tools may produce different canonical forms for the same structure.

## Evidence

- [other] Load standardized molecular structures (SMILES or SDF format) from input: "Load standardized molecular structures (SMILES or SDF format) from input."
- [other] Compile fingerprints and descriptors into a single table with molecule identifiers as rows and fingerprint bits / descriptor columns: "Compile fingerprints and descriptors into a single table with molecule identifiers as rows and fingerprint bits / descriptor columns."
- [readme] structures are standardized using the PubChem standardization: "From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk."
- [other] Export table to CSV or TSV format with header row naming each fingerprint bit and descriptor field: "Export table to CSV or TSV format with header row naming each fingerprint bit and descriptor field."
