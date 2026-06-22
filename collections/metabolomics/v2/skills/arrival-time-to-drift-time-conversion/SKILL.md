---
name: arrival-time-to-drift-time-conversion
description: Use when when processing raw TWIM-MS experimental data that contains arrival time measurements but you need drift times for CCS calibration or class-specific CCS calculations.
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

# arrival-time-to-drift-time-conversion

## Summary

Convert TWIM-MS arrival times (detector arrival) to drift times (time spent in ion mobility cell) by subtracting the instrument-specific time-of-flight offset. This conversion is a prerequisite for accurate collision cross section (CCS) calibration in multi-omic ion mobility mass spectrometry workflows.

## When to use

When processing raw TWIM-MS experimental data that contains arrival time measurements but you need drift times for CCS calibration or class-specific CCS calculations. TWIM instruments record arrival time (when the ion reaches the detector) rather than drift time (time spent within the TWIM cell), making this conversion essential before applying calibration curves.

## When NOT to use

- Drift times are already provided in the raw data — verify the time origin (detector vs. cell entry) before applying conversion
- Working with non-TWIM ion mobility platforms (e.g., DTIMS, TWIMS with different architectures) that may use different time definitions
- The TOF offset is unknown and cannot be reliably estimated from calibration standards

## Inputs

- TWIM-MS experimental data with arrival time measurements (typically in milliseconds)
- Ion m/z values and charge state assignments
- Time-of-flight (TOF) offset specific to the instrument platform (in milliseconds)

## Outputs

- Drift time values for each ion (time spent in TWIM cell, in milliseconds)
- Converted data table with m/z, charge state, and drift time columns ready for CCS calibration

## How to apply

Load the TWIM-MS experimental data containing arrival times and the instrument platform's time-of-flight (TOF) offset parameter. For each ion measurement, subtract the TOF offset from the recorded arrival time to obtain the drift time. The TOF offset is instrument-specific and should be established during instrument characterization or provided in the experimental metadata. This converted drift time is then used as input to the CCS calibration function (linear or polynomial regression against reference standards with known CCS values). Verify the conversion by checking that drift times are positive, physically reasonable (typically milliseconds for small molecules, seconds for proteins), and show appropriate clustering by charge state and m/z.

## Related tools

- **MOCCal** (Python application that implements arrival-time-to-drift-time conversion as part of its CCS calibration workflow for TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (PNNL ion mobility data processing library used upstream in MOCCal's RawDT workflow for handling raw calibration files and time offset calculations) — http://github.com/pnnl/deimos

## Evaluation signals

- Converted drift times are positive and within expected range for the biomolecule class (e.g., 10–100 ms for small molecules, 100–500 ms for peptides, > 1 s for proteins)
- Drift times scale appropriately with charge state (higher charge → shorter drift time for same m/z) and m/z (higher m/z → longer drift time for same charge)
- Post-conversion CCS calibration produces a monotonic or smooth calibration curve (linear or polynomial fit) with residual errors consistent with instrument precision
- Drift times derived from the same ion source and instrument show consistent clustering across replicate measurements
- The TOF offset applied is consistent across all ions in the dataset (no per-ion variation unless explicitly specified in metadata)

## Limitations

- The TOF offset must be accurately determined for the specific instrument platform; uncertainty in the offset directly propagates to drift time error and subsequent CCS calibration error
- Arrival time vs. drift time terminology is used interchangeably in MOCCal 'for convenience', which may cause confusion; users must verify their instrument's actual time definition
- The conversion assumes a single, constant TOF offset; heterogeneous instrument configurations (e.g., multiple detector types or field geometries) may require per-ion or per-region offsets
- No built-in validation or quality control to detect when TOF offset is incorrect or when arrival times are corrupted; downstream CCS calibration failure may be the first sign of error

## Evidence

- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time): "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)"
- [other] Convert arrival times to drift times by accounting for the time-of-flight offset specific to the instrument platform: "Convert arrival times to drift times by accounting for the time-of-flight offset specific to the instrument platform"
- [other] For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset: "For each class stratum, extract arrival time measurements and convert to drift time by subtracting the time-of-flight offset"
- [readme] The terms arrival time and drift time are used interchangeably within the software for convenience: "The terms arrival time and drift time are used interchangeably within the software for convenience"
