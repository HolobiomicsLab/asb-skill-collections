---
name: uncertainty-estimation-across-models
description: Use when when you have multiple independently trained models (e.g., ROASMI_1 through ROASMI_5) making predictions on the same set of compounds or samples, and you need to assess confidence in individual predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - pandas
  - NumPy
  - ROASMI (ensemble models)
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

# uncertainty-estimation-across-models

## Summary

Quantify model prediction uncertainty by computing the variance of outputs across an ensemble of independently trained models. This approach is particularly useful when ensemble members have been trained on the same task with different random initializations or data splits, providing a distribution-free estimate of epistemic uncertainty without requiring probabilistic model outputs.

## When to use

When you have multiple independently trained models (e.g., ROASMI_1 through ROASMI_5) making predictions on the same set of compounds or samples, and you need to assess confidence in individual predictions. Apply this skill when the research question requires quantifying model disagreement as a proxy for prediction reliability, especially in small-molecule identification tasks where retention order predictions must be ranked across chemical space.

## When NOT to use

- When you have only a single trained model; ensemble variance requires at least 2–3 independent members to be meaningful.
- When predictions are already probabilistic (e.g., Bayesian posterior samples or calibrated confidence scores); use those distributions directly instead.
- When ensemble members are not independently trained or differ substantially in architecture/hyperparameters; variance will reflect design differences rather than epistemic uncertainty.

## Inputs

- Retention order predictions from each trained ROASMI model (ROASMI_1 through ROASMI_5)
- Compound identifiers and their corresponding predictions across all ensemble members
- CSV or tabular files containing per-model predictions

## Outputs

- Structured table mapping compound identifiers to variance of retention order predictions
- CSV export containing compounds and their ensemble prediction variance values
- Uncertainty quantification metric for each compound suitable for integration with MS/MS scoring

## How to apply

Load predictions from each trained ensemble member for all input compounds. For each compound, extract its predicted value (retention order, score, or ranking) across all ensemble members. Calculate the variance of these predictions for each compound independently using NumPy or pandas. Compile the results into a structured table with compound identifiers paired to their variance values. Higher variance indicates greater model disagreement and lower confidence; lower variance suggests consistent, more reliable predictions. Export results as CSV for downstream integration with other scoring modules (e.g., MS/MS scores in the Identify module).

## Related tools

- **pandas** (Data aggregation and table construction for loading and compiling predictions across ensemble members)
- **NumPy** (Variance calculation and numerical computation of prediction statistics across ensemble outputs)
- **ROASMI (ensemble models)** (Source of the four to five independently trained retention order prediction models that form the ensemble) — https://github.com/FangYuan717/ROASMI

## Examples

```
import pandas as pd; import numpy as np; predictions = pd.read_csv('predictions_ensemble.csv'); variance = predictions.groupby('compound_id')[['ROASMI_1', 'ROASMI_2', 'ROASMI_3', 'ROASMI_4']].var(axis=1); variance.to_csv('compound_uncertainty.csv')
```

## Evaluation signals

- Variance values are non-negative and fall within a sensible range relative to the prediction scale (e.g., retention order rankings).
- Compounds with identical predictions across all ensemble members have variance = 0; compounds with divergent predictions have variance > 0.
- CSV output contains all input compounds with no missing variance values; no NA or NaN entries unless prediction data was incomplete.
- Variance correlates inversely with prediction consensus: high-variance compounds should show larger differences in retention rank across models.
- Integration with downstream Identify module produces lower confidence scores for high-variance compounds and higher scores for low-variance compounds.

## Limitations

- Variance is sensitive to the number of ensemble members; results are not directly comparable across ensembles of different sizes. The ROASMI paper uses 4–5 models; smaller ensembles may yield unstable estimates.
- Variance does not account for systematic bias shared across all ensemble members; all models may converge on an incorrect prediction, yielding low variance despite high error.
- Learning-to-rank formulation (RankNet) means predictions are ordinal (retention rank), not pointwise retention times; variance of ranks may not correspond linearly to variance in retention times or chromatographic properties.
- The approach assumes consistent pH conditions (~2.7) and reversed-phase RPLC systems; extrapolation to other chromatographic modes or pH ranges may not preserve the relationship between ensemble variance and prediction reliability.

## Evidence

- [other] The ensemble approach quantifies model uncertainty by computing the variance of retention order predictions across the trained ROASMI models for each compound.: "The ensemble approach quantifies model uncertainty by computing the variance of retention order predictions across the trained ROASMI models for each compound."
- [other] For each compound, extract its predicted retention order across all ensemble members. Calculate the variance of retention order predictions for each compound across the ensemble.: "For each compound, extract its predicted retention order across all ensemble members. 3. Calculate the variance of retention order predictions for each compound across the ensemble."
- [readme] The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models.: "The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models."
- [readme] We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around 2.7.: "We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around"
- [other] Compile compound identifiers with their corresponding variance values into a structured table and export as CSV.: "Compile compound identifiers with their corresponding variance values into a structured table and export as CSV."
