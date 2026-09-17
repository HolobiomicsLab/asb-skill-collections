---
name: ccs-value-assignment-from-standards
description: Use when you have TWIM-MS experimental data with arrival/drift times
  and m/z values, and you possess calibrant reference standards with known CCS values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
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
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CCS value assignment from standards

## Summary

Assign collision cross section (CCS) values to ions in TWIM-MS data by loading known calibrant reference standards and establishing a calibration curve that maps drift time to CCS across the m/z range. This enables accurate CCS determination without requiring prior feature identification.

## When to use

You have TWIM-MS experimental data with arrival/drift times and m/z values, and you possess calibrant reference standards with known CCS values. Use this skill to convert raw ion arrival times into calibrated CCS values that can then be used for biomolecular identification and comparison across experiments.

## When NOT to use

- You lack reference calibrant standards with known CCS values — calibration cannot proceed without ground truth
- Your input is already a processed CCS table (e.g., from a prior calibration run) rather than raw arrival time data
- You are using ion mobility techniques other than TWIM (e.g., drift tube IMS or trapped IMS) where the arrival time–drift time relationship differs

## Inputs

- TWIM-MS experimental data file with arrival times and m/z values
- Calibrant reference standards with known CCS values (calibration template)
- Instrument-specific time-of-flight offset parameter

## Outputs

- Calibrated CCS table with m/z values, charge states, and quality metrics
- Calibration curve model (linear or polynomial regression function)
- Calibrated CCS values for all experimental ions

## How to apply

Load your TWIM-MS experimental data (arrival times and m/z values) using MOCCal's data import module. Separately load calibrant reference standards with known CCS values from a calibration template. Convert arrival times to drift times by accounting for the instrument-specific time-of-flight offset. Apply linear or polynomial regression to establish a calibration curve mapping drift time to CCS across the m/z range. Apply the resulting calibration function to your experimental arrival times to generate calibrated CCS values for all ions. Export the calibrated CCS table with associated m/z, charge state, and quality metrics for downstream analysis.

## Related tools

- **MOCCal** (Implements CCS calibration via linear/polynomial regression; imports TWIM-MS data and calibrant templates; exports calibrated CCS tables with quality metrics) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Required dependency for RawDT version of MOCCal when processing raw calibration files instead of pre-processed data) — http://github.com/pnnl/deimos

## Examples

```
python MOCCal_UserDT.py --input experimental_data.csv --calibrants calibration_template.csv --method polynomial --output calibrated_CCS.csv
```

## Evaluation signals

- Calibration curve shows monotonic drift time–CCS relationship with R² > 0.95 across the m/z range
- Calibrated CCS values for calibrant standards match their reference values within ±2% (instrument/method dependent)
- Exported CCS table contains valid m/z, charge state, and quality metric columns with no missing values for ions above a quality threshold
- Residual distribution from calibration regression is approximately normal and centered near zero across all m/z bins
- Calibrated CCS values for experimental ions fall within biologically plausible ranges for their inferred biomolecular class

## Limitations

- TWIM platforms record arrival time (time to detector) not drift time (time in TWIM cell); MOCCal terms these interchangeably for convenience but requires offset correction specific to instrument platform
- Calibration accuracy depends critically on quality and diversity of reference standards across the m/z range of interest
- Linear calibration may introduce systematic bias at extremes of m/z or CCS ranges; polynomial regression should be evaluated for better fit
- No changelog available in repository to track breaking changes or validation improvements across versions

## Evidence

- [other] MOCCal implements CCS calibration as a core functionality for high-dimensional, multi-omic TWIM-MS data analysis: "MOCCal implements CCS calibration as a core functionality for high-dimensional, multi-omic TWIM-MS data analysis, with supporting python scripts, data templates, and example data provided in UserDT"
- [other] Calibrant reference standards with known CCS values are loaded and used to establish calibration curve: "Load calibrant reference standards with known CCS values from the calibration template. Apply linear or polynomial regression to establish a calibration curve mapping drift time to CCS"
- [other] Arrival times are converted to drift times via instrument-specific offset: "Convert arrival times to drift times by accounting for the time-of-flight offset specific to the instrument platform."
- [intro] MOCCal enables CCS assignment without requiring prior feature identification: "MOCCal offers class assignment and CCS calculations without need for identifying the features first."
- [readme] TWIM platforms record arrival time rather than drift time: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
