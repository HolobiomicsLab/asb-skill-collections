---
name: molecular-fingerprint-calculation
description: Use when you have a collection of small molecules in standardized format (SMILES or SDF) that require quantitative chemical feature representation for machine learning or comparative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - rcdk
  - PubChem standardization
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-fingerprint-calculation

## Summary

Compute molecular fingerprints and chemical descriptors from standardized chemical structures using rcdk, generating a feature table suitable for retention time prediction model training. This skill transforms SMILES or SDF input into a normalized descriptor matrix with fingerprint bits and molecular properties as columns.

## When to use

Apply this skill when you have a collection of small molecules in standardized format (SMILES or SDF) that require quantitative chemical feature representation for machine learning or comparative analysis. Use it as the feature engineering step after PubChem standardization and before model training or molecular classification.

## When NOT to use

- Input structures have not been standardized using PubChem standardization — apply standardization first
- Output is already a computed fingerprint or descriptor table — this skill is redundant
- You require only structural classification (use ClassyFire instead) without numerical fingerprint features
- Input molecules lack clear SMILES or SDF representation due to ambiguous or invalid chemical notation

## Inputs

- Standardized molecular structures in SMILES format
- Standardized molecular structures in SDF format
- Molecule identifiers or names

## Outputs

- CSV or TSV feature table with molecule identifiers as rows
- Molecular fingerprint bits (columns)
- Chemical descriptor values (columns: molecular weight, LogP, hydrogen bond donors/acceptors, rotatable bonds, etc.)

## How to apply

First, ensure input structures have been standardized using PubChem standardization protocol to guarantee consistency across the molecular dataset. Load the standardized structures from SMILES or SDF format. Use rcdk to calculate molecular fingerprints (e.g., ECFP, FCFP, or other available types) and chemical descriptors (molecular weight, LogP, hydrogen bond donors/acceptors, rotatable bonds, and other standard molecular properties). Compile all fingerprints and descriptors into a single table with molecule identifiers as rows and fingerprint bits / descriptor columns. Validate that the fingerprint type and descriptor set match the requirements of downstream models (e.g., retention time prediction). Export the resulting feature matrix to CSV or TSF format with a header row naming each fingerprint bit and descriptor field.

## Related tools

- **rcdk** (Calculates molecular fingerprints (ECFP, FCFP, etc.) and chemical descriptors from standardized structures)
- **PubChem standardization** (Standardizes input molecular structures prior to fingerprint calculation to ensure consistency)

## Evaluation signals

- Output CSV/TSV has number of rows equal to number of input molecules and contains molecule identifiers
- All columns are numeric (fingerprint bits 0/1 or descriptor values with expected ranges: MW > 0, LogP typically −5 to +5, H-bond counts ≥ 0)
- Header row names each fingerprint bit and descriptor field unambiguously
- No missing values (NaN or null) in the feature matrix; if present, document reason (e.g., calculation failure for specific molecule)
- Fingerprint bit cardinality and descriptor set match the rcdk configuration and documented parameters

## Limitations

- Fingerprint calculation depends on quality of input structure standardization; invalid or ambiguous SMILES will produce erroneous features
- rcdk descriptor set is fixed; highly specialized molecular properties not in the standard rcdk library cannot be computed with this skill
- Fingerprint type (ECFP vs. FCFP) significantly affects feature space dimensionality and interpretation; choice must be justified for the downstream model
- Very large molecular datasets may exceed memory constraints during simultaneous fingerprint calculation; batch processing may be required

## Evidence

- [other] Molecular fingerprints and chemical descriptors are calculated using rcdk following PubChem standardization of input structures.: "Molecular fingerprints and chemical descriptors are calculated using rcdk following PubChem standardization of input structures."
- [other] Load standardized molecular structures (SMILES or SDF format) from input. Standardize structures using PubChem standardization protocol to ensure consistency. Calculate molecular fingerprints using rcdk (e.g., ECFP, FCFP, or other available fingerprint types). Calculate chemical descriptors using rcdk (e.g., molecular weight, LogP, hydrogen bond donors/acceptors, rotatable bonds, and other standard molecular properties). Compile fingerprints and descriptors into a single table with molecule identifiers as rows and fingerprint bits / descriptor columns. Export table to CSV or TSV format with header row naming each fingerprint bit and descriptor field.: "Load standardized molecular structures (SMILES or SDF format) from input. Standardize structures using PubChem standardization protocol to ensure consistency. Calculate molecular fingerprints using"
- [readme] From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk.: "From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk."
