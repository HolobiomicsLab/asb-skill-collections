---
name: collision-cross-section-calculation
description: Use when you have raw or processed arrival-time data from a traveling-wave
  ion mobility mass spectrometry (TWIM-MS) platform and need to convert it into standardized
  collision cross section (CCS) values for comparative analysis across samples or
  datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - HinesLab/MOCCal
  - MOCCal
  - DEIMoS
  - MOCCal (Multi-Omic CCS Calibrator)
  - DEIMoS (Data-Exploratory Ion Mobility MS)
  techniques:
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
- HinesLab/MOCCal
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_autoccs_cq
    doi: 10.1093/bioinformatics/btab429
    title: AutoCCS
  - build: coll_moccal
    doi: 10.1021/acs.analchem.3c04290
    title: moccal
  - build: coll_moccal_cq
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

# collision-cross-section-calculation

## Summary

Transform raw TWIM-MS arrival-time measurements into calibrated collision cross section (CCS) values using reference compound calibration curves. This skill enables quantitative ion-mobility characterization for high-dimensional multi-omic datasets without requiring prior feature identification.

## When to use

You have raw or processed arrival-time data from a traveling-wave ion mobility mass spectrometry (TWIM-MS) platform and need to convert it into standardized collision cross section (CCS) values for comparative analysis across samples or datasets. This is the required first step before biomolecular class assignment or cross-dataset CCS comparisons in the MOCCal workflow.

## When NOT to use

- Arrival-time data is already pre-calibrated or CCS values are already available in the input file.
- No validated calibration standard compounds or reference CCS values are available for the instrument platform.
- The TWIM platform records drift time (time spent in the TWIM cell) rather than arrival time; nomenclature must be verified first as MOCCal internally treats them interchangeably but they represent different physical quantities.

## Inputs

- raw arrival-time measurements (TWIM-MS data matrix with ion identifiers and arrival times)
- calibration template file (reference compounds with known CCS values)
- optional: processed TWIM-MS dataset (UserDT format) if raw calibration data preprocessing is not required

## Outputs

- calibrated CCS table (matrix with ion identifiers and corresponding CCS values in Ų)
- calibration curve coefficients or mapping function
- calibration residual metrics (error on reference compounds)

## How to apply

Load raw arrival-time measurements and a calibration template containing reference compounds with known CCS values. Parse the reference compound identities and their literature CCS values from the template file. Establish a mathematical mapping function (typically polynomial or linear) between arrival time and CCS using calibration reference points as anchors. Apply this arrival-time-to-CCS transformation to all experimental ion features in the dataset. Validate that the output CCS values fall within expected ranges for the biomolecular classes present (e.g., lipids typically 200–500 Ų, proteins 1000–5000 Ų) and that the calibration residuals are acceptably small (typically < 2–5% error on reference compounds).

## Related tools

- **MOCCal** (Python application that implements CCS calibration, biomolecular class assignment, and class-specific CCS calculations as an integrated workflow for TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Dependency required only for raw calibration file processing (RawDT version); preprocesses raw TWIM data before MOCCal calibration) — http://github.com/pnnl/deimos

## Evaluation signals

- Calibration reference compounds achieve < 2–5% CCS error (difference between observed and literature CCS values) when the mapping function is applied to them.
- The output CCS table contains no null values for ions that passed quality filtering; all feature rows map to a valid CCS value.
- CCS values fall within plausible ranges for the detected biomolecular classes (e.g., small metabolites 100–300 Ų, lipids 200–600 Ų, proteins 1000–5000 Ų).
- The calibration curve is monotonic (arrival time increases with CCS) with a reasonable R² fit (typically > 0.95) to reference points.
- Output CCS table schema matches expected structure: at minimum, ion identifier columns and a CCS column with units (Ų) clearly labeled.

## Limitations

- Accuracy depends critically on the quality and representativeness of calibration reference compounds; if references are not chemically similar to experimental analytes, systematic bias may occur.
- TWIM platforms measure arrival time (time to detector) not drift time (time in TWIM cell); MOCCal uses these terms interchangeably for convenience but users must ensure consistency with their instrument's actual output.
- No changelog is publicly available for version tracking or reproducibility assurance.
- The UserDT (processed calibration data) pathway does not require Python or dependency installation, but the RawDT pathway requires external installation of DEIMoS version 1.3.2, which may introduce version-compatibility issues.

## Evidence

- [other] MOCCal implements CCS calibration as a core functionality that transforms TWIM-MS arrival-time data into collision cross section values: "MOCCal implements CCS calibration as a core functionality that transforms TWIM-MS arrival-time data into collision cross section values for multi-omic high-dimensional analysis."
- [other] Establish arrival-time-to-CCS mapping function using calibration reference points and apply it to experimental values: "3. Establish arrival-time-to-CCS mapping function using calibration reference points. 4. Apply calibration transform to experimental arrival-time values to produce calibrated CCS values."
- [readme] TWIM platforms record arrival time rather than drift time: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [readme] MOCCal is a Python application designed to perform collision cross section calibration on high-dimensional multi-omic TWIM-MS data: "MOCCal, or Multi-Omic CCS Calibrator, is a Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data anlaysis. Functionality includes collision"
- [other] Parse calibration reference compounds and their known CCS values from the template: "2. Parse calibration reference compounds and their known CCS values from the template. 3. Establish arrival-time-to-CCS mapping function using calibration reference points."
