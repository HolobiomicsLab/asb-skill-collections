---
name: multi-charge-state-ccs-handling
description: Use when your TWIM-MS dataset contains ions with multiple charge states
  (e.g., +1, +2, +3 for the same molecular species) and you need CCS values that correctly
  account for the relationship between drift time, m/z, and charge state.
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

# multi-charge-state-ccs-handling

## Summary

Calibrate collision cross section (CCS) values for ions across multiple charge states in TWIM-MS data by establishing separate or unified calibration curves and applying charge-state-aware regression. This skill enables accurate CCS assignment for complex biomolecular mixtures where ions exist in multiple protonation or ionization states.

## When to use

Your TWIM-MS dataset contains ions with multiple charge states (e.g., +1, +2, +3 for the same molecular species) and you need CCS values that correctly account for the relationship between drift time, m/z, and charge state. Use this skill when calibrant reference standards are available at multiple charge states, or when your experimental data spans a wide m/z range where charge heterogeneity is expected.

## When NOT to use

- Your calibration data or experimental ions are restricted to a single charge state; simpler single-charge calibration workflows are more appropriate.
- You lack reference standards at multiple charge states and cannot validate charge-dependent CCS behavior.
- Your input data are already calibrated CCS values or feature tables; re-calibration would be redundant.

## Inputs

- TWIM-MS raw arrival times (list or array)
- Ion m/z values (list or array)
- Ion charge states (list or array)
- Calibrant reference standards with known CCS values and their charge states
- Instrument-specific time-of-flight offset parameter

## Outputs

- Calibrated CCS values (numeric array, one per ion)
- Calibration curve coefficients (linear or polynomial, per charge state or unified)
- Quality metrics (residuals, R² values, prediction confidence per charge state)
- CCS table with m/z, charge state, and associated CCS and quality annotations

## How to apply

Load TWIM-MS experimental data (arrival times and m/z values) alongside calibrant reference standards with known CCS values at each charge state. Convert arrival times to drift times accounting for time-of-flight offset. Stratify calibration data by charge state (or apply polynomial regression that captures charge-dependent drift-time–CCS relationships across the m/z range). Apply the charge-aware calibration function to map each experimental ion's drift time and m/z to its calibrated CCS, preserving charge state metadata. Export the calibrated CCS table with m/z, charge state, and quality metrics (e.g., residuals from the calibration curve) to enable downstream validation.

## Related tools

- **MOCCal** (Python application for CCS calibration and charge-aware class assignment from TWIM-MS data; executes linear or polynomial regression per charge state and exports calibrated CCS tables) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (PNNL ion mobility processing toolkit; used by MOCCal (RawDT workflow) for raw calibration file handling and drift-time feature extraction before charge-state stratification) — http://github.com/pnnl/deimos

## Evaluation signals

- Calibration curve R² values are ≥0.95 within each charge state stratum; residuals are randomly distributed around zero with magnitude consistent across the m/z range.
- CCS values for the same molecule at different charge states show expected relationships (e.g., CCS increases slightly with charge state due to Coulomb repulsion); literature or external database validation confirms biological plausibility.
- Exported CCS table contains no missing or null charge-state entries; each ion has a paired m/z, charge state, CCS, and quality metric.
- Charge-state-specific calibration curves (if generated separately) show overlapping or smoothly transitional relationships; unified polynomial curves have appropriate degree (typically 2–3) without overfitting.
- Comparison of calibrated CCS against known standards (orthogonal method or literature values) yields average absolute error <2–3% across all charge states.

## Limitations

- MOCCal terminology uses 'arrival time' and 'drift time' interchangeably for convenience, but TWIM platforms record arrival time (time to detector) not drift time (time in TWIM cell); users must correctly convert arrival time to true drift time using the instrument-specific offset to avoid systematic bias in CCS values.
- Charge-state-specific calibration requires sufficient calibrant coverage at each charge state; sparse or missing charge states may degrade curve fitting and prediction confidence.
- Linear calibration curves may not capture non-linear drift-time–CCS relationships across very wide m/z or charge-state ranges; polynomial or machine-learning alternatives may be needed.
- No changelog provided; version reproducibility and backward compatibility with older data formats are not documented.

## Evidence

- [readme] Charge-state handling in calibration: "Apply linear or polynomial regression to establish a calibration curve mapping drift time to CCS across the m/z range"
- [readme] Arrival vs. drift time distinction: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)"
- [other] Export of charge-state-associated CCS: "Export the calibrated CCS table with associated m/z, charge state, and quality metrics"
- [intro] Class-specific CCS calculations: "MOCCal enables biomolecular class assignment and class-specific CCS calculations without requiring prior feature identification"
- [readme] Multi-omic multi-charge capability: "MOCCal, or Multi-Omic CCS Calibrator, is a Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data analysis"
