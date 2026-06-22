---
name: root-mean-squared-error-calculation
description: Use when when you have paired predictions and ground-truth structural similarity labels (e.g., predicted Tanimoto scores from a neural network and reference Tanimoto scores from RDKit Daylight fingerprints) and need to report a single scalar metric of model prediction error across all pairs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MS2DeepScore
  - Python
  - RDKit
  - NumPy
  - PyTorch or TensorFlow
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- mean squared error (MSE) loss
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

# root-mean-squared-error-calculation

## Summary

Compute root mean squared error (RMSE) between predicted and reference structural similarity scores (Tanimoto) across all spectrum pairs to quantify prediction accuracy of neural network models. RMSE serves as the primary regression loss metric and final evaluation criterion for MS2DeepScore model performance.

## When to use

When you have paired predictions and ground-truth structural similarity labels (e.g., predicted Tanimoto scores from a neural network and reference Tanimoto scores from RDKit Daylight fingerprints) and need to report a single scalar metric of model prediction error across all pairs. Use this skill when evaluating trained MS2DeepScore models on test sets or when monitoring validation loss during training.

## When NOT to use

- Input is already a scalar performance metric (e.g., already-computed RMSE or R² value) — do not recompute.
- Predictions and references have different lengths or misaligned indexing — ensure paired data before calculation.
- Reference labels are binary or categorical (e.g., compound match/no-match) rather than continuous similarity scores — use classification metrics instead.

## Inputs

- predicted_tanimoto_scores (array of float; typically 200-dimensional embeddings converted via cosine similarity)
- reference_tanimoto_scores (array of float; computed from RDKit Daylight fingerprints 2048-bit)
- spectrum_pairs (set of unique pairs; typically 6,485,401 pairs from 3,601 test spectra)

## Outputs

- rmse_metric (scalar float; root mean squared error between predictions and references)
- mse_loss_array (optional; per-pair squared error values for further analysis)

## How to apply

Load reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits) for each test spectrum pair. Generate predictions from the trained model (e.g., cosine similarity between 200-dimensional spectral embeddings converted to Tanimoto scores). Compute MSE loss formulation between predicted and reference scores across all pairs, then take the square root to obtain RMSE. Report the final RMSE value; typical target ranges are ~0.15 without uncertainty restrictions or ~0.10 with stricter interquartile range (IQR) filtering applied. Use this metric to compare model variants and assess generalization to unseen compounds.

## Related tools

- **NumPy** (Vectorized computation of MSE loss and RMSE across large arrays of predictions and references)
- **RDKit** (Generate reference Tanimoto scores from Daylight fingerprints (2048 bits) for ground-truth comparison)
- **MS2DeepScore** (Generate predicted Tanimoto scores via trained Siamese network embeddings for RMSE calculation) — https://github.com/matchms/ms2deepscore
- **PyTorch or TensorFlow** (MSE loss computation during model training (Adam optimizer with MSE loss formulation))

## Examples

```
import numpy as np
from sklearn.metrics import mean_squared_error
predicted = np.array([...])  # cosine similarities converted to Tanimoto
reference = np.array([...])  # RDKit Daylight fingerprint Tanimoto scores
rmse = np.sqrt(mean_squared_error(reference, predicted))
print(f'RMSE: {rmse:.4f}')
```

## Evaluation signals

- RMSE value is in the expected range: ~0.15 for unfiltered predictions or ~0.10 with IQR-based uncertainty restrictions applied.
- RMSE is computed over all 6,485,401 test spectrum pairs (or the full test set) and reported as a single scalar; verify pair count matches spectrum pair generation output.
- Predicted and reference arrays have identical length and correct alignment (no index mismatches).
- RMSE is monotonically lower or equal when uncertainty filtering (IQR thresholds) is applied; stricter filtering should yield smaller error on the filtered subset.
- Comparison across model variants (e.g., with/without Monte-Carlo Dropout) shows consistent relative ordering (e.g., uncertainty-filtered variant has lower RMSE).

## Limitations

- RMSE treats all prediction errors equally; outliers or extreme mispredictions have outsized influence. For robustness, complement with median absolute error (MAE) or IQR-based filtering (as done in the paper for ~0.10 target).
- RMSE aggregates error across all similarity ranges; model may perform better on high-similarity pairs and worse on low-similarity pairs. Breakdown by similarity bin or separate reporting per range recommended.
- Reference labels (RDKit Tanimoto scores) are not ground truth but themselves derived from fingerprints, which may not capture all chemical similarity aspects; reported RMSE is relative to this proxy, not true chemical similarity.
- Computational cost scales linearly with number of spectrum pairs; for very large test sets (millions of pairs), batch processing or downsampling may be needed.

## Evidence

- [other] MS2DeepScore achieves a root mean squared error of approximately 0.15 for predicted Tanimoto scores on the test set without uncertainty restrictions.: "MS2DeepScore achieves a root mean squared error of approximately 0.15 for predicted Tanimoto scores on the test set without uncertainty restrictions."
- [other] Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores (no uncertainty filtering applied). Retrieve reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits) for each test spectrum pair. Compute root mean squared error (RMSE) between predicted and reference Tanimoto scores across all test pairs using the MSE loss formulation.: "Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores (no uncertainty filtering applied). Retrieve reference Tanimoto scores computed from RDKit Daylight"
- [methods] Models were trained with the Adam optimizer [44, 45] that optimized the mean squared error (MSE) loss: "Models were trained with the Adam optimizer that optimized the mean squared error (MSE) loss"
- [intro] MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [results] filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds: "filtered out scores, according to increasingly stringent interquartile range (IQR) thresholds"
- [methods] Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities: "Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
