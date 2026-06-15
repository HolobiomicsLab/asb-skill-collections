---
name: deep-neural-network-training-regularization
description: 'Use when training a DNN on retention time prediction or similar continuous regression tasks where: (1) the feature space is very high-dimensional (thousands of molecular descriptors and fingerprints), (2) the training set is moderately sized (tens of thousands of molecules), (3) you observe or.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_2275
  tools:
  - alvaDesc
  - constantino-garcia/cmmrt
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
schema_version: 0.2.0
---

# deep-neural-network-training-regularization

## Summary

Training a deep neural network with heavy L1/L2 regularization, cosine annealing warm restarts, and stochastic weight averaging to achieve robust regression on high-dimensional molecular feature spaces. This skill is used when you need to prevent overfitting on modestly-sized datasets (e.g., 80K molecules) with thousands of features and improve generalization on held-out test sets.

## When to use

Apply this skill when training a DNN on retention time prediction or similar continuous regression tasks where: (1) the feature space is very high-dimensional (thousands of molecular descriptors and fingerprints), (2) the training set is moderately sized (tens of thousands of molecules), (3) you observe or expect overfitting, and (4) you need both mean and median absolute error to be competitive on held-out test data. This is especially relevant when comparing feature modalities (descriptors vs. fingerprints) and want a single architecture that works well across all conditions.

## When NOT to use

- Your input feature set is already low-dimensional (< 100 features); heavy regularization may unduly constrain model capacity and hurt performance.
- Your dataset is very small (< 1,000 training samples); the added complexity of cosine annealing + weight averaging may not generalize well without sufficient data.
- You are performing classification rather than regression; the choice of loss function and evaluation metrics (MAE, MdAE) is specific to continuous targets like retention time.

## Inputs

- Feature matrix combining molecular descriptors (5,666 per molecule) and fingerprints (2,214 per molecule; MACCS166, Extended Connectivity, Path Fingerprints)
- Target vector of experimental retention times (in seconds)
- Train–test split of the METLIN SMRT dataset (80,038 molecules total)

## Outputs

- Trained DNN model with optimized weights
- Mean absolute error (MAE) metric on test set (e.g., 39.2±1.2 s)
- Median absolute error (MdAE) metric on test set (e.g., 17.2±0.9 s)
- Per-molecule predictions and prediction errors on held-out test data

## How to apply

Configure a DNN with heavy L1/L2 penalties applied to all weight matrices to constrain model capacity. During training, use cosine annealing with warm restarts as the learning rate scheduler, which periodically resets the learning rate to its initial value while following a cosine decay curve between restarts; this encourages exploration of the loss landscape and escapes local minima. After training convergence, apply stochastic weight averaging by averaging model weights collected at regular intervals during the latter training epochs; this improves generalization by finding flatter minima in the loss surface. Evaluate on a held-out test set and report both mean absolute error (MAE) and median absolute error (MdAE) with their uncertainties. The rationale is that heavy regularization + learning rate scheduling + weight averaging together reduce overfitting and improve generalization on unseen molecules compared to standard training.

## Related tools

- **alvaDesc** (Generate 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for input molecules before DNN training) — https://www.alvascience.com/alvadesc/
- **constantino-garcia/cmmrt** (Reference implementation of DNN training with cosine annealing warm restarts and stochastic weight averaging for retention time prediction; includes train_model.py script and Makefile rules (make train_predictor) to execute full hyperparameter tuning and training) — https://github.com/constantino-garcia/cmmrt

## Examples

```
python cmmrt/rt/train_model.py --storage sqlite:///results/optuna/train.db --save_to saved_models --param_search_folds 5 --trials 100
```

## Evaluation signals

- Mean absolute error (MAE) on held-out test set should be in the range of 39.2±1.2 seconds or lower for SMRT dataset; verify that test MAE does not substantially exceed training MAE (sign of underfitting, not overfitting).
- Median absolute error (MdAE) should be substantially lower than MAE (e.g., 17.2±0.9 s), indicating robust predictions not dominated by outliers.
- Regularization strength and learning rate schedule should be tuned via Bayesian hyperparameter search (e.g., Optuna); inspect the hyperparameter search database to confirm multiple L1/L2 penalties and cosine annealing period lengths were tested.
- Stochastic weight averaging should produce lower test error than the final single model without averaging; compare final model MAE/MdAE before and after weight averaging.
- Cross-validation or repeated train–test splits should show low variance in MAE/MdAE across folds, indicating stable generalization across different random splits.

## Limitations

- The approach requires access to alvaDesc software (under commercial license) to generate the specific 5,666 descriptors and 2,214 fingerprints; open-source fingerprint generators (RDKit) may produce different feature spaces and may not replicate the reported error metrics.
- Cosine annealing warm restarts and stochastic weight averaging add computational overhead and are sensitive to hyperparameters (restart period, weight averaging interval); improper tuning may degrade performance.
- Performance is benchmarked only on METLIN SMRT (small molecule retention time data); generalization to other chemical domains, larger molecules, or different chromatographic methods requires re-training and validation.
- The reported uncertainties (±1.2 s for MAE, ±0.9 s for MdAE) reflect variability across runs or cross-validation folds; absolute error on individual predictions can be much higher (median 17 s does not imply all predictions are within ±17 s).

## Evidence

- [readme] A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s respectively: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [intro] Heavy L1/L2 regularization applied during DNN training: "Configure a deeply regularized DNN architecture with heavy regularization (L1/L2 penalties) and train using cosine annealing with warm restarts as the learning rate scheduler."
- [intro] Stochastic weight averaging improves generalization: "Apply stochastic weight averaging during training to improve generalization."
- [readme] Feature inputs: 5,666 molecular descriptors and 2,214 fingerprints generated with alvaDesc: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software."
- [readme] METLIN SMRT dataset size and content: "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
