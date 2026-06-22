---
name: biomolecular-class-annotation
description: Use when you have raw or processed TWIM-MS data with arrival time and m/z dimensions, and you need to label experimental features by biomolecular class before performing CCS calibration or validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
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

# biomolecular-class-annotation

## Summary

Assign biomolecular class labels (lipid, peptide, carbohydrate, etc.) directly to experimental features in TWIM-MS data without prior feature identification, enabling downstream class-specific CCS calculations. This skill bypasses the need for peak picking or feature deconvolution by operating on high-dimensional arrival time and m/z dimensions.

## When to use

You have raw or processed TWIM-MS data with arrival time and m/z dimensions, and you need to label experimental features by biomolecular class before performing CCS calibration or validation. Use this skill when feature identification pipelines are unavailable, unreliable, or when you want to avoid bias from pre-identified peaks.

## When NOT to use

- Input is already a curated, manually validated feature table with known identifications—use class labels from your external database instead.
- You require compound-level structural identifications or chemical names—MOCCal assigns biomolecular class only, not specific chemical identity.
- Raw calibration data is not preprocessed and DEIMoS (v1.3.2) is unavailable—use UserDT mode with pre-processed calibration data instead.

## Inputs

- TWIM-MS data matrix (arrival time × m/z dimensions)
- Raw or processed TWIM-MS data file (UserDT or RawDT format)
- Optional: calibration reference compounds or standards

## Outputs

- Class-labeled feature table (structured file with m/z, arrival time, class assignment)
- Class-specific CCS values (if CCS calculation step follows)
- MOCCal Output directory with formatted results

## How to apply

Load your TWIM-MS data (arrival time and m/z arrays) into MOCCal. Apply MOCCal's biomolecular class assignment algorithm, which operates directly on the high-dimensional experimental data to label each feature by class without requiring pre-identified peaks. The algorithm assigns class labels such as lipid, peptide, carbohydrate, or other based on intrinsic properties of the arrival time–m/z space. Once features are class-labeled, MOCCal can then perform class-specific CCS calculations for calibration or validation. Output a structured feature table containing arrival time, m/z, assigned class label, and optionally class-specific CCS values.

## Related tools

- **MOCCal** (Primary tool for biomolecular class assignment and CCS calibration from TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Preprocessing and ion mobility feature extraction for raw TWIM-MS data (required for RawDT workflow only)) — https://github.com/pnnl/deimos

## Evaluation signals

- All experimental features in the output feature table have a class label assigned (lipid, peptide, carbohydrate, or other); no missing class assignments.
- Class-labeled features show biologically plausible separation in the arrival time–m/z space; lipids cluster in expected m/z and drift regions, peptides in others.
- Downstream class-specific CCS calculations are stable and consistent with literature reference values for each class.
- Feature count and m/z range match the input raw data; no unexpected loss or duplication of features.
- Output file is present in the MOCCal Output directory with correct schema (m/z, arrival time, class label columns).

## Limitations

- MOCCal assigns biomolecular class only, not specific compound identifications. Users must perform secondary identification if compound-level metadata is required.
- RawDT workflow requires DEIMoS v1.3.2 installation and Python environment setup; UserDT mode avoids this but requires pre-processed calibration data.
- Class assignment accuracy depends on the quality and representativeness of the input TWIM-MS data and intrinsic properties of the arrival time–m/z space; sparse or noisy data may reduce confidence.
- No changelog provided for version tracking or reproducibility across releases.

## Evidence

- [other] MOCCal implements biomolecular class assignment functionality that operates on experimental TWIM-MS data to label features by class, and performs class-specific CCS calculations, without requiring features to be identified first.: "implements biomolecular class assignment functionality that operates on experimental TWIM-MS data to label features by class, and performs class-specific CCS calculations, without requiring features"
- [intro] MOCCal offers class assignment and CCS calculations without need for identifying the features first.: "MOCCal offers class assignment and CCS calculations without need for identifying the features first"
- [intro] Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations.: "Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations"
- [intro] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)"
- [other] Apply MOCCal's biomolecular class assignment algorithm to label each experimental feature by class (e.g., lipid, peptide, carbohydrate, or other) directly from the high-dimensional data without requiring pre-identified feature peaks.: "Apply MOCCal's biomolecular class assignment algorithm to label each experimental feature by class (e.g., lipid, peptide, carbohydrate, or other) directly from the high-dimensional data"
