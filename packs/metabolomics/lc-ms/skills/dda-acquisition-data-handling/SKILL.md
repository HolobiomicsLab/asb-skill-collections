---
name: dda-acquisition-data-handling
description: Use when you have raw or processed LC-MS/MS data from DDA mode acquisitions and need to extract, annotate, and structure MS/MS spectra with purity labels (or quality indicators) to serve as input to the DNMS2Purifier customized model training workflow, or to prepare data for purification of.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - R
  - DNMS2Purifier_model_generation.r
  - DNMS2Purifier.r
  - R 4.2.1
  techniques:
  - LC-MS
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

# dda-acquisition-data-handling

## Summary

Prepare and format LC-MS/MS data acquired in Data-Dependent Acquisition (DDA) mode for chimeric MS/MS spectrum purification. This skill encompasses loading annotated MS/MS spectra and purity labels from DDA acquisitions into a structured training or analysis dataset suitable for model training or purification workflows.

## When to use

You have raw or processed LC-MS/MS data from DDA mode acquisitions and need to extract, annotate, and structure MS/MS spectra with purity labels (or quality indicators) to serve as input to the DNMS2Purifier customized model training workflow, or to prepare data for purification of chimeric spectra in untargeted metabolomics studies.

## When NOT to use

- Your data is from Parallel Reaction Monitoring (PRM) or Selected Reaction Monitoring (SRM) mode — these targeted acquisition modes do not produce the complex chimeric spectra that DNMS2Purifier is designed to address.
- MS/MS spectra are already purified or you lack any annotation of spectrum quality or purity status — the model requires labeled training data to learn the distinction between chimeric and pure spectra.
- Your study does not involve untargeted metabolomics or does not need to address chimeric spectrum contamination.

## Inputs

- LC-MS/MS raw data files from DDA mode acquisition (mzML, mzXML, or vendor formats)
- Annotated MS/MS spectra with precursor m/z, retention time, and intensity values
- Purity labels or quality indicators for each MS/MS spectrum

## Outputs

- Structured training dataset (R data frame or matrix) with MS/MS features and purity labels
- Serialized trained model object (.rds file) for downstream use in DNMS2Purifier.r purification workflow

## How to apply

Load your LC-MS/MS DDA acquisition data (typically in mzML, mzXML, or vendor-specific formats) and extract MS/MS spectra along with their precursor m/z, retention time, and intensity information. Annotate each spectrum with a purity label (e.g., chimeric vs. pure, or a continuous purity score) based on manual inspection, spectral quality metrics, or reference standards. Organize the annotated spectra and purity labels into a structured training dataset (e.g., a data frame or matrix) compatible with R 4.2.1. This dataset serves as input to the DNMS2Purifier_model_generation.r script, which trains a customized purification model on your data. Ensure that spectra cover diverse m/z ranges and ionization conditions representative of your experimental workflow to maximize model generalizability.

## Related tools

- **DNMS2Purifier_model_generation.r** (Executes customized model training on the prepared DDA training dataset to generate a purification model) — https://github.com/HuanLab/DNMS2Purifier
- **DNMS2Purifier.r** (Main purification workflow that applies the trained model to purify chimeric MS/MS spectra from new DDA acquisitions) — https://github.com/HuanLab/DNMS2Purifier
- **R 4.2.1** (Runtime environment for loading, manipulating, and preparing DDA data structures before model training)

## Examples

```
# Load DDA acquisition data, annotate MS/MS spectra with purity labels, and prepare training set
# source('DNMS2Purifier_model_generation.r'); train_model(training_data, output_file='model.rds')
```

## Evaluation signals

- Training dataset contains MS/MS spectra with complete intensity arrays, precursor m/z values, and retention times with no missing or corrupted entries.
- Each spectrum in the training set has a corresponding purity label (binary chimeric/pure classification or continuous purity score) with no null values.
- Purity label distribution across the training set shows reasonable coverage of both chimeric and pure spectra (e.g., not heavily skewed to one class).
- Trained model (.rds file) is successfully serialized and can be loaded into the DNMS2Purifier.r purification workflow without errors.
- Model performance on held-out validation data (if available) shows improved purification accuracy compared to unpurified spectra, indicating that the model learned meaningful discriminative features from the DDA training data.

## Limitations

- The quality and completeness of purity annotations directly determine model performance; manual annotation is labor-intensive and subject to observer bias.
- Training on a small or non-representative sample of DDA conditions (m/z range, ionization method, chromatographic gradient) may reduce model generalizability to new experimental setups.
- DDA mode inherently produces variable MS/MS spectral quality and chimeric events depending on precursor intensity, isolation window width, and dynamic exclusion settings; preprocessing and filtering of raw spectra may be necessary before annotation.
- The skill assumes access to R 4.2.1 and required R packages (dependencies not fully specified in README); missing or incompatible packages will halt model training.

## Evidence

- [other] Prepare training data containing annotated MS/MS spectra and purity labels from LC-MS/MS acquisitions in DDA mode.: "Prepare training data containing annotated MS/MS spectra and purity labels from LC-MS/MS acquisitions in DDA mode."
- [readme] DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode.: "DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode."
- [readme] The program is written in R (ver 4.2.1).: "The program is written in R (ver 4.2.1)."
- [other] Execute the model generation script to train the customized purification model on the prepared training dataset.: "Execute the model generation script to train the customized purification model on the prepared training dataset."
- [other] Serialize and save the trained model object to an .rds file for downstream use in the DNMS2Purifier.r purification workflow.: "Serialize and save the trained model object to an .rds file for downstream use in the DNMS2Purifier.r purification workflow."
