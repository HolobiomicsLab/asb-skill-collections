---
name: ion-mobility-feature-classification
description: Use when you have high-dimensional TWIM-MS data (arrival time and m/z dimensions) from a multi-omic sample and need to associate experimental features with biomolecular classes *before* running peak detection or feature identification pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
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
- Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moccal
    doi: 10.1021/acs.analchem.3c04290
    title: moccal
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

# ion-mobility-feature-classification

## Summary

Assigns biomolecular class labels (lipid, peptide, carbohydrate, etc.) to experimental features directly from TWIM-MS arrival time and m/z dimensions without requiring prior feature identification. This enables class-specific collision cross section (CCS) calibration and downstream multi-omic analysis on raw or minimally processed ion mobility data.

## When to use

Apply this skill when you have high-dimensional TWIM-MS data (arrival time and m/z dimensions) from a multi-omic sample and need to associate experimental features with biomolecular classes *before* running peak detection or feature identification pipelines. Use it particularly when your goal is to perform class-stratified CCS calibration or when you want to avoid bias from pre-identification thresholds.

## When NOT to use

- Input is already a feature table with pre-identified peaks or annotated molecular identities; use MOCCal for class assignment only on raw or minimally processed arrival time–m/z data.
- You require drift time (time spent within the TWIM cell); MOCCal works with arrival time recorded by TWIM platforms, not true drift time.
- Your analysis goal is single-class or non-stratified CCS calibration; class assignment adds overhead without benefit if all features will be pooled.

## Inputs

- Raw TWIM-MS data: arrival time dimension (time at which ion reaches detector)
- m/z (mass-to-charge ratio) dimension
- Multi-omic experimental sample data (unidentified features)

## Outputs

- Class-labeled feature table (structured format with feature ID, m/z, arrival time, assigned biomolecular class)
- Class assignments for lipids, peptides, carbohydrates, or other biomolecular classes

## How to apply

Load raw or processed TWIM-MS data (arrival time and m/z arrays) into MOCCal. MOCCal's biomolecular class assignment algorithm operates directly on the high-dimensional feature space to label each experimental observation by class without requiring features to be identified first. The algorithm generates a class-labeled feature table as structured output. Class labels enable downstream class-specific CCS calculations and calibration, allowing you to build separate calibration models for lipids, peptides, carbohydrates, and other biomolecule types. Validation is performed by inspecting the resulting feature-class assignments and confirming that the class distribution matches expected composition for your sample type.

## Related tools

- **MOCCal** (Python application that implements biomolecular class assignment and class-specific CCS calculations directly on high-dimensional TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Optional dependency for processing raw calibration files; required for RawDT (raw data) workflows in MOCCal) — http://github.com/pnnl/deimos

## Evaluation signals

- Output feature table contains a new class column with non-null biomolecular class assignments (e.g. lipid, peptide, carbohydrate) for all or nearly all input features.
- Class distribution is reasonable for the sample type (e.g., lipid-rich sample should have high proportion of lipid class).
- Feature count is preserved between input and output; no features are dropped during class assignment.
- Class-specific CCS calculations can be generated without error, indicating that class labels are consistent and usable for downstream stratified calibration.
- Output file is in expected structured format (e.g., CSV, HDF5, or specified template format from UserDT or RawDT folders).

## Limitations

- MOCCal distinguishes arrival time (when ion reaches detector) from drift time (time spent in TWIM cell); users must understand that TWIM platforms record arrival time, not true drift time.
- Class assignment operates on high-dimensional feature space without requiring prior identification, but assignment quality depends on the discriminability of biomolecular classes in the arrival time–m/z space; overlapping classes may be misassigned.
- No changelog is available, limiting visibility into method changes or improvements between versions.
- UserDT (processed calibration) and RawDT (raw calibration) workflows require different dependencies and data preparation; users must select the appropriate mode for their input.

## Evidence

- [other] MOCCal implements biomolecular class assignment functionality that operates on experimental TWIM-MS data to label features by class, and performs class-specific CCS calculations, without requiring features to be identified first.: "biomolecular class assignment functionality that operates on experimental TWIM-MS data to label features by class, and performs class-specific CCS calculations, without requiring features to be"
- [readme] MOCCal, or Multi-Omic CCS Calibrator, is a Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data anlaysis. Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations.: "Python application for high-dimensional, multi-omic traveling-wave ion mobility mass spectrometry (TWIM-MS) data. Functionality includes collision cross section (CCS) calibration, experimental data"
- [readme] MOCCal offers class assignment and CCS calculations without need for identifying the features first.: "MOCCal offers class assignment and CCS calculations without need for identifying the features first"
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)"
- [other] Apply MOCCal's biomolecular class assignment algorithm to label each experimental feature by class (e.g., lipid, peptide, carbohydrate, or other) directly from the high-dimensional data without requiring pre-identified feature peaks.: "label each experimental feature by class (e.g., lipid, peptide, carbohydrate, or other) directly from the high-dimensional data without requiring pre-identified feature peaks"
