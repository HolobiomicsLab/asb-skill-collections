---
name: deep-neural-network-regularization
description: Use when when training a DNN on molecular properties (e.g., retention
  time) using high-dimensional feature sets (>2000 fingerprints + descriptors) where
  test performance is critical and overfitting risk is high due to model capacity
  or limited validation data;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3047
  - http://edamontology.org/topic_3611
  tools:
  - alvaDesc
  - PyTorch or TensorFlow
  - Optuna
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity,
  and Path Fingerprints fingerprints) were generated with the alvaDesc software
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

# deep-neural-network-regularization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply heavy L1/L2 regularization combined with cosine annealing warm restarts and stochastic weight averaging to train deep neural networks for retention time prediction, reducing overfitting and improving generalization on molecular descriptor/fingerprint feature spaces.

## When to use

When training a DNN on molecular properties (e.g., retention time) using high-dimensional feature sets (>2000 fingerprints + descriptors) where test performance is critical and overfitting risk is high due to model capacity or limited validation data; when target metrics require sub-40 s mean absolute error and sub-18 s median absolute error on held-out test sets.

## When NOT to use

- Input is already regularized or uses ensemble methods that handle overfitting independently
- Target problem has <10,000 training samples and feature dimensionality <100 (standard regularization may be sufficient)
- Computational budget is severely constrained; cosine annealing warm restarts and SWA require multiple full training passes

## Inputs

- training dataset with molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) and/or descriptors
- validation dataset partition
- test dataset partition
- hyperparameter search space (L1/L2 coefficients, learning rate schedule parameters)

## Outputs

- trained DNN model weights
- mean absolute error (MAE) on test set with confidence interval
- median absolute error on test set with confidence interval
- hyperparameter optimization database (Optuna or equivalent)

## How to apply

Initialize a DNN with L1/L2 penalty coefficients calibrated via Bayesian hyperparameter search. Train using a cosine annealing warm restart scheduler (which periodically resets the learning rate) to escape local minima and explore the loss landscape more thoroughly. Apply stochastic weight averaging (SWA) by averaging model weights from multiple epochs in later training stages to find flatter minima that generalize better. Evaluate on held-out test data using mean absolute error and median absolute error as primary metrics, reporting results with confidence intervals (±1.2 s for mean, ±0.9 s for median is the reference benchmark). Compare final metrics against the reference performance to confirm regularization efficacy.

## Related tools

- **alvaDesc** (Generate molecular descriptors (5,666 total) and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints; 2,214 total) as input features for DNN training) — https://www.alvascience.com/alvadesc/
- **PyTorch or TensorFlow** (DNN framework for implementing regularized layers, cosine annealing scheduler (torch.optim.lr_scheduler.CosineAnnealingWarmRestarts), and stochastic weight averaging)
- **Optuna** (Bayesian hyperparameter optimization for tuning L1/L2 coefficients and scheduler parameters) — https://optuna.org

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models --trials 100 --param_search_folds 5
```

## Evaluation signals

- Mean absolute error (MAE) on test set ≤ 39.2 ± 1.2 s (reference benchmark from paper)
- Median absolute error on test set ≤ 17.2 ± 0.9 s (reference benchmark from paper)
- Cross-validation curves show reduced overfitting gap between training and validation loss
- Stochastic weight averaging produces a model checkpoint with lower validation error than the final epoch before averaging
- Confidence intervals on MAE/median error overlap or are contained within reference intervals, indicating reproducible performance

## Limitations

- Requires alvaDesc software (under license) to generate fingerprints; alternative fingerprint sources may not reproduce exact error bounds
- Hyperparameter search via Bayesian optimization is computationally expensive; smoke tests in the repository use subsampled data and fewer trials
- Performance is dataset-specific; METLIN SMRT (80,038 molecules) may not generalize to smaller or chemically different retention time datasets
- Cosine annealing warm restarts and SWA add training time compared to standard SGD; full training on the complete dataset requires hours to days depending on hardware

## Evidence

- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT); both retained and unretained molecules were considered.: "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software.: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software."
- [other] Initialize a heavily regularized deep neural network with appropriate L1/L2 penalties.: "Initialize a heavily regularized deep neural network with appropriate L1/L2 penalties."
- [other] Train the model using cosine annealing warm restarts scheduler and stochastic weight averaging to reduce overfitting and improve generalization.: "Train the model using cosine annealing warm restarts scheduler and stochastic weight averaging to reduce overfitting and improve generalization."
