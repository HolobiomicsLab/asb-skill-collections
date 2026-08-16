---
name: regression-model-evaluation-metrics
description: Use when after training a deep-learning regression model (e.g., for CCS
  prediction from voxel projected area features), evaluate it on held-out test data
  to report per-molecule predictions and aggregate performance metrics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - Python 3
  - RDKit
  - PyTorch
  - PyG
  - pandas
  - NumPy
  - conda
  - pip
  - scikit-learn
  techniques:
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1002/cem.70040
  title: PACCS
evidence_spans:
- '[python3](https://www.python.org/)'
- '[RDKit](https://rdkit.org/)'
- '[PyTorch](https://pytorch.org/)'
- '[PyG](https://pytorch-geometric.readthedocs.io/en/latest/)'
- '[pandas](https://pandas.pydata.org/)'
- '[NumPy](https://numpy.org/)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_paccs_cq
    doi: 10.1002/cem.70040
    title: PACCS
  dedup_kept_from: coll_paccs_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/cem.70040
  all_source_dois:
  - 10.1002/cem.70040
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# regression-model-evaluation-metrics

## Summary

Compute and interpret performance metrics on held-out test data for continuous-value regression models, such as CCS prediction from molecular features. This skill ensures trained models generalize beyond training and validation sets by quantifying prediction accuracy across multiple statistical measures.

## When to use

After training a deep-learning regression model (e.g., for CCS prediction from voxel projected area features), evaluate it on held-out test data to report per-molecule predictions and aggregate performance metrics. Apply this skill whenever you need to validate model accuracy on unseen molecules and generate publishable performance reports.

## When NOT to use

- Input is already a feature table without ground-truth labels — metrics require paired predictions and reference values.
- Test data was not held out during training or hyperparameter tuning — evaluation will be overly optimistic and not reflect generalization.
- Model output is categorical or probabilistic rather than continuous — use classification metrics (accuracy, F1, AUC) instead.

## Inputs

- trained PyTorch neural network model (checkpoint file)
- test dataset (SMILES, adduct type, ground-truth CCS labels)
- computed test features (voxel projected area, molecular graph, m/z, adduct encoding)

## Outputs

- per-molecule CCS predictions (numerical values)
- regression performance metrics (MAE, RMSE, R², MRE)
- model performance summary report (aggregated statistics)

## How to apply

Load the trained PyTorch model and the held-out test dataset (containing molecular features: voxel projected area, molecular graph, adduct one-hot encoding, m/z, and ground-truth CCS labels). Feed test features through the model to generate per-molecule CCS predictions. Compute standard regression metrics: mean absolute error (MAE), root mean squared error (RMSE), coefficient of determination (R²), and optionally mean relative error (MRE). Report predictions alongside metrics to assess both individual prediction quality and overall model generalization. Inspect residuals (predicted − actual) for systematic bias or heteroscedasticity.

## Related tools

- **PyTorch** (Load trained regression model checkpoint and compute batch predictions on test data) — https://pytorch.org/
- **pandas** (Organize test features, ground-truth labels, and predicted CCS values into DataFrames for metric computation and export) — https://pandas.pydata.org/
- **NumPy** (Compute regression metrics (MAE, RMSE, R²) and residual analysis via vectorized operations) — https://numpy.org/
- **scikit-learn** (Provide standard regression metrics functions (mean_absolute_error, mean_squared_error, r2_score))

## Examples

```
from PACCS.Prediction import PACCS_predict; PACCS_predict(input_path='data/external_test_set.csv', model_path='trained_model.pth', output_path='test_predictions.csv')
```

## Evaluation signals

- R² value is positive and close to 1 (>0.8 typical for well-fit models); negative R² indicates model performs worse than a simple mean baseline
- MAE and RMSE are in physically plausible units (Ångströms² for CCS); compare against literature benchmarks and external test set performance
- Per-molecule prediction residuals (actual − predicted) are normally distributed with mean near zero; systematic bias or heteroscedasticity suggests model deficiency
- Test set metrics are comparable to validation metrics from training; large gap suggests overfitting
- External test set predictions (if available) show similar accuracy to curated dataset test fold, confirming generalization

## Limitations

- Metrics are computed only on the held-out test set; performance on new, real-world molecules may differ if they have different chemical distributions.
- Single-fold evaluation does not capture variance across random seeds or data splits; k-fold or repeated-hold-out evaluation is more robust.
- RMSE is sensitive to outlier predictions; MAE may be more interpretable for applications with extreme values.
- R² can be misleading for non-linear relationships or when prediction errors are systematically biased in certain input regions.
- README mentions 8:1:1 split (training:validation:test) but does not specify random seed or stratification strategy, affecting reproducibility.

## Evidence

- [other] Evaluate the trained model on held-out test data and output per-molecule CCS predictions alongside model performance metrics.: "Evaluate the trained model on held-out test data and output per-molecule CCS predictions alongside model performance metrics."
- [readme] The curated dataset is randomly split into the training, validation, and test sets in a ratio of 8:1:1.: "The curated dataset is randomly split into the training, validation, and test sets in a ratio of 8:1:1."
- [other] Train the model on the prepared dataset using PyTorch, optimizing for CCS prediction accuracy across epochs with appropriate loss function and learning rate scheduling.: "Train the model on the prepared dataset using PyTorch, optimizing for CCS prediction accuracy across epochs"
- [readme] The predicted CCS values of molecules are obtained by feeding the voxel projected area, molecular graph, one-hot encoding of adduct type, and m/z into the already trained PACCS model: "The predicted CCS values of molecules are obtained by feeding the voxel projected area, molecular graph, one-hot encoding of adduct type, and m/z into the already trained PACCS model"
