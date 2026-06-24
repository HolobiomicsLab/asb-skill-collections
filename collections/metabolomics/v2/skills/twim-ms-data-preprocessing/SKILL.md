---
name: twim-ms-data-preprocessing
description: Use when you have raw or processed TWIM-MS experimental data (arrival
  times, m/z, ion mobility parameters) and need to compute class-conditioned CCS values
  or assign biomolecular class labels directly from high-dimensional ion mobility
  measurements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - MOCCal
  - DEIMoS
  techniques:
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
- Functionality includes collision cross section (CCS) calibration, experimental data
  biomolecular class assignment, and experimental class-specific CCS calculations
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# TWIM-MS Data Preprocessing

## Summary

Prepare raw or processed traveling-wave ion mobility mass spectrometry (TWIM-MS) data for collision cross section (CCS) calibration and biomolecular class assignment by converting arrival time measurements to drift time, partitioning by class stratum, and applying reference standard calibration. This skill enables downstream CCS computation without requiring prior feature identification.

## When to use

Apply this skill when you have raw or processed TWIM-MS experimental data (arrival times, m/z, ion mobility parameters) and need to compute class-conditioned CCS values or assign biomolecular class labels directly from high-dimensional ion mobility measurements. Specifically, use this when you want to bypass traditional feature identification and work directly from arrival time and mass spectrometry dimensions.

## When NOT to use

- Input data are already processed into identified feature peaks with pre-computed CCS values; preprocessing would be redundant.
- TWIM-MS data lack arrival time or m/z dimensions; preprocessing requires both high-dimensional data streams.
- No class-specific reference standards are available for the biomolecular classes present in your sample; class-conditioned calibration requires appropriate calibrant data.

## Inputs

- Raw TWIM-MS data (arrival time and m/z dimensions)
- Ion mobility parameters (drift time, time-of-flight offset)
- Biomolecular class assignments (if pre-labeled) or unlabeled experimental features
- Class-specific reference standard calibration sets

## Outputs

- Drift-time-corrected ion measurement table
- Biomolecular class-labeled feature table
- Ion identifier to class-conditioned CCS mapping table
- Structured output file with class labels and CCS values

## How to apply

Load TWIM-MS experimental data containing arrival times and ion mobility parameters into MOCCal. Subtract the time-of-flight offset from arrival time measurements to convert to drift time values that represent the time an ion spends within the TWIM cell. Partition the ion population by biomolecular class label (if available) or apply MOCCal's class assignment algorithm to label features directly from the high-dimensional data. For each class stratum, apply class-specific CCS calibration using the appropriate reference standard set for that biomolecular class. Compute CCS for each ion using the calibrated drift-time-to-CCS relationship, then output a structured table mapping ion identifiers to class labels and class-conditioned CCS values. The key rationale is that class-specific calibration accounts for systematic differences in ion behavior across biomolecular classes (lipid, peptide, carbohydrate, etc.), improving CCS accuracy without requiring feature peaks to be identified beforehand.

## Related tools

- **MOCCal** (Primary application for class assignment, drift-time conversion, and class-specific CCS calibration from TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Optional dependency for processing raw calibration files when using MOCCal_RawDT module) — http://github.com/pnnl/deimos
- **Python** (Programming language runtime for executing MOCCal scripts and data transformation workflows)

## Evaluation signals

- Drift time values are positive, finite, and consistent with time-of-flight offset subtraction (arrival time - offset = drift time).
- Ion populations are successfully partitioned by class label with no ions missing or duplicated across strata.
- CCS values for each class stratum fall within expected ranges for that biomolecular class (e.g., lipids typically have higher CCS than peptides of equivalent mass).
- Output table schema matches the documented structure: ion identifiers, class labels, drift times, and class-conditioned CCS values with no null or NaN entries in required columns.
- Class-specific calibration curves (drift-time-to-CCS) are monotonic and pass through or near the appropriate reference standards for each class.

## Limitations

- Arrival time and drift time are used interchangeably within MOCCal software, but TWIM platforms record arrival time (time at detector), not drift time (time in TWIM cell); preprocessing must correctly subtract the time-of-flight offset to recover true drift time.
- Class-specific CCS calculations require appropriate reference standard sets for each biomolecular class; missing or incorrect calibrants will introduce systematic bias.
- MOCCal offers class assignment without prior feature identification, but accuracy of class labels depends on the quality of the training or assignment algorithm; misclassified ions will receive incorrect CCS calibration.
- No changelog is available, limiting traceability of updates or methodological changes in the software.

## Evidence

- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [other] For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset.: "For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset."
- [other] Apply class-specific CCS calibration using the appropriate reference standard set for that biomolecular class.: "Apply class-specific CCS calibration using the appropriate reference standard set for that biomolecular class."
- [other] MOCCal implements biomolecular class assignment functionality that operates on experimental TWIM-MS data to label features by class without requiring features to be identified first.: "MOCCal implements biomolecular class assignment functionality that operates on experimental TWIM-MS data to label features by class without requiring features to be identified first."
- [readme] Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations.: "Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations."
