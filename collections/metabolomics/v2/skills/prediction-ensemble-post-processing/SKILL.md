---
name: prediction-ensemble-post-processing
description: Use when you have retention order predictions from multiple trained ROASMI
  models (e.g., ROASMI_1 through ROASMI_5) for the same set of compounds and need
  to estimate prediction uncertainty to support small molecule identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - pandas
  - NumPy
  - ROASMI
  license_tier: open
derived_from:
- doi: 10.1186/s13321-025-00968-8
  title: ROASMI
evidence_spans:
- Four initial ROASMI models (ROASMI_1 - ROASMI_5)
- variance of the retention order predictions
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_roasmi_cq
    doi: 10.1186/s13321-025-00968-8
    title: ROASMI
  dedup_kept_from: coll_roasmi_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-025-00968-8
  all_source_dois:
  - 10.1186/s13321-025-00968-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# prediction-ensemble-post-processing

## Summary

Aggregate predictions across an ensemble of trained models and compute per-sample variance to quantify model uncertainty. This skill is essential when multiple models make different predictions on the same input and you need a principled measure of prediction confidence for downstream decision-making.

## When to use

You have retention order predictions from multiple trained ROASMI models (e.g., ROASMI_1 through ROASMI_5) for the same set of compounds and need to estimate prediction uncertainty to support small molecule identification. Apply this skill when ensemble disagreement directly informs confidence in retention-based matching or when you must prioritize candidate compounds by prediction confidence.

## When NOT to use

- Only a single model is available; variance requires at least 2 independent predictions.
- Predictions are already aggregated or consensus scores; you cannot recompute variance from a single value.
- Input predictions are not retention orders (e.g., continuous retention times); the variance interpretation may not align with learning-to-rank semantics.

## Inputs

- Retention order predictions from each ensemble member model (CSV or array-like)
- Compound identifiers (strings or indices)
- Predictions from at least 2 trained ROASMI models

## Outputs

- Structured table with compound identifiers and variance values (CSV)
- Per-compound uncertainty estimates (numeric variance)

## How to apply

Load retention order predictions from each of the trained ensemble members (all ROASMI models) for all input compounds. For each compound, extract its predicted retention order across all ensemble members. Calculate the variance of retention order predictions for each compound across the ensemble using NumPy or pandas. Compile compound identifiers with their corresponding variance values into a structured table. Higher variance indicates greater model disagreement and lower confidence; lower variance indicates consensus and higher confidence. Export the result as CSV for downstream use in the identification module or for filtering low-confidence predictions.

## Related tools

- **pandas** (Organize and aggregate retention predictions from multiple models into structured tables; compute variance per compound)
- **NumPy** (Compute variance of retention order predictions across ensemble members)
- **ROASMI** (Source of trained ensemble models (ROASMI_1 through ROASMI_5) that generate retention order predictions) — https://github.com/FangYuan717/ROASMI

## Examples

```
import pandas as pd; import numpy as np; preds = {f'ROASMI_{i}': pd.read_csv(f'predictions_{i}.csv') for i in range(1, 6)}; variance = preds['ROASMI_1'].set_index('compound_id').apply(lambda row: np.var([preds[f'ROASMI_{i}'].set_index('compound_id').loc[row.name, 'retention_order'] for i in range(1, 6)]), axis=1); pd.DataFrame({'compound_id': variance.index, 'variance': variance.values}).to_csv('ensemble_variance.csv', index=False)
```

## Evaluation signals

- Variance table has one row per compound with no missing values and variance ≥ 0.
- Variance values are in a plausible range for retention order predictions (e.g., non-negative, bounded by ensemble size and prediction discretization).
- Compounds with identical predictions across all ensemble members have variance = 0.
- Compounds with maximally disagreeing predictions across ensemble members have the highest variance.
- CSV export is valid and can be read back into pandas/NumPy without errors; column names match expected schema (e.g., 'compound_id', 'variance').

## Limitations

- Variance as a measure of uncertainty assumes retention order predictions are comparable across models; systematic biases in individual models may inflate or deflate variance.
- Small ensemble size (e.g., fewer than 4 models) may yield unreliable variance estimates.
- Variance does not account for the magnitude of retention order differences; two models predicting ranks that differ by 1 vs. 10 both contribute equally to variance.
- Variance is sensitive to outlier predictions from individual ensemble members; robust alternatives (e.g., IQR, median absolute deviation) may be preferable for highly heterogeneous ensembles.

## Evidence

- [readme] The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models.: "The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models."
- [other] For each compound, extract its predicted retention order across all ensemble members. Calculate the variance of retention order predictions for each compound across the ensemble.: "For each compound, extract its predicted retention order across all ensemble members. 3. Calculate the variance of retention order predictions for each compound across the ensemble."
- [other] Load retention order predictions from each of the four trained ROASMI models (ROASMI_1 through ROASMI_5) for all input compounds.: "Load retention order predictions from each of the four trained ROASMI models (ROASMI_1 through ROASMI_5) for all input compounds."
- [other] Compile compound identifiers with their corresponding variance values into a structured table and export as CSV.: "Compile compound identifiers with their corresponding variance values into a structured table and export as CSV."
