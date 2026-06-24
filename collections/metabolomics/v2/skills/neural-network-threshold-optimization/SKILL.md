---
name: neural-network-threshold-optimization
description: Use when after training a NeatMS neural network model on labelled peak
  data (High_quality, Low_quality, Noise) and you need to determine the optimal probability
  threshold for classifying peaks in your untargeted LCMS dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3372
  tools:
  - NeatMS
  - Python
  - pandas
  - scikit-learn
  - NumPy
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create
  a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
- import pandas as pd
- from sklearn.metrics import auc
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02220
  all_source_dois:
  - 10.1021/acs.analchem.1c02220
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neural-network-threshold-optimization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Optimize classification thresholds for a trained neural network model by computing true vs. false positive rates across probability thresholds and selecting the threshold that maximizes the difference between true positives and false positives. This skill is essential for tuning NeatMS peak classification to balance sensitivity and specificity in automated LCMS false positive filtering.

## When to use

Apply this skill after training a NeatMS neural network model on labelled peak data (High_quality, Low_quality, Noise) and you need to determine the optimal probability threshold for classifying peaks in your untargeted LCMS dataset. Use it when you have a validation dataset with known labels and want to avoid manually selecting an arbitrary threshold.

## When NOT to use

- Input peak dataset is unlabelled or lacks ground-truth class annotations — threshold optimization requires comparison against known labels.
- Neural network model has not been trained or validated; optimize only after the model converges on a held-out validation set.
- Raw LCMS data is not yet processed into a feature table or peak list — data import and feature detection must precede threshold selection.

## Inputs

- Trained NeatMS neural network model (.h5 format)
- Labelled validation peak dataset with class labels (High_quality, Low_quality, Noise)
- Batch-prepared peak data via NN_handler object

## Outputs

- Optimal classification probability threshold (scalar numeric value)
- True vs. false positive rates table (pandas DataFrame with columns: Probability_threshold, True, False, False_low, False_noise)
- Classification metrics at the optimal threshold

## How to apply

Load the trained NeatMS neural network model in .h5 format using nn_handler.create_model(). Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to generate a threshold-dependent recall table spanning probability thresholds from 0.00 to 0.99, which computes True Positive Rate, False Positive Rate, and false positive composition (Low_quality vs. Noise) at each threshold. The method internally selects the threshold that maximizes (True positives − False positives), returning a scalar optimal threshold value. Verify the returned threshold against expected reference values (e.g., 0.22 for the default NeatMS model) before applying it to classify peaks in new datasets. The rationale is that this optimization balances the trade-off between retaining genuine peaks and rejecting false positives without manual ROC curve inspection.

## Related tools

- **NeatMS** (Provides NN_handler class and get_threshold() / get_true_vs_false_positive_df() methods for threshold optimization) — https://github.com/bihealth/NeatMS
- **Python** (Programming language for calling NeatMS API and data processing)
- **pandas** (Manipulates and inspects threshold-dependent recall DataFrame)
- **scikit-learn** (Computes AUC and other classification metrics during threshold analysis)
- **NumPy** (Numerical computation for threshold iteration and metric aggregation)

## Examples

```
nn_handler = create_model(model='path_to_model.h5')
optimal_threshold = nn_handler.get_threshold()
threshold_df = nn_handler.get_true_vs_false_positive_df(label='High_quality')
print(f'Optimal threshold: {optimal_threshold}')
```

## Evaluation signals

- Returned optimal threshold scalar value matches expected reference (e.g., 0.22 for default NeatMS model).
- True vs. false positive rates table contains rows for all probability thresholds (0.00–0.99 in increments) with non-null True, False, False_low, False_noise columns.
- At the optimal threshold, (True positives − False positives) is maximized compared to all other thresholds in the table.
- Spot-check specific thresholds (e.g., at threshold 0.01, verify True ≈ 1.0, False ≈ 0.44, False_low ≈ 0.803) against expected ROC analysis results.
- Threshold value falls within [0.0, 1.0] and is appropriate for the neural network output (probability) range.

## Limitations

- Threshold optimization is sensitive to the labelling quality and representativeness of the validation dataset; mislabelled peaks or an unbalanced class distribution will produce misleading thresholds.
- The (True positives − False positives) criterion may not be optimal for all use cases; domain-specific cost functions (e.g., prioritizing recall over precision) may require manual threshold selection instead.
- Default NeatMS model threshold (0.22) is pre-optimized for general untargeted LCMS peak filtering; transfer-learned or custom-trained models may require re-optimization on project-specific validation data.
- No automated mechanism in NeatMS to detect overfitting of the threshold to the validation set; external test data is recommended for final model evaluation.

## Evidence

- [other] Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds.: "Call nn_handler.get_threshold() which internally invokes get_true_vs_false_positive_df(label='High_quality') to compute true vs. false positive rates across probability thresholds."
- [other] The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value.: "The method selects the threshold that maximizes (True positives minus False positives) and returns the optimal scalar value."
- [other] Verify the returned threshold matches the expected reference value (0.22 for the default model).: "Verify the returned threshold matches the expected reference value (0.22 for the default model)."
- [other] Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to compute the threshold-dependent recall table across probability thresholds from 0.00 to 0.99.: "Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to compute the threshold-dependent recall table across probability thresholds from 0.00 to 0.99."
- [readme] NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines."
