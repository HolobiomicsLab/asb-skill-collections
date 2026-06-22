---
name: biomolecular-class-ccs-mapping
description: Use when after biomolecular class labels have been assigned to features in a TWIM-MS dataset and you have raw ion mobility arrival time measurements. Use it when you need to convert arrival times to standardized CCS values where calibration accuracy depends critically on the biomolecular class (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - MOCCal
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

# biomolecular-class-ccs-mapping

## Summary

Compute class-specific collision cross section (CCS) values for ion mobility features by applying biomolecule-class-appropriate calibration models to arrival time measurements. This skill enables conversion of raw TWIM-MS arrival times to calibrated CCS using class-dependent linear or non-linear regression models fitted during the calibration phase.

## When to use

Apply this skill after biomolecular class labels have been assigned to features in a TWIM-MS dataset and you have raw ion mobility arrival time measurements. Use it when you need to convert arrival times to standardized CCS values where calibration accuracy depends critically on the biomolecular class (e.g., lipids, proteins, carbohydrates may require different calibration models). Do not use if features lack explicit class labels or if CCS calibration is class-agnostic.

## When NOT to use

- Input feature table already contains pre-computed CCS values or does not require recalibration.
- Biomolecular class labels have not yet been assigned to features; class assignment must precede this skill.
- Raw arrival time measurements are unavailable or corrupted; arrival time is a mandatory input.

## Inputs

- Feature table with assigned biomolecular class labels (e.g., lipid, protein, carbohydrate)
- Raw ion mobility arrival time measurements (TWIM-MS detector readings)
- Class-specific calibration model parameters (regression coefficients fitted per class)

## Outputs

- Calibrated CCS values table (indexed by feature identifier with class label and computed CCS columns)
- Feature table with appended CCS values and class labels

## How to apply

Load the feature table containing assigned biomolecular class labels and raw ion mobility arrival time measurements from the preceding class assignment workflow step. For each feature, retrieve the class-specific calibration model parameters (e.g., slope, intercept, or non-linear coefficients) that were fitted for that biomolecular class during calibration. Apply the class-specific CCS calculation algorithm by substituting the feature's arrival time into the calibration equation selected for its assigned class. Output the computed CCS values in a structured table indexed by feature identifier with columns for class label and resulting CCS. Validate that all features received a CCS output and that values fall within physically plausible ranges for the assigned class.

## Related tools

- **MOCCal** (Implements class-specific CCS calculation as a functional module within the multi-omic TWIM-MS data analysis workflow; selects and applies class-appropriate calibration parameters to convert arrival times to CCS values.) — https://github.com/HinesLab/MOCCal

## Evaluation signals

- All features in the input table receive a CCS output value; no null or missing CCS entries for assigned features.
- CCS values are physically plausible and consistent with expected ranges for the assigned biomolecular class (e.g., lipids typically lower CCS than intact proteins).
- Class label is correctly propagated to the output table for every feature; no class assignment mismatches.
- Arrival time to CCS conversion is monotonic and follows the fitted class-specific calibration model (e.g., linear or non-linear relationship is preserved).
- Output table schema includes columns for feature identifier, class label, arrival time, and computed CCS in a structured, indexable format.

## Limitations

- Accuracy of CCS values depends on the quality and completeness of the class-specific calibration models; poorly fitted models for a given class will propagate calibration error to all features assigned to that class.
- TWIM platforms record arrival time (time to detector) rather than drift time (time in cell); the software treats these interchangeably for convenience, but this distinction affects the physical interpretation of CCS values.
- Requires prior biomolecular class assignment; features without valid class labels cannot be processed by this skill and will be excluded or cause errors.
- Class-specific calibration models must be pre-fitted or available in the workflow context; the skill does not perform model training itself.

## Evidence

- [other] Apply class-specific CCS calculation algorithm using the biomolecular class label to select appropriate calibration parameters for each feature.: "Apply class-specific CCS calculation algorithm using the biomolecular class label to select appropriate calibration parameters for each feature."
- [other] Convert arrival time to CCS using the class-specific calibration model (e.g., linear or non-linear relationship fitted for that class).: "Convert arrival time to CCS using the class-specific calibration model (e.g., linear or non-linear relationship fitted for that class)."
- [intro] MOCCal performs experimental class-specific CCS calculations as a functional capability, applying class-appropriate methods to compute CCS values for assigned biomolecular features.: "MOCCal performs experimental class-specific CCS calculations as a functional capability, applying class-appropriate methods to compute CCS values for assigned biomolecular features."
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [other] Output calibrated CCS values in a structured table indexed by feature identifier with columns for class label and computed CCS.: "Output calibrated CCS values in a structured table indexed by feature identifier with columns for class label and computed CCS."
