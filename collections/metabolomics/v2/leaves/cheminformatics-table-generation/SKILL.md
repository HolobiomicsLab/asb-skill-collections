---
name: cheminformatics-table-generation
description: Use when when you have standardized molecular structures (SMILES or SDF
  format) and need to compute molecular fingerprint bits and chemical property descriptors
  for downstream retention time prediction, molecular classification, or machine-learning-based
  identification tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
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

# cheminformatics-table-generation

## Summary

Generate a structured table of molecular fingerprints and chemical descriptors from standardized chemical structures using rcdk, suitable for retention time prediction model training and small-molecule identification workflows. This skill converts SMILES or SDF inputs into machine-learning-ready feature matrices.

## When to use

When you have standardized molecular structures (SMILES or SDF format) and need to compute molecular fingerprint bits and chemical property descriptors for downstream retention time prediction, molecular classification, or machine-learning-based identification tasks. Apply this skill after structure standardization and before model training or property-based analysis.

## When NOT to use

- Input structures are not yet standardized using PubChem protocol — standardize first.
- Molecular structures are in non-standard or proprietary formats not parseable by rcdk.
- You need only a single descriptor or fingerprint for a single molecule — this skill is designed for batch table generation and would be overkill for one-off calculations.

## Inputs

- Standardized molecular structures (SMILES strings or SDF file)
- List of molecule identifiers (IDs, names, or InChI keys)
- Configuration specifying which fingerprint types to calculate (e.g., ECFP, FCFP)
- Configuration specifying which chemical descriptors to compute (e.g., molecular weight, LogP, HBA, HBD, rotatable bonds)

## Outputs

- Fingerprint and descriptor table (CSV or TSV format)
- Table with molecule identifiers as row names
- Fingerprint bit columns (binary or count values)
- Descriptor columns (numeric values with appropriate units or log scale)
- Header row with standardized field names

## How to apply

First, load standardized molecular structures in SMILES or SDF format from input files; structures should have already been standardized using PubChem standardization protocol. Second, use rcdk to calculate molecular fingerprints (e.g., ECFP, FCFP types) and chemical descriptors (molecular weight, LogP, hydrogen bond donors/acceptors, rotatable bonds, and other standard molecular properties). Third, compile the fingerprint bits and descriptor values into a single table with molecule identifiers as rows and each fingerprint bit or descriptor field as columns. Fourth, add a header row naming each fingerprint bit and descriptor field unambiguously. Finally, export the completed table to CSV or TSF format with proper delimiters and quoting to preserve column structure.

## Related tools

- **rcdk** (Calculate molecular fingerprints (ECFP, FCFP) and chemical descriptors (molecular weight, LogP, HBD, HBA, rotatable bonds) from standardized structures)
- **PubChem standardization** (Standardize input molecular structures prior to fingerprint and descriptor calculation to ensure consistency)

## Evaluation signals

- Output table has correct number of rows matching input molecule count with no missing or duplicated identifiers.
- All fingerprint bit columns contain only binary (0/1) or non-negative integer count values; no NaN or null entries unless structure could not be parsed.
- All descriptor columns contain numeric values within expected chemical ranges (e.g., molecular weight > 0, LogP ∈ [−10, 10], HBA/HBD ∈ [0, 50]).
- Header row names are unique, non-empty, and match the fingerprint type and descriptor names specified in the configuration.
- Table can be successfully read back into a machine-learning framework (e.g., pandas, sklearn, R data.frame) without parsing errors; column dtypes are numeric.

## Limitations

- rcdk may fail to compute fingerprints or descriptors for structures containing non-standard atoms, radicals, or multiple disconnected components; such rows should be flagged or excluded.
- Fingerprint type (ECFP vs. FCFP) and radius/diameter parameters affect bit sparsity and interpretability; users must specify these consistently across analyses to ensure comparability.
- The output table does not include retention time labels or chromatographic metadata; those are collected separately and must be joined on molecule identifier for model training.
- Large chemical descriptor sets (>200 columns) may introduce multicollinearity and require feature selection or dimensionality reduction before model training.

## Evidence

- [other] From the workflow in task_002: "Load standardized molecular structures (SMILES or SDF format) from input. Standardize structures using PubChem standardization protocol to ensure consistency. Calculate molecular fingerprints using"
- [readme] From README: "From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk."
