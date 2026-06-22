---
name: molecular-spectrum-prediction-baseline
description: Use when you have multiple mass spectrum prediction models to compare and need to establish a level playing field by implementing at least one well-characterized baseline (such as NEIMS) with both FFN and GNN encoder variants.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - NEIMS FFN/GNN baseline
  - ICEBERG
  - PubChem
  techniques:
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_fragmentation_graph_generation_cq
    doi: 10.1021/acs.analchem.3c04654
    title: ICEBERG / fragmentation graph generation
  dedup_kept_from: coll_iceberg_fragmentation_graph_generation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04654
  all_source_dois:
  - 10.1021/acs.analchem.3c04654
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct and Implement Baseline Spectrum Prediction Models with Equivalent Encoder Architectures

## Summary

Implement equivalent baseline architectures (FFN and GNN encoders) for mass spectrum prediction with matched hyperparameters, covariates, and random seeds to enable fair quantitative comparison across spectrum prediction methods. This skill ensures that performance differences reflect architectural choices rather than training disparities.

## When to use

You have multiple mass spectrum prediction models to compare and need to establish a level playing field by implementing at least one well-characterized baseline (such as NEIMS) with both FFN and GNN encoder variants. Use this skill when the literature baseline exists but requires reimplementation to match your dataset preprocessing, feature extraction, and hyperparameter sweep protocol.

## When NOT to use

- The baseline model is already fully trained and published with official weights available; instead, load and evaluate pre-trained checkpoints.
- Your goal is to propose a novel architecture without establishing fair comparison; equivalence baselines are only useful if you plan to measure relative improvement.
- The input dataset differs substantially in curation, collision energy distribution, or molecular space from the baseline's original training data; retrain the baseline on your data rather than assuming transferred weights are representative.

## Inputs

- Processed mass spectrum dataset with molecular features (e.g., NIST'20 .hdf5 with spec_files, labels.tsv, and splits/)
- Molecular covariates (molecular weight, formula, InChI key, SMILES)
- Original baseline hyperparameter sweep specification and architecture description
- Train/validation/test split indices

## Outputs

- Trained FFN encoder model weights and checkpoint
- Trained GNN encoder model weights and checkpoint
- Performance metrics table (top-1 accuracy, top-10 accuracy, mean squared error on intensity prediction)
- Comparison report documenting architecture parity checks and encoder performance divergence analysis

## How to apply

Load the tandem mass spectrometry dataset (e.g., NIST'20 .SDF with collision energy annotations or processed .hdf5 with spectrum files). Extract molecular features and covariates consistent across all encoder implementations. Implement the FFN encoder variant following the original hyperparameter sweep specification, then implement the GNN encoder using identical covariate inputs and sweep bounds. Train both encoder variants on the same training split with matched random seeds, batch sizes, and optimization schedules. Evaluate both models on held-out test data using the same retrieval or ranking metrics (e.g., top-1 accuracy, cosine similarity). Generate a side-by-side comparison report documenting any performance divergence; if divergence exceeds acceptable tolerance (typically <2% in top-1 accuracy), debug covariate alignment, initialization, or hyperparameter implementation before declaring parity.

## Related tools

- **NEIMS FFN/GNN baseline** (Reference encoder architecture to reimplement with matched hyperparameters; provides the original model specification for fair comparison) — github.com/samgoldman97/ms-pred
- **ICEBERG** (Fragment-level spectrum prediction model used as a downstream comparison target against equivalently-trained baselines) — http://github.com/coleygroup/ms-pred
- **PubChem** (Source library for structural elucidation validation and candidate ranking; provides molecules for retrieval evaluation)

## Evaluation signals

- FFN and GNN encoder implementations produce comparable top-1 retrieval accuracy on held-out test set (within <2% relative difference when trained with identical hyperparameters and seeds)
- Both encoders consume the same covariate feature set (same molecular descriptors, same normalization) without dimension mismatch or data leakage
- Training curves (loss vs. epoch) show similar convergence trajectories for both encoder variants when plotted on the same scale
- Prediction time and memory footprint are documented and reasonable given the encoder complexity (GNN slightly higher due to graph convolutions)
- Comparison report explicitly lists any architectural divergence (e.g., layer counts, activation functions) and explains why it was necessary or avoided

## Limitations

- Fair comparison requires access to the original baseline's training/validation/test splits; if unavailable, reconstructing equivalent splits (e.g., random + scaffold splits with matched random seeds) introduces minor variability.
- NEIMS baseline assumes electron ionization (EI); adapting to electrospray ionization (ESI) or other ionization modes requires retraining on matched collision energy distributions.
- Hyperparameter sweep results are sensitive to GPU/CPU hardware and library versions (PyTorch, cuDNN); reported parity may not replicate exactly across different compute environments unless random seeds and hardware configurations are identical.
- GNN encoder implementation requires molecular graph representation (e.g., RDKit mol objects); sparse or malformed SMILES in the dataset can silently fail during graph construction.

## Evidence

- [other] NEIMS baseline implementation includes both FFN and GNN encoder variants, configured with equivalent settings (same covariates and hyperparameter sweeps) across all models to enable fair comparison of spectrum prediction approaches.: "NEIMS baseline implementation includes both FFN and GNN encoder variants, configured with equivalent settings (same covariates and hyperparameter sweeps) across all models to enable fair comparison"
- [other] Implement the FFN encoder architecture with the standard hyperparameter sweep settings. 3. Implement the GNN encoder architecture using the same hyperparameter sweep and covariate inputs as the FFN variant. 4. Train both encoder variants on the same training set with matched hyperparameters and random seeds.: "Implement the FFN encoder architecture with the standard hyperparameter sweep settings. Implement the GNN encoder architecture using the same hyperparameter sweep and covariate inputs as the FFN"
- [readme] In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): "In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for"
- [other] Evaluate both trained models on held-out test data and record performance metrics for each encoder type. 6. Generate a comparison report documenting architecture differences, performance parity checks, and any observed divergence between encoders.: "Evaluate both trained models on held-out test data and record performance metrics for each encoder type. Generate a comparison report documenting architecture differences, performance parity checks,"
