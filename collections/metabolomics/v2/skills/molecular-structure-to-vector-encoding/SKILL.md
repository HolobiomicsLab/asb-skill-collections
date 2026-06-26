---
name: molecular-structure-to-vector-encoding
description: Use when when you have a collection of molecular structures (SMILES,
  InChI, or SDF format) and need to train or compare neural network-based spectrum
  predictors (such as NEIMS, MassFormer, or ICEBERG variants) on the same benchmark
  dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - PyTorch
  - TensorFlow
  - PubChem
  - PyTorch / TensorFlow
  - ms-pred
  - MAGMa / RDKit
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- _No usage/docs found._
- By inputting the chemical formula and your experimental spectrum, the WebUI will
  rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-024-00816-8
  all_source_dois:
  - 10.1038/s42256-024-00816-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-to-vector-encoding

## Summary

Convert molecular structures into fixed-length numerical feature vectors suitable for neural network input, enabling direct comparison and benchmarking of spectrum prediction models. This preprocessing step is essential for training FFN and GNN encoders on equivalent settings across baseline and novel spectrum prediction architectures.

## When to use

When you have a collection of molecular structures (SMILES, InChI, or SDF format) and need to train or compare neural network-based spectrum predictors (such as NEIMS, MassFormer, or ICEBERG variants) on the same benchmark dataset. The input structures must be converted to fixed-length feature vectors to ensure equivalent model settings across different encoder architectures (FFN vs. GNN) during hyperparameter sweeps and evaluation.

## When NOT to use

- When input is already a pre-computed feature table or numerical matrix (featurization already applied).
- When comparing models that require different molecular representations (e.g., fragment-level predictions vs. formula-level predictions) — alignment on single featurization may obscure genuine model differences.
- When the benchmark dataset lacks sufficient structural annotation or metadata to verify consistent featurization across all compounds.

## Inputs

- Molecular structures in SMILES, InChI, or SDF format
- Benchmark dataset metadata (e.g., NIST'20 labels.tsv or MassSpecGym catalog)
- Molecular property annotations (if available)

## Outputs

- Fixed-length numerical feature vectors (one per molecule)
- Feature vector matrix suitable for FFN/GNN encoder input
- Featurization parameter configuration (for reproducibility)

## How to apply

Load molecular structures from the benchmark dataset (e.g., NIST'20 or MassSpecGym spectra paired with SMILES/InChI data). Represent each structure as a fixed-length feature vector compatible with FFN input layers, typically using molecular descriptors or learned embeddings. Ensure all structures in the dataset are encoded using identical featurization rules to maintain equivalent settings across compared baseline and alternative models. Validate that the resulting feature vectors have uniform dimensionality and pass schema checks before feeding to downstream encoders. The choice of featurization (classical descriptors vs. graph-derived features vs. pre-trained molecular embeddings) should be documented and held constant across all compared models to enable fair benchmarking.

## Related tools

- **PyTorch / TensorFlow** (Neural network framework for encoding and training spectrum predictors on vectorized molecular inputs)
- **PubChem** (Source of molecular structures, SMILES, and formula mappings for featurization and retrieval experiments)
- **ms-pred** (Benchmark framework implementing equivalent featurization and encoder training across NEIMS, MassFormer, 3DMolMS, and other baselines) — github.com/coleygroup/ms-pred
- **MAGMa / RDKit** (Molecular annotation and descriptor calculation tools for structure-to-vector conversion)

## Evaluation signals

- All output feature vectors have identical dimensionality and numeric dtype (e.g., float32).
- Feature vectors contain no NaN or Inf values; min/max ranges are consistent across the dataset.
- Featurization is deterministic: re-encoding the same structure yields identical vectors.
- Model training proceeds without shape mismatch errors; FFN encoder input layer receives vectors of expected dimensionality.
- Benchmark comparison metrics (e.g., cosine similarity, spectral match score between NEIMS-FFN and NEIMS-GNN variants) show equivalent performance when only encoder architecture differs, confirming featurization consistency.

## Limitations

- Fixed-length vectorization may lose structural detail or context-dependent information compared to graph or fragment-based representations (ICEBERG predicts at fragment level, SCARF at formula level).
- Choice of featurization method (classical descriptors, learned embeddings, or graph features) significantly impacts model performance; no single encoding is optimal across all spectrum prediction tasks.
- Structures with ambiguous or missing stereochemistry or those outside the training domain may produce uninformative or out-of-distribution vectors.
- Large-scale featurization of PubChem or MassSpecGym requires substantial computational resources and time (formula subset generation documented as 'several hours, even parallelized').

## Evidence

- [other] Preprocess molecular structures into fixed-length feature vectors suitable for FFN input.: "Preprocess molecular structures into fixed-length feature vectors suitable for FFN input."
- [readme] implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): "implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.)"
- [readme] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] formula subset generation takes longer (on the order of several hours, even parallelized) as it requires converting each molecule in PubChem to a mol / InChI.: "formula subset generation takes longer (on the order of several hours, even parallelized) as it requires converting each molecule in PubChem to a mol / InChI."
- [other] Train the FFN encoder on the spectrum prediction task using mean squared error loss and an optimization algorithm (e.g. Adam).: "Train the FFN encoder on the spectrum prediction task using mean squared error loss and an optimization algorithm (e.g. Adam)."
