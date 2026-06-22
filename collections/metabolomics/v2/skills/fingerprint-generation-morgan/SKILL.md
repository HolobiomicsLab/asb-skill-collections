---
name: fingerprint-generation-morgan
description: Use when you have parsed molecular structures from the SMRT dataset or similar small molecule collections and need to create a vectorized molecular representation suitable for neural network input alongside molecular graph representations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_3372
  tools:
  - torch
  - Python
  - rdkit-pypi
  - torch_geometric
  - scikit-learn
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- torch
- Python 3.9
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rt_transformer_cq
    doi: 10.1093/bioinformatics/btae084
    title: RT-Transformer
  dedup_kept_from: coll_rt_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae084
  all_source_dois:
  - 10.1093/bioinformatics/btae084
  - 10.1038/s41467-019-13680-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fingerprint-generation-morgan

## Summary

Generate Morgan fingerprints from molecular structures (SMILES or SDF format) using RDKit to create fixed-length binary vector representations of small molecules. Morgan fingerprints serve as one of two complementary molecular input modalities for retention time prediction in the RT-Transformer architecture.

## When to use

Use this skill when you have parsed molecular structures from the SMRT dataset or similar small molecule collections and need to create a vectorized molecular representation suitable for neural network input alongside molecular graph representations. This is particularly appropriate when dual fingerprint and graph modalities are required to capture both local chemical features and global molecular connectivity for retention time or property prediction tasks.

## When NOT to use

- Input molecules are already represented as pre-computed fingerprint vectors or feature matrices.
- The analysis does not require fixed-length vector representations (e.g., if only graph-based methods are sufficient).
- Molecular structures cannot be parsed or are incomplete (missing stereochemistry or bond orders critical for fingerprint reproducibility).

## Inputs

- SMILES strings or SDF molecular structure files
- Parsed RDKit Mol objects representing small molecules

## Outputs

- Morgan fingerprint vectors (binary or count-based, typically 2048-bit length)
- Serialized fingerprint representations (pickle or PyTorch tensor format)
- Feature matrix compatible with RT-Transformer dual-input architecture

## How to apply

Parse molecular structures from SMILES or SDF format files using RDKit's molecular parsing functions. Generate Morgan fingerprints for each molecule by calling RDKit's fingerprinting function with configurable radius (typically 2–3 hops) and bit-vector length (commonly 2048 bits). Serialize the resulting fingerprint vectors to disk in a format compatible with downstream PyTorch model training, such as pickle or PyTorch tensor format (.pt or .pth). Fingerprints are combined with molecular graph representations (derived separately via RDKit's Chem.Descriptors and torch_geometric) to form the dual-input feature set for the RT-Transformer model.

## Related tools

- **rdkit-pypi** (Parses molecular structures and generates Morgan fingerprints from SMILES/SDF input)
- **torch** (Serializes and manages fingerprint tensors for PyTorch model training)
- **torch_geometric** (Works in tandem with fingerprints to provide complementary graph-based molecular representations)
- **scikit-learn** (Optional utility for fingerprint normalization and feature scaling prior to model input)

## Evaluation signals

- Fingerprint vectors have consistent dimensionality (e.g., 2048 bits) across all molecules in the dataset.
- No NaN or infinite values in generated fingerprint tensors; all entries are valid binary or count values.
- Serialized fingerprints can be successfully loaded and passed to RT-Transformer model without shape mismatch errors.
- Fingerprint generation is deterministic: identical SMILES strings produce identical fingerprint vectors across separate runs.
- Fingerprint feature coverage: at least 5–10% of bit positions are set to 1 across the molecule population (indicating adequate molecular diversity capture).

## Limitations

- Morgan fingerprints encode local connectivity patterns up to a fixed radius; long-range spatial or 3D structural information is not captured.
- Different SMILES representations of the same molecule (e.g., different atom ordering or aromaticity notation) may produce identical or very similar fingerprints; canonicalization is recommended to ensure reproducibility.
- Fixed bit-vector length (e.g., 2048 bits) may lead to hash collisions in very large or chemically diverse datasets, potentially conflating distinct molecular features.
- Fingerprint radius and bit length are hyperparameters; the article does not specify optimal values for the SMRT retention time prediction task.

## Evidence

- [other] Parse molecular structures (SMILES or SDF format) using RDKit to generate Morgan fingerprints for each molecule.: "Parse molecular structures (SMILES or SDF format) using RDKit to generate Morgan fingerprints for each molecule."
- [other] The RT-Transformer architecture combines fingerprint and molecular graph data as dual inputs for retention time prediction.: "The RT-Transformer architecture combines fingerprint and molecular graph data as dual inputs for retention time prediction."
- [other] Fingerprints and molecular graphs are derived using rdkit-pypi for molecular representation and torch_geometric for graph processing, with the SMRT dataset sourced from the METLIN small molecule dataset paper.: "Fingerprints and molecular graphs are derived using rdkit-pypi for molecular representation and torch_geometric for graph processing, with the SMRT dataset sourced from the METLIN small molecule"
- [other] Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format).: "Serialize fingerprint and graph representations to disk in a format compatible with downstream model training (e.g., pickle or PyTorch tensor format)."
- [readme] The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output.: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
