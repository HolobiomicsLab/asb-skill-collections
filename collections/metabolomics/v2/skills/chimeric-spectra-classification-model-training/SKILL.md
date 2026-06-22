---
name: chimeric-spectra-classification-model-training
description: Use when when your DDA-mode LC-MS/MS data exhibits chimeric spectra patterns that differ systematically from the reference training set used in DNMS2Purifier, or when you wish to optimize purification sensitivity/specificity for your particular instrument, ionization method, or sample matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - DNMS2Purifier_model_generation.r
  - DNMS2Purifier.r
derived_from:
- doi: 10.1021/acs.analchem.3c00736
  title: DNMS2Purifier
evidence_spans:
- The program is written in R (ver 4.2.1).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dnms2purifier_cq
    doi: 10.1021/acs.analchem.3c00736
    title: DNMS2Purifier
  dedup_kept_from: coll_dnms2purifier_cq
schema_version: 0.2.0
---

# chimeric-spectra-classification-model-training

## Summary

Train a customized machine-learning model to classify and purify chimeric MS/MS spectra in untargeted metabolomics workflows. This skill enables adaptation of the DNMS2Purifier purification engine to user-specific LC-MS/MS acquisition protocols by retraining on annotated spectra with known purity labels.

## When to use

When your DDA-mode LC-MS/MS data exhibits chimeric spectra patterns that differ systematically from the reference training set used in DNMS2Purifier, or when you wish to optimize purification sensitivity/specificity for your particular instrument, ionization method, or sample matrix. Apply this skill before running the main DNMS2Purifier.r purification workflow if the default model does not meet your accuracy requirements.

## When NOT to use

- Your DDA-mode LC-MS/MS data are limited to <50 reliably annotated spectra; insufficient training data will lead to overfitting.
- You do not have access to ground-truth chimeric vs. pure spectrum labels; the model cannot be trained without supervised annotations.
- Your primary goal is to perform a one-time purification run without model customization; use the default DNMS2Purifier.r model instead.

## Inputs

- Annotated MS/MS spectra dataset (DDA-mode LC-MS/MS acquisitions)
- Binary purity labels (pure vs. chimeric) for each spectrum
- DNMS2Purifier_model_generation.r script

## Outputs

- Trained model object serialized to .rds file
- Model checkpoint ready for integration into DNMS2Purifier.r workflow

## How to apply

Prepare a training dataset of annotated MS/MS spectra acquired in DDA mode, labeled with binary purity status (pure vs. chimeric). Load the DNMS2Purifier_model_generation.r script in R 4.2.1 and execute it on your labeled training data. The script will train a classification model on spectral features and purity labels. Serialize the resulting model object to an .rds file. This trained model can then be integrated into downstream DNMS2Purifier.r purification runs by loading the .rds checkpoint, allowing the purification workflow to apply your customized decision boundary instead of the default model.

## Related tools

- **DNMS2Purifier_model_generation.r** (R script that loads training data, trains the classification model, and serializes the model object for downstream use) — https://github.com/HuanLab/DNMS2Purifier
- **DNMS2Purifier.r** (Main purification workflow that consumes the trained .rds model checkpoint to classify and filter chimeric spectra) — https://github.com/HuanLab/DNMS2Purifier
- **R** (Language and runtime environment (version 4.2.1) required to execute model training and serialization)

## Examples

```
source('DNMS2Purifier_model_generation.r'); trained_model <- train_purifier_model(training_spectra, purity_labels); saveRDS(trained_model, 'custom_model.rds')
```

## Evaluation signals

- The .rds model checkpoint file is created and can be deserialized without errors in R 4.2.1.
- Model object contains serialized feature weights or coefficients consistent with the number of spectral features in the training data.
- When the trained model is loaded into DNMS2Purifier.r and applied to a held-out test set of annotated spectra, the resulting purity classifications match the ground-truth labels with expected accuracy (e.g., sensitivity/specificity, ROC-AUC).
- The model performs better (measured by cross-validation or independent test set) on spectra from your instrument/method than the default DNMS2Purifier model, validating the customization.
- No serialization errors or model corruption during checkpoint save/load cycle; reproducible predictions when the same .rds is reloaded.

## Limitations

- Model training requires manual annotation of a sufficient training corpus; labeling is labor-intensive and must reflect true chimeric vs. pure status determined by orthogonal validation.
- Overfitting risk when training set is small or unrepresentative of the full diversity of acquisition contexts; cross-validation or separate held-out test set validation is recommended.
- Model generalization to future acquisitions may degrade if MS instrument settings, column chemistry, or sample matrix composition drift significantly from training conditions.
- No automated or semi-supervised annotation provided; users bear full responsibility for ground-truth label accuracy.

## Evidence

- [other] The DNMS2Purifier_model_generation.r script is provided to enable customized model training within the DNMS2Purifier workflow.: "The DNMS2Purifier_model_generation.r script is provided to enable customized model training within the DNMS2Purifier workflow."
- [other] Prepare training data containing annotated MS/MS spectra and purity labels from LC-MS/MS acquisitions in DDA mode.: "Prepare training data containing annotated MS/MS spectra and purity labels from LC-MS/MS acquisitions in DDA mode."
- [other] Execute the model generation script to train the customized purification model on the prepared training dataset.: "Execute the model generation script to train the customized purification model on the prepared training dataset."
- [other] Serialize and save the trained model object to an .rds file for downstream use in the DNMS2Purifier.r purification workflow.: "Serialize and save the trained model object to an .rds file for downstream use in the DNMS2Purifier.r purification workflow."
- [readme] The program is written in R (ver 4.2.1).: "The program is written in R (ver 4.2.1)."
