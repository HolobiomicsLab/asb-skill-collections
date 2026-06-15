---
name: class-specific-ccs-calculation
description: Use when when you have multi-omic TWIM-MS data (raw or processed arrival-time records) and have already assigned features or detected ion features to biomolecular classes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3291
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - HinesLab/MOCCal
  - MOCCal
  - DEIMoS
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
- HinesLab/MOCCal
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moccal
    doi: 10.1021/acs.analchem.3c04290
    title: moccal
  dedup_kept_from: coll_moccal
schema_version: 0.2.0
---

# class-specific-ccs-calculation

## Summary

Calculate collision cross section (CCS) values partitioned by biomolecular class for TWIM-MS data using MOCCal, enabling class-aware mobility calibration without prior feature identification. This skill produces class-stratified CCS tables suitable for downstream biomolecular annotation and structure elucidation.

## When to use

When you have multi-omic TWIM-MS data (raw or processed arrival-time records) and have already assigned features or detected ion features to biomolecular classes (e.g., lipid, carbohydrate, protein), and you need CCS values stratified by class to improve calibration accuracy or enable structure-informed mobility analysis. Specifically applicable when a single global CCS calibration curve does not adequately model the arrival-time–to–CCS relationship across diverse chemical classes.

## When NOT to use

- Input data lacks biomolecular class assignments (apply biomolecular class assignment step first).
- CCS calibration curve has not been established; feature arrival times cannot be converted to CCS without a validated calibration model.
- Data is already a fully annotated feature table with CCS values pre-computed; recalculation would be redundant.

## Inputs

- TWIM-MS arrival-time dataset (multi-omic, raw or processed HDF5/NetCDF/CSV format)
- Biomolecular class assignment labels (feature ID → class mapping, e.g., 'lipid', 'carbohydrate', 'protein')
- CCS calibration curve (from prior CCS calibration step: polynomial or spline coefficients mapping arrival time to CCS)

## Outputs

- Class-specific CCS table (CSV or formatted table with feature ID, assigned class, arrival time, calculated CCS, and metadata fields)
- CCS validation report (completeness check, field structure verification, physical range flags per class)

## How to apply

After CCS calibration and biomolecular class assignment steps, MOCCal's class-specific CCS calculation module accepts the calibrated TWIM dataset and class labels, then computes class-stratified CCS values by applying the established calibration curve separately within each biomolecular class partition. The workflow partitions features by assigned class (e.g., lipid, carbohydrate), applies the calibration transformation to arrival-time values within each partition, and outputs a CCS table with correct field structure and completeness. Validation involves confirming the output CCS table contains all assigned features, that CCS values fall within expected physical ranges for each class, and that the table schema matches the documented format (field names, data types, units).

## Related tools

- **MOCCal** (Python application that orchestrates CCS calibration, biomolecular class assignment, and class-specific CCS calculations on multi-omic TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Dependency for MOCCal's RawDT workflow; processes raw TWIM-MS calibration files prior to MOCCal execution) — http://github.com/pnnl/deimos
- **Python** (Programming environment and runtime for MOCCal scripts)

## Evaluation signals

- Output CCS table contains all input features with no missing entries in the class-specific CCS column.
- CCS values for each biomolecular class fall within literature-expected physical ranges (e.g., lipids 200–400 Å², carbohydrates 100–250 Å²).
- Output table schema matches documented field structure (feature ID, assigned class, arrival time, CCS value, units, metadata fields present and correctly named).
- Class-stratified CCS distributions show distinct, non-overlapping or minimally overlapping peaks per class, indicating that class-specific calibration has improved separation.
- Validation report flags no structural errors, incomplete records, or out-of-range CCS values for the queried classes.

## Limitations

- MOCCal requires a prior, validated CCS calibration curve; without reference standards or calibration data, class-specific CCS calculation cannot proceed.
- Biomolecular class assignment accuracy directly impacts CCS calculation quality; misclassified features will receive incorrect class-specific CCS values.
- TWIM platforms record arrival time (time to detector) rather than drift time (transit within the cell); MOCCal requires platform-specific conversion, and mixing platform types without recalibration will introduce systematic error.
- No changelog documented in repository; version stability and breaking changes between releases are not explicitly tracked.

## Evidence

- [intro] MOCCal enables collision cross section (CCS) calibration for high-dimensional, multi-omic TWIM-MS data: "Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data anlaysis. Functionality includes collision cross section (CCS) calibration"
- [intro] MOCCal performs experimental data biomolecular class assignment and experimental class-specific CCS calculations: "experimental data biomolecular class assignment, and experimental class-specific CCS calculations"
- [intro] MOCCal can perform class assignment and CCS calculations without requiring prior feature identification: "MOCCal offers class assignment and CCS calculations without need for identifying the features first"
- [intro] TWIM platforms record arrival time rather than drift time: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)"
- [other] Workflow step: class-specific CCS calculations: "Calculate class-specific CCS values for the assigned biomolecular classes"
- [other] Validation of CCS output table for completeness and structure: "Validate the output CCS table for completeness and correct field structure"
