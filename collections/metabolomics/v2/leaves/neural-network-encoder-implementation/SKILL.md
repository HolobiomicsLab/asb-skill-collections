---
name: neural-network-encoder-implementation
description: Use when when you need to benchmark multiple encoder types (e.g., FFN
  vs. GNN) on the same predictive task and require evidence that performance differences
  reflect genuine architectural trade-offs rather than suboptimal tuning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0154
  tools:
  - NEIMS FFN encoder
  - NEIMS GNN encoder
  - ms-pred repository
  - PyTorch or TensorFlow
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
- doi: 10.1021/acscentsci.9b00085
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neural-network-encoder-implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Implement equivalent FFN and GNN encoder architectures with matched hyperparameters, covariates, and random seeds to enable fair empirical comparison of neural network variants for spectrum prediction. This skill ensures that architectural differences—not hyperparameter choices or training variations—drive observed performance divergence.

## When to use

When you need to benchmark multiple encoder types (e.g., FFN vs. GNN) on the same predictive task and require evidence that performance differences reflect genuine architectural trade-offs rather than suboptimal tuning. Specifically, when reproducing or extending baseline implementations like NEIMS or comparing novel architectures against established ones in mass spectrum prediction.

## When NOT to use

- When you are tuning hyperparameters for a single encoder type (this skill enforces fixed hyperparameters to isolate architecture effects)
- When encoder implementations already exist in the literature and your goal is only deployment or inference—not methodological comparison
- When your input dataset or feature set is fundamentally different between encoder variants, violating the 'equivalent settings' requirement

## Inputs

- Molecular dataset with extracted features and covariates (e.g., InChI, SMILES, collision energy)
- Hyperparameter configuration dictionary (learning rate, batch size, hidden dimensions, regularization)
- Training/validation/test data splits with matched random seed
- Published FFN and GNN encoder architecture specifications

## Outputs

- Trained FFN encoder model checkpoint
- Trained GNN encoder model checkpoint
- Performance metric table (per-encoder scores: spectral similarity, top-k accuracy, loss curves)
- Comparison report documenting architecture differences and performance parity analysis

## How to apply

First, define a shared hyperparameter sweep (e.g., learning rate, batch size, dropout, layer dimensions) applied uniformly across all encoder variants. Extract and preprocess identical molecular feature sets and covariates (e.g., molecular weight, functional groups, ionization mode) for both encoders. Implement the FFN encoder variant following its published architecture, then implement the GNN encoder with equivalent configuration (same input dimension, hidden sizes, and optimization schedule). Train both models on the same training split using matched random seeds to control variance. Evaluate on held-out test data and compute performance metrics (e.g., spectral similarity, top-k retrieval accuracy) for each encoder. Generate a comparison report documenting: (1) architectural differences in graph representation vs. feedforward propagation, (2) performance parity checks (e.g., statistical significance tests), and (3) any divergence in convergence speed or generalization, attributing these to encoder design rather than tuning.

## Related tools

- **NEIMS FFN encoder** (Reference feedforward neural network variant from Rapid prediction of electron–ionization mass spectrometry; defines baseline architecture and hyperparameter sweep template) — https://pubs.acs.org/doi/full/10.1021/acscentsci.9b00085
- **NEIMS GNN encoder** (Reference graph neural network variant from same NEIMS work; implements molecular structure as graph to compare against FFN) — https://pubs.acs.org/doi/full/10.1021/acscentsci.9b00085
- **ms-pred repository** (Contains implementations of ICEBERG, SCARF, MassFormer, and baseline encoders (FFN/GNN NEIMS variants) with matched experimental pipeline and hyperparameter sweeps) — https://github.com/coleygroup/ms-pred
- **PyTorch or TensorFlow** (Deep learning framework for implementing and training both FFN and GNN encoder models with matched configuration)

## Evaluation signals

- Both encoders trained with identical random seed and hyperparameters converge to comparable loss curves (no significant systematic training divergence)
- Performance metrics (top-k retrieval accuracy, spectral similarity scores) for both encoders fall within a reasonable tolerance band (e.g., within 1–2% absolute difference if parity is expected)
- Comparison report explicitly documents which performance differences are statistically significant vs. within noise
- Encoder architectural differences (e.g., graph convolution layers vs. dense layers) are clearly documented and tied to observed metric divergence
- Test set evaluation uses held-out data unseen during hyperparameter sweep; validation curves show no sign of overfitting one encoder more than the other

## Limitations

- Matched hyperparameter sweeps may not be optimal for all encoder types; FFN and GNN may respond differently to the same learning rate or regularization, potentially disadvantaging one variant
- Covariates must be extractable for both architectures; if one encoder cannot consume certain feature types (e.g., edge features in GNN), either omit them globally or augment the FFN to match, adding complexity
- Fair comparison requires sufficient model capacity parity; if the FFN has substantially more parameters than the GNN or vice versa, capacity imbalance may confound architectural conclusions
- Random seed control reduces stochastic variance but does not eliminate hardware or library version effects; reproducibility across different compute environments may vary

## Evidence

- [other] NEIMS baseline implementation includes both FFN and GNN encoder variants, configured with equivalent settings (same covariates and hyperparameter sweeps) across all models to enable fair comparison of spectrum prediction approaches.: "NEIMS baseline implementation includes both FFN and GNN encoder variants, configured with equivalent settings (same covariates and hyperparameter sweeps) across all models to enable fair comparison"
- [other] Implement the FFN encoder architecture with the standard hyperparameter sweep settings. 3. Implement the GNN encoder architecture using the same hyperparameter sweep and covariate inputs as the FFN variant. 4. Train both encoder variants on the same training set with matched hyperparameters and random seeds.: "Implement the GNN encoder architecture using the same hyperparameter sweep and covariate inputs as the FFN variant. Train both encoder variants on the same training set with matched hyperparameters"
- [readme] In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): "In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (same covariates, hyperparameter sweeps for each,"
- [other] Evaluate both trained models on held-out test data and record performance metrics for each encoder type. Generate a comparison report documenting architecture differences, performance parity checks, and any observed divergence between encoders.: "Evaluate both trained models on held-out test data and record performance metrics for each encoder type. Generate a comparison report documenting architecture differences, performance parity checks"
