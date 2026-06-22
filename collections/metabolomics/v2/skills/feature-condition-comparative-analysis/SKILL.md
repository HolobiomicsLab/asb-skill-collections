---
name: feature-condition-comparative-analysis
description: Use when when you have molecular structures, a regression target (e.g. retention time), and want to establish whether one class of molecular features (e.g., fingerprints) outperforms another (e.g., descriptors) or whether combining them yields marginal gains.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3344
  tools:
  - alvaDesc
  - RDKit
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
schema_version: 0.2.0
---

# feature-condition-comparative-analysis

## Summary

A comparative experimental workflow that trains machine learning models under multiple feature input conditions (e.g., descriptors-only, fingerprints-only, combined) on the same dataset and architecture to quantify the independent contribution of each feature type to prediction accuracy. This skill is applied when the research question hinges on determining which molecular representation—or combination thereof—yields superior generalization.

## When to use

When you have molecular structures, a regression target (e.g. retention time), and want to establish whether one class of molecular features (e.g., fingerprints) outperforms another (e.g., descriptors) or whether combining them yields marginal gains. Specifically, apply this when the hypothesis is that certain feature types encode structural information more efficiently for your task.

## When NOT to use

- Input is already a pre-computed feature matrix; regenerating features is wasteful—skip feature generation and train directly.
- The dataset is too small (<1000 samples) or imbalanced; high variance in condition comparisons may obscure true feature efficacy.
- Feature types are semantically redundant (e.g., two algorithms generating nearly identical fingerprints); no meaningful signal from comparison.

## Inputs

- Molecular structure collection (SMILES, SDF, mol, or InChI format)
- Experimental target property values (e.g., retention times; numeric vector matching molecular count)
- Training/test split indices (or random seed for reproducible split)

## Outputs

- Mean Absolute Error (MAE) and Median Absolute Error (MdAE) per condition (descriptors-only, fingerprints-only, combined)
- Trained model weights/coefficients for each condition
- Ranked comparison table of feature conditions by error metric

## How to apply

Generate all candidate feature types from the molecular structures using a tool like alvaDesc (e.g., 5,666 descriptors and 2,214 fingerprints including MACCS, Extended Connectivity, and Path fingerprints). Split the dataset into training and test sets once, to ensure fair comparison. Train identical model architectures (here, a heavily regularized deep neural network with cosine annealing warm restarts and stochastic weight averaging) under three conditions: (1) descriptors only, (2) fingerprints only, (3) both combined. Record performance metrics (MAE, MdAE, or equivalent) for each condition. Compare metrics across conditions; superior performance in fingerprints-only vs descriptors-only indicates fingerprints capture relevant structural variance more parsimoniously. If combined features do not substantially outperform fingerprints-only, conclude fingerprints are sufficient and descriptors add noise or redundancy.

## Related tools

- **alvaDesc** (Generates both molecular descriptors (5,666) and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) from chemical structures for feature-condition comparison) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative open-source toolkit for fingerprint generation; used in supplementary notebooks for reproducible feature engineering)

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models --train_size 0.8 --param_search_folds 5 --trials 100
```

## Evaluation signals

- Fingerprints-only MAE/MdAE is lower than descriptors-only MAE/MdAE, confirming superior discriminative power.
- Combined (descriptors + fingerprints) MAE/MdAE is not substantially lower than fingerprints-only (e.g., <5% improvement), indicating limited or no synergy.
- Error distributions across train/test splits are stable within each condition, ruling out high variance or overfitting bias.
- Model hyperparameters (regularization strength, learning rate, architecture) are held constant across conditions; any difference in MAE/MdAE is attributable to features, not tuning.
- Reported ±SEM or confidence intervals overlap minimally between conditions (e.g., 39.2±1.2 s vs 41.5±1.8 s), supporting a statistically meaningful ranking.

## Limitations

- Fingerprint type and descriptor set must be chosen a priori; the comparison is specific to MACCS166, Extended Connectivity, and Path fingerprints—other fingerprint families may yield different rankings.
- A single model architecture (heavily regularized DNN with cosine annealing) is used across conditions; results may not generalize to other ML algorithms (e.g., random forests, SVMs) that may favor descriptors.
- The METLIN SMRT dataset includes both retained and unretained molecules; applicability to other chromatographic methods or chemical spaces is not guaranteed by this single-condition study.
- High-dimensional feature spaces (5,666 descriptors) may incur computational overhead and require strong regularization; sparse or low-rank feature sets may behave differently.

## Evidence

- [readme] The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better.: "The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better."
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [readme] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [other] Fingerprints tend to perform better than descriptors alone or descriptors combined with fingerprints for retention time prediction: "Fingerprints tend to perform better than descriptors alone or descriptors combined with fingerprints for retention time prediction"
