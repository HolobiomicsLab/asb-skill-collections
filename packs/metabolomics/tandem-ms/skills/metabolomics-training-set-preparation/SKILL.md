---
name: metabolomics-training-set-preparation
description: Use when when you have LC-MS/MS acquisitions in DDA mode and need to train a customized DNMS2Purifier model to purify chimeric MS/MS spectra specific to your experimental conditions, metabolite classes, or ionization settings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - DNMS2Purifier_model_generation.r
  - DNMS2Purifier.r
  techniques:
  - LC-MS
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c00736
  all_source_dois:
  - 10.1021/acs.analchem.3c00736
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-training-set-preparation

## Summary

Preparation of annotated MS/MS spectra with purity labels from LC-MS/MS Data-Dependent Acquisition (DDA) mode for training customized chimeric spectra purification models. This skill bridges raw mass spectrometry data collection and machine learning model training within the DNMS2Purifier workflow.

## When to use

When you have LC-MS/MS acquisitions in DDA mode and need to train a customized DNMS2Purifier model to purify chimeric MS/MS spectra specific to your experimental conditions, metabolite classes, or ionization settings. Use this skill if the default model does not adequately separate pure from chimeric spectra in your dataset.

## When NOT to use

- Input spectra are already pre-filtered or purified by instrument-level methods and no chimeric contamination is suspected.
- Training data contains fewer than 50–100 reliably annotated spectra (insufficient for stable model training).
- MS/MS data are acquired in targeted or parallel reaction monitoring (PRM/MRM) mode rather than DDA, as chimeric spectra are an artifact specific to DDA.

## Inputs

- LC-MS/MS DDA-mode spectra (MS/MS peak lists with m/z and intensity values)
- Purity annotations or labels for each spectrum (binary or quantitative)
- Precursor m/z and isolation window metadata
- Feature vectors derived from MS/MS spectral properties

## Outputs

- Serialized trained model object (.rds file)
- Model performance metrics (accuracy, precision, recall, or equivalent)
- Feature importance rankings (if provided by the model)

## How to apply

Collect LC-MS/MS data in DDA (Data-Dependent Acquisition) mode to generate MS/MS spectra. Annotate each MS/MS spectrum with a purity label (e.g., binary: pure vs. chimeric, or quantitative purity score) based on manual inspection, fragmentation consistency, or precursor isolation quality. Organize the annotated spectra and labels into a structured training dataset with explicit feature vectors and target labels. Load this prepared training dataset into the R 4.2.1 environment, then execute the DNMS2Purifier_model_generation.r script to train the customized model. The trained model object is serialized and saved to an .rds file for downstream use in the DNMS2Purifier.r purification workflow.

## Related tools

- **R** (Execution environment for DNMS2Purifier_model_generation.r script; required version 4.2.1)
- **DNMS2Purifier_model_generation.r** (R script that trains customized model on annotated MS/MS spectra and purity labels) — https://github.com/HuanLab/DNMS2Purifier
- **DNMS2Purifier.r** (Main purification script that consumes the trained .rds model for MS/MS purification) — https://github.com/HuanLab/DNMS2Purifier

## Examples

```
source('DNMS2Purifier_model_generation.r'); trainedModel <- trainDNMS2PurifierModel(spectraData = annotated_spectra, purityLabels = purity_labels); saveRDS(trainedModel, file = 'custom_purification_model.rds')
```

## Evaluation signals

- Trained model .rds file is successfully serialized and can be loaded without errors into the R environment.
- Model achieves acceptable classification performance on a held-out test set (e.g., >80% accuracy or AUC >0.85 for pure vs. chimeric discrimination).
- When the trained model is applied within DNMS2Purifier.r purification workflow, the number of flagged chimeric spectra matches manual inspection or known chimera rate in the sample.
- Feature importance plot or coefficients show that model relies on plausible spectral properties (e.g., precursor isolation width, spectral entropy, fragment intensity variance) rather than random features.
- Training dataset contains sufficient annotation diversity (e.g., representation across precursor mass ranges, charge states, and fragmentation patterns) to avoid overfitting to specific metabolite classes.

## Limitations

- Model training requires manual or semi-automated annotation of MS/MS purity, which is labor-intensive and may introduce subjective bias.
- Trained model is specific to the LC-MS/MS platform, ionization mode, and instrument settings used during training; transfer to different instruments or conditions may require retraining.
- No changelog or versioning guidance is provided in the repository, making it difficult to track which training datasets correspond to which model versions.
- The DNMS2Purifier_model_generation.r script documentation is limited; exact statistical method, feature engineering, and hyperparameter tuning are not fully detailed.

## Evidence

- [other] Prepare training data containing annotated MS/MS spectra and purity labels from LC-MS/MS acquisitions in DDA mode.: "Prepare training data containing annotated MS/MS spectra and purity labels from LC-MS/MS acquisitions in DDA mode."
- [other] Execute the model generation script to train the customized purification model on the prepared training dataset.: "Execute the model generation script to train the customized purification model on the prepared training dataset."
- [other] Serialize and save the trained model object to an .rds file for downstream use in the DNMS2Purifier.r purification workflow.: "Serialize and save the trained model object to an .rds file for downstream use in the DNMS2Purifier.r purification workflow."
- [readme] we also provide the script DNMS2Purifier_model_generation.r for customized model training: "we also provide the script DNMS2Purifier_model_generation.r for customized model training"
- [readme] The program is written in R (ver 4.2.1).: "The program is written in R (ver 4.2.1)."
