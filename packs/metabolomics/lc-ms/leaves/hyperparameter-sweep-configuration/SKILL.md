---
name: hyperparameter-sweep-configuration
description: Use when when implementing multiple competing model architectures (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3664
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - NEIMS (FFN and GNN encoder variants)
  - MassFormer
  - 3DMolMS
  - GrAFF-MS
  - coleygroup/ms-pred repository
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
- doi: 10.1021/acscentsci.9b00085
  title: ''
- doi: 10.1101/2023.03.15.532823v1
  title: ''
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
  - 10.1021/acscentsci.9b00085
  - 10.1101/2023.03.15.532823v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Hyperparameter-sweep-configuration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure and execute systematic hyperparameter sweeps across multiple baseline spectrum prediction models using identical covariate sets and search spaces to enable fair comparative evaluation. This ensures that performance differences reflect architectural choices rather than tuning disparities.

## When to use

When implementing multiple competing model architectures (e.g., FFN vs. GNN encoders, or NEIMS vs. MassFormer vs. 3DMolMS) for the same prediction task (tandem mass spectrum prediction) and you need to establish whether observed performance differences arise from the model design itself or from differential hyperparameter optimization. Apply this skill before any final performance comparison across models.

## When NOT to use

- Models are trained on different datasets or use non-overlapping feature sets; hyperparameter parity alone cannot control for data confounds.
- One model has a fixed, pre-trained checkpoint that cannot be retrained with new hyperparameters (e.g., CFM-ID for which only running instructions are provided, not retraining).
- The goal is model selection for deployment rather than comparative research; in production, tune each model independently to maximize its individual performance.

## Inputs

- Molecular dataset with spectra and metadata (NIST'20 format: .SDF, .tsv labels, .mgf or .hdf5 spec files)
- Extracted molecular features and covariates (fingerprints, collision energy, precursor m/z)
- Training/validation/test split definitions
- Model architecture specifications for each variant (FFN encoder, GNN encoder, MassFormer, 3DMolMS, GrAFF-MS, CFM-ID)

## Outputs

- Hyperparameter sweep configuration file (YAML or JSON with unified parameter bounds)
- Trained model checkpoints for each architecture at its best hyperparameter setting
- Evaluation metrics table (e.g., top-1 accuracy, top-10 accuracy, spectral similarity) per model
- Comparison report documenting architecture differences, performance parity, and observed divergence

## How to apply

Define a single shared hyperparameter sweep specification that covers all models' tunable parameters (learning rate, batch size, dropout, layer dimensions, etc.). Extract identical molecular features and covariates (e.g., molecular fingerprints, collision energy, precursor m/z) for all models from the same training dataset. Train each model variant—including both encoder types (FFN and GNN) for NEIMS and alternative architectures like MassFormer or GrAFF-MS—using the same hyperparameter search space, training set, and random seeds. After hyperparameter optimization, evaluate each model's best-performing configuration on a held-out test set and compare performance metrics (e.g., top-1 retrieval accuracy, spectral similarity, prediction error). Document the architecture differences and any systematic divergence between encoders; if performance differs substantially, investigate whether the disparity reflects model capacity, feature representation, or optimization landscape rather than search bias.

## Related tools

- **NEIMS (FFN and GNN encoder variants)** (Baseline spectrum predictor with two encoder architectures to be swept over identical hyperparameter spaces) — https://pubs.acs.org/doi/full/10.1021/acscentsci.9b00085
- **MassFormer** (Tandem mass spectrum prediction model with transformer architecture; included in sweep for fair comparison) — https://arxiv.org/abs/2111.04824
- **3DMolMS** (3D conformation-based spectrum predictor; part of baseline comparison suite) — https://www.biorxiv.org/content/10.1101/2023.03.15.532823v1
- **GrAFF-MS** (Graph neural network spectrum predictor with same hyperparameter sweep applied) — https://arxiv.org/pdf/2301.11419.pdf
- **coleygroup/ms-pred repository** (Implementation and experiment orchestration for unified hyperparameter sweep across all baseline models) — https://github.com/coleygroup/ms-pred

## Examples

```
# After installing ms-pred and preparing NIST'20 data, define a unified hyperparameter sweep in configs/baseline_sweep.yaml with all models' parameter bounds, then:
python src/ms_pred/baselines/sweep_hyperparams.py --config configs/baseline_sweep.yaml --models neims_ffn neims_gnn massformer graff_ms --dataset nist20 --output-dir results/hyperparameter_sweep
```

## Evaluation signals

- All models use identical covariate feature sets and no model receives additional features or preprocessing not available to others.
- Hyperparameter search spaces (bounds, grid density, random seed ranges) are identical across all model variants; document any architecture-specific parameters separately.
- Validation metrics (e.g., hold-out top-1 accuracy, top-10 accuracy, spectral cosine similarity) are computed on the same test set for all models with no data leakage.
- Comparison report explicitly notes whether observed performance differences exceed expected variance bounds (e.g., confidence intervals from multiple random seeds); if CI ranges overlap, architectures have equivalent empirical performance given the same tuning effort.
- Training dynamics (loss curves, gradient norms, convergence speed) are logged for each model and each hyperparameter setting to diagnose optimization disparities independent of final metrics.

## Limitations

- Hyperparameter sweep does not guarantee each model reaches its theoretical optimum; models with more complex loss landscapes may require domain-specific tuning strategies beyond a uniform grid.
- Some models (e.g., CFM-ID) are provided pre-trained only; comparison is limited to inference-time performance and cannot isolate the effect of hyperparameter choice during training.
- Computational cost scales linearly with the number of models and hyperparameter combinations; sweep configuration must balance coverage with available GPU memory and wall-clock time.
- Fair comparison assumes all models operate on the same chemical space; if one model cannot process certain molecular features (e.g., 3D conformations for CFM-ID), comparison is restricted to the intersection of supported inputs.

## Evidence

- [readme] In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): "In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for"
- [other] NEIMS baseline implementation includes both FFN and GNN encoder variants, configured with equivalent settings (same covariates and hyperparameter sweeps) across all models to enable fair comparison of spectrum prediction approaches.: "NEIMS baseline implementation includes both FFN and GNN encoder variants, configured with equivalent settings (same covariates and hyperparameter sweeps) across all models"
- [other] Train both encoder variants on the same training set with matched hyperparameters and random seeds. Evaluate both trained models on held-out test data and record performance metrics for each encoder type.: "Train both encoder variants on the same training set with matched hyperparameters and random seeds. Evaluate both trained models on held-out test data and record performance metrics"
- [other] Generate a comparison report documenting architecture differences, performance parity checks, and any observed divergence between encoders.: "Generate a comparison report documenting architecture differences, performance parity checks, and any observed divergence between encoders"
