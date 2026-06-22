---
name: baseline-model-implementation-for-comparison
description: Use when you are introducing a novel spectrum prediction model and need to demonstrate that performance improvements come from architectural innovation rather than experimental advantage.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - PubChem
  - ms-pred (coleygroup)
  - MAGMa
  techniques:
  - direct-infusion-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# baseline-model-implementation-for-comparison

## Summary

Implement reference baseline models (e.g., NEIMS with FFN and GNN encoders) under strictly equivalent settings—same covariates, hyperparameter sweeps, train/test splits—to enable fair quantitative comparison with novel spectrum prediction methods. This skill ensures reproducible benchmarking and isolates model architectural differences from confounding experimental factors.

## When to use

You are introducing a novel spectrum prediction model and need to demonstrate that performance improvements come from architectural innovation rather than experimental advantage. Baseline implementation is required when comparing across NEIMS, MassFormer, 3DMolMS, GrAFF-MS, or CFM-ID on the same dataset (e.g., NIST'20) with tandem mass spectrum prediction as the evaluation task.

## When NOT to use

- Input dataset or splits differ from the novel model's (comparison requires identical data provenance and preprocessing).
- Hyperparameter sweeps for the baseline are not exhaustively identical to the novel model (unfair advantage to one method).
- Baseline source code or paper is unavailable or ambiguously specified (use only published methods with reproducible details).

## Inputs

- Molecular structures as SMILES strings or chemical graphs (PubChem records)
- Experimental tandem mass spectra in standardized format (.SDF, .mgf, .hdf5)
- Dataset split specification (train/validation/test indices with seed)
- Hyperparameter sweep configuration (learning rate, batch size, encoder hidden dims, num_layers)

## Outputs

- Trained baseline model checkpoint (.pt or equivalent)
- Spectrum predictions on test set (m/z, intensity tuples or ranking scores)
- Evaluation metrics (top-1/top-k retrieval accuracy, spectral similarity, cosine distance)
- Metadata log (hyperparameters, random seed, training time, hardware used)

## How to apply

Select a reference baseline architecture from the literature (e.g., NEIMS FFN or GNN encoder from Goldman et al. 2009). Load the molecular dataset and chemical structures from PubChem or a commercial source (NIST'20) with associated experimental mass spectra in standardized format (.SDF or .hdf5). Construct the encoder (FFN or GNN) and train end-to-end on the spectrum prediction task using the exact same dataset splits, hyperparameter sweep grid, learning rate schedule, and batch settings as your novel model. Evaluate on the held-out test set computing prediction accuracy and comparison metrics (e.g., top-1/top-k retrieval accuracy for structural elucidation, spectral similarity cosine scores). Save model weights, predictions, and evaluation metrics to output artifacts. Document all hyperparameters and random seeds (e.g., split_1_rnd1) to enable replication.

## Related tools

- **PubChem** (Source of molecular structures and chemical formula lookups for dataset construction and retrieval experiments)
- **ms-pred (coleygroup)** (Reference implementation of NEIMS and other baseline models under equivalent-settings framework for spectrum prediction) — https://github.com/coleygroup/ms-pred
- **MAGMa** (Annotation tool for generating fragmentation trees and substructure labels used in baseline and novel model training pipelines)

## Evaluation signals

- Hyperparameter sweep configuration is identical between baseline and novel model (same ranges, grid resolution, learning rate schedules).
- Train/validation/test split indices and random seeds are reproducible and identical across both implementations.
- Baseline model achieves published or expected performance on the reference test set (e.g., NIST'20 top-1 accuracy ~30–40% for NEIMS GNN).
- Evaluation metrics (top-k retrieval accuracy, cosine similarity scores) are computed on the same held-out test set using identical metric definitions.
- Model checkpoint, predictions, and metadata are saved and can be reloaded to reproduce results without retraining.

## Limitations

- NIST'20 is a commercial dataset requiring purchase; open-source alternatives (MassSpecGym) have less manual curation and yield different results.
- Baseline code availability and clarity vary; some published methods (e.g., CFM-ID 4.0) are not retrained in the comparison—only reference results are provided.
- GPU memory and training time scale with dataset size and hyperparameter sweep breadth; smaller GPUs (<24 GB) require reduced batch sizes and may not replicate published results.
- Contrastive finetuning steps (e.g., for ICEBERG intensity models) are optional and affect final performance; equivalent-settings comparison requires explicit choices about which optional steps to include.

## Evidence

- [readme] In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): "In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for"
- [other] NEIMS baseline is implemented with both FFN and GNN encoder variants as part of an equivalent-settings comparison framework where all models use the same covariates and hyperparameter sweeps.: "NEIMS baseline is implemented with both FFN and GNN encoder variants as part of an equivalent-settings comparison framework where all models use the same covariates and hyperparameter sweeps."
- [other] Construct a graph neural network (GNN) encoder to learn molecular representations from chemical graphs. 3. Train the GNN encoder end-to-end on the spectrum prediction task using the dataset split and hyperparameters specified for the baseline comparison. 4. Evaluate the trained GNN-encoder NEIMS model on the held-out test set, computing prediction accuracy and comparison metrics against ms-pred reference results.: "Construct a graph neural network (GNN) encoder to learn molecular representations from chemical graphs. 3. Train the GNN encoder end-to-end on the spectrum prediction task using the dataset split and"
- [other] Load the molecular dataset and chemical structures from PubChem with associated experimental mass spectra.: "Load the molecular dataset and chemical structures from PubChem with associated experimental mass spectra."
- [readme] 1. *NEIMS* using both FFN and GNN encoders from Rapid prediction of electron–ionization mass spectrometry using neural networks: "1. *NEIMS* using both FFN and GNN encoders from Rapid prediction of electron–ionization mass spectrometry using neural networks"
