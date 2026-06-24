---
name: twim-ms-calibration-mapping
description: Use when you have raw or processed arrival-time data from a TWIM-MS instrument
  and need to convert it to CCS values for comparison across experiments or biomolecular
  classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# TWIM-MS CCS Calibration Mapping

## Summary

Transform raw arrival-time measurements from traveling-wave ion mobility mass spectrometry (TWIM-MS) into collision cross section (CCS) values by establishing and applying a calibration mapping function derived from reference compounds with known CCS values. This skill enables downstream multi-omic analysis without prior feature identification.

## When to use

You have raw or processed arrival-time data from a TWIM-MS instrument and need to convert it to CCS values for comparison across experiments or biomolecular classes. Use this skill when you possess a set of calibration reference compounds with known or literature CCS values and want to establish a quantitative mapping between your instrument's arrival-time measurements and standardized CCS units.

## When NOT to use

- Your input data is already in calibrated CCS units—mapping is redundant and will introduce error.
- You lack calibration reference compounds with known or reliable CCS values; the mapping function cannot be established without anchor points.
- Your arrival-time measurements are drift time (time spent within the TWIM cell) rather than arrival time (time to detector); MOCCal and this workflow are specific to arrival-time-based TWIM platforms.

## Inputs

- Raw or processed arrival-time data from TWIM-MS instrument (numeric table with ion identifiers and arrival-time values)
- Calibration template file (reference compounds with known CCS values)
- Instrument calibration reference compounds list

## Outputs

- Calibrated CCS value table (ion identifiers with corresponding CCS values)
- Arrival-time-to-CCS mapping function parameters

## How to apply

Load your raw arrival-time data and a calibration template containing reference compounds and their known CCS values (e.g., from MOCCal repository example files). Parse the calibration reference compounds to identify the arrival-time-to-CCS mapping points. Establish a calibration transform function using these reference points—typically a linear or polynomial relationship between arrival time and CCS. Apply this transform to your experimental arrival-time values to produce calibrated CCS values. Output a calibrated CCS table paired with ion identifiers. The mapping function should be validated by checking that reference compound CCS values reproduce within instrument tolerance after transformation.

## Related tools

- **MOCCal** (Python application that implements CCS calibration for TWIM-MS arrival-time data and provides UserDT (processed data) and RawDT (raw calibration file) workflows) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Required for RawDT workflow to preprocess raw calibration files before CCS mapping in MOCCal) — http://github.com/pnnl/deimos

## Evaluation signals

- Calibration reference compounds' measured arrival times map back to their known CCS values with residuals below instrument detection threshold.
- Output CCS table contains no null or negative values; all ion identifiers are paired with corresponding CCS values.
- CCS values for biological samples fall within expected ranges for their biomolecular classes (e.g., peptides, lipids, carbohydrates).
- Arrival-time-to-CCS mapping function is monotonic and physically plausible (CCS increases or remains constant as arrival time increases).
- Calibrated CCS values are comparable across independent instrument runs or different sample plates when using the same calibration reference set.

## Limitations

- MOCCal does not provide a changelog, limiting reproducibility tracking and change documentation for different versions.
- The mapping function's accuracy depends critically on the quality and representativeness of calibration reference compounds; poor reference selection will propagate errors through all experimental CCS values.
- RawDT workflow requires DEIMoS version 1.3.2, introducing a dependency on external software and its specific version; UserDT workflow avoids this but requires pre-processed calibration data.
- Arrival time and drift time are used interchangeably in MOCCal documentation for convenience, but the underlying physics differs; users must ensure their instrument records arrival time, not drift time within the TWIM cell.

## Evidence

- [other] MOCCal implements CCS calibration as a core functionality that transforms TWIM-MS arrival-time data into collision cross section values: "MOCCal implements CCS calibration as a core functionality that transforms TWIM-MS arrival-time data into collision cross section values for multi-omic high-dimensional analysis."
- [other] Establish arrival-time-to-CCS mapping function using calibration reference points and apply calibration transform to experimental arrival-time values: "Establish arrival-time-to-CCS mapping function using calibration reference points. 4. Apply calibration transform to experimental arrival-time values to produce calibrated CCS values."
- [intro] MOCCal offers class assignment and CCS calculations without need for identifying the features first: "MOCCal offers class assignment and CCS calculations without need for identifying the features first."
- [intro] TWIM platforms record arrival time (when the ion reaches the detector) rather than drift time (time an ion spends within the TWIM cell): "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [readme] For processed calibration data, use MOCCal executable with processed data templates; for raw calibration files, install pnnl's DEIMoS version 1.3.2: "If you plan to use raw calibration files, you will need to install pnnl's DEIMoS, version 1.3.2"
