---
name: ms-ms-spectrum-annotation-preprocessing
description: Use when you have raw LC-MS/MS data acquired in Data-Dependent Acquisition
  (DDA) mode and need to create a labeled training dataset for customized purification
  model development.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - DNMS2Purifier_model_generation.r
  - DNMS2Purifier.r
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS/MS Spectrum Annotation Preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare and annotate MS/MS spectra from LC-MS/MS acquisitions in DDA mode by curating training datasets with purity labels to enable downstream chimeric spectrum purification and customized model training. This skill bridges raw spectral acquisition and machine-learning-ready training sets.

## When to use

You have raw LC-MS/MS data acquired in Data-Dependent Acquisition (DDA) mode and need to create a labeled training dataset for customized purification model development. Specifically, when you want to train DNMS2Purifier or similar spectrum-quality classifiers on your own instrument, sample matrix, or experimental conditions rather than relying on pre-trained models.

## When NOT to use

- Your input spectra are already pre-processed, quality-filtered, or de-chimeric from another tool — this skill assumes raw or minimally processed spectra requiring annotation.
- You are applying an existing pre-trained DNMS2Purifier model to new data without retraining — use the main DNMS2Purifier.r purification script directly instead.
- Your MS/MS data was acquired in targeted or Selected Reaction Monitoring (SRM) mode rather than Data-Dependent Acquisition (DDA) mode.

## Inputs

- Raw MS/MS spectra from LC-MS/MS DDA acquisitions
- Annotated purity labels or quality scores for each spectrum
- Structured training data (data frame or matrix) containing spectral features and annotations

## Outputs

- Serialized trained purification model (.rds file)
- Customized model object compatible with DNMS2Purifier.r workflow

## How to apply

Collect MS/MS spectra from LC-MS/MS acquisitions performed in DDA mode, ensuring representative coverage of your experimental conditions and sample matrices. Manually or semi-automatically annotate each spectrum with a purity label (typically binary: pure or chimeric, or continuous quality scores) based on visual inspection, spectral quality metrics, or ground-truth tandem MS interpretation. Organize the annotated spectra and their purity labels into a structured dataset (e.g., a data frame with spectral features and labels). Load this training dataset into the DNMS2Purifier_model_generation.r script running under R 4.2.1, which will train a customized purification model on the annotated data. The trained model is serialized and saved as an .rds file for integration into the main DNMS2Purifier.r workflow.

## Related tools

- **DNMS2Purifier_model_generation.r** (R script that trains the customized purification model on annotated training data and serializes the model to .rds format) — https://github.com/HuanLab/DNMS2Purifier
- **R** (Runtime environment (version 4.2.1 required) for executing model training and serialization)
- **DNMS2Purifier.r** (Main purification script that consumes the trained model .rds file for MS/MS spectrum purification) — https://github.com/HuanLab/DNMS2Purifier

## Examples

```
# Load training data with annotated MS/MS spectra and purity labels, then execute:
Rscript DNMS2Purifier_model_generation.R --input training_data.csv --output customized_model.rds
```

## Evaluation signals

- Training dataset contains annotated MS/MS spectra with corresponding purity labels; no missing or mismatched entries between spectra and labels.
- Trained model .rds file is successfully serialized and can be loaded into R 4.2.1 without errors.
- Model object contains expected structure and parameters (e.g., feature weights, classification thresholds) compatible with DNMS2Purifier.r intake.
- When the trained model is applied to held-out test spectra, classification accuracy, sensitivity, and specificity meet domain expectations for chimeric vs. pure spectrum discrimination.
- Training data distribution reflects the instrument, sample matrix, and ionization conditions of the target application (e.g., representative sample diversity, ion abundance ranges).

## Limitations

- Annotation quality and completeness directly affect model performance; subjective or incomplete purity labeling will propagate as classification bias.
- Training dataset must be sufficiently large and representative to avoid overfitting; no minimum sample size is specified in the documentation.
- Model trained on one LC-MS/MS platform or sample matrix may not generalize well to different instruments, ion sources, or chemical spaces without retraining.
- No changelog or version history is publicly available, limiting reproducibility and tracking of model training updates.
- The skill is specific to the DNMS2Purifier framework; compatibility with other spectrum purification tools or formats is not addressed.

## Evidence

- [other] Prepare training data containing annotated MS/MS spectra and purity labels from LC-MS/MS acquisitions in DDA mode.: "Prepare training data containing annotated MS/MS spectra and purity labels from LC-MS/MS acquisitions in DDA mode."
- [other] Execute the model generation script to train the customized purification model on the prepared training dataset.: "Execute the model generation script to train the customized purification model on the prepared training dataset."
- [other] Serialize and save the trained model object to an .rds file for downstream use in the DNMS2Purifier.r purification workflow.: "Serialize and save the trained model object to an .rds file for downstream use in the DNMS2Purifier.r purification workflow."
- [readme] The program is written in R (ver 4.2.1).: "The program is written in R (ver 4.2.1)."
- [readme] DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode.: "DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode."
