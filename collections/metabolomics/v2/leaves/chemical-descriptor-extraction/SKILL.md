---
name: chemical-descriptor-extraction
description: Use when you have standardized molecular structures (SMILES or SDF format)
  and need to generate a uniform feature matrix for machine learning models (e.g.,
  retention time prediction).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0360
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
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

# chemical-descriptor-extraction

## Summary

Compute a standardized table of molecular fingerprints and chemical descriptors (e.g., molecular weight, LogP, hydrogen bond donors/acceptors, rotatable bonds) from PubChem-standardized molecular structures using rcdk. This skill bridges molecular structure input to feature-rich representations suitable for retention time prediction and small-molecule identification models.

## When to use

You have standardized molecular structures (SMILES or SDF format) and need to generate a uniform feature matrix for machine learning models (e.g., retention time prediction). Apply this skill when you are building or training models that require both fingerprint-based similarity metrics and physicochemical property descriptors as input features.

## When NOT to use

- Input structures are not PubChem-standardized or have not been validated for consistency (standardize first with PubChem protocol before applying this skill).
- You already have a pre-computed feature matrix or descriptor table and need only to integrate it into a downstream model.
- Your workflow requires only molecular classification (use ClassyFire instead) and not descriptor/fingerprint feature engineering.

## Inputs

- Standardized molecular structures in SMILES format
- Standardized molecular structures in SDF format
- Molecule identifier list

## Outputs

- CSV or TSV feature table with molecule identifiers as rows
- Molecular fingerprint bit columns (binary values)
- Chemical descriptor columns (numeric values: molecular weight, LogP, H-bond donors/acceptors, rotatable bonds, etc.)

## How to apply

Load standardized molecular structures (SMILES or SDF) from input files. Use rcdk to calculate molecular fingerprints (e.g., ECFP, FCFP) and standard chemical descriptors (molecular weight, LogP, hydrogen bond donors/acceptors, rotatable bonds, and other standard molecular properties). Compile fingerprints and descriptors into a single table with molecule identifiers as rows and fingerprint bits / descriptor columns. Verify that no missing values appear in descriptor columns and that fingerprint bits are binary (0/1). Export the feature table to CSV or TSV format with a header row naming each fingerprint bit and descriptor field.

## Related tools

- **rcdk** (Calculates molecular fingerprints (ECFP, FCFP) and chemical descriptors (molecular weight, LogP, H-bond donors/acceptors, rotatable bonds) from standardized structures)
- **PubChem standardization** (Pre-processes molecular structures to ensure consistency before fingerprint and descriptor calculation) — https://pubchem.ncbi.nlm.nih.gov/

## Evaluation signals

- Feature table contains no missing values in descriptor columns; all rows have complete data.
- Fingerprint bit columns contain only binary values (0 or 1); no intermediate or fractional values present.
- Molecular weight values fall within known biological ranges (typically 50–1000 Da for small molecules in metabolomics).
- LogP values are within typical ranges for drug-like molecules (approximately −5 to +5).
- Header row names match the expected descriptor fields and fingerprint bit identifiers; table structure matches input molecule count (one row per unique identifier).

## Limitations

- rcdk descriptor calculation depends on the quality and consistency of PubChem standardization; poorly standardized or non-standard structures will produce incorrect or undefined descriptors.
- Some molecular structures may lack valid rcdk fingerprints or descriptor values if they contain unusual functional groups or atoms not recognized by rcdk (e.g., exotic isotopes or organometallic centers).
- Fingerprint type choice (ECFP, FCFP, etc.) impacts downstream model performance and must be selected based on the retention time prediction use case; no single fingerprint type is universally optimal.

## Evidence

- [readme] structures are standardized using the PubChem standardization: "From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk."
- [readme] molecular fingerprints and chemical descriptors are calculated using rcdk: "From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk."
- [other] fingerprint bits / descriptor columns workflow: "Compile fingerprints and descriptors into a single table with molecule identifiers as rows and fingerprint bits / descriptor columns. 6. Export table to CSV or TSV format with header row naming each"
- [other] descriptor types calculated: "Calculate chemical descriptors using rcdk (e.g., molecular weight, LogP, hydrogen bond donors/acceptors, rotatable bonds, and other standard molecular properties)."
- [other] fingerprint types supported: "Calculate molecular fingerprints using rcdk (e.g., ECFP, FCFP, or other available fingerprint types)."
