---
name: performance-threshold-filtering-and-analysis
description: Use when when a trained model produces probabilistic or ensemble predictions and you need to achieve a specific target accuracy metric (e.g., RMSE ≤ 0.1) or minimize error on a test set, but the unfiltered model does not meet that target.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - scikit-learn
  - Monte-Carlo Dropout
  - matchms
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
- Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore_cq
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

# Performance-threshold filtering and analysis

## Summary

Incrementally filter model predictions by uncertainty quantile thresholds to trade off between prediction accuracy and retrieval rate, identifying the threshold at which a target performance metric (e.g., RMSE) is achieved. This skill applies ensemble-based uncertainty estimates (e.g., interquartile range from Monte-Carlo Dropout) to systematically reduce prediction error by discarding high-uncertainty predictions.

## When to use

When a trained model produces probabilistic or ensemble predictions and you need to achieve a specific target accuracy metric (e.g., RMSE ≤ 0.1) or minimize error on a test set, but the unfiltered model does not meet that target. Apply this skill when you have a quantifiable uncertainty estimate (variance, IQR, or confidence interval) per prediction and can accept loss of retrieval rate in exchange for improved precision on retained predictions.

## When NOT to use

- When no uncertainty estimate is available from the model (e.g., point predictions only, no ensemble).
- When you must retain all predictions (e.g., full population coverage is a hard constraint and accuracy cannot be traded for precision).
- When ground truth labels are unavailable for the test set; accuracy cannot be computed or validated without reference scores.

## Inputs

- Ensemble predictions (multiple forward passes or model samples per test instance)
- Per-prediction uncertainty estimates (e.g., IQR, variance, or confidence intervals)
- Reference labels or ground truth scores (e.g., Tanimoto structural similarity scores)
- Test set of spectrum pairs or other paired observations

## Outputs

- Filtered prediction set (subset of original predictions meeting uncertainty threshold)
- Performance metric (RMSE, MAE, or other loss) as a function of uncertainty threshold
- Retrieval rate (fraction of predictions retained) as a function of uncertainty threshold
- Threshold recommendation and corresponding accuracy–retrieval tradeoff curve

## How to apply

First, generate ensemble predictions by enabling dropout during inference (e.g., N=10 forward passes per spectrum pair). Compute a per-prediction uncertainty metric—typically the interquartile range (IQR) across ensemble members. Then, systematically increment the uncertainty threshold (e.g., IQR cutoffs of 0.05, 0.10, 0.15, etc.), filtering out all predictions exceeding each threshold. For each threshold, recompute the target metric (RMSE, MAE, etc.) against reference labels (e.g., Tanimoto scores from RDKit Daylight fingerprints) and record both the accuracy and the fraction of retained predictions. Plot accuracy versus retrieval rate to identify the threshold that achieves your target performance. This approach quantifies the accuracy-coverage tradeoff and reveals whether your target is achievable with uncertainty filtering.

## Related tools

- **MS2DeepScore** (Siamese neural network trained to predict structural similarity scores from MS/MS spectrum pairs; provides embeddings and uncertainty estimates via Monte-Carlo Dropout) — https://github.com/matchms/ms2deepscore
- **Monte-Carlo Dropout** (Enables uncertainty quantification by running multiple forward passes with dropout enabled at inference time to generate ensemble predictions)
- **RDKit** (Computes reference Tanimoto scores from Daylight fingerprints (2048 bits) for validation and accuracy evaluation)
- **scikit-learn** (Provides metrics and visualization utilities for computing and plotting accuracy (RMSE) and retrieval rate curves)
- **matchms** (Cleans and preprocesses MS/MS spectrum metadata and pairs; integrates with MS2DeepScore for data preparation) — https://github.com/matchms/matchms

## Examples

```
from ms2deepscore.models import load_model; from ms2deepscore import MS2DeepScore; import numpy as np; model = load_model('ms2deepscore_model.pt'); ms2ds = MS2DeepScore(model); embeddings_ensemble = [ms2ds.get_embedding_array(spectra) for _ in range(10)]; similarities = [np.median([emb[i] for emb in embeddings_ensemble], axis=0) for i in range(len(spectra))]; iqrs = [np.percentile([emb[i] for emb in embeddings_ensemble], 75, axis=0) - np.percentile([emb[i] for emb in embeddings_ensemble], 25, axis=0) for i in range(len(spectra))]; filtered_idx = [i for i, iqr in enumerate(iqrs) if iqr <= 0.10]; rmse_filtered = np.sqrt(np.mean((similarities[filtered_idx] - reference_scores[filtered_idx])**2))
```

## Evaluation signals

- RMSE (or other target metric) decreases monotonically or plateaus as the IQR threshold increases, approaching the target value (e.g., 0.1) at high thresholds.
- Retrieval rate (fraction of retained predictions) decreases as the uncertainty threshold becomes more stringent, following an expected inverse relationship with accuracy gain.
- The accuracy–retrieval tradeoff curve is smooth and monotonic; no large discontinuities or reversals indicate inconsistent filtering or data errors.
- At the recommended threshold, the reported RMSE matches the target metric and the number of retained predictions is realistic (e.g., not < 1% or > 100% of the test set).
- Filtered and unfiltered predictions can be compared: unfiltered RMSE should be higher (worse) than filtered RMSE at the same threshold, confirming that uncertainty filtering improves accuracy.

## Limitations

- Requires an ensemble or probabilistic model; point estimates without uncertainty quantification cannot be filtered this way.
- Trading accuracy for retrieval rate means a fraction of predictions are discarded; if the discarded subset is biased (e.g., systematically excludes rare or difficult cases), downstream analyses may be skewed.
- The choice of uncertainty metric (IQR, variance, entropy, etc.) and its interpretation are model-dependent; no single threshold generalizes across different models or datasets without empirical validation.
- High-uncertainty restrictions can discard > 75% of predictions (as demonstrated in the study), severely limiting practical applicability in scenarios requiring high coverage.
- Threshold selection is dataset- and metric-specific; a threshold tuned on one test set may not transfer to a different test set or when the reference ground truth changes.

## Evidence

- [other] Monte-Carlo Dropout ensemble predictions with IQR-based filtering reduce average RMSE from ~0.17 to ~0.11 by discarding ~75% of predictions with highest uncertainty: "Monte-Carlo Dropout ensemble predictions with IQR-based filtering reduce average RMSE from ~0.17 to ~0.11 by discarding ~75% of predictions with highest uncertainty, demonstrating that strong"
- [other] For each spectrum pair, enable dropout during inference and generate N=10 forward passes through the network with dropout rate 0.2 to create an ensemble of 200-dimensional spectral embeddings.: "For each spectrum pair, enable dropout during inference and generate N=10 forward passes through the network with dropout rate 0.2 to create an ensemble of 200-dimensional spectral embeddings."
- [other] Calculate the median and interquartile range (IQR) across the 10 predictions for each pair.: "Calculate the median and interquartile range (IQR) across the 10 predictions for each pair."
- [other] Filter predictions by incrementally raising the IQR threshold (e.g., discarding predictions with IQR above 0.05, 0.10, 0.15, etc.) and compute RMSE against reference Tanimoto scores for each threshold.: "Filter predictions by incrementally raising the IQR threshold (e.g., discarding predictions with IQR above 0.05, 0.10, 0.15, etc.) and compute RMSE against reference Tanimoto scores for each"
- [other] Plot RMSE and retrieval rate (fraction of retained predictions) versus IQR threshold and verify that RMSE approaches 0.10 at high uncertainty restriction levels.: "Plot RMSE and retrieval rate (fraction of retained predictions) versus IQR threshold and verify that RMSE approaches 0.10 at high uncertainty restriction levels."
- [other] Compute the reference Tanimoto scores using RDKit Daylight fingerprints (2048 bits) for all test pairs.: "Compute the reference Tanimoto scores using RDKit Daylight fingerprints (2048 bits) for all test pairs."
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network"
- [intro] MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [results] filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds: "filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds"
