---
name: monte-carlo-dropout-uncertainty-quantification
description: Use when when a trained Siamese neural network model makes predictions on new spectrum pairs and you need to identify and exclude high-uncertainty predictions to improve RMSE.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - matchms
  - Monte-Carlo Dropout
  - scikit-learn
  techniques:
  - LC-MS
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

# monte-carlo-dropout-uncertainty-quantification

## Summary

Quantify prediction uncertainty for neural network outputs by running multiple forward passes with dropout enabled, then computing interquartile range (IQR) across the ensemble predictions. This method enables filtering low-confidence predictions and improving model performance on downstream similarity scoring tasks.

## When to use

When a trained Siamese neural network model makes predictions on new spectrum pairs and you need to identify and exclude high-uncertainty predictions to improve RMSE. Use this when working with MS/MS spectra and Tanimoto score predictions, particularly when you want to stratify performance across different score ranges or when downstream analysis depends on prediction confidence.

## When NOT to use

- Model was not trained with dropout regularization, or dropout layers are absent in the architecture—uncertainty estimation requires stochastic forward passes
- You have a deterministic model without dropout capability or cannot afford N=10 forward passes per pair due to computational constraints
- Predictions are already known to be highly confident (e.g., very high or very low scores with natural low variance), making IQR filtering redundant

## Inputs

- trained Siamese neural network model with dropout layers
- test set of MS/MS spectrum pairs (e.g., 6,485,401 unique pairs from 3,601 spectra)
- ground-truth Tanimoto scores (computed from RDKit Daylight fingerprints, 2048 bits)
- preprocessed spectrum data (peaks binned into 10,000 equally-sized bins, intensities square-root transformed)

## Outputs

- ensemble predictions: N×(number of spectrum pairs) array of similarity scores
- uncertainty estimates: IQR values for each spectrum pair prediction
- filtered prediction set: subset of pairs passing IQR threshold (e.g., IQR < 0.025)
- per-bin RMSE: root mean squared error stratified by Tanimoto score bins (0.0–0.1, 0.1–0.2, …, 0.9–1.0)
- uncertainty-filtered RMSE: improved RMSE metric on low-uncertainty predictions

## How to apply

At inference time, disable the first layer but enable dropout in all subsequent layers of the base network. Run N=10 forward passes per spectrum pair through the same model, collecting the output similarity scores from each pass. For each pair, compute the median prediction and interquartile range (IQR) across the 10 predictions. Filter predictions by applying an IQR threshold (e.g., IQR < 0.025) to retain only low-uncertainty pairs, then recalculate RMSE on the filtered subset. This filtering typically reduces average RMSE from ~0.17 to ~0.11 (34% improvement), with the most significant gains in low (< 0.4) and high (> 0.8) Tanimoto score ranges.

## Related tools

- **MS2DeepScore** (Siamese neural network model for predicting structural similarity scores from MS/MS spectrum pairs; inference backbone for Monte-Carlo Dropout uncertainty quantification) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectrum data loading, preprocessing, and metadata cleaning; pipeline integration for computing similarities on spectrum collections) — https://github.com/matchms/matchms
- **RDKit** (Compute ground-truth Tanimoto scores from molecular fingerprints (2048-bit Daylight) for validation and training label generation)
- **scikit-learn** (Statistical analysis and visualization of stratified RMSE metrics across Tanimoto score bins)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
import numpy as np

model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)
# Run 10 forward passes with dropout enabled per spectrum pair
predictions = ms2ds.compute_similarity_with_uncertainty(spectrum_pairs, num_passes=10)
iqr_values = np.percentile(predictions, 75, axis=0) - np.percentile(predictions, 25, axis=0)
filtered_mask = iqr_values < 0.025
filtered_predictions = predictions[:, filtered_mask]
rmse_filtered = np.sqrt(np.mean((filtered_predictions.mean(axis=0) - ground_truth[filtered_mask])**2))
```

## Evaluation signals

- IQR values are computed from exactly N=10 forward passes per spectrum pair, with each pass drawing independent dropout samples
- RMSE on unfiltered predictions falls within expected range (~0.15–0.17 for MS2DeepScore Tanimoto predictions)
- RMSE on IQR-filtered predictions (IQR < 0.025 threshold) improves by ≥30% relative to unfiltered RMSE (e.g., 0.17 → 0.11)
- Per-bin RMSE stratification shows greatest improvement in extreme score ranges (< 0.4 and > 0.8) and modest or negative change in mid-range (0.5–0.7)
- Filtered prediction set size is 30–50% of original predictions for typical IQR < 0.025 thresholds, indicating selective high-confidence retention

## Limitations

- Uncertainty estimation quality depends on dropout rate and network architecture; the original model used dropout rate 0.2 and may not generalize to different architectures or rates
- Monte-Carlo Dropout is a post-hoc approximation to Bayesian uncertainty; actual calibration and coverage guarantees are not provided in the article
- IQR filtering improves overall RMSE but slightly increases error in the mid-range Tanimoto score region (0.5–0.7), potentially creating biased estimates in that range
- Computational cost scales linearly with ensemble size (N=10 passes per pair); large-scale inference on millions of pairs may require GPU acceleration

## Evidence

- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles [17]. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were"
- [other] Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges: "Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges"
- [other] Stratify all predictions into 10 equally-sized bins by reference Tanimoto score (0.0–0.1, 0.1–0.2, …, 0.9–1.0). Compute RMSE (root mean squared error) for each bin using all predictions. Filter predictions by IQR threshold (retain only those with IQR < 0.025) and recompute per-bin RMSE.: "Stratify all predictions into 10 equally-sized bins by reference Tanimoto score (0.0–0.1, 0.1–0.2, …, 0.9–1.0). Compute RMSE (root mean squared error) for each bin using all predictions. Filter"
- [readme] In addition to the prediction of a structural similarity, MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum.: "In addition to the prediction of a structural similarity, MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum."
- [intro] we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
