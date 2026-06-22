---
name: small-molecule-compound-indexing
description: Use when when you have retention order predictions from multiple ensemble members (e.g., ROASMI_1 through ROASMI_5) for a set of candidate compounds and need to assign a per-compound uncertainty score that reflects how consistently the ensemble members rank that compound relative to others.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - pandas
  - NumPy
  - ROASMI ensemble models (ROASMI_1 – ROASMI_5)
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

# small-molecule-compound-indexing

## Summary

Compute and tabulate ensemble-derived uncertainty estimates (variance of retention order predictions) for each compound across multiple trained retention prediction models. This skill quantifies model disagreement as a confidence measure for small molecule identification workflows.

## When to use

When you have retention order predictions from multiple ensemble members (e.g., ROASMI_1 through ROASMI_5) for a set of candidate compounds and need to assign a per-compound uncertainty score that reflects how consistently the ensemble members rank that compound relative to others. Essential before integrating retention predictions with MS/MS scores in probabilistic small molecule identification.

## When NOT to use

- Single-model predictions: variance requires ≥2 independent ensemble members; single predictions yield zero variance and no uncertainty signal.
- Pointwise retention values without ranking context: this skill operates on retention order (ranks), not absolute retention times; conversion to rank space is necessary first.
- Pre-aggregated or already-uncertainty-quantified predictions: if uncertainty has already been computed or calibrated, recomputing variance would be redundant.

## Inputs

- Retention order predictions from multiple trained models (e.g., ROASMI_1 through ROASMI_5)
- Compound identifiers (SMILES or other molecular identifiers)
- Predicted retention order ranks or scores per compound per model

## Outputs

- CSV table with compound identifiers and corresponding ensemble retention order prediction variance
- Per-compound uncertainty quantification metric (variance values)

## How to apply

Load retention order predictions from each trained ensemble member model for all input compounds. For each compound, extract its predicted retention order position (or rank) across all ensemble members. Calculate the variance of these retention order predictions across the ensemble—compounds with high variance indicate low model consensus and high uncertainty, while low variance indicates confident, consistent predictions. Compile a structured table pairing each compound identifier with its corresponding variance value, then export as CSV. This variance serves as a model uncertainty quantification metric suitable for downstream probabilistic integration with MS/MS scores.

## Related tools

- **pandas** (Load, structure, and export compound-variance pairs as CSV; group and aggregate predictions by compound ID across ensemble members)
- **NumPy** (Compute variance of retention order predictions across ensemble members for each compound)
- **ROASMI ensemble models (ROASMI_1 – ROASMI_5)** (Generate retention order predictions for input compounds; ensemble diversity provides basis for variance calculation) — https://github.com/FangYuan717/ROASMI

## Examples

```
import pandas as pd; import numpy as np; predictions = {f'ROASMI_{i}': pd.read_csv(f'roasmi_{i}_predictions.csv') for i in range(1, 6)}; compound_variance = predictions['ROASMI_1'].groupby('compound_id').apply(lambda cid: np.var([predictions[f'ROASMI_{i}'].loc[predictions[f'ROASMI_{i}']['compound_id']==cid, 'retention_order'].values[0] for i in range(1, 6)])); pd.DataFrame({'compound_id': compound_variance.index, 'variance': compound_variance.values}).to_csv('compound_uncertainty.csv', index=False)
```

## Evaluation signals

- CSV output contains one row per compound with compound identifier and variance columns; no missing or NaN values for compounds with predictions from all ensemble members.
- Variance values are non-negative (mathematically valid); compounds with identical predictions across all ensemble members have variance = 0.
- Compounds with high disagreement (e.g., widely different predicted ranks across models) have variance significantly larger than the median/mean variance across the dataset.
- Schema consistency: all output rows conform to expected column structure (compound_id, variance); file is parseable by standard CSV readers.
- Spot-check: manually verify that a high-variance compound shows visibly different rank predictions across individual models, and a low-variance compound shows consistent ranks.

## Limitations

- Variance is a symmetric measure and does not distinguish directional bias; a compound ranked 1st by half the ensemble and 5th by the other half has high variance but may systematically mislead if one model is biased.
- Ensemble size matters: variance with only 2–3 models may be unstable; the ROASMI paper provides 4–5 models, which is a practical minimum.
- Variance assumes models are trained on similar data and have similar calibration; if ensemble members are trained on disparate datasets or use different architectures, variance may not translate directly to prediction confidence.
- Retention order predictions are specific to reversed-phase liquid chromatography (RPLC) systems with eluent pH around 2.7 per the ROASMI models; variance computed from these predictions does not generalize to other chromatographic systems without retraining.

## Evidence

- [other] The ensemble approach quantifies model uncertainty by computing the variance of retention order predictions across the trained ROASMI models for each compound.: "The ensemble approach quantifies model uncertainty by computing the variance of retention order predictions across the trained ROASMI models for each compound."
- [other] 1. Load retention order predictions from each of the four trained ROASMI models (ROASMI_1 through ROASMI_5) for all input compounds. 2. For each compound, extract its predicted retention order across all ensemble members. 3. Calculate the variance of retention order predictions for each compound across the ensemble. 4. Compile compound identifiers with their corresponding variance values into a structured table and export as CSV.: "1. Load retention order predictions from each of the four trained ROASMI models (ROASMI_1 through ROASMI_5) for all input compounds. 2. For each compound, extract its predicted retention order across"
- [readme] The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models.: "The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models."
- [readme] We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around 2.7.: "We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around"
