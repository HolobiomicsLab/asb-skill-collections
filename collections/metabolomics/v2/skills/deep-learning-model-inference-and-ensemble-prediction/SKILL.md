---
name: deep-learning-model-inference-and-ensemble-prediction
description: Use when you have a trained deep learning model and want to quantify
  prediction uncertainty for each input pair or decision point. Use this when you
  need to identify low-confidence predictions (high IQR) and filter them out to reduce
  error in specific score ranges (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3318
  tools:
  - matchms
  - MS2DeepScore
  - Python
  - RDKit
  - scikit-learn
  - PyTorch
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included
  cleaning compound names
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral
  embeddings for all 3601 spectra in the test set
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
- we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute
  structural similarities
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

# Deep-learning model inference and ensemble prediction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Run a trained deep learning model (e.g., Siamese neural network) on pairs of inputs with Monte-Carlo Dropout enabled to generate multiple stochastic predictions per pair, then compute ensemble statistics (median, interquartile range) to estimate prediction confidence and filter predictions by uncertainty thresholds.

## When to use

You have a trained deep learning model and want to quantify prediction uncertainty for each input pair or decision point. Use this when you need to identify low-confidence predictions (high IQR) and filter them out to reduce error in specific score ranges (e.g., low or high similarity bins). This is particularly valuable when predictions must be stratified by reference labels and uncertainty filtering is expected to improve per-stratum error metrics.

## When NOT to use

- The model has not been trained on representative data or does not achieve acceptable baseline accuracy (RMSE ~0.15 or better); ensemble filtering will not recover a fundamentally poor model.
- Your goal is to improve overall RMSE uniformly across all score ranges; ensemble filtering is effective only in extreme bins and may increase error in mid-range (0.5–0.7) predictions.
- You need predictions on every input pair without exception; uncertainty-based filtering will discard a fraction of pairs, reducing coverage.

## Inputs

- trained Siamese neural network model (PyTorch .pt file)
- test-set spectrum embeddings or spectrum pairs (numerical arrays, shape [n_pairs, embedding_dim])
- reference labels for stratification (e.g., Tanimoto scores, molecular fingerprint similarities)
- number of Monte-Carlo forward passes (N, typically 10)

## Outputs

- ensemble predictions per pair (median of N forward passes)
- prediction uncertainties per pair (interquartile range, IQR)
- per-bin RMSE before and after IQR filtering
- RMSE improvement (% reduction) by reference label bin
- filtered prediction set (only pairs with IQR below threshold)

## How to apply

Load the trained model and test-set input embeddings. Enable dropout during inference (set dropout=True at prediction time) and run N forward passes (typically N=10) per input pair with dropout stochastically active in all non-input layers. For each pair, compute the median prediction and interquartile range (IQR) across the N predictions. Stratify all predictions into bins by reference label (e.g., 10 equal-width bins by Tanimoto score: 0.0–0.1, 0.1–0.2, …, 0.9–1.0). Calculate per-bin RMSE on unfiltered predictions, then apply an IQR threshold (e.g., IQR < 0.025) to retain only low-uncertainty predictions and recompute per-bin RMSE. Compare improvement (% reduction in RMSE) especially in extreme bins to verify that uncertainty filtering concentrates error reduction where needed.

## Related tools

- **MS2DeepScore** (trained Siamese neural network model that predicts structural similarity (Tanimoto scores) from tandem mass spectra pairs; enables dropout-based inference for uncertainty quantification) — https://github.com/matchms/ms2deepscore
- **matchms** (spectrum data loading, cleaning, and metadata extraction before feeding spectra into the neural network) — https://github.com/matchms/matchms
- **RDKit** (computation of Tanimoto scores on molecular fingerprints (2048-bit Daylight) to generate reference labels for stratification and error evaluation)
- **PyTorch** (underlying framework for model loading, forward pass execution with dropout enabled, and tensor operations)
- **scikit-learn** (RMSE calculation and per-bin error metrics via metrics.mean_squared_error)

## Examples

```
from ms2deepscore.models import load_model; from ms2deepscore import MS2DeepScore; model = load_model('ms2deepscore_model.pt'); ms2ds = MS2DeepScore(model); predictions = ms2ds.predict_mces(spectrum_pairs, return_predictions_df=True); predictions_filtered = predictions[predictions['prediction_uncertainty'] < 0.025]; rmse_filtered = np.sqrt(np.mean((predictions_filtered['prediction'] - predictions_filtered['tanimoto']) ** 2))
```

## Evaluation signals

- IQR values should be non-negative and substantially smaller than the full prediction range; median IQR across all pairs should be << 1.0 (e.g., 0.02–0.15 in Tanimoto space).
- Per-bin RMSE after IQR filtering should be lower than before filtering, with the largest absolute reduction in extreme bins (< 0.4 and > 0.7 Tanimoto); typical improvement is 20–35% overall (e.g., 0.17 → 0.11).
- Filtering should not eliminate >50% of predictions; retained fraction should vary by bin (low and high bins typically lose more pairs than mid-range bins due to higher uncertainty).
- Mid-range bins (0.5–0.7 Tanimoto) may show slight RMSE increase after filtering, which is an expected trade-off; this pattern confirms the filter is working as designed.
- Histogram or scatter plot of prediction vs. IQR should show a positive relationship: higher IQR predictions tend to have larger absolute errors, justifying the filtering criterion.

## Limitations

- Monte-Carlo Dropout is a stochastic approximation of Bayesian uncertainty; it does not provide true Bayesian posterior estimates and may underestimate uncertainty in out-of-distribution regions.
- Effectiveness depends strongly on dropout rate and layer placement during training; models not trained with dropout in mind may not produce well-calibrated uncertainties.
- IQR filtering reduces coverage (discards predictions) and is most effective only in extreme score ranges; it does not uniformly improve accuracy across all prediction types.
- N=10 forward passes is a computational trade-off; larger N improves IQR stability but increases runtime proportionally (10× the inference cost of single-pass prediction).
- Stratification and evaluation depend on availability of reference labels (e.g., Tanimoto scores); this skill is not applicable to fully unsupervised prediction without ground truth.

## Evidence

- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were generated per spectrum pair: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles [17]. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were"
- [other] Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges, while slightly increasing error in the mid score range (0.5–0.7): "Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges,"
- [other] For each pair, compute the median prediction and interquartile range (IQR) from the 10 predictions. 4. Stratify all predictions into 10 equally-sized bins by reference Tanimoto score: "For each pair, compute the median prediction and interquartile range (IQR) from the 10 predictions. 4. Stratify all predictions into 10 equally-sized bins by reference Tanimoto score"
- [intro] MS2DeepScore can also make use of Monte-Carlo dropout [17] to assess the model uncertainty: "MS2DeepScore can also make use of Monte-Carlo dropout [17] to assess the model uncertainty"
- [intro] we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [readme] In addition to the prediction of a structural similarity, MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum.: "In addition to the prediction of a structural similarity, MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum"
