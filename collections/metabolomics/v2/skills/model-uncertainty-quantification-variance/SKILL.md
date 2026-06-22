---
name: model-uncertainty-quantification-variance
description: Use when when you have predictions from multiple independently trained models (e.g., ROASMI_1–ROASMI_5) for the same set of compounds in a reversed-phase liquid chromatography system at eluent pH ~2.7, and you need to estimate prediction reliability without ground-truth labels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3931
  edam_topics:
  - http://edamontology.org/topic_3957
  - http://edamontology.org/topic_2258
  tools:
  - ROASMI
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

# Model Uncertainty Quantification via Ensemble Variance

## Summary

Quantify prediction uncertainty in machine learning ensembles by computing the variance of retention order predictions across multiple trained models. This approach enables assessment of model confidence and identification of high-uncertainty predictions in compound retention forecasting.

## When to use

When you have predictions from multiple independently trained models (e.g., ROASMI_1–ROASMI_5) for the same set of compounds in a reversed-phase liquid chromatography system at eluent pH ~2.7, and you need to estimate prediction reliability without ground-truth labels. Use this when ensemble disagreement is informative about whether a retention order prediction is trustworthy.

## When NOT to use

- When you have only a single trained model—variance requires multiple independent predictions to be meaningful.
- When compounds are outside the chromatographic space or pH conditions (pH ~2.7 reversed-phase) used to train the ensemble models.
- When retention order predictions have already been merged or post-processed into a single consensus value without preserving individual model outputs.

## Inputs

- Ensemble of trained ROASMI models (ROASMI_1–ROASMI_5)
- Compound input data (SMILES or molecular structures)
- Retention order predictions from each model in the ensemble

## Outputs

- Table with compound identifiers, predicted retention orders from each model, ensemble mean retention order, and model uncertainty (variance)
- Uncertainty scores per compound (variance values)

## How to apply

Load retention order predictions from all trained models in the ensemble for each compound. For each compound, compute the variance of predicted retention orders across all models—this variance serves as a model uncertainty metric. Higher variance indicates lower consensus and thus higher uncertainty; lower variance indicates higher confidence. Compile results into a table pairing each compound with its ensemble mean retention order, individual model predictions, and computed variance. This variance-based uncertainty can inform downstream small molecule identification by down-weighting or flagging high-uncertainty predictions in the identification module.

## Related tools

- **ROASMI** (Trained ensemble models (ROASMI_1–ROASMI_5) that generate retention order predictions for small molecule identification) — https://github.com/FangYuan717/ROASMI

## Evaluation signals

- Variance is computed for every compound in the input set with no missing values.
- Variance values are non-negative numbers reflecting spread across model predictions.
- Compounds with zero variance indicate perfect agreement across all models; non-zero variance indicates disagreement.
- Output table schema matches specification: compound identifier, per-model predictions, ensemble mean, variance column.
- Variance values are reasonable in magnitude relative to the range of possible retention orders (e.g., rank positions in the compound list).

## Limitations

- Variance is sensitive to the number of models in the ensemble; larger ensembles may reduce variance spuriously if models are highly correlated.
- Variance does not account for systematic bias; all models could agree on a wrong prediction, yielding low variance but poor accuracy.
- Uncertainty quantification is valid only for compounds in the same chromatographic conditions (pH ~2.7, reversed-phase RPLC) as the training data; extrapolation to other pH or systems is not supported by the provided models.
- The method assumes independent or weakly correlated models; if models share training data or architecture, variance may underestimate true uncertainty.

## Evidence

- [intro] The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models.: "The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models."
- [other] Compute model uncertainty as the variance of retention order predictions across the trained models.: "Compute model uncertainty as the variance of retention order predictions across the trained models."
- [other] Compile predictions into a table with compound identifiers, predicted retention orders from each model, ensemble mean retention order, and model uncertainty (variance).: "Compile predictions into a table with compound identifiers, predicted retention orders from each model, ensemble mean retention order, and model uncertainty (variance)."
- [readme] We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around 2.7.: "We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around"
