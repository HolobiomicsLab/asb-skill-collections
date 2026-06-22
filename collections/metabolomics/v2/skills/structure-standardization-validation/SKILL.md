---
name: structure-standardization-validation
description: Use when you have raw or heterogeneous molecular structure inputs (SMILES strings or SDF files) that will be used for fingerprint calculation, descriptor extraction, or retention time prediction modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - PubChem standardization
  - rcdk
derived_from:
- doi: 10.1038/s41592-023-02143-z
  title: RepoRT (retention-time repository)
evidence_spans:
- structures are standardized using the PubChem standardization
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

# structure-standardization-validation

## Summary

Standardize molecular structures using PubChem standardization protocol to ensure consistency and validity before downstream chemical descriptor and fingerprint calculation. This preprocessing step guarantees that all input structures (SMILES or SDF format) conform to a uniform chemical representation suitable for comparative analysis.

## When to use

Apply this skill when you have raw or heterogeneous molecular structure inputs (SMILES strings or SDF files) that will be used for fingerprint calculation, descriptor extraction, or retention time prediction modeling. Use it before any machine learning feature engineering or retention time model development to ensure all molecules are represented in a canonical, standardized form.

## When NOT to use

- Input structures are already validated and standardized by an upstream workflow — skip to fingerprint calculation directly.
- Working with large peptides, proteins, or macromolecules outside the small-molecule scope of the RepoRT pipeline.
- Structures are already in a project-specific canonical form and interoperability with PubChem standardization is not required.

## Inputs

- molecular structures in SMILES format
- molecular structures in SDF format
- molecule identifiers (to track structures through standardization)

## Outputs

- standardized molecular structures in SMILES format
- standardized molecular structures in SDF format
- standardization status report (indicating success/failure per molecule)

## How to apply

Load molecular structures from input files in SMILES or SDF format. Apply the PubChem standardization protocol to each structure, which normalizes chemical representation, resolves stereochemistry ambiguities, and corrects common structural errors. Validate that standardization completed without loss or corruption by checking that each input structure produces exactly one standardized output structure. Retain the standardized structures in the same format (SMILES or SDF) for export to the next workflow step (fingerprint and descriptor calculation). The standardized structures serve as the authoritative chemical representation for all subsequent analyses in the retention time prediction pipeline.

## Related tools

- **PubChem standardization** (Applies chemical standardization protocol to normalize molecular structures, resolve stereochemistry, and ensure canonical representation for fingerprint and descriptor calculation)

## Evaluation signals

- Each input structure yields exactly one standardized output structure with no loss or rejection.
- Standardized structures conform to PubChem canonical SMILES or SDF format (deterministic, reproducible across runs).
- Molecule identifiers and standardized structures are correctly paired in the output table with no row misalignment.
- Standardization does not introduce or remove heavy atoms, stereocenters, or functional groups — only normalizes representation.
- Downstream fingerprint and descriptor calculation produces consistent, non-null results for all standardized structures.

## Limitations

- PubChem standardization may reject or alter structures with unusual or non-standard chemical entities; such structures should be reviewed and potentially excluded from the training dataset.
- Standardization resolves many stereochemical ambiguities, but explicitly undefined or contradictory stereochemistry in input structures may be lost or corrected in unpredictable ways — validation against known stereochemistry is advised.
- Very large molecules or highly complex polycyclic structures may timeout or fail during standardization; consider filtering by molecular weight or complexity if needed.

## Evidence

- [intro] structures are standardized using the PubChem standardization: "structures are standardized using the PubChem standardization"
- [readme] standardization ensures consistency before fingerprint/descriptor calculation: "From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk."
- [other] workflow step definition: "1. Load standardized molecular structures (SMILES or SDF format) from input. 2. Standardize structures using PubChem standardization protocol to ensure consistency."
