---
name: model-comparison-evaluation
description: Use when when you have multiple candidate spectrum prediction models (e.g., FFN vs. GNN encoders, NEIMS vs. MassFormer vs. ICEBERG) and need to determine which performs better on a shared task like tandem mass spectrum prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3473
  tools:
  - NEIMS
  - MassFormer
  - 3DMolMS
  - GrAFF-MS
  - CFM-ID
  - ICEBERG
  - coleygroup/ms-pred
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
- doi: 10.1021/acs.analchem.1c01465
  title: ''
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
---

# model-comparison-evaluation

## Summary

A systematic approach to comparing spectrum prediction models by implementing baseline and alternative architectures using equivalent settings (same covariates, hyperparameter sweeps, training/test splits, random seeds) to enable fair performance attribution. This skill ensures that observed performance differences reflect true model capability rather than experimental confounds.

## When to use

When you have multiple candidate spectrum prediction models (e.g., FFN vs. GNN encoders, NEIMS vs. MassFormer vs. ICEBERG) and need to determine which performs better on a shared task like tandem mass spectrum prediction. Use this skill when baseline comparisons are required to validate that novel models genuinely outperform prior work, or when you must report performance parity across encoder variants.

## When NOT to use

- Input datasets use different preprocessing, feature extraction, or covariate selection pipelines—standardize first.
- Models have been independently hyperparameter-tuned by their respective authors; this confounds comparison. Only use if you can re-tune all models uniformly.
- The task is not retrieval/ranking but absolute spectrum prediction quality on a single molecule—use per-molecule evaluation metrics instead.

## Inputs

- molecular dataset with spectra (NIST'20 .SDF or MassSpecGym; requires processed splits with labels.tsv, spec_files.hdf5, mgf_files)
- extracted molecular features and covariates (standardized SMILES, molecular descriptors, collision energy annotations)
- candidate model architectures (e.g., NEIMS FFN encoder, NEIMS GNN encoder, MassFormer, ICEBERG, 3DMolMS, GrAFF-MS, CFM-ID)
- hyperparameter grid (learning rate, batch size, number of layers, dropout, optimizer settings)

## Outputs

- trained model checkpoints for each candidate architecture
- performance metrics table (top-1/top-5 retrieval accuracy, cosine similarity, or spectrum prediction loss per model)
- comparison report with documented architecture differences, hyperparameter tables, performance parity checks, and divergence annotations
- optional: statistical significance tests or confidence intervals on retrieval metrics

## How to apply

First, select a common dataset (e.g., NIST'20 or MassSpecGym) and define a unified feature extraction pipeline to produce identical molecular covariates for all models. Second, perform a single hyperparameter sweep and apply the same hyperparameter configurations to all candidate models—not independent sweeps per model. Third, train all models on the same train/validation/test splits using fixed random seeds (e.g., seed=1 for quick validation; seeds 1–3 with random + scaffold splits for full replication). Fourth, evaluate each trained model on the held-out test set and record the same performance metrics (e.g., top-1 retrieval accuracy, cosine similarity, or spectrum prediction loss). Fifth, generate a comparison report that documents architecture differences, lists all hyperparameters used, confirms performance parity checks where applicable, and flags any observed divergence. Use manual expert review or statistical significance testing to interpret differences.

## Related tools

- **NEIMS** (FFN and GNN encoder baseline models; both configured with equivalent hyperparameter sweeps and covariates to enable fair comparison) — https://pubs.acs.org/doi/full/10.1021/acscentsci.9b00085
- **MassFormer** (Graph Transformer baseline for tandem mass spectrum prediction; trained with matched hyperparameters and splits) — https://arxiv.org/abs/2111.04824
- **3DMolMS** (Three-dimensional conformation-based baseline spectrum predictor; evaluated alongside other models with uniform settings) — https://www.biorxiv.org/content/10.1101/2023.03.15.532823v1
- **GrAFF-MS** (Graph neural network baseline for high-resolution mass spectra; included in fair comparison cohort) — https://arxiv.org/pdf/2301.11419.pdf
- **CFM-ID** (Rule-based reference model (not retrained); external benchmark provided with execution instructions) — https://pubs.acs.org/doi/10.1021/acs.analchem.1c01465
- **ICEBERG** (Novel fragment-level spectrum prediction model; compared against baselines using equivalent experimental setup) — https://github.com/coleygroup/ms-pred
- **coleygroup/ms-pred** (Central repository containing all baseline implementations (NEIMS, MassFormer, 3DMolMS, GrAFF-MS) with unified training and evaluation pipelines) — https://github.com/coleygroup/ms-pred

## Evaluation signals

- Verify identical covariates are passed to all models by inspecting feature extraction logs or dumped covariate files; confirm dimensionality and value ranges match across models.
- Confirm hyperparameter sweep results were generated once and applied uniformly—check that all models received the same set of (learning_rate, batch_size, …) configurations, not independent sweeps.
- Validate that all models were trained on identical train/validation/test splits and random seeds; inspect split logs and ensure seed=1 for quick validation, seeds={1,2,3} for full replication.
- Check performance metrics table for completeness and consistency of reported statistics (top-1/top-5 accuracy, retrieval ranks, cosine similarity). For significance, verify CI overlap or run paired t-tests on retrieval ranks.
- Confirm the comparison report explicitly documents any architecture-specific tuning (e.g., 'CFM-ID not retrained, external benchmark only'; 'GNN and FFN encoders use same hyperparameters') and flags any intentional deviations from the uniform protocol.

## Limitations

- Fair comparison requires access to all source code and pretrained weights; some models (e.g., CFM-ID) may not be retrainable and must be used as external references only.
- NIST'20 is a commercial dataset (requires purchase). MassSpecGym is publicly available but has undergone less manual curation and quality control, affecting reported performance and reproducibility.
- Hyperparameter sweeps can be computationally expensive (ICEBERG requires two GPUs with ≥24 GB RAM each); smaller GPU memory may necessitate reduced batch size, which can impact final performance.
- Models may have different input requirements (e.g., 3D conformations, collision energy annotations); ensure all covariates can be extracted uniformly or explicitly document which covariates each model receives.
- Random seed effects and data splits (random vs. scaffold splits) can produce different absolute performance; document all random seed choices and split strategy in the comparison report.

## Evidence

- [readme] In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): "In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for"
- [other] Implement the FFN encoder architecture with the standard hyperparameter sweep settings. 3. Implement the GNN encoder architecture using the same hyperparameter sweep and covariate inputs as the FFN variant. 4. Train both encoder variants on the same training set with matched hyperparameters and random seeds.: "Implement the GNN encoder architecture using the same hyperparameter sweep and covariate inputs as the FFN variant. 4. Train both encoder variants on the same training set with matched"
- [other] Evaluate both trained models on held-out test data and record performance metrics for each encoder type. 6. Generate a comparison report documenting architecture differences, performance parity checks, and any observed divergence between encoders.: "Evaluate both trained models on held-out test data and record performance metrics for each encoder type. 6. Generate a comparison report documenting architecture differences, performance parity"
- [readme] The above scripts will only run for split_1_rnd1 (random split, seed=1), which is suitable if you want to train your own ICEBERG for structural elucidation applications. If you want to replicate our reported result with random + scaffold splits and 3 random seeds…: "If you want to replicate our reported result with random + scaffold splits and 3 random seeds, please uncomment all entries in the following files"
- [readme] ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor…There is an all-in-one script run_scripts/iceberg/run_all.sh that trains the up-to-date version of ICEBERG on NIST'20 dataset: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor. The pipeline for training and evaluating this model can be accessed in `run_scripts/iceberg/`."
