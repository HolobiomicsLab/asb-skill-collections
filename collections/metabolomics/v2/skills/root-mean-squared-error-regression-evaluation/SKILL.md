---
name: root-mean-squared-error-regression-evaluation
description: Use when you have a trained regression model (e.g., a neural network or similar predictor) and a held-out test set with ground-truth continuous labels, and you need to measure whether the model's predictions match the true values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3958
  - http://edamontology.org/topic_0091
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - matchms
  - Monte-Carlo Dropout
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set
- we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# root-mean-squared-error-regression-evaluation

## Summary

RMSE is a summary metric for evaluating regression model predictions by computing the square root of mean squared differences between predicted and ground-truth continuous values. It is useful when you need a single interpretable number (in the same units as the target variable) to quantify overall prediction error across a test set.

## When to use

Apply this skill when you have a trained regression model (e.g., a neural network or similar predictor) and a held-out test set with ground-truth continuous labels, and you need to measure whether the model's predictions match the true values. Use RMSE particularly when prediction errors are approximately normally distributed and you want to penalize larger errors more heavily than smaller ones.

## When NOT to use

- Do not use RMSE when the target variable is categorical or ordinal; use classification metrics (accuracy, F1, AUC-ROC) instead.
- Do not use RMSE alone when your test set contains extreme outliers or heavy-tailed error distributions; supplement with robust metrics like median absolute error or report RMSE alongside percentile-based error bounds.
- Do not report RMSE without stratification when test data is heavily imbalanced across different regions of the target range (e.g., Tanimoto scores 0.1–0.9 vs. 0.9–1.0); disaggregate RMSE by score bins to identify model failures in specific ranges.

## Inputs

- Predicted continuous values (vector of length N, e.g., Tanimoto scores from model inference)
- Ground-truth continuous labels (vector of length N, e.g., RDKit Daylight fingerprint-based Tanimoto scores)
- Optional: uncertainty estimates (e.g., MC-Dropout prediction samples for each test instance)

## Outputs

- RMSE scalar value (root mean squared error, in same units as target)
- Optional: filtered test set indices (samples passing IQR threshold)
- Optional: RMSE on filtered subset (e.g., high-confidence predictions only)

## How to apply

For each spectrum or sample pair in the test set, obtain the model's predicted continuous value (e.g., Tanimoto similarity score between 0 and 1 from a Siamese network inference). Compute the squared difference between the predicted value and the ground-truth label for every sample. Average these squared differences across all N test samples, then take the square root to yield RMSE in the original units. Report RMSE for the full unfiltered test set as the primary metric. Optionally, apply uncertainty quantification (e.g., Monte-Carlo Dropout with N=10 forward passes) to estimate prediction confidence intervals for each sample; filter the test set to retain only predictions with interquartile range (IQR) below a threshold (e.g., IQR < 0.025), then recalculate RMSE on the filtered subset to assess performance on high-confidence predictions.

## Related tools

- **MS2DeepScore** (Siamese neural network model that outputs predicted Tanimoto scores; RMSE evaluates these predictions against ground-truth structural similarity labels) — https://github.com/matchms/ms2deepscore
- **RDKit** (Computes ground-truth Tanimoto scores from molecular fingerprints (2048-bit Daylight) to serve as regression targets for RMSE calculation)
- **Monte-Carlo Dropout** (Provides uncertainty estimates (via multiple stochastic forward passes) used to filter predictions before RMSE recalculation, enabling stratified evaluation)
- **matchms** (Handles spectrum data preparation, metadata cleaning, and infrastructure for loading test spectra and their annotations) — https://github.com/matchms/matchms

## Examples

```
from sklearn.metrics import mean_squared_error; import numpy as np; rmse = np.sqrt(mean_squared_error(y_true=ground_truth_tanimoto, y_pred=predicted_tanimoto)); print(f'RMSE (full test set): {rmse:.4f}'); filtered_idx = iqu_values < 0.025; rmse_filtered = np.sqrt(mean_squared_error(y_true=ground_truth_tanimoto[filtered_idx], y_pred=predicted_tanimoto[filtered_idx])); print(f'RMSE (IQR < 0.025): {rmse_filtered:.4f}')
```

## Evaluation signals

- RMSE should be reported for both the full unfiltered test set and any filtered subsets (e.g., IQR < 0.025), with improvement quantified as percentage reduction when filtering is applied.
- RMSE values should fall within expected ranges reported in the literature (e.g., ~0.15 without filtering, ~0.10 with strict IQR filtering for MS2DeepScore on 3,601-spectrum test set).
- RMSE should be computed and reported separately for different regions of the target range (e.g., Tanimoto scores 0.1–0.3, 0.3–0.6, 0.6–0.9) to detect if the model systematically underperforms on low, medium, or high similarity pairs.
- Verify that the number of samples included in RMSE matches the test set size (3,601 spectra for MS2DeepScore) and document how many predictions were excluded by any filtering step.
- Check that all predicted values and ground-truth labels are in the expected range (Tanimoto scores between 0 and 1) and that no NaN or infinite values are present before RMSE calculation.

## Limitations

- RMSE equally weights all samples and error magnitudes; very large errors on a few outlier samples can inflate RMSE substantially. Complement with median absolute error or robust quantile-based metrics if outliers are suspected.
- RMSE does not directly indicate whether the model is suitable for ranking or retrieval tasks (e.g., finding true structural neighbors); use precision/recall or ROC analysis to assess ranking performance.
- RMSE on a held-out test set of 3,601 spectra from only 500 unique compounds may not reflect generalization to completely novel compounds or chemical scaffolds not seen during training; test set diversity limitations are inherited from the data.

## Evidence

- [other] root mean squared error of approximately 0.15 without uncertainty filtering and 0.1 when applying interquartile range (IQR < 0.025) thresholds: "MS2DeepScore predicts Tanimoto scores on the 3,601-spectrum test set with root mean squared error of approximately 0.15 without uncertainty filtering and 0.1 when applying interquartile range (IQR <"
- [other] Calculate root mean squared error (RMSE) between predicted and ground-truth scores for the full test set (no filter). Apply Monte-Carlo Dropout uncertainty quantification and filter predictions, then recalculate RMSE on the filtered subset.: "Calculate root mean squared error (RMSE) between predicted and ground-truth scores for the full test set (no filter). 6. Apply Monte-Carlo Dropout uncertainty quantification (N=10 forward passes with"
- [intro] a root mean squared error of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [results] MS2DeepScore generally performs very well and can predict Tanimoto scores between 0.1 and 0.9 with a RMSE between 0.13 and 0.2: "MS2DeepScore generally performs very well and can predict Tanimoto scores between 0.1 and 0.9 with a RMSE between 0.13 and 0.2"
- [results] filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds: "filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds"
