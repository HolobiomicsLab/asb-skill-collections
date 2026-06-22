---
name: chimeric-spectrum-detection-and-filtering
description: Use when you have acquired LC-MS/MS data in Data-Dependent Acquisition (DDA) mode for untargeted metabolomics and suspect contamination from chimeric (co-fragmented) MS/MS spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - R
  - DNMS2Purifier.r
  - DNMS2Purifier_model_generation.r
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chimeric-spectrum-detection-and-filtering

## Summary

Detection and removal of chimeric MS/MS spectra from LC-MS/MS Data-Dependent Acquisition (DDA) metabolomics datasets using the DNMS2Purifier bioinformatic solution. This skill purifies untargeted metabolomics data by identifying and filtering co-fragmentation artifacts that occur when multiple precursor ions are isolated and fragmented simultaneously.

## When to use

Apply this skill when you have acquired LC-MS/MS data in Data-Dependent Acquisition (DDA) mode for untargeted metabolomics and suspect contamination from chimeric (co-fragmented) MS/MS spectra. Chimeric spectra arise when the instrument's isolation window captures multiple precursor ions, leading to composite fragment patterns that confound downstream spectral library matching and metabolite identification. Use this skill before spectral annotation or compound database searching to improve confidence in MS/MS identifications.

## When NOT to use

- Data acquired in targeted or selective reaction monitoring (SRM/MRM) mode — isolation windows are too narrow to capture co-fragmentation, making chimeric filtering unnecessary.
- Already-processed or aggregated spectral libraries where individual MS/MS events cannot be re-scored or flagged.
- Metabolomics datasets from parallel reaction monitoring (PRM) or other high-resolution targeted acquisition modes where precursor isolation is stringent by design.

## Inputs

- LC-MS/MS raw data acquired in Data-Dependent Acquisition (DDA) mode
- mzML or equivalent structured MS/MS spectra file
- Machine learning model (pre-trained or custom-trained via DNMS2Purifier_model_generation.r)

## Outputs

- Purified MS/MS spectra dataset with chimeric spectra removed or flagged
- Quality-filtered spectrum annotations indicating chimeric status
- Processed data ready for spectral library matching and metabolite identification

## How to apply

Load your DDA-mode LC-MS/MS data (e.g., raw or mzML format) into the DNMS2Purifier.r main program in R 4.2.1. The program applies machine-learning-based chimeric spectrum detection logic and filtering routines to score and flag spectra that exhibit multi-precursor contamination patterns. The algorithm processes each MS/MS spectrum, applying the pre-trained or customized model (from DNMS2Purifier_model_generation.r if retraining is needed) to distinguish pure MS/MS signals from chimeric blends. Validate output by confirming that flagged spectra show reduced signal complexity and improved alignment to single-compound fragmentation patterns. Retain the purified spectrum dataset for downstream spectral matching and metabolite annotation.

## Related tools

- **DNMS2Purifier.r** (Main executable R script that performs MS/MS purification, chimeric spectrum detection, and filtering) — https://github.com/HuanLab/DNMS2Purifier
- **DNMS2Purifier_model_generation.r** (R script for training customized machine-learning models for chimeric spectrum classification on user-specific datasets) — https://github.com/HuanLab/DNMS2Purifier
- **R 4.2.1** (Runtime environment required to execute DNMS2Purifier scripts)

## Evaluation signals

- Output spectra are properly formatted and match the input schema (precursor m/z, retention time, fragment ion list retained).
- Chimeric spectra flagged by the algorithm show reduced fragment ion complexity compared to unflagged spectra, with fewer unexplained high-intensity peaks outside the expected fragmentation pattern of the labeled precursor.
- Post-purification spectral library matching yields higher cosine similarity or annotation confidence scores, indicating that noise from co-fragmentation has been reduced.
- Manual inspection of a representative subset of flagged spectra confirms visual co-fragmentation artifacts (e.g., multiple precursor neutral loss patterns, incongruous fragment clusters).
- Retention or removal of flagged spectra is statistically justified by measurable improvement in metabolite identification rate or reduction in false-positive compound assignments downstream.

## Limitations

- DNMS2Purifier is optimized for DDA-mode metabolomics and may not generalize to other ionization modes or instrument types not represented in training data.
- Model performance depends on the quality and diversity of training data; custom retraining via DNMS2Purifier_model_generation.r may be necessary for specialized sample types or LC-MS instruments.
- The tool requires R 4.2.1 and associated dependencies; installation and dependency management may pose barriers for users unfamiliar with R environments.
- No detailed changelog is available in the provided documentation, limiting transparency on algorithm updates, bug fixes, or version-specific behavior changes.

## Evidence

- [readme] DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode.: "DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode."
- [readme] The R script DNMS2Purifier.r is the main program for MS/MS purification: "The R script DNMS2Purifier.r is the main program for MS/MS purification"
- [readme] we also provide the script DNMS2Purifier_model_generation.r for customized model training: "we also provide the script DNMS2Purifier_model_generation.r for customized model training"
- [readme] The program is written in R (ver 4.2.1).: "The program is written in R (ver 4.2.1)."
- [other] Execute the program on representative DDA-mode LC-MS/MS test data (if available in the repository) to demonstrate chimeric spectrum detection and purification.: "Execute the program on representative DDA-mode LC-MS/MS test data (if available in the repository) to demonstrate chimeric spectrum detection and purification."
- [other] Validate that the output spectra are properly formatted and chimeric MS/MS signals have been successfully removed or flagged.: "Validate that the output spectra are properly formatted and chimeric MS/MS signals have been successfully removed or flagged."
