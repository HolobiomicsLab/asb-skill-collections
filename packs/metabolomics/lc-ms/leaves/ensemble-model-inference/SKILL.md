---
name: ensemble-model-inference
description: Use when you have a set of compounds (as SMILES strings or molecular structures) that need retention order predictions in a reversed-phase liquid chromatography (RPLC) system at eluent pH ~2.7, and you want to quantify prediction uncertainty rather than relying on a single model's output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3372
  tools:
  - ROASMI
  - chemprop
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ensemble-model-inference

## Summary

Apply multiple trained neural network models in parallel to generate predictions for the same input compounds, then aggregate outputs to compute ensemble statistics and model uncertainty. This skill enables quantification of prediction confidence via variance across model outputs for small-molecule retention order prediction in reversed-phase liquid chromatography.

## When to use

You have a set of compounds (as SMILES strings or molecular structures) that need retention order predictions in a reversed-phase liquid chromatography (RPLC) system at eluent pH ~2.7, and you want to quantify prediction uncertainty rather than relying on a single model's output. Apply this skill when you need to assess the robustness of retention predictions across independent model instances trained on the same or similar chromatographic datasets.

## When NOT to use

- Input compounds are outside the chemical space of reversed-phase systems at pH ~2.7 (e.g., HILIC, ion-exchange, or significantly different pH conditions).
- You need pointwise absolute retention times rather than relative retention order predictions.
- Only a single trained model is available or accessible; ensemble inference requires multiple independent model instances.

## Inputs

- compound SMILES strings or molecular structures
- four trained ROASMI neural network model checkpoints (ROASMI_1–ROASMI_5)

## Outputs

- retention order predictions per model (one value per compound per model)
- ensemble mean retention order (averaged across four models)
- model uncertainty quantified as variance of retention order predictions
- structured table with compound identifiers, per-model predictions, ensemble values, and uncertainty

## How to apply

Load all four pre-trained ROASMI models (ROASMI_1 through ROASMI_5) from the deposited model files in the ROASMI repository. Prepare your compound input data as SMILES strings or molecular structures. For each compound, invoke prediction in inference mode on each of the four trained models sequentially (or in parallel). Collect the retention order prediction from each model. Compute the ensemble mean retention order by averaging predictions across models, and compute model uncertainty as the variance of retention order predictions across the four models. The variance quantifies disagreement among models—higher variance indicates lower confidence in the prediction. Compile results into a structured table with compound identifiers, per-model predictions, ensemble mean, and uncertainty metric.

## Related tools

- **ROASMI** (Provides four pre-trained ensemble models for retention order prediction and inference API; integrates D-MPNN for molecular embedding and RankNet for ranking-to-learn retention order) — https://github.com/FangYuan717/ROASMI
- **chemprop** (Underlying directed message-passing neural network (D-MPNN) architecture used by ROASMI's molecular embedding module to learn compound representations directly from structure) — https://github.com/chemprop/chemprop

## Examples

```
python code/ROASMI_predict.py --model_path data/models/ROASMI_1 --pred_path data/predict_toy_set.csv --ensemble_mode true
```

## Evaluation signals

- All four model predictions are successfully generated for each compound with no NaN or missing values.
- Variance (model uncertainty) is non-negative and reflects relative model disagreement; compounds with low variance show consistent predictions across models, and compounds with high variance show diverse predictions.
- Ensemble mean retention order falls within the range of the four individual model predictions (ensemble mean ≥ min per-model prediction AND ≤ max per-model prediction).
- Output table contains exactly one row per input compound with five columns: compound_id, ROASMI_1_prediction, ROASMI_2_prediction, ROASMI_3_prediction, ROASMI_4_prediction, ensemble_mean, and uncertainty_variance.
- Retention order predictions are consistent with known reference sets of the RPLC system used for model training (can be verified against retained training/test data if available).

## Limitations

- Ensemble models are trained and validated specifically for reversed-phase liquid chromatography at eluent pH ~2.7; predictions may be unreliable for other pH regimes or chromatographic modes (e.g., HILIC).
- Predictions are relative retention orders (pairwise rankings), not absolute retention times; linking predictions to a common gradient range requires additional calibration.
- Model variance quantifies disagreement among the four ensemble members but does not directly measure external accuracy without comparison to experimental retention data.
- Compounds in novel chemical spaces not represented in the training data may produce high variance (low confidence) or incorrect predictions despite the ensemble approach.
- Computational cost scales linearly with the number of models (four in the current ensemble); inference requires GPU or CPU resources proportional to model size and dataset size.

## Evidence

- [readme] We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around 2.7.: "We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around"
- [readme] The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models.: "The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models."
- [other] Generate retention order predictions for each compound using all four models in ensemble mode. Compute model uncertainty as the variance of retention order predictions across the trained models.: "Generate retention order predictions for each compound using all four models in ensemble mode. Compute model uncertainty as the variance of retention order predictions across the trained models."
- [readme] A Ranking Neural Network (RankNet) was used to learn elution orders from consistent retention sequences in reference sets with similar pH conditions and same chromatographic systems (e.g. reversed phase).: "A Ranking Neural Network (RankNet) was used to learn elution orders from consistent retention sequences in reference sets with similar pH conditions and same chromatographic systems (e.g. reversed"
