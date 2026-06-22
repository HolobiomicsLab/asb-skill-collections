---
name: class-stratified-calibration-model-application
description: Use when you have a feature table with assigned biomolecular class labels (e.g., from preceding class assignment step) and raw ion mobility arrival time measurements from TWIM-MS data, and you need to compute class-appropriate CCS values for downstream multi-omic analysis.
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
  techniques:
  - ion-mobility-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# class-stratified-calibration-model-application

## Summary

Apply class-specific calibration models to convert ion mobility arrival time measurements into collision cross section (CCS) values, using biomolecular class labels to select appropriate calibration parameters for each feature. This skill bridges class assignment and quantitative CCS computation in TWIM-MS workflows.

## When to use

You have a feature table with assigned biomolecular class labels (e.g., from preceding class assignment step) and raw ion mobility arrival time measurements from TWIM-MS data, and you need to compute class-appropriate CCS values for downstream multi-omic analysis. Apply this skill when class-specific calibration relationships have been established or are available for your experimental classes.

## When NOT to use

- Features have not yet been assigned to experimental biomolecular classes (use class assignment skill first)
- Arrival time measurements are absent or incomplete in the input data
- Class-specific calibration models or parameters have not been established for the classes present in your data

## Inputs

- feature table with assigned biomolecular class labels
- raw ion mobility arrival time measurements
- class-specific calibration parameters or fitted models (linear or non-linear relationships per class)

## Outputs

- calibrated CCS values in structured table format indexed by feature identifier
- table with columns for feature ID, assigned class label, and computed CCS

## How to apply

Load the feature table containing assigned biomolecular class labels and raw arrival time measurements from the preceding class assignment step. Select the appropriate calibration model for each feature based on its assigned class label; MOCCal applies class-specific CCS calculation algorithms using the class label to retrieve fitted calibration parameters (linear or non-linear relationships fitted for that class). Convert each arrival time to CCS using the selected class-specific calibration model. Output the results in a structured table indexed by feature identifier, with columns for class label and computed CCS values. Verify that all features have been assigned a class and that calibration parameters exist for each class present in your data.

## Related tools

- **MOCCal** (Python application that implements class-specific CCS calculation; loads feature tables with class labels and arrival times, applies class-stratified calibration models, and outputs CCS tables) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Upstream tool for raw calibration file processing when using MOCCal RawDT; required dependency for raw data workflows) — http://github.com/pnnl/deimos

## Evaluation signals

- All features in the output table have a non-null class label and corresponding CCS value
- CCS values are numeric, fall within expected range for the assigned biomolecular class (e.g., no negative or implausibly large values)
- Output table structure matches specification: indexed by feature identifier with columns for class label and CCS
- Class labels in output match the set of classes present in the input feature table
- Conversion from arrival time to CCS is monotonic and consistent within each class (same arrival time should produce same CCS within a class)

## Limitations

- Requires that class-specific calibration models have been pre-computed or pre-fitted for each class; if calibration parameters are missing for a class, CCS calculation will fail for features assigned to that class
- TWIM platforms record arrival time (ion reaching detector) rather than drift time (ion time in cell); MOCCal documentation notes these terms are used interchangeably in the software for convenience but users should be aware of the distinction
- Features must have passed prior class assignment step; the skill cannot recover from misclassification in upstream steps

## Evidence

- [other] Load feature table with assigned biomolecular class labels and raw ion mobility arrival time measurements from preceding class assignment step.: "Load feature table with assigned biomolecular class labels and raw ion mobility arrival time measurements from preceding class assignment step."
- [other] Apply class-specific CCS calculation algorithm using the biomolecular class label to select appropriate calibration parameters for each feature.: "Apply class-specific CCS calculation algorithm using the biomolecular class label to select appropriate calibration parameters for each feature."
- [other] Convert arrival time to CCS using the class-specific calibration model (e.g., linear or non-linear relationship fitted for that class).: "Convert arrival time to CCS using the class-specific calibration model (e.g., linear or non-linear relationship fitted for that class)."
- [other] Output calibrated CCS values in a structured table indexed by feature identifier with columns for class label and computed CCS.: "Output calibrated CCS values in a structured table indexed by feature identifier with columns for class label and computed CCS."
- [intro] MOCCal performs experimental class-specific CCS calculations as a functional capability, applying class-appropriate methods to compute CCS values for assigned biomolecular features.: "MOCCal performs experimental class-specific CCS calculations as a functional capability, applying class-appropriate methods to compute CCS values for assigned biomolecular features."
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
