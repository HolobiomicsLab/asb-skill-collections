---
name: ensemble-variance-quantification
description: Use when when you have retention order predictions from multiple independently trained models (e.g., ROASMI_1 through ROASMI_5) for the same set of compounds and need to estimate prediction confidence or identify compounds with high model disagreement.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3676
  tools:
  - pandas
  - NumPy
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Ensemble Variance Quantification

## Summary

Quantify model uncertainty in retention order predictions by computing the variance of predictions across an ensemble of independently trained models. This approach provides per-compound uncertainty estimates without retraining or modifying individual models.

## When to use

When you have retention order predictions from multiple independently trained models (e.g., ROASMI_1 through ROASMI_5) for the same set of compounds and need to estimate prediction confidence or identify compounds with high model disagreement. Use this when ensemble members were trained on the same or similar chromatographic systems but may have learned slightly different decision boundaries.

## When NOT to use

- Only a single trained model is available; variance of one value is undefined or uninformative.
- Retention order predictions have already been aggregated or consensus has been reached without variance preservation.
- Models were trained on very different chromatographic systems or reference datasets; aggregated variance may not be interpretable.

## Inputs

- Retention order predictions from each trained ROASMI model (CSV or tabular format with compound identifiers and predicted retention orders)
- List of all input compounds (identifiers matching across all model outputs)

## Outputs

- CSV table with compound identifiers and variance of retention order predictions across ensemble members
- Per-compound uncertainty quantification (variance values) for ranking or filtering

## How to apply

Load retention order predictions from each trained ensemble member for all input compounds. For each compound, extract its predicted retention order across all models (e.g., from ROASMI_1, ROASMI_2, ROASMI_3, ROASMI_4, ROASMI_5). Calculate the variance of these retention order predictions per compound using NumPy or pandas—this variance reflects the spread or disagreement among ensemble members. Compounds with high variance indicate uncertain predictions where models disagree on retention rank; low variance indicates high confidence consensus. Compile compound identifiers with their corresponding variance values into a structured CSV table for downstream analysis or filtering.

## Related tools

- **pandas** (Loading model predictions, extracting per-compound retention orders, and compiling variance results into structured tables)
- **NumPy** (Computing variance of retention order predictions across ensemble members for each compound)

## Examples

```
import pandas as pd; import numpy as np; predictions = {f'ROASMI_{i}': pd.read_csv(f'roasmi_{i}_predictions.csv') for i in range(1, 6)}; variance = predictions['ROASMI_1'][['compound_id']].copy(); variance['retention_order_variance'] = [np.var([predictions[f'ROASMI_{i}'].loc[predictions[f'ROASMI_{i}']['compound_id'] == cid, 'retention_order'].values[0] for i in range(1, 6)]) for cid in variance['compound_id']]; variance.to_csv('ensemble_variance.csv', index=False)
```

## Evaluation signals

- Output CSV contains all input compound identifiers with no missing entries.
- Variance values are non-negative and consistent with the formula Var(X) = E[X²] − E[X]².
- Compounds with identical predictions across all ensemble members have variance ≈ 0; compounds with divergent ranks have variance > 0.
- Row count and compound ordering match the input prediction tables.
- Variance distribution is interpretable as a measure of model disagreement (e.g., histogram shows reasonable spread, no NaN or infinite values).

## Limitations

- Variance depends critically on the diversity and quality of ensemble members; if all models were trained identically or on very similar data, variance will be artificially low and uninformative.
- Retention order is discrete; variance of rank values may not have the same statistical interpretation as continuous predictions, especially with small ensemble sizes.
- This method estimates epistemic (model) uncertainty but does not capture aleatoric (data) uncertainty or systematic bias in the ensemble.
- The ensemble approach is designed for RPLC systems with eluent pH around 2.7; variance computed on different chromatographic conditions may not be comparable.

## Evidence

- [other] The ensemble approach quantifies model uncertainty by computing the variance of retention order predictions across the trained ROASMI models for each compound.: "The ensemble approach quantifies model uncertainty by computing the variance of retention order predictions across the trained ROASMI models for each compound."
- [other] For each compound, extract its predicted retention order across all ensemble members. Calculate the variance of retention order predictions for each compound across the ensemble.: "For each compound, extract its predicted retention order across all ensemble members. 3. Calculate the variance of retention order predictions for each compound across the ensemble."
- [readme] The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models.: "The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models."
- [readme] We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around 2.7.: "We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around"
- [other] Compile compound identifiers with their corresponding variance values into a structured table and export as CSV.: "Compile compound identifiers with their corresponding variance values into a structured table and export as CSV."
