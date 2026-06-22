---
name: interquartile-range-filtering-for-outlier-rejection
description: Use when when you have ensemble predictions (e.g., from Monte-Carlo Dropout inference with N ≥ 10 forward passes per input) and need to distinguish high-confidence from uncertain predictions before downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3379
  tools:
  - matchms
  - MS2DeepScore
  - Python
  - RDKit
  - scikit-learn
  - Monte-Carlo Dropout
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
---

# Interquartile-range filtering for outlier rejection

## Summary

Filter ensemble predictions by interquartile range (IQR) thresholds to identify and retain only high-confidence predictions, reducing model uncertainty and improving error metrics across prediction bins. This technique leverages multiple forward passes through a Monte-Carlo Dropout network to quantify prediction confidence and reject outliers.

## When to use

When you have ensemble predictions (e.g., from Monte-Carlo Dropout inference with N ≥ 10 forward passes per input) and need to distinguish high-confidence from uncertain predictions before downstream analysis. Use this when model uncertainty correlates with prediction error and you can afford to discard a fraction of predictions in exchange for improved accuracy in retained samples.

## When NOT to use

- Input predictions come from a single forward pass (no ensemble); IQR filtering requires multiple predictions per input to compute meaningful uncertainty.
- Ground-truth labels are not available; filtering requires validation against known targets to assess error reduction.
- The analysis requires 100% prediction coverage; IQR filtering discards predictions, reducing the dataset size and potentially introducing bias if uncertainty correlates with input characteristics rather than model confidence.

## Inputs

- Ensemble predictions (N forward passes per input, typically N=10)
- Ground-truth labels or binning targets (e.g., reference Tanimoto scores)
- IQR threshold value (e.g., 0.025)

## Outputs

- Filtered prediction set (subset of input predictions passing IQR threshold)
- Per-bin RMSE or error metric summary
- Sample retention rate and error reduction statistics

## How to apply

For each input (e.g., spectrum pair), compute the median and interquartile range (IQR) from the N ensemble predictions. IQR is defined as the difference between the 75th and 25th percentiles. Retain only predictions where IQR falls below a chosen threshold (e.g., IQR < 0.025 for MS2DeepScore Tanimoto predictions). Stratify the retained predictions by ground-truth bins (e.g., by reference Tanimoto score ranges: 0.0–0.1, 0.1–0.2, etc.) and recompute per-bin error metrics (RMSE, MAE, or similar). Compare filtered and unfiltered RMSE to quantify the improvement; focus on bins where uncertainty is highest (typically extreme score ranges like <0.4 or >0.8 for similarity scores). The threshold is a hyperparameter that should be tuned based on the acceptable trade-off between sample retention rate and error reduction.

## Related tools

- **MS2DeepScore** (Siamese neural network producing ensemble predictions via Monte-Carlo Dropout; IQR filtering applied to its Tanimoto score predictions) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectrum data cleaning and preparation; used upstream to prepare spectra before MS2DeepScore inference) — https://github.com/matchms/matchms
- **Monte-Carlo Dropout** (Uncertainty quantification technique enabling multiple stochastic forward passes; provides the ensemble of predictions from which IQR is computed)
- **scikit-learn** (Percentile computation for IQR calculation; used for binning and stratified analysis)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
import numpy as np

model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)

# Run 10 forward passes with dropout enabled
predictions_ensemble = np.array([ms2ds.predict(spectrum_pairs) for _ in range(10)])
median_pred = np.median(predictions_ensemble, axis=0)
iqr_pred = np.percentile(predictions_ensemble, 75, axis=0) - np.percentile(predictions_ensemble, 25, axis=0)

# Filter by IQR < 0.025
filtered_mask = iqr_pred < 0.025
filtered_predictions = median_pred[filtered_mask]
```

## Evaluation signals

- Per-bin RMSE for filtered predictions is lower than unfiltered baseline (expect 20–40% reduction in extreme bins, e.g., <0.4 and >0.8 Tanimoto ranges).
- Sample retention rate (fraction of predictions passing IQR threshold) is reported and trade-off with error reduction is quantified.
- IQR distribution shows clear separation between retained (low IQR) and rejected (high IQR) predictions; histograms should be unimodal or bimodal with a cutoff visible.
- Error reduction is most pronounced in extreme bins (Tanimoto <0.4 and >0.8); mid-range bins (0.5–0.7) may show slight degradation due to lower sample count.
- Threshold choice (e.g., IQR < 0.025) is justified by hyperparameter sweep showing optimal trade-off point on validation data.

## Limitations

- IQR filtering assumes uncertainty (measured by IQR) is a reliable proxy for prediction error; systematic model biases unrelated to dropout variation will not be corrected.
- Threshold selection is dataset- and model-dependent; a threshold optimal for MS2DeepScore Tanimoto predictions may not generalize to other models or prediction targets.
- Discarding predictions reduces effective sample size, particularly in sparse bins; statistical power for bin-level analysis may be compromised.
- Extreme score ranges (Tanimoto <0.1 or >0.9) often have fewer ground-truth pairs in training data, so ensemble predictions in these regions may be inherently unreliable regardless of IQR.
- No guidance provided on computational requirements for N=10 forward passes; runtime scales linearly with ensemble size.

## Evidence

- [other] Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement): "Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement)"
- [methods] At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were computed per spectrum pair: "At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were"
- [other] For each pair, compute the median prediction and interquartile range (IQR) from the 10 predictions: "For each pair, compute the median prediction and interquartile range (IQR) from the 10 predictions."
- [results] filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds: "filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds"
- [other] most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges, while slightly increasing error in the mid score range (0.5–0.7): "most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges, while slightly increasing error in the mid score range (0.5–0.7)"
- [intro] we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
