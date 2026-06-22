---
name: multi-omic-data-integration
description: Use when you have raw or processed TWIM-MS data with arrival time and m/z dimensions, and you need to assign biomolecular class labels and compute class-specific CCS values across multiple compound classes simultaneously, particularly when you lack pre-identified feature peaks or want to bypass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - Python
  - MOCCal
  - DEIMoS (Data-Extraction for Integrated Multiomic Sources)
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
- Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moccal_cq
    doi: 10.1021/acs.analchem.3c04290
    title: moccal
  dedup_kept_from: coll_moccal_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04290
  all_source_dois:
  - 10.1021/acs.analchem.3c04290
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-omic-data-integration

## Summary

Integrate and calibrate collision cross section (CCS) values across multiple biomolecular classes from traveling-wave ion mobility mass spectrometry (TWIM-MS) data without requiring prior feature identification. This skill enables unified CCS calibration and class-specific calculations across lipids, peptides, carbohydrates, and other biomolecular species in a single workflow.

## When to use

Apply this skill when you have raw or processed TWIM-MS data with arrival time and m/z dimensions, and you need to assign biomolecular class labels and compute class-specific CCS values across multiple compound classes simultaneously, particularly when you lack pre-identified feature peaks or want to bypass traditional feature detection bottlenecks.

## When NOT to use

- Input data is already a fully annotated and CCS-calibrated feature table—MOCCal class assignment and calibration would be redundant.
- You require drift time (time spent in TWIM cell) rather than arrival time; MOCCal operates on arrival time and the software uses these terms interchangeably, which may introduce confusion.
- Your input is not TWIM-MS data or uses a different ion-mobility platform (e.g., DTIMS, TIMS); MOCCal is specific to traveling-wave platforms.

## Inputs

- Raw TWIM-MS data (arrival time and m/z dimensions)
- Processed TWIM-MS feature table (UserDT format)
- Calibration reference standards (with known CCS values)
- Raw calibration files (RawDT format, if using DEIMoS preprocessing)

## Outputs

- Class-labeled feature table with assigned biomolecular classes
- CCS-calibrated feature annotations (class-specific CCS values)
- Structured output file with integrated multi-omic metadata

## How to apply

Load your TWIM-MS data (raw arrival time and m/z pairs, or processed feature table) into MOCCal. Apply MOCCal's biomolecular class assignment algorithm to label each experimental feature by class (lipid, peptide, carbohydrate, or other) directly from the high-dimensional data. For each class, perform CCS calibration using reference standards appropriate to that class, then calculate class-specific CCS values for experimental features. The rationale is that biomolecular class membership determines the optimal CCS calibration model; treating all classes together would introduce systematic bias, whereas class-stratified calibration exploits the differential ion-mobility behavior of different molecular types. Output a class-labeled feature table with calibrated CCS annotations for downstream structural or functional annotation.

## Related tools

- **MOCCal** (Primary Python application for CCS calibration, biomolecular class assignment, and class-specific CCS calculation from TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS (Data-Extraction for Integrated Multiomic Sources)** (Optional preprocessing tool for raw calibration files (version 1.3.2 required); used in MOCCal_RawDT workflow) — http://github.com/pnnl/deimos

## Examples

```
python MOCCal_UserDT.py --input processed_twim_data.csv --output class_labeled_features.csv
```

## Evaluation signals

- Each experimental feature in the output table has a non-null biomolecular class label (e.g., 'lipid', 'peptide', 'carbohydrate', 'other') assigned by MOCCal.
- CCS values are present and fall within expected ranges for the assigned class (e.g., lipids typically have higher CCS than peptides of equivalent m/z).
- Class-specific calibration curves show acceptable fit quality and residuals; internal standards or reference compounds align with their literature CCS values within instrument tolerance.
- Output file schema matches MOCCal's structured format (e.g., columns for m/z, arrival time, assigned class, calibrated CCS).
- No features are missing or dropped unexpectedly; row counts in the output table remain consistent with or exceed the input feature count, accounting only for any intentional filtering steps.

## Limitations

- MOCCal conflates arrival time and drift time terminology for convenience, which may cause confusion in cross-platform comparisons; practitioners must remember that TWIM platforms record arrival time (time to detector), not drift time (residence in cell).
- Biomolecular class assignment accuracy depends on the quality and completeness of training data and calibration reference standards; classes with sparse reference data may receive lower-confidence assignments.
- The UserDT (processed calibration data) version requires no Python installation but is limited to pre-processed inputs; RawDT requires DEIMoS setup and additional dependencies, creating a two-tier workflow with different use cases.
- No changelog is available in the repository, making it difficult to track version-specific behavior or known issues.

## Evidence

- [other] MOCCal implements biomolecular class assignment functionality that operates on experimental TWIM-MS data to label features by class, and performs class-specific CCS calculations, without requiring features to be identified first.: "MOCCal implements biomolecular class assignment functionality that operates on experimental TWIM-MS data to label features by class, and performs class-specific CCS calculations, without requiring"
- [readme] MOCCal, or Multi-Omic CCS Calibrator, is a Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data anlaysis. Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations.: "MOCCal, or Multi-Omic CCS Calibrator, is a Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data anlaysis. Functionality includes collision"
- [other] Apply MOCCal's biomolecular class assignment algorithm to label each experimental feature by class (e.g., lipid, peptide, carbohydrate, or other) directly from the high-dimensional data without requiring pre-identified feature peaks.: "Apply MOCCal's biomolecular class assignment algorithm to label each experimental feature by class (e.g., lipid, peptide, carbohydrate, or other) directly from the high-dimensional data without"
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [readme] If you plan to use raw calibration files, you will need to install pnnl's DEIMoS, version 1.3.2 (http://github.com/pnnl/deimos). After DEIMoS is set up, you can then run MOCCal_RawDT.py in the DEIMoS virtual environment.: "If you plan to use raw calibration files, you will need to install pnnl's DEIMoS, version 1.3.2 (http://github.com/pnnl/deimos). After DEIMoS is set up, you can then run MOCCal_RawDT.py in the DEIMoS"
