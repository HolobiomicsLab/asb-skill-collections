---
name: retention-order-prediction-rplc
description: Use when when you have a set of small molecules (as SMILES or structures)
  that need to be identified or ranked by their elution order in RPLC systems with
  acidic pH (~2.7), and you want to assess model confidence in retention predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - ROASMI
  - pandas
  - NumPy
  - chemprop
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-025-00968-8
  title: ROASMI
evidence_spans:
- ROASMI is a Retention Order model to Assist Small Molecule Identification
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

# retention-order-prediction-rplc

## Summary

Predict retention order rankings for compounds in reversed-phase liquid chromatography (RPLC) systems at eluent pH ~2.7 using an ensemble of trained ROASMI neural network models. This skill enables quantification of prediction uncertainty by computing variance across ensemble members.

## When to use

When you have a set of small molecules (as SMILES or structures) that need to be identified or ranked by their elution order in RPLC systems with acidic pH (~2.7), and you want to assess model confidence in retention predictions. Use this skill when uncertainty quantification via ensemble variance is needed for downstream integration with MS/MS scores or other orthogonal data.

## When NOT to use

- Input compounds are from chromatographic systems with pH significantly different from ~2.7 (e.g., HILIC systems, high pH RPLC); models are pH-specific.
- Absolute retention time values (minutes) are required; ROASMI predicts relative order, not pointwise retention times.
- Input dataset is already annotated with high-confidence retention assignments; ensemble prediction is unnecessary.

## Inputs

- SMILES strings or molecular structures for candidate compounds
- Pre-trained ROASMI model files (ROASMI_1 through ROASMI_5)
- Comma-separated or tabular dataset with compound identifiers and structures

## Outputs

- Retention order predictions (rankings) for each compound per model
- Ensemble mean retention order per compound
- Variance of retention order predictions across ensemble (uncertainty quantification)
- CSV table with compound identifiers, per-model predictions, ensemble mean, and variance

## How to apply

Load the four pre-trained ROASMI models (ROASMI_1 through ROASMI_5) from the deposited model files in the repository. Prepare compound input data in SMILES or molecular structure format. Run inference on each compound through all four ensemble members using the ROASMI predict module to obtain retention order predictions for each model. For each compound, compute the variance of retention order predictions across the ensemble to quantify model uncertainty. Compile results into a structured table with compound identifiers, predictions from each model, ensemble mean retention order, and uncertainty (variance). This learning-to-rank approach is grounded in RankNet, which learns pairwise retention orders rather than pointwise values, allowing robust cross-dataset predictions.

## Related tools

- **ROASMI** (Ensemble of four trained D-MPNN molecular embedding and RankNet retention prediction models for RPLC pH ~2.7 compounds) — https://github.com/FangYuan717/ROASMI
- **chemprop** (Base framework for directed message passing neural networks (D-MPNN) used in ROASMI molecular embedding module) — https://github.com/chemprop/chemprop
- **pandas** (Data manipulation and tabular output compilation)
- **NumPy** (Variance computation and numerical calculations across ensemble predictions)

## Examples

```
python code/ROASMI_predict.py --pred_path data/predict_toy_set.csv --model ROASMI_1
```

## Evaluation signals

- Variance values must be non-negative and reflect spread in ensemble predictions; zero variance indicates perfect agreement among all four models.
- Each compound in output table must have exactly four per-model predictions (one from ROASMI_1, ROASMI_2, ROASMI_3, ROASMI_5) and one computed variance value.
- Ensemble mean retention order should fall within the range of the four individual model predictions for each compound.
- All compound identifiers in output match input compound identifiers; no compounds are dropped or duplicated.
- Variance should correlate with model disagreement: high variance suggests low confidence; low variance suggests high model agreement and higher confidence in rank prediction.

## Limitations

- Models are trained specifically for RPLC systems at eluent pH around 2.7; predictions outside this pH range (e.g., neutral or high-pH RPLC, HILIC systems) are not validated and should not be trusted.
- Predictions are relative retention orders (ranks), not absolute retention times; integration with other data (MS/MS scores, reference standards) is required for final compound identification.
- Ensemble uncertainty (variance) quantifies model disagreement but does not account for systematic biases common to all models or training set distribution shifts to novel chemical spaces.
- Repository README notes that optional descriptastorus RDKit features were not incorporated into provided models; retraining with additional computed features may alter performance.

## Evidence

- [readme] We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around 2.7.: "We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around"
- [readme] The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models.: "The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models."
- [readme] A Ranking Neural Network (RankNet) was used to learn elution orders from consistent retention sequences in reference sets with similar pH conditions and same chromatographic systems.: "A Ranking Neural Network (RankNet) was used to learn elution orders from consistent retention sequences in reference sets with similar pH conditions and same chromatographic systems."
- [other] For each compound, extract its predicted retention order across all ensemble members. 3. Calculate the variance of retention order predictions for each compound across the ensemble.: "For each compound, extract its predicted retention order across all ensemble members. Calculate the variance of retention order predictions for each compound across the ensemble."
