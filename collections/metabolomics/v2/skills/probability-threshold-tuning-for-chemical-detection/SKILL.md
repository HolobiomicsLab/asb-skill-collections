---
name: probability-threshold-tuning-for-chemical-detection
description: Use when you have a trained NeatMS neural network model (.h5 format)
  and need to select an operating threshold for peak classification on your LCMS dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - NeatMS
  - Python
  - pandas
  - NumPy
  - scikit-learn
  techniques:
  - LC-MS
  license_tier: open
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
- import numpy as np
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

# probability-threshold-tuning-for-chemical-detection

## Summary

Optimize NeatMS neural network classification thresholds to balance true positive retention and false positive filtering in untargeted LCMS peak detection. This skill identifies the probability cutoff that best separates high-quality peaks from low-quality and noise peaks based on threshold-dependent ROC metrics.

## When to use

You have a trained NeatMS neural network model (.h5 format) and need to select an operating threshold for peak classification on your LCMS dataset. Use this skill when you must trade off sensitivity (TPR—keeping true peaks) against specificity (1-FPR—rejecting false peaks), and want to understand the composition of false positives (low-quality vs. noise) at each threshold.

## When NOT to use

- Input model is not trained on your data domain (e.g., model trained on positive-mode LCMS applied to negative-mode without retraining or transfer learning).
- You have fewer than ~500 labeled peaks per class; insufficient training data undermines threshold optimization reliability.
- Peak detection pipeline output is already validated by independent orthogonal method; further filtering may remove true signals.

## Inputs

- Trained NeatMS neural network model in .h5 format
- NeatMS experiment object with labeled peaks (High_quality, Low_quality, Noise classes)

## Outputs

- Threshold-dependent recall table (pandas DataFrame) with columns: Probability_threshold, True (TPR), False (FPR), False_low, False_noise
- Selected probability threshold value (float, 0.00–0.99)
- Performance metrics at chosen threshold (TPR, FPR, composition of false positives)

## How to apply

Load the trained NeatMS model using nn_handler.create_model(model='path_to_model.h5'). Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to generate a threshold-dependent recall table across probability thresholds (0.00–0.99). Extract rows corresponding to candidate thresholds and inspect the True (TPR), False (FPR), False_low (fraction of false positives that are Low_quality), and False_noise (fraction that are Noise) columns. Compare TPR and FPR values across thresholds to identify the cutoff that meets your retention and filtering objectives. For example, a threshold of 0.01 yields TPR=1.0 (100% retention) but FPR=0.440 (44% false positive rate), whereas higher thresholds reduce FPR at the cost of losing true peaks. Document the selected threshold and its associated metrics for reproducibility.

## Related tools

- **NeatMS** (Provides neural network handler (nn_handler) to load trained models and compute threshold-dependent true/false positive rates via get_true_vs_false_positive_df() method) — https://github.com/bihealth/NeatMS
- **Python** (Scripting environment for importing NeatMS, iterating over threshold dataframes, and data manipulation)
- **pandas** (Dataframe library for loading and filtering threshold-dependent recall tables)
- **scikit-learn** (Optional—metrics module for computing AUC and ROC curves if visualizing threshold trade-offs)

## Examples

```
from neatms import nn_handler; model = nn_handler.create_model(model='trained_model.h5'); threshold_df = nn_handler.get_true_vs_false_positive_df(label='High_quality'); threshold_row = threshold_df[threshold_df['Probability_threshold'] == 0.01]; print(threshold_row[['True', 'False', 'False_low', 'False_noise']])
```

## Evaluation signals

- Verify output dataframe contains all probability thresholds from 0.00 to 0.99 with no missing rows.
- Confirm that TPR is monotonically non-increasing as threshold increases (higher threshold → fewer peaks retained).
- Confirm that FPR is monotonically non-increasing as threshold increases (higher threshold → fewer false positives).
- Check that True + False_low + False_noise = 1.0 (or within ~1% due to rounding) at each row—composition of false positives must sum to 100%.
- Spot-check a selected threshold row: verify reported TPR and FPR values align with domain expectations (e.g., at threshold=0.01, TPR should be ≥0.95 for high-sensitivity use cases; at threshold=0.5, FPR should be <0.1 for high-specificity filtering).

## Limitations

- NeatMS does not currently provide automatic callback functions to halt training; threshold optimization is valid only for a fully trained model. Resume training cautiously to avoid overfitting.
- Threshold selection is sensitive to the composition and representativeness of the labeled training dataset. If training peaks were selected from only a subset of samples or acquisition conditions, threshold performance may degrade on out-of-sample data.
- False positive composition (False_low vs. False_noise ratio) is informative but not actionable via threshold alone; a threshold that reduces FPR equally affects both classes. Separate filtering or manual review may be needed if you want to retain Low_quality peaks while discarding Noise.
- No changelog is provided in the repository; versioning and reproducibility of model behavior across NeatMS releases is not documented.

## Evidence

- [other] Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to compute the threshold-dependent recall table across probability thresholds from 0.00 to 0.99.: "Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to compute the threshold-dependent recall table across probability thresholds from 0.00 to 0.99."
- [other] Extract the row corresponding to Probability_threshold=0.01 and read the True, False, False_low, and False_noise column values.: "Extract the row corresponding to Probability_threshold=0.01 and read the True, False, False_low, and False_noise column values."
- [other] NeatMS relies on neural network based classification to distinguish true from false positive peaks in untargeted LCMS data.: "NeatMS relies on neural network based classification to distinguish true from false positive peaks in untargeted LCMS data."
- [readme] NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS enables automated filtering of false positive MS<sup>1</sup> peaks reported by commonly used LCMS data processing pipelines."
- [other] Load a trained NeatMS neural network model (in .h5 format) using nn_handler.create_model(model='path_to_model.h5').: "Load a trained NeatMS neural network model (in .h5 format) using nn_handler.create_model(model='path_to_model.h5')."
