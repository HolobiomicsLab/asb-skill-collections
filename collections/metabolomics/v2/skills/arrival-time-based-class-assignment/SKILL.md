---
name: arrival-time-based-class-assignment
description: Use when you have raw or processed TWIM-MS data with arrival time and m/z dimensions, and you need to label each experimental feature by biomolecular class before feature identification or peak detection steps are complete.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
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
- Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations
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

# arrival-time-based-class-assignment

## Summary

Assign biomolecular class labels (lipid, peptide, carbohydrate, etc.) to experimental features directly from TWIM-MS arrival time and m/z data without requiring prior feature identification. This enables immediate class-specific CCS calculations on raw multi-omic ion mobility data.

## When to use

You have raw or processed TWIM-MS data with arrival time and m/z dimensions, and you need to label each experimental feature by biomolecular class before feature identification or peak detection steps are complete. Use this when you want to bypass traditional feature detection workflows and assign class labels directly to the high-dimensional data for downstream class-specific CCS calibration.

## When NOT to use

- Input data has already been pre-processed with identified feature peaks; use class assignment on raw data to avoid redundant labeling.
- Your workflow requires drift time (time spent in the TWIM cell) rather than arrival time; MOCCal records and uses arrival time (detector arrival) by design.
- You need to assign classes to features from mass spectrometry platforms other than TWIM; this skill is specific to traveling-wave ion mobility data with arrival time information.

## Inputs

- Raw or processed TWIM-MS data with arrival time and m/z dimensions
- Multi-omic experimental ion mobility dataset

## Outputs

- Class-labeled feature table (structured output file)
- Biomolecular class assignments per experimental feature
- Class-specific CCS calculations

## How to apply

Load your TWIM-MS data (containing arrival time and m/z dimensions) into MOCCal. Apply MOCCal's biomolecular class assignment algorithm to label each experimental feature by class directly from the high-dimensional data without pre-identifying feature peaks. The algorithm operates on arrival time (the time at which ions reach the detector, not drift time within the TWIM cell) and m/z to infer biomolecular class. Once class labels are assigned, MOCCal generates class-specific CCS calculations. Output the class-labeled feature table as a structured file for downstream analysis or validation.

## Related tools

- **MOCCal** (Implements biomolecular class assignment and class-specific CCS calculations on TWIM-MS data without prior feature identification) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Optional preprocessing dependency for raw calibration data files (version 1.3.2 required for RawDT workflow)) — https://github.com/pnnl/deimos

## Examples

```
python MOCCal_UserDT.py --input experimental_data.csv --output class_labeled_features.csv
```

## Evaluation signals

- Class-labeled feature table is generated with all experimental features assigned to one of the biomolecular classes (lipid, peptide, carbohydrate, or other)
- Output file structure matches expected format with arrival time, m/z, and class label columns
- Class-specific CCS values are computed and vary appropriately by assigned biomolecular class
- No features are dropped or marked invalid during class assignment; all input features receive a class label
- Comparison of class assignment consistency: re-running on the same data yields identical class labels for the same features

## Limitations

- MOCCal uses arrival time (detector arrival) rather than drift time (time in TWIM cell); users must understand this distinction to correctly interpret CCS values
- No changelog is available for version tracking or historical reproducibility
- The skill requires either a Python environment with MOCCal installed or use of the pre-built executable (which requires an Output folder in the same directory)
- Raw data workflow (RawDT) depends on external DEIMoS version 1.3.2 availability and compatibility

## Evidence

- [other] MOCCal implements biomolecular class assignment functionality that operates on experimental TWIM-MS data to label features by class, and performs class-specific CCS calculations, without requiring features to be identified first.: "biomolecular class assignment algorithm to label each experimental feature by class (e.g., lipid, peptide, carbohydrate, or other) directly from the high-dimensional data without requiring"
- [intro] MOCCal offers class assignment and CCS calculations without need for identifying the features first.: "MOCCal offers class assignment and CCS calculations without need for identifying the features first"
- [intro] TWIM platforms record arrival time (when ion reaches detector) rather than drift time (time spent in TWIM cell).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)"
- [readme] MOCCal functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations.: "Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations"
- [other] Workflow steps for arrival-time-based-class-assignment include loading raw TWIM-MS data and applying MOCCal's biomolecular class assignment algorithm.: "Load raw TWIM-MS data (arrival time and m/z dimensions) into MOCCal. Apply MOCCal's biomolecular class assignment algorithm to label each experimental feature by class"
