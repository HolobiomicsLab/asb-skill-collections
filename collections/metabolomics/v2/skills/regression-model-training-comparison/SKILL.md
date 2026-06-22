---
name: regression-model-training-comparison
description: Use when you have a labeled dataset of molecular structures with experimental continuous outcomes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0154
  tools:
  - alvaDesc
  - RDKit
  - Optuna
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
  - build: coll_cmmrt_cq
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-022-00613-8
  all_source_dois:
  - 10.1186/s13321-022-00613-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# regression-model-training-comparison

## Summary

Train and compare multiple machine learning regressors on the same dataset using different feature representations (descriptors, fingerprints, or combined) to identify which feature set and model architecture yield the lowest prediction error. This skill is essential when optimizing retention time or other continuous molecular property prediction, where feature engineering significantly impacts model performance.

## When to use

You have a labeled dataset of molecular structures with experimental continuous outcomes (e.g., retention times, solubility) and you need to determine which molecular representation (descriptors vs. fingerprints vs. combined) or which regressor architecture produces the most accurate predictions. Apply this skill when feature representation choice is uncertain and prediction error (MAE, median absolute error) is the primary evaluation metric.

## When NOT to use

- Input already includes only a single fixed feature representation; comparison requires at least two alternative representations.
- Target variable is categorical or discrete (use classification instead).
- Molecular structures cannot be reliably converted to SMILES or standard structure formats.

## Inputs

- SMILES strings or molecular structure files (SDF, mol, mol2, inchi)
- Experimental retention times or other continuous target variable
- Split specifications (train/test ratio, cross-validation folds)

## Outputs

- Trained regressor models (one per feature set configuration)
- Prediction error metrics (MAE and MdAE per model and feature set)
- Error distribution comparisons and ranking of feature sets
- Model coefficients or feature importance (if interpretable regressor)

## How to apply

Generate molecular descriptors and fingerprints (e.g., MACCS166, Extended Connectivity, Path Fingerprints) for all molecules using a tool like alvaDesc. Train independent machine learning regressors on three feature configurations: (1) descriptors only, (2) fingerprints only, (3) both combined. Use identical train/test splits and hyperparameter tuning protocols across all three to ensure fair comparison. Compute mean absolute error (MAE) and median absolute error (MdAE) on a held-out test set for each trained model. Compare error distributions across feature sets and model types; select the configuration with the lowest test error. For large datasets like SMRT (80,038 molecules), consider nested cross-validation and Bayesian hyperparameter optimization (via Optuna or equivalent) to avoid overfitting during model selection.

## Related tools

- **alvaDesc** (Generates molecular descriptors (5,666 total) and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints; 2,214 total) for input molecules in SMILES, mol, SDF, mol2, or inchi formats) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative open-source tool for fingerprint generation; used in provided notebooks for training DNNs with RDKit fingerprints)
- **Optuna** (Bayesian hyperparameter optimization framework for tuning regressor hyperparameters during nested cross-validation)

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models --train_size 0.8 --param_search_folds 5 --trials 100
```

## Evaluation signals

- MAE and MdAE are computed on identical held-out test sets for all three feature configurations; fingerprint-only models achieve lower errors than descriptor-only models.
- Error distributions are statistically comparable (same train/test split, same random seed across all models) to isolate the effect of feature representation.
- Nested cross-validation results stored in optuna/*.db files show consistent ranking of feature sets across outer CV folds, confirming reproducibility.
- Best regressor (e.g., heavily regularized DNN with cosine annealing warm restarts) achieves reported MAE and MdAE within ±1–2 seconds of published results (e.g., 39.2±1.2 s and 17.2±0.9 s for SMRT).
- Feature importance or learned weights differ meaningfully between descriptor-only and fingerprint-only models, confirming that feature representation drives performance differences.

## Limitations

- Comparison is limited to the three feature configurations (descriptors only, fingerprints only, combined); other molecular representations (e.g., graph neural networks, SMILES embeddings) are not tested in the source work.
- alvaDesc is a licensed commercial tool; open-source alternatives (RDKit) may generate different fingerprints and produce different model rankings.
- SMRT dataset includes both retained and unretained molecules; generalization to other retention time databases or chromatographic methods requires separate meta-learning or transfer learning steps (see related Bayesian meta-learning skill).
- Results are specific to retention time prediction; feature ranking may differ for other molecular property targets (e.g., solubility, toxicity).

## Evidence

- [other] Do fingerprints outperform molecular descriptors alone or in combination with descriptors for machine learning-based retention time prediction?: "Do fingerprints outperform molecular descriptors alone or in combination with descriptors for machine learning-based retention time prediction?"
- [intro] The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better.: "The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better."
- [intro] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [intro] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [intro] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] make train_predictor: Trains a subset of regressors on a subset of the SMRT database using Bayesian hyperparameter search.: "make train_predictor: Trains a subset of regressors on a subset of the SMRT database using Bayesian hyperparameter search."
- [readme] A summary of all tested models is stored in the database results/optuna/train.db.: "A summary of all tested models is stored in the database results/optuna/train.db."
