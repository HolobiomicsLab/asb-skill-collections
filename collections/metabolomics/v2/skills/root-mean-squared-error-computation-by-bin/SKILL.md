---
name: root-mean-squared-error-computation-by-bin
description: Use when when evaluating a regression or similarity prediction model and you need to understand whether prediction error is uniform across the outcome space or concentrated in particular ranges (e.g., low structural similarity vs. high similarity scores).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0091
  tools:
  - matchms
  - MS2DeepScore
  - Python
  - RDKit
  - scikit-learn
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
- we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Root-mean-squared-error computation by bin

## Summary

Stratifies predictions into equally-sized bins across a reference variable (e.g., Tanimoto score range) and computes RMSE independently for each bin to reveal performance variation across the prediction space. This enables detection of systematic error patterns in specific score ranges, which is essential for model validation and uncertainty-based filtering in deep learning similarity prediction.

## When to use

When evaluating a regression or similarity prediction model and you need to understand whether prediction error is uniform across the outcome space or concentrated in particular ranges (e.g., low structural similarity vs. high similarity scores). Apply this skill when you suspect that a model's overall RMSE may mask poor performance in specific score bins, or when you want to validate the effect of uncertainty filtering (e.g., IQR thresholds) on per-bin error reduction.

## When NOT to use

- Input predictions are already aggregated or pre-binned; you need raw predictions and reference values aligned at the record level.
- Reference variable is categorical or ordinal with few unique values; stratification by equal-width bins on continuous scale is not meaningful.
- Sample size is very small and bins become sparsely populated (RMSE estimates become unstable); consider adaptive binning or larger sample sizes.

## Inputs

- Predictions (array of model outputs, e.g., predicted structural similarity scores)
- Reference values (array of ground truth labels aligned with predictions, e.g., Tanimoto scores computed from molecular fingerprints)
- Bin edges or bin count (specification of how to stratify the reference variable)
- Optional: uncertainty estimates per prediction (e.g., interquartile range from Monte-Carlo Dropout ensemble) for filtering

## Outputs

- Per-bin RMSE values (numeric array, one RMSE per bin)
- Filtered per-bin RMSE values (if filtering is applied)
- RMSE improvement per bin (numeric array: difference between unfiltered and filtered RMSE)
- Visualization or summary table showing RMSE trends across bins

## How to apply

First, stratify all predictions into N equally-sized bins by a reference variable (e.g., 10 bins for Tanimoto scores 0.0–0.1, 0.1–0.2, …, 0.9–1.0). For each bin, compute RMSE independently using the subset of predictions and their corresponding reference values: RMSE_bin = sqrt(mean((predicted - reference)²)). Optionally, apply filtering criteria (e.g., retain only predictions with interquartile range < 0.025 from Monte-Carlo Dropout ensemble) and recompute per-bin RMSE. Calculate the difference (improvement) between unfiltered and filtered RMSE for each bin. Focus analysis on bins of interest (e.g., low similarity < 0.4 and high similarity > 0.8) to determine whether the filter reduces error more effectively in specific ranges.

## Related tools

- **MS2DeepScore** (Deep learning model that generates predictions (structural similarity scores) to be binned and evaluated by RMSE computation) — https://github.com/matchms/ms2deepscore
- **scikit-learn** (Used for stratification and binning operations; provides computational utilities for grouping and error calculation)
- **RDKit** (Computes reference labels (Tanimoto scores on molecular fingerprints) used as ground truth for RMSE computation)
- **matchms** (Provides spectrum data structures and filtering utilities that prepare inputs for model prediction) — https://github.com/matchms/matchms

## Examples

```
import numpy as np
from sklearn.metrics import mean_squared_error

# Predict and reference are 1D arrays
predicted = model.predict(test_spectra)  # MS2DeepScore predictions
reference = np.array([tanimoto_scores])  # RDKit Tanimoto ground truth

# Bin by Tanimoto score into 10 equal-width bins
bins = np.linspace(0, 1, 11)
bin_indices = np.digitize(reference, bins) - 1

# Compute RMSE per bin
rmse_per_bin = []
for b in range(10):
    mask = bin_indices == b
    if mask.sum() > 0:
        rmse = np.sqrt(mean_squared_error(reference[mask], predicted[mask]))
        rmse_per_bin.append(rmse)
    else:
        rmse_per_bin.append(np.nan)

print(f"RMSE by bin: {rmse_per_bin}")
```

## Evaluation signals

- Verify that all bins contain roughly equal numbers of predictions (or confirm the binning strategy is intentional); imbalanced bins indicate stratification failure.
- Check that per-bin RMSE values are monotonic or follow an expected trend (e.g., typically higher error in low or high similarity ranges); erratic variation may signal data quality issues or implementation error.
- Confirm that RMSE improvement (unfiltered minus filtered) is non-negative and greatest in bins expected to have high uncertainty (e.g., low similarity bins); negative improvement indicates filter is harmful.
- Validate that sum or weighted average of per-bin contributions approximates the overall RMSE (accounting for bin sizes); large discrepancy signals calculation error.
- Cross-check a few hand-calculated RMSE values for a single bin against the computed results to confirm mathematical correctness.

## Limitations

- Equal-width binning may produce bins with very few samples in tails (e.g., few predictions near 0.0 or 1.0 Tanimoto score); consider quantile-based binning for sparse regions.
- Per-bin RMSE is highly sensitive to sample size within each bin; small bins have unstable estimates. The paper does not report bin population sizes, limiting assessment of statistical reliability.
- RMSE is symmetric and dominated by large outliers; median absolute error or quantile-based metrics may be more robust if extreme errors are present.
- Filtering (e.g., by IQR threshold) reduces sample size per bin, potentially creating empty or very small bins where RMSE cannot be computed; the paper notes this effect but does not detail how empty bins are handled.
- The skill assumes reference labels (e.g., Tanimoto scores) are error-free; mislabeled or noisy ground truth will inflate RMSE and invalidate per-bin comparisons.

## Evidence

- [methods] Stratify all predictions into 10 equally-sized bins by reference Tanimoto score (0.0–0.1, 0.1–0.2, …, 0.9–1.0). Compute RMSE (root mean squared error) for each bin using all predictions.: "Stratify all predictions into 10 equally-sized bins by reference Tanimoto score (0.0–0.1, 0.1–0.2, …, 0.9–1.0). 5. Compute RMSE (root mean squared error) for each bin using all predictions."
- [methods] Filter predictions by IQR threshold (retain only those with IQR < 0.025) and recompute per-bin RMSE. Calculate the RMSE difference (improvement) between unfiltered and IQR-filtered predictions for each Tanimoto bin, with particular focus on bins < 0.4 and > 0.7.: "Filter predictions by IQR threshold (retain only those with IQR < 0.025) and recompute per-bin RMSE. 7. Calculate the RMSE difference (improvement) between unfiltered and IQR-filtered predictions for"
- [full_text] Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges, while slightly increasing error in the mid score range (0.5–0.7).: "Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges,"
