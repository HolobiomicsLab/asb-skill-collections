---
name: stochastic-weight-averaging-ensemble
description: Use when training a heavily regularized deep neural network on molecular property prediction tasks (e.g., retention time prediction) where you observe signs of overfitting despite L1/L2 penalties, or when you need to reduce variance in predictions on held-out test sets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
  tools:
  - alvaDesc
  - PyTorch / TensorFlow
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# stochastic-weight-averaging-ensemble

## Summary

Stochastic weight averaging (SWA) is a regularization and ensemble technique that improves deep neural network generalization by averaging model weights collected at regular intervals during training, particularly when combined with learning rate scheduling like cosine annealing warm restarts. It reduces overfitting and stabilizes predictions on retention time and similar regression tasks.

## When to use

Apply this skill when training a heavily regularized deep neural network on molecular property prediction tasks (e.g., retention time prediction) where you observe signs of overfitting despite L1/L2 penalties, or when you need to reduce variance in predictions on held-out test sets. It is especially valuable when combined with cosine annealing learning rate schedules that naturally produce multiple local minima during training.

## When NOT to use

- Input is a single model checkpoint rather than a collection of snapshots from different training phases.
- Training does not use a cyclic learning rate schedule (e.g., fixed or exponential decay); SWA is most effective when weight snapshots are drawn from distinct local minima.
- Target task is classification rather than regression, unless the ensemble averaging rationale applies to your loss landscape.

## Inputs

- trained deep neural network checkpoints (multiple weight snapshots from different training epochs)
- molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) or descriptors as feature vectors
- validation/test dataset with experimental retention time labels

## Outputs

- averaged weight model (single DNN with consolidated weights)
- predicted retention times for test molecules
- mean absolute error and median absolute error metrics with confidence intervals

## How to apply

During training of a regularized DNN, periodically save model weights at regular intervals (typically after each cosine annealing warm restart cycle). After the final epoch, average the collected weight snapshots into a single model. This averaged model is evaluated on held-out test data to compute final metrics (mean absolute error, median absolute error, or other regression losses). The rationale is that averaging weights across multiple points in the loss landscape produces a model with better generalization than any single checkpoint, especially when those checkpoints are drawn from distinct local minima created by the warm-restart schedule. Combine SWA with L1/L2 regularization to further constrain the weight magnitudes during this averaging process.

## Related tools

- **alvaDesc** (generates molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) and descriptors used as input features for the DNN trained with stochastic weight averaging) — https://www.alvascience.com/alvadesc/
- **PyTorch / TensorFlow** (deep learning framework for implementing the heavily regularized DNN, cosine annealing warm restarts scheduler, and weight averaging logic)

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models
```

## Evaluation signals

- Mean absolute error on held-out test set matches or improves upon reported baseline (39.2±1.2 s for SMRT retention time prediction).
- Median absolute error on held-out test set matches or improves upon reported baseline (17.2±0.9 s for SMRT).
- Confidence intervals (±1.2 s for MAE, ±0.9 s for median) are reproducible across multiple random seeds or cross-validation folds.
- Averaged model exhibits lower test-set error than any individual weight snapshot before averaging, confirming the ensemble benefit.
- Regularization (L1/L2 penalties) remains applied during weight averaging; inspect final model weights for reasonable magnitude ranges consistent with regularization strength.

## Limitations

- Requires multiple weight snapshots during training, increasing memory and storage overhead; not suitable for extremely large models or limited-resource environments.
- Effectiveness depends strongly on the learning rate schedule; if the schedule does not produce meaningful diversity in local minima (e.g., static or slowly changing learning rate), averaging may provide minimal benefit.
- The paper reports results on SMRT dataset (80,038 molecules); generalization to smaller datasets or very different molecular domains is not explicitly tested.
- No explicit guidance on optimal checkpoint frequency, cooling schedule, or number of snapshots to average; hyperparameter tuning may be required for new tasks or datasets.

## Evidence

- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively.: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [other] A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean and median absolute errors of 39.2±1.2 s and 17.2±0.9 s on retention time prediction.: "A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean and median absolute errors of 39.2±1.2 s and 17.2±0.9 s on retention time"
- [other] Train the model using cosine annealing warm restarts scheduler and stochastic weight averaging to reduce overfitting and improve generalization.: "Train the model using cosine annealing warm restarts scheduler and stochastic weight averaging to reduce overfitting and improve generalization."
- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [readme] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
