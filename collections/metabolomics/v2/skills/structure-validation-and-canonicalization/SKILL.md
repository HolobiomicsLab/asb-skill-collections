---
name: structure-validation-and-canonicalization
description: Use when ingesting heterogeneous raw chemical structures from external datasets, publications, or user submissions into a retention time or molecular property prediction pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3966
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - PubChem standardization
  - rcdk
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
---

# structure-validation-and-canonicalization

## Summary

Standardize and validate raw chemical structures (SMILES, SDF, or other molecular formats) using PubChem's standardization procedure to normalize representation, remove salts, canonicalize connectivity, and ensure chemical validity for downstream analysis in retention time prediction and small-molecule identification pipelines.

## When to use

Apply this skill when ingesting heterogeneous raw chemical structures from external datasets, publications, or user submissions into a retention time or molecular property prediction pipeline. Trigger conditions: input structures are in non-canonical formats (mixed SMILES variants, unnormalized SDF files, or structures with explicit salts/counterions), or when downstream tools (molecular fingerprinting, classification, retention time modeling) require chemically valid, canonicalized input.

## When NOT to use

- Structures are already canonicalized and validated by an upstream standardization step.
- Input contains only abstract molecular descriptors or pre-computed fingerprints (no structures).
- Retention time prediction or classification is not part of the intended downstream workflow.

## Inputs

- Raw chemical structures in SMILES format
- Raw chemical structures in SDF format
- Raw chemical structures in other molecular formats
- Tabular dataset with chemical identifiers and structure columns

## Outputs

- Canonicalized chemical structures (canonical SMILES or standardized SDF)
- Validated structure dataset (structures passing chemical validity checks)
- Standardization metadata (e.g., pass/fail flags, error logs for failed structures)

## How to apply

Load raw chemical structures in any common molecular format (SMILES, SDF, or others) from the input dataset. Apply the PubChem standardization procedure to each structure, which normalizes representation, removes explicit salts and counterions, and canonicalizes connectivity according to PubChem's protocol. Validate each standardized structure for chemical validity (e.g., proper valence, connectivity, absence of undefined atoms or bonds). Retain only structures that pass standardization without error; discard or flag structures that fail validation. Export the standardized, validated structures to a canonical output format (e.g., canonical SMILES or standardized SDF) for use in fingerprinting, classification, and downstream modeling steps.

## Related tools

- **PubChem standardization** (Normalize molecular representation, remove salts, and canonicalize connectivity for all input structures)
- **rcdk** (Calculate molecular fingerprints and chemical descriptors on standardized structures for downstream property prediction)

## Evaluation signals

- All input structures are successfully standardized without error; the standardized-structure output file has the same record count as the input, or the error log documents all discarded structures with reasons.
- Standardized structures are in canonical form (e.g., canonical SMILES are consistent across repeated standardization runs; identical molecules in different input formats map to the same canonical SMILES).
- No explicit salts, counterions, or disconnected fragments remain in standardized output; structures comply with PubChem standardization protocol.
- Downstream tools (rcdk fingerprinting, ClassyFire classification) accept all standardized structures without parse errors or valence warnings.
- Retentions time prediction models trained on standardized structures show reproducible model performance and feature importance metrics across validation folds.

## Limitations

- Standardization may alter or remove chemical information in highly unusual or non-standard structures; salt removal could affect compounds intended as salt forms.
- Structures with undefined stereochemistry or ambiguous connectivity may fail validation despite being chemically plausible.
- PubChem standardization is optimized for organic small molecules; inorganic compounds, metals, or unusual coordinated systems may not standardize correctly.
- Large-scale standardization can be computationally expensive; performance depends on dataset size and structure complexity.

## Evidence

- [other] Raw input structures are standardized using the PubChem standardization procedure as part of the RepoRT pipeline.: "Raw input structures are standardized using the PubChem standardization procedure as part of the RepoRT pipeline."
- [other] Load raw chemical structures (SMILES, SDF, or other molecular format) from input dataset. Apply PubChem standardization procedure to each structure to normalize representation, remove salts, and canonicalize connectivity.: "Load raw chemical structures (SMILES, SDF, or other molecular format) from input dataset. 2. Apply PubChem standardization procedure to each structure to normalize representation, remove salts, and"
- [other] Validate standardized structures for chemical validity and retain only structures that pass standardization without error.: "Validate standardized structures for chemical validity and retain only structures that pass standardization without error."
- [readme] From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk.: "From the input data structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk."
- [readme] We are collecting information such as retention time (RT) and chemical structures of small molecules in standardized format.: "We are collecting information such as retention time (RT) and chemical structures of small molecules in standardized format."
