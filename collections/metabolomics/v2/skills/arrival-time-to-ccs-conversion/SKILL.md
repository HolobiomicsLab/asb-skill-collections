---
name: arrival-time-to-ccs-conversion
description: Use when when you have raw TWIM-MS arrival-time data and need to transform
  it into absolute CCS values for downstream biomolecular class assignment or comparative
  analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - HinesLab/MOCCal
  - MOCCal
  - DEIMoS
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
- HinesLab/MOCCal
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moccal
    doi: 10.1021/acs.analchem.3c04290
    title: moccal
  dedup_kept_from: coll_moccal
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

# arrival-time-to-ccs-conversion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert raw arrival-time measurements from TWIM-MS into calibrated collision cross section (CCS) values by establishing a mapping function from reference compounds with known CCS values. This enables standardized, comparable ion mobility measurements across multi-omic datasets.

## When to use

When you have raw TWIM-MS arrival-time data and need to transform it into absolute CCS values for downstream biomolecular class assignment or comparative analysis. Specifically applicable when a calibration template with reference compounds and their known CCS values is available, and you require feature-independent CCS quantitation without prior feature identification.

## When NOT to use

- Input data already contains calibrated CCS values (not raw arrival times)—skip directly to class assignment or quantitation.
- No reference compounds or known CCS values are available—calibration cannot be established without calibration standards.
- Data is from drift-time (not arrival-time) ion mobility spectrometry, or the instrument uses a different ion mobility principle not compatible with TWIM calibration.

## Inputs

- Raw TWIM-MS arrival-time data (arrival times for experimental ions)
- Calibration reference template (reference compounds with known CCS values)
- Ion identifiers associated with arrival-time measurements

## Outputs

- Calibrated CCS table (arrival times mapped to CCS values with ion identifiers)
- Arrival-time-to-CCS mapping function / calibration curve

## How to apply

Load raw arrival-time data and a calibration reference template containing known CCS values for calibration compounds. Parse the reference compounds and their associated CCS values from the template. Establish an arrival-time-to-CCS mapping function (calibration curve) using the reference points—this function transforms experimental arrival-time measurements into absolute CCS values by linear or nonlinear regression. Apply the calibration transform to all experimental arrival-time values to produce calibrated CCS output. Validate the output CCS table for completeness (no missing values for assigned ions) and correct field structure (ion identifiers, arrival times, calibrated CCS values).

## Related tools

- **MOCCal** (Python application that implements CCS calibration module to transform arrival-time data into CCS values for multi-omic TWIM-MS analysis) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Optional dependency for processing raw calibration files (version 1.3.2 required when using RawDT workflow)) — http://github.com/pnnl/deimos

## Evaluation signals

- Output CCS table contains no missing values for all ions with assigned arrival times.
- Calibration curve R² or residual error on reference compounds is within acceptable range (article does not specify threshold, but visual inspection of calibration fit should show low scatter).
- CCS values for reference compounds match or closely approximate their known literature values.
- Output CCS table has correct field structure: ion identifiers, arrival times, and calibrated CCS values in expected column order.
- CCS values are monotonically increasing or decreasing with arrival time across the dataset, consistent with the established calibration function.

## Limitations

- TWIM platforms record arrival time (when ion reaches detector) rather than drift time (time spent in TWIM cell); MOCCal uses these terms interchangeably for convenience, which may cause confusion with drift-time instruments.
- Calibration accuracy depends on the quality and completeness of the reference compound set; sparse or non-representative reference compounds may produce poor calibration curves.
- No changelog documented in the repository, limiting visibility into method changes or validation history across versions.
- DEIMoS dependency (version 1.3.2) is required only for raw calibration data processing; processed data does not require additional dependencies, creating two separate execution paths.

## Evidence

- [other] MOCCal implements CCS calibration as a core functionality that transforms TWIM-MS arrival-time data into collision cross section values: "MOCCal implements CCS calibration as a core functionality that transforms TWIM-MS arrival-time data into collision cross section values for multi-omic high-dimensional analysis."
- [other] Parse calibration reference compounds and establish arrival-time-to-CCS mapping function using calibration reference points: "Parse calibration reference compounds and their known CCS values from the template. Establish arrival-time-to-CCS mapping function using calibration reference points."
- [other] Apply calibration transform to experimental arrival-time values to produce calibrated CCS values: "Apply calibration transform to experimental arrival-time values to produce calibrated CCS values. Output calibrated CCS table with corresponding ion identifiers."
- [readme] TWIM platforms record arrival time rather than drift time: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [readme] MOCCal offers class assignment and CCS calculations without need for identifying features first: "MOCCal offers class assignment and CCS calculations without need for identifying the features first"
- [other] Load raw arrival-time data and calibration template from MOCCal repository example files: "Load raw arrival-time data and calibration template from MOCCal repository example files."
