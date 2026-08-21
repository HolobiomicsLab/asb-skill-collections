---
name: neural-network-ensemble-inference-via-dropout
description: Use when when you have a trained neural network and need to quantify
  prediction uncertainty or improve accuracy by filtering low-confidence predictions.
  Particularly useful when input spectra pairs have variable quality or when downstream
  tasks (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0081
  tools:
  - MS2DeepScore
  - Monte-Carlo Dropout
  - RDKit
  - Python
  - scikit-learn
  - matchms
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
  [17]. At inference time, dropout was applied to all but the first layer of the base
  network.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates
  over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over
  all spectra and was used for
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neural-network-ensemble-inference-via-dropout

## Summary

Generate uncertainty-aware ensemble predictions from a trained neural network by enabling dropout during inference and aggregating multiple stochastic forward passes. This technique produces both point estimates and confidence intervals for each prediction without retraining.

## When to use

When you have a trained neural network and need to quantify prediction uncertainty or improve accuracy by filtering low-confidence predictions. Particularly useful when input spectra pairs have variable quality or when downstream tasks (e.g., compound retrieval) require high-confidence matches. Apply when base model RMSE (~0.15–0.17) is too high and uncertainty-driven filtering is acceptable.

## When NOT to use

- If the network was trained without dropout regularization, ensemble sampling will not produce meaningful uncertainty estimates.
- If ground-truth similarity labels are unavailable or cannot be computed, you cannot evaluate whether filtering improves accuracy.
- If speed is critical and you cannot afford N forward passes per prediction; ensemble inference is ~N times more expensive than single inference.

## Inputs

- pre-trained Siamese neural network with dropout layers
- test set spectrum pairs (MS/MS spectra with metadata)
- reference structural similarity scores (e.g., Tanimoto scores on RDKit Daylight fingerprints)

## Outputs

- ensemble predictions: N similarity scores per spectrum pair
- aggregated statistics per pair: median, IQR
- filtered predictions after uncertainty thresholding
- RMSE vs. IQR threshold curve
- retrieval rate vs. IQR threshold curve

## How to apply

Load the pre-trained neural network and enable dropout at inference time (do not set to eval mode). For each input spectrum pair, perform N forward passes (e.g., N=10) through the network with dropout active (typical dropout rate 0.2), collecting the output embedding or similarity score from each pass. Compute the median and interquartile range (IQR) across the N predictions per pair. Filter predictions by applying an IQR threshold: retain only predictions where IQR ≤ threshold (e.g., 0.05, 0.10, 0.15). Incrementally raise the threshold to trade off prediction volume against accuracy. Compute RMSE against reference ground truth (e.g., RDKit Tanimoto scores) and retrieval rate (fraction of retained predictions) at each threshold. Select the threshold that achieves your accuracy target (e.g., RMSE ≤ 0.1).

## Related tools

- **MS2DeepScore** (Pre-trained Siamese network that predicts structural similarity from MS/MS spectrum pairs; ensemble inference with dropout is applied to this model) — https://github.com/matchms/ms2deepscore
- **RDKit** (Computes reference Tanimoto scores on Daylight fingerprints (2048 bits) for ground-truth evaluation)
- **matchms** (Loads, cleans, and prepares MS/MS spectra metadata and annotations for inference) — https://github.com/matchms/matchms
- **Python** (Scripting language for implementing ensemble inference loop and threshold optimization)
- **scikit-learn** (Provides utilities (e.g., metrics) for computing and plotting RMSE and retrieval statistics)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
import numpy as np

model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)

# N=10 forward passes with dropout enabled
ensemble_scores = np.array([ms2ds.pair_predictions(spectrum_pairs, use_dropout=True) for _ in range(10)])
median_pred = np.median(ensemble_scores, axis=0)
iqr_pred = np.percentile(ensemble_scores, 75, axis=0) - np.percentile(ensemble_scores, 25, axis=0)

# Filter by IQR threshold
threshold = 0.10
filtered_mask = iqr_pred <= threshold
filtered_scores = median_pred[filtered_mask]
```

## Evaluation signals

- RMSE decreases monotonically as IQR threshold increases (uncertainty filtering removes high-error predictions).
- Retrieval rate (fraction of retained predictions) decreases as IQR threshold becomes stricter; typical target is ~25–75% retention at RMSE ≤ 0.1.
- Median and IQR values are reproducible across repeated runs with the same random seed and dropout rate.
- Predictions with low IQR (<0.05) have lower RMSE than predictions with high IQR (>0.15), confirming IQR is a useful uncertainty proxy.
- At high uncertainty restriction (e.g., IQR ≤ 0.05), RMSE approaches 0.10 on retained predictions, matching the published finding.

## Limitations

- Ensemble quality depends on dropout rate and number of forward passes (N); too few passes or poor dropout configuration yield unreliable uncertainty estimates.
- IQR-based filtering discards potentially useful predictions; retrieval rate may be too low for large-scale screening applications.
- The method requires pre-trained networks with dropout; it cannot be applied to frozen or eval-mode networks.
- Ground-truth structural similarity labels (e.g., RDKit Tanimoto) must be available to evaluate and calibrate the threshold; performance on unlabeled data is unknown.
- Computational cost is ~N times higher than single inference; for N=10 and large datasets, this can be prohibitive without GPU acceleration.

## Evidence

- [other] For each spectrum pair, enable dropout during inference and generate N=10 forward passes through the network with dropout rate 0.2 to create an ensemble of 200-dimensional spectral embeddings.: "For each spectrum pair, enable dropout during inference and generate N=10 forward passes through the network with dropout rate 0.2 to create an ensemble of 200-dimensional spectral embeddings."
- [other] Calculate the median and interquartile range (IQR) across the 10 predictions for each pair.: "Calculate the median and interquartile range (IQR) across the 10 predictions for each pair."
- [other] Filter predictions by incrementally raising the IQR threshold (e.g., discarding predictions with IQR above 0.05, 0.10, 0.15, etc.) and compute RMSE against reference Tanimoto scores for each threshold.: "Filter predictions by incrementally raising the IQR threshold (e.g., discarding predictions with IQR above 0.05, 0.10, 0.15, etc.) and compute RMSE against reference Tanimoto scores for each"
- [other] Monte-Carlo Dropout ensemble predictions with IQR-based filtering reduce average RMSE from ~0.17 to ~0.11 by discarding ~75% of predictions with highest uncertainty, demonstrating that strong uncertainty restrictions achieve near 0.1 RMSE on the test set.: "Monte-Carlo Dropout ensemble predictions with IQR-based filtering reduce average RMSE from ~0.17 to ~0.11 by discarding ~75% of predictions with highest uncertainty"
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network.: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network."
- [intro] MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [results] filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds: "filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds"
- [readme] In addition to the prediction of a structural similarity, MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum.: "In addition to the prediction of a structural similarity, MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum."
