---
name: classifier-prediction-inference
description: Use when you have a CSV or Excel file containing chemical structure descriptors for one or more molecules, and you want to obtain binary bitter/not-bitter predictions for each molecule using the BitterPredict classifier.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0154
  tools:
  - BitterPredict
  - BitterPredict.m
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bittermass
    doi: 10.1021/acs.jafc.3c09767
    title: bittermass
  dedup_kept_from: coll_bittermass
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jafc.3c09767
  all_source_dois:
  - 10.1021/acs.jafc.3c09767
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# classifier-prediction-inference

## Summary

Apply a trained machine-learning classifier to predict binary class labels (bitter/not-bitter) for a set of molecules given their chemical structure descriptors. This skill is used when you have pre-computed molecular descriptors and need to generate taste predictions without retraining the classifier.

## When to use

You have a CSV or Excel file containing chemical structure descriptors for one or more molecules, and you want to obtain binary bitter/not-bitter predictions for each molecule using the BitterPredict classifier. This is appropriate when molecular descriptors have already been calculated and you seek inference only, not model training or descriptor engineering.

## When NOT to use

- Your input lacks computed chemical structure descriptors — BitterPredict.m requires pre-calculated descriptors, not raw chemical structures or SMILES strings
- You need to retrain or fine-tune the classifier — this skill is for inference only on a frozen model
- Your molecules are already classified or labeled — use this skill only when ground-truth labels are unknown and predictions are needed

## Inputs

- CSV file with chemical structure descriptors and molecule identifiers
- Excel file with chemical structure descriptors and molecule identifiers

## Outputs

- CSV file with molecule identifiers and binary bitter/not-bitter class predictions
- Prediction table (bitter or not-bitter label for each molecule)

## How to apply

Load your input CSV or Excel file containing the required chemical structure descriptors for each molecule. Execute the BitterPredict.m classifier on the loaded descriptor table. The classifier will compute and assign a binary prediction (bitter or not-bitter) to each molecule row. Compile the predictions into an output CSV file that pairs molecule identifiers with their predicted class labels. Verify that each molecule received exactly one prediction and that no rows were dropped due to missing or malformed descriptors.

## Related tools

- **BitterPredict.m** (MATLAB classifier that accepts descriptor tables and produces binary bitter/not-bitter predictions for molecules) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- Output CSV contains one row per input molecule with no rows dropped
- Every molecule has exactly one binary prediction (bitter or not-bitter), no nulls or ambiguous values
- Predictions are binary class labels, not probabilities or continuous scores
- Output file schema matches input identifiers — molecule IDs are preserved and correctly paired with predictions
- BitterPredict.m execution completes without errors or warnings about missing descriptors

## Limitations

- BitterPredict.m requires specific pre-computed chemical structure descriptors; the README does not enumerate which descriptors are required, so descriptor mismatch may cause silent failures or incorrect predictions
- Full code is stated to be available only upon publication; current availability and descriptor specifications are unclear
- The classifier is designed for binary bitter/not-bitter prediction only; it cannot rank molecules by bitterness intensity or provide confidence scores

## Evidence

- [readme] BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.: "BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure."
- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not.: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not."
- [other] Execute BitterPredict.m classifier on the loaded descriptor data. 3. Generate binary predictions (bitter or not-bitter) for each molecule.: "Execute BitterPredict.m classifier on the loaded descriptor data. 3. Generate binary predictions (bitter or not-bitter) for each molecule."
- [other] Compile predictions into output CSV file with molecule identifiers and predicted class labels.: "Compile predictions into output CSV file with molecule identifiers and predicted class labels."
