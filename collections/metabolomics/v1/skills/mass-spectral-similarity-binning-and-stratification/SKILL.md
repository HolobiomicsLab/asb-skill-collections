---
name: mass-spectral-similarity-binning-and-stratification
description: Use when you have predicted structural similarity scores (e.g., Tanimoto or Dice scores) for a large set of spectrum pairs and need to assess prediction accuracy across the full range of possible similarities. Critical when evaluating whether uncertainty filtering (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3070
  tools:
  - matchms
  - MS2DeepScore
  - Python
  - RDKit
  - scikit-learn
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
schema_version: 0.2.0
---

# Mass-spectral similarity binning and stratification

## Summary

Stratify MS/MS spectrum pairs into equal-width bins by reference Tanimoto structural similarity score to enable per-bin error analysis and detection of performance disparities across similarity ranges. This skill is essential for evaluating whether deep learning spectral similarity models exhibit systematic bias toward specific similarity ranges (e.g., low vs. high structural similarity).

## When to use

Apply this skill when you have predicted structural similarity scores (e.g., Tanimoto or Dice scores) for a large set of spectrum pairs and need to assess prediction accuracy across the full range of possible similarities. Critical when evaluating whether uncertainty filtering (e.g., IQR thresholds) or ensemble methods improve performance uniformly or only in specific similarity ranges, or when investigating whether predictions are biased toward mid-range scores.

## When NOT to use

- Input similarity scores are already binned or aggregated; you need raw predictions to stratify
- Reference labels are missing or sparse (binning requires complete ground-truth Tanimoto or Dice scores for all pairs)
- Similarity range is narrow or bimodal (equal-width binning may produce empty or highly imbalanced bins; consider quantile binning instead)

## Inputs

- Predicted structural similarity scores (e.g., MS2DeepScore Tanimoto predictions, shape N)
- Reference structural similarity labels (e.g., RDKit Tanimoto fingerprint scores, shape N)
- Optional: uncertainty estimates per prediction (e.g., IQR from Monte-Carlo Dropout ensembles)

## Outputs

- Per-bin RMSE or error metric array (shape: number of bins)
- Binned prediction assignments (mapping each prediction to its bin index)
- Per-bin sample counts (to assess bin balance)
- Optional: per-bin improvement metrics (e.g., % RMSE reduction after filtering)

## How to apply

First, obtain reference structural similarity labels for all spectrum pairs (computed from molecular fingerprints using RDKit Daylight fingerprints or equivalent). Divide the full similarity range (0.0–1.0) into N equally-sized bins (e.g., 10 bins of width 0.1: [0.0–0.1], [0.1–0.2], …, [0.9–1.0]). Assign each predicted score to its corresponding bin using the reference label. For each bin, compute per-bin error metrics (RMSE, MAE) separately. When filtering predictions by uncertainty thresholds (e.g., IQR < 0.025 from Monte-Carlo Dropout ensembles), recompute per-bin RMSE and calculate the absolute or percentage improvement. Pay particular attention to tail bins (< 0.4 and > 0.8) where model confidence often differs most from mid-range predictions.

## Related tools

- **RDKit** (Compute reference Tanimoto structural similarity scores from molecular fingerprints (Daylight 2048-bit))
- **matchms** (Load, filter, and manage MS/MS spectrum metadata and predictions for binning workflow) — https://github.com/matchms/matchms
- **MS2DeepScore** (Generate predicted structural similarity scores and optional uncertainty estimates (IQR from Monte-Carlo Dropout)) — https://github.com/matchms/ms2deepscore
- **scikit-learn** (Compute RMSE and other error metrics for per-bin evaluation)
- **Python** (Implement binning logic, assign predictions to bins, and calculate per-bin statistics)

## Examples

```
```python
import numpy as np
from sklearn.metrics import mean_squared_error

# Assume: predictions (N,), reference_tanimoto (N,), uncertainty_iqr (N,)
bin_edges = np.arange(0, 1.1, 0.1)  # 10 bins: [0–0.1], [0.1–0.2], …, [0.9–1.0]
bin_indices = np.digitize(reference_tanimoto, bin_edges) - 1

per_bin_rmse_unfiltered = []
per_bin_rmse_filtered = []

for bin_id in range(10):
    mask = bin_indices == bin_id
    if mask.sum() > 0:
        rmse_unfilt = np.sqrt(mean_squared_error(
            reference_tanimoto[mask], predictions[mask]))
        per_bin_rmse_unfiltered.append(rmse_unfilt)
        
        mask_filtered = mask & (uncertainty_iqr < 0.025)
        if mask_filtered.sum() > 0:
            rmse_filt = np.sqrt(mean_squared_error(
                reference_tanimoto[mask_filtered], predictions[mask_filtered]))
            per_bin_rmse_filtered.append(rmse_filt)

print('Per-bin RMSE (unfiltered):', per_bin_rmse_unfiltered)
print('Per-bin RMSE (IQR < 0.025 filtered):', per_bin_rmse_filtered)
```
```

## Evaluation signals

- Each bin contains roughly equal numbers of predictions (N_total / N_bins) unless intentionally stratified by quantile; verify bin size distribution is approximately uniform
- Per-bin RMSE values fall within expected range for the model (e.g., 0.13–0.2 for MS2DeepScore on Tanimoto 0.1–0.9 range)
- RMSE is lower in high-confidence bins (e.g., > 0.8 or < 0.4 after filtering) than in mid-range bins when uncertainty filtering is applied; improvements should be monotonic or follow model behavior
- Sum of per-bin prediction counts equals total number of predictions; no predictions are lost or duplicated during binning
- When comparing unfiltered vs. filtered (IQR-thresholded) predictions, per-bin RMSE improves (decreases) in at least 70% of bins, with largest absolute improvements in extreme bins (< 0.4 and > 0.8)

## Limitations

- Equal-width binning produces imbalanced or empty bins if predictions/reference scores cluster in specific ranges; quantile-based binning may be more robust for skewed distributions
- Per-bin RMSE becomes unreliable in sparsely-populated bins (< 10 predictions); minimum bin size should be enforced or reported
- Binning strategy assumes reference labels (e.g., Tanimoto from RDKit fingerprints) are ground truth; if fingerprints are inconsistent or missing for some molecules, binning accuracy degrades
- IQR-based filtering (e.g., IQR < 0.025) removes predictions preferentially from mid-range bins, potentially biasing per-bin statistics; report removal rates per bin
- Performance on very-low (< 0.1) or very-high (> 0.9) similarity bins may be limited by training data imbalance; article reports 'most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges'

## Evidence

- [other] Stratify all predictions into 10 equally-sized bins by reference Tanimoto score (0.0–0.1, 0.1–0.2, …, 0.9–1.0). Compute RMSE (root mean squared error) for each bin using all predictions.: "Stratify all predictions into 10 equally-sized bins by reference Tanimoto score (0.0–0.1, 0.1–0.2, …, 0.9–1.0). Compute RMSE (root mean squared error) for each bin using all predictions."
- [other] Filter predictions by IQR threshold (retain only those with IQR < 0.025) and recompute per-bin RMSE. Calculate the RMSE difference (improvement) between unfiltered and IQR-filtered predictions for each Tanimoto bin, with particular focus on bins < 0.4 and > 0.7.: "Filter predictions by IQR threshold (retain only those with IQR < 0.025) and recompute per-bin RMSE. Calculate the RMSE difference (improvement) between unfiltered and IQR-filtered predictions for"
- [other] Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges: "Monte-Carlo Dropout filtering at IQR < 0.025 reduces average RMSE from 0.17 to 0.11 (34% improvement) with most significant RMSE reductions in low (< 0.4) and high (> 0.8) Tanimoto score ranges"
- [methods] we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities: "we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
- [methods] For every unique 14-character InChIKey the most common InChI was selected and used to generate a molecular fingerprint. For each pair of molecular fingerprints Tanimoto scores were calculated: "For every unique 14-character InChIKey the most common InChI was selected and used to generate a molecular fingerprint. For each pair of molecular fingerprints Tanimoto scores were calculated"
