---
name: twim-instrument-offset-correction
description: Use when you have raw TWIM-MS data with arrival times (detector timestamps) rather than drift times, and you need to calibrate collision cross section values. TWIM platforms inherently record arrival time, not drift time, so this correction must precede CCS calibration workflows.
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
---

# TWIM instrument offset correction

## Summary

Convert arrival times (detector arrival) recorded by TWIM-MS platforms into drift times (time spent in the mobility cell) by applying an instrument-specific time-of-flight offset, a prerequisite for accurate collision cross section (CCS) calibration.

## When to use

You have raw TWIM-MS data with arrival times (detector timestamps) rather than drift times, and you need to calibrate collision cross section values. TWIM platforms inherently record arrival time, not drift time, so this correction must precede CCS calibration workflows. Apply this when you are preparing experimental data for the MOCCal calibration pipeline.

## When NOT to use

- Your data already contains measured drift times rather than arrival times (no correction needed).
- You are using a non-TWIM ion mobility platform (e.g., DTIMS or TIMS) with different timing conventions.
- You lack knowledge of or access to your instrument's time-of-flight offset; contact your instrument vendor or calibration reference.

## Inputs

- TWIM-MS raw experimental data (arrival times and m/z values)
- Instrument-specific time-of-flight offset value (numeric, milliseconds or microseconds)

## Outputs

- Corrected drift times aligned to TWIM cell transit
- TOF-corrected experimental dataset ready for CCS calibration

## How to apply

Load the TWIM-MS experimental data containing arrival times and m/z values using the MOCCal data import module. Identify or measure the time-of-flight (TOF) offset specific to your instrument platform—this offset represents the dead time between ion generation/acceleration and entry into the TWIM cell. Subtract this offset from all recorded arrival times to recover the true drift time (time spent in the mobility cell). The corrected drift times are then used as input to the linear or polynomial regression step that establishes the calibration curve mapping drift time to CCS. Validate that corrected drift times are physically reasonable (positive, within the TWIM cell transit time range for your platform).

## Related tools

- **MOCCal** (Python application that implements CCS calibration; uses corrected drift times as input to regression-based calibration curve construction) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Optional dependency for raw data preprocessing; required for RawDT workflow variant) — http://github.com/pnnl/deimos

## Evaluation signals

- Corrected drift times are all positive and fall within the expected TWIM cell transit time range for your instrument (e.g., 0–100 ms).
- Drift time ordering is preserved: ions with the same m/z and charge state show consistent drift times across replicates.
- Downstream CCS calibration produces a smooth, monotonic regression curve (linear or polynomial) with high R² and low residuals.
- Known calibrant standards (with reference CCS values) yield CCS estimates within literature or vendor specification after calibration.
- No systematic bias or shift in the m/z-dependent CCS residuals post-calibration (homoscedastic scatter around the fitted curve).

## Limitations

- Time-of-flight offset is instrument-specific and platform-dependent; it must be known or measured empirically. Incorrect offset values will propagate into all downstream CCS values.
- The README and workflow do not provide explicit methods for determining or validating the TOF offset; users are expected to obtain this from instrument documentation or prior calibration data.
- No changelog is provided in the repository, limiting visibility into how offset correction may have been refined across software versions.

## Evidence

- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)"
- [other] Convert arrival times to drift times by accounting for the time-of-flight offset specific to the instrument platform.: "Convert arrival times to drift times by accounting for the time-of-flight offset specific to the instrument platform"
- [other] Load TWIM-MS experimental data (arrival times and m/z values) using the MOCCal data import module.: "Load TWIM-MS experimental data (arrival times and m/z values) using the MOCCal data import module"
- [other] Apply linear or polynomial regression to establish a calibration curve mapping drift time to CCS across the m/z range.: "Apply linear or polynomial regression to establish a calibration curve mapping drift time to CCS across the m/z range"
- [readme] For python scripts, usage tutorials, data templates, and example data, please see the UserDT or RawDT folders.: "For python scripts, usage tutorials, data templates, and example data, please see the UserDT or RawDT folders"
