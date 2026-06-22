---
name: small-molecule-chromatography-modeling
description: Use when when you have a set of small molecule structures (as SMILES or molecular graphs) and need to predict their elution order in RPLC systems with eluent pH around 2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - ROASMI
  - chemprop
  - RankNet
derived_from:
- doi: 10.1186/s13321-025-00968-8
  title: ROASMI
evidence_spans:
- ROASMI is a Retention Order model to Assist Small Molecule Identification
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

# small-molecule-chromatography-modeling

## Summary

Predict retention order of small molecules in reversed-phase liquid chromatography (RPLC) systems at pH ~2.7 using ensemble ROASMI models trained on chemical structure. This skill enables quantification of model uncertainty across ensemble predictions to assist in compound identification workflows.

## When to use

When you have a set of small molecule structures (as SMILES or molecular graphs) and need to predict their elution order in RPLC systems with eluent pH around 2.7, particularly when you require uncertainty estimates across multiple model predictions to support compound identification or validation tasks.

## When NOT to use

- Input compounds are intended for chromatographic systems at pH values substantially different from ~2.7 (e.g., pH > 4 or HILIC conditions), as the provided models are specific to RPLC at eluent pH ~2.7.
- Compounds fall outside the chemical space covered by the training data (highly unusual scaffolds or extreme molecular properties); the model outputs will not be reliable without retraining.
- Absolute retention time values (minutes) are required instead of retention order; ROASMI predicts relative elution order, not absolute gradient time.

## Inputs

- SMILES strings or molecular structure representations of small molecules
- Pre-trained ROASMI model files (ROASMI_1, ROASMI_2, ROASMI_3, ROASMI_4, ROASMI_5)
- Compound identifier list or dataset index

## Outputs

- Table of retention order predictions (one row per compound, columns: compound ID, ROASMI_1 prediction, ROASMI_2 prediction, ROASMI_3 prediction, ROASMI_4 prediction, ROASMI_5 prediction, ensemble mean retention order, variance/uncertainty)
- Ensemble retention order ranking for each compound
- Model uncertainty estimates (variance) per compound

## How to apply

Load the four pre-trained ROASMI models (ROASMI_1 through ROASMI_5) from the repository, prepare compound input data as SMILES strings or molecular structures, and run inference on each model in ensemble mode to generate retention order predictions. Compute model uncertainty by calculating the variance of retention order predictions across all four trained models. Compile results into a table containing compound identifiers, per-model retention orders, ensemble mean retention order, and model uncertainty (variance). The ensemble variance quantifies prediction confidence—higher variance indicates lower consensus and should trigger closer inspection of borderline retention assignments.

## Related tools

- **ROASMI** (Ensemble of four trained neural network models (D-MPNN molecular embedding + RankNet retention prediction) that generate retention order predictions for RPLC compounds at pH ~2.7; used to produce per-model predictions and ensemble uncertainty estimates) — https://github.com/FangYuan717/ROASMI
- **chemprop** (Underlying directed message-passing neural network (D-MPNN) architecture extended by ROASMI's molecular embedding module to learn directly from compound structure) — https://github.com/chemprop/chemprop
- **RankNet** (Learning-to-rank neural network used by ROASMI's retention prediction module to learn elution orders from pairwise retention sequences across heterogeneous datasets)

## Examples

```
python code/ROASMI_predict.py --model_path models/ROASMI_1 --pred_path data/predict_toy_set.csv
```

## Evaluation signals

- Ensemble variance is non-negative and finite for all compounds; check for NaN or Inf values indicating failed inference.
- Retention order predictions from individual models are numeric ranks or scores within a defined range; verify consistency of output format across all four models.
- Compounds with high ensemble variance (e.g., top quartile) should be manually reviewed or cross-validated against experimental retention data if available to confirm model uncertainty is genuine.
- Ensemble mean retention order is a valid weighted or averaged statistic derived from all four model predictions; verify mathematical consistency (e.g., mean is bounded by min and max of individual predictions).
- Ensemble predictions for a test set (if ground truth is available) should show lower variance for high-confidence predictions and higher variance for borderline or mispredicted compounds, indicating calibration.

## Limitations

- ROASMI_1–ROASMI_5 models are trained specifically for RPLC systems at eluent pH ~2.7; predictions for other pH conditions or chromatographic modes (e.g., HILIC) will be unreliable.
- The models learn retention order (pairwise ranking) rather than absolute retention times; they predict relative elution sequences but cannot estimate gradient time or absolute retention values.
- Model uncertainty is estimated as variance across the four ensemble members; this provides only an internal measure of disagreement and does not account for systematic errors shared by all models.
- Compounds far outside the chemical space of the training data may receive uninformed predictions; the paper does not provide explicit guidance on applicability domain limits.

## Evidence

- [readme] We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around 2.7.: "We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around"
- [readme] The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models.: "The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models."
- [readme] A directed message transfer neural network (D-MPNN) is used to learn directly from the structure of compounds, allowing prediction of compounds in new chemical spaces: "A directed message transfer neural network (D-MPNN) is used to learn directly from the structure of compounds, allowing prediction of compounds in new chemical spaces"
- [readme] A Ranking Neural Network (RankNet) was used to learn elution orders from consistent retention sequences in reference sets with similar pH conditions and same chromatographic systems: "A Ranking Neural Network (RankNet) was used to learn elution orders from consistent retention sequences in reference sets with similar pH conditions and same chromatographic systems"
- [other] Compute model uncertainty as the variance of retention order predictions across the trained models.: "Compute model uncertainty as the variance of retention order predictions across the trained models."
