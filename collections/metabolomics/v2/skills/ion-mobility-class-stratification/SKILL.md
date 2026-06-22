---
name: ion-mobility-class-stratification
description: Use when you have TWIM-MS experimental data with assigned biomolecular class labels (e.g., peptides, lipids, carbohydrates) and arrival time measurements, and you need to compute CCS values conditioned on class membership.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
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

# ion-mobility-class-stratification

## Summary

Partition TWIM-MS ion populations by biomolecular class assignment, then apply class-specific CCS calibration to compute collision cross section values without requiring prior feature identification. This enables direct CCS computation on class-stratified ion subsets.

## When to use

You have TWIM-MS experimental data with assigned biomolecular class labels (e.g., peptides, lipids, carbohydrates) and arrival time measurements, and you need to compute CCS values conditioned on class membership. Use this skill when class-specific reference standards are available and you want to avoid feature identification as a prerequisite step.

## When NOT to use

- Ion population lacks pre-assigned biomolecular class labels; use general CCS calibration instead.
- Class-specific reference standards are unavailable for assigned classes; fall back to global calibration.
- Input is already a feature table with identified m/z and CCS pairs; skip to downstream analysis.

## Inputs

- biomolecular class assignments (class labels per ion)
- TWIM-MS experimental data (arrival times, ion mobility parameters)
- time-of-flight offset values
- class-specific reference standard calibration data

## Outputs

- table mapping ion identifiers to class labels and class-conditioned CCS values
- class-stratified CCS table

## How to apply

Load the biomolecular class assignments and corresponding TWIM-MS experimental data (arrival times and ion mobility parameters). Partition the ion population by assigned class label to create class-stratified subsets. For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset. Apply class-specific CCS calibration using the appropriate reference standard set for that biomolecular class. Compute CCS for each ion using the calibrated drift-time-to-CCS relationship. Output a table mapping ion identifiers to their class labels and class-conditioned CCS values.

## Related tools

- **MOCCal** (Python application that implements class-specific CCS calibration workflow on TWIM-MS data with biomolecular class assignments) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Required dependency for processing raw calibration files in MOCCal's RawDT workflow) — http://github.com/pnnl/deimos

## Evaluation signals

- Output table contains no null CCS values for any ion in the input; all ions in each class stratum receive a CCS assignment.
- Class labels in output match input class assignments exactly; no ion changes class label during stratification.
- CCS values for ions within the same class fall within expected range for reference standards used for that class.
- Drift time conversion is consistent: (arrival_time - tof_offset) yields physically plausible drift times (positive, within instrument response window).
- Output row count equals input ion count; no ions are dropped or duplicated during stratification and calibration.

## Limitations

- MOCCal terminology uses 'arrival time' and 'drift time' interchangeably for convenience, but TWIM platforms record arrival time (detector arrival) not true drift time (time in mobility cell); practitioners must ensure offset correction is applied correctly.
- Class-specific calibration is only as accurate as the reference standards available for each class; missing or poor-quality standards for a class will degrade CCS accuracy for that stratum.
- No changelog available in the repository; version stability and breaking changes are not explicitly tracked.
- Workflow requires pre-computed biomolecular class assignments from an external classifier; this skill does not perform class assignment itself.

## Evidence

- [other] MOCCal performs experimental class-specific CCS calculations as a workflow component that operates on biomolecular class assignments, enabling CCS computation without requiring prior feature identification.: "MOCCal performs experimental class-specific CCS calculations as a workflow component that operates on biomolecular class assignments, enabling CCS computation without requiring prior feature"
- [other] 1. Load the biomolecular class assignments and corresponding TWIM-MS experimental data (arrival times and ion mobility parameters). 2. Partition the ion population by assigned class label. 3. For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset. 4. Apply class-specific CCS calibration using the appropriate reference standard set for that biomolecular class. 5. Compute CCS for each ion using the calibrated drift-time-to-CCS relationship. 6. Output a table mapping ion identifiers to their class labels and class-conditioned CCS values.: "Partition the ion population by assigned class label. For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset. Apply"
- [intro] MOCCal offers class assignment and CCS calculations without need for identifying the features first.: "MOCCal offers class assignment and CCS calculations without need for identifying the features first."
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
