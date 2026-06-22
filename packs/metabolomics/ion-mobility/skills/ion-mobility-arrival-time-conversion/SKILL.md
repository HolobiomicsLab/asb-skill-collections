---
name: ion-mobility-arrival-time-conversion
description: Use when you have a feature table containing raw ion mobility arrival time measurements paired with experimentally assigned biomolecular class labels (e.g., lipid, protein, carbohydrate), and you need to compute CCS values for downstream structural or comparative analysis.
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

# ion-mobility-arrival-time-conversion

## Summary

Convert TWIM-MS ion arrival time measurements to calibrated collision cross section (CCS) values using class-specific calibration parameters. This skill is essential for quantifying biomolecular structural properties in high-dimensional multi-omic ion mobility workflows where class-appropriate calibration models must be applied to raw arrival time data.

## When to use

Apply this skill when you have a feature table containing raw ion mobility arrival time measurements paired with experimentally assigned biomolecular class labels (e.g., lipid, protein, carbohydrate), and you need to compute CCS values for downstream structural or comparative analysis. The skill is particularly valuable in MOCCal workflows where features have already been assigned to a biomolecular class but CCS quantification has not yet been performed.

## When NOT to use

- Features have not yet been assigned to a biomolecular class; use class assignment first.
- Raw arrival time data is unavailable or corrupted; CCS conversion requires valid arrival time input.
- Calibration parameters have not been established or validated for the represented biomolecular classes in your dataset.

## Inputs

- Feature table with raw ion mobility arrival time measurements
- Biomolecular class labels assigned to features
- Class-specific calibration parameters (linear or non-linear coefficients)

## Outputs

- Calibrated CCS value table indexed by feature identifier
- CCS values with associated class labels and feature identifiers

## How to apply

Load the feature table with raw arrival time measurements and corresponding class labels from the preceding class assignment step. Select the appropriate calibration model (linear or non-linear relationship) based on the biomolecular class label assigned to each feature. Apply the class-specific calibration parameters to convert each arrival time value to CCS using the fitted relationship for that class. Validate that all features have been assigned a class label and that the calibration model parameters exist for each represented class before conversion. Output the computed CCS values in a structured table indexed by feature identifier, with columns preserving the class label and computed CCS value.

## Related tools

- **MOCCal** (Python application that implements class-specific CCS calibration and conversion from arrival time to CCS values for TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Required dependency for MOCCal RawDT module when processing raw calibration files prior to arrival time conversion) — http://github.com/pnnl/deimos

## Evaluation signals

- All features in the input table have a class label and a corresponding CCS output value; no missing or null CCS entries.
- CCS values are physically reasonable for the assigned biomolecular class (e.g., within expected ranges for lipids vs. proteins).
- The output table schema matches the specified structure: indexed by feature identifier with columns for class label and computed CCS.
- Class label values in the output match the input class assignments; no reassignment or reordering has occurred.
- Calibration model choice (linear vs. non-linear) was applied consistently within each class; verify by inspecting residuals or fit statistics if available.

## Limitations

- Requires that biomolecular class assignment has been completed prior to arrival time conversion; cannot infer classes de novo from arrival time alone.
- Calibration parameters must be established and validated for each biomolecular class represented in the input; missing calibration for any class will cause conversion to fail or produce invalid CCS values.
- TWIM platforms record arrival time (time to detector) rather than drift time (residence time in the ion mobility cell); the conversion must use arrival time, not drift time, to produce accurate CCS values.
- No changelog is available for MOCCal, limiting ability to assess improvements or bug fixes in calibration methodology across versions.

## Evidence

- [other] Apply class-specific CCS calculation algorithm using the biomolecular class label to select appropriate calibration parameters for each feature.: "Apply class-specific CCS calculation algorithm using the biomolecular class label to select appropriate calibration parameters for each feature."
- [other] Convert arrival time to CCS using the class-specific calibration model (e.g., linear or non-linear relationship fitted for that class).: "Convert arrival time to CCS using the class-specific calibration model (e.g., linear or non-linear relationship fitted for that class)."
- [other] Output calibrated CCS values in a structured table indexed by feature identifier with columns for class label and computed CCS.: "Output calibrated CCS values in a structured table indexed by feature identifier with columns for class label and computed CCS."
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [other] MOCCal performs experimental class-specific CCS calculations as a functional capability, applying class-appropriate methods to compute CCS values for assigned biomolecular features.: "MOCCal performs experimental class-specific CCS calculations as a functional capability, applying class-appropriate methods to compute CCS values for assigned biomolecular features."
