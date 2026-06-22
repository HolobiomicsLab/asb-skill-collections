---
name: class-conditional-calibration-mapping
description: Use when you have TWIM-MS experimental data (arrival times and ion mobility parameters) paired with pre-assigned biomolecular class labels for an ion population, and you need to obtain class-conditioned CCS values without first performing feature-level identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - MOCCal
  - DEIMoS
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
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

# class-conditional-calibration-mapping

## Summary

Compute collision cross section (CCS) values for ions stratified by biomolecular class assignment, using class-specific reference standards to calibrate drift-time-to-CCS relationships without requiring prior feature identification. This enables direct CCS calculation from TWIM-MS arrival time data conditioned on experimental class labels.

## When to use

Apply this skill when you have TWIM-MS experimental data (arrival times and ion mobility parameters) paired with pre-assigned biomolecular class labels for an ion population, and you need to obtain class-conditioned CCS values without first performing feature-level identification. This is especially valuable in high-dimensional multi-omic workflows where class assignment precedes feature detection.

## When NOT to use

- Input ions lack pre-assigned biomolecular class labels or class assignment is unavailable.
- Reference standard calibration sets are not available or defined for the classes present in your data.
- Raw uncalibrated TWIM data has not been processed to extract arrival times and ion mobility parameters.

## Inputs

- Biomolecular class assignments (ion identifier → class label mapping)
- TWIM-MS experimental data: arrival times and ion mobility parameters
- Class-specific reference standard calibration data

## Outputs

- Ion identifier table with class labels and class-conditioned CCS values

## How to apply

Partition the ion population by assigned class label. For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset. Apply the appropriate reference standard calibration set for that biomolecular class to establish a class-specific drift-time-to-CCS mapping function. Compute CCS for each ion using its calibrated relationship. Output a table mapping ion identifiers to both their class labels and class-conditioned CCS values. The rationale is that different biomolecular classes (e.g., lipids, peptides, carbohydrates) may have different ion behavior in TWIM, so using class-matched calibration standards improves accuracy over global calibration.

## Related tools

- **MOCCal** (Python application that implements class-specific CCS calibration workflow, partitions ions by class label, and computes class-conditioned CCS values from TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Dependency for MOCCal_RawDT.py; required to preprocess raw calibration files before class-conditional calibration) — http://github.com/pnnl/deimos

## Evaluation signals

- Class-stratified CCS outputs have no missing or null values for ions assigned to defined classes.
- CCS values fall within expected ranges for their assigned biomolecular class (e.g., lipids typically 200–600 Ų; peptides 400–1200 Ų).
- Class-specific calibration R² or RMSE values meet acceptable thresholds (article does not specify exact cutoffs, but calibration fit should be documented).
- Ion count per class matches the input partition; no ions are dropped or misallocated during class-conditional processing.
- CCS values computed from the same drift time differ only if ions are assigned to different classes, demonstrating class-conditional differentiation.

## Limitations

- Requires pre-existing biomolecular class assignments; skill cannot perform de novo class discovery or inference.
- Accuracy depends on availability and quality of class-specific reference standard calibration sets; missing or low-quality standards for a class will degrade CCS computation for that class.
- TWIM platforms record arrival time (time at detector) rather than drift time (time in TWIM cell); conversion requires accurate time-of-flight offset, which must be independently determined.
- No changelog or version history provided in the repository, making it difficult to track improvements, bug fixes, or methodological changes over time.

## Evidence

- [other] MOCCal performs experimental class-specific CCS calculations as a workflow component that operates on biomolecular class assignments, enabling CCS computation without requiring prior feature identification.: "MOCCal performs experimental class-specific CCS calculations as a workflow component that operates on biomolecular class assignments, enabling CCS computation without requiring prior feature"
- [other] Partition the ion population by assigned class label. For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset. Apply class-specific CCS calibration using the appropriate reference standard set for that biomolecular class.: "Partition the ion population by assigned class label. For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset. Apply"
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [intro] MOCCal offers class assignment and CCS calculations without need for identifying the features first.: "MOCCal offers class assignment and CCS calculations without need for identifying the features first."
- [intro] Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations.: "Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations."
