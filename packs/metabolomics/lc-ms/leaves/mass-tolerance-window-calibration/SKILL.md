---
name: mass-tolerance-window-calibration
description: Use when when implementing adduct detection in LC-MS metabolomics workflows,
  after defining theoretical adduct mass offsets (e.g., [M+NH4]+ at +17.0266 Da, [M+K]+
  at +38.9815 Da), and before assigning adduct labels to a feature table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - pytest
  - fermo_core
  - FERMO
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-024-50111-8
  title: FERMO
evidence_spans:
- No discussion section present in document
- See our organization-level document on [CONTRIBUTING]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fermo_2_cq
    doi: 10.1038/s41467-024-50111-8
    title: FERMO
  dedup_kept_from: coll_fermo_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-50111-8
  all_source_dois:
  - 10.1038/s41467-024-50111-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-tolerance-window-calibration

## Summary

Calibration and validation of mass tolerance windows used to match observed m/z values against theoretical adduct masses in metabolomics feature annotation. This skill ensures accurate assignment of ionization adducts by defining and testing appropriate tolerance thresholds for mass-matching logic.

## When to use

When implementing adduct detection in LC-MS metabolomics workflows, after defining theoretical adduct mass offsets (e.g., [M+NH4]+ at +17.0266 Da, [M+K]+ at +38.9815 Da), and before assigning adduct labels to a feature table. Use this skill when you need to validate that mass-matching produces no false positives on a reference feature set.

## When NOT to use

- Input feature table is already fully annotated with adduct types from another source
- Mass spectrometry data lack sufficient m/z resolution or calibration to distinguish adducts within the tolerance window
- No reference feature set with ground-truth adduct labels is available for validation

## Inputs

- Feature table (CSV format, with observed m/z and intensity columns)
- Reference feature set with known adduct annotations (for validation)
- Defined adduct mass offsets and theoretical masses (as constants or configuration)

## Outputs

- Labeled feature table with adduct annotations and assigned adduct types
- Verification report documenting assigned labels, accuracy metrics, and false positive count

## How to apply

First, define the adduct mass offsets for each ionization species to be recognized (e.g., [M+NH4]+, [M+K]+, [M+H2O+H]+, [M-H2O+H]+) with their precise mass deltas in Daltons. Then, establish a mass tolerance window (e.g., within a specified ppm or Da threshold) around each theoretical adduct mass. Implement mass-matching logic that scans the input feature table and compares observed m/z values against theoretical adduct masses within this tolerance window. Run unit tests (using pytest) to validate that the detection correctly identifies each adduct type on a reference feature set and reports no false positives. Finally, generate a labeled feature table with adduct annotations and produce a verification report that lists assigned labels and their accuracy against known adducts.

## Related tools

- **pytest** (Unit testing framework to validate adduct detection correctness, confirm no false positives, and verify that observed m/z values are correctly matched within mass tolerance windows)
- **fermo_core** (Core metabolomics processing library that implements adduct detection and feature annotation logic) — https://github.com/fermo-metabolomics/fermo_core
- **FERMO** (Dashboard and GUI that integrates metabolomics data with adduct detection for rapid hypothesis-driven analysis) — https://github.com/fermo-metabolomics/FERMO

## Evaluation signals

- All reference features with known adducts are correctly identified and labeled in the output feature table
- False positive rate is zero or below a pre-specified threshold on the validation set
- No m/z values outside the defined tolerance window are incorrectly assigned to an adduct
- Unit test suite passes all adduct type detection tests (pytest output shows zero failures)
- Verification report documents exact match counts for each adduct species and overall accuracy percentage

## Limitations

- Requires accurate prior calibration of the mass spectrometer; uncalibrated or poorly calibrated instruments may violate the tolerance window assumptions
- Only recognizes adduct types for which mass offsets have been explicitly defined; novel or unexpected ionization species will be missed
- Mass tolerance window must be chosen to balance specificity (avoiding false positives) and sensitivity (avoiding false negatives); overly tight windows may miss valid adducts with slight calibration drift

## Evidence

- [other] Define adduct mass offsets for [M+NH4]+ (+17.0266 Da), [M+K]+ (+38.9815 Da), [M+H2O+H]+ (+19.0184 Da), and [M-H2O+H]+ (+1.0078 Da): "Define adduct mass offsets for [M+NH4]+ (+17.0266 Da), [M+K]+ (+38.9815 Da), [M+H2O+H]+ (+19.0184 Da), and [M-H2O+H]+ (+1.0078 Da) in the adduct detection module."
- [other] Implement mass-matching logic to scan input feature table and assign adduct labels by comparing observed m/z values against theoretical adduct masses within a specified mass tolerance window: "Implement mass-matching logic to scan an input feature table and assign adduct labels by comparing observed m/z values against theoretical adduct masses within a specified mass tolerance window."
- [other] Run pytest unit tests to validate that the adduct detection correctly identifies each adduct type on a reference feature set and reports no false positives: "Run pytest unit tests to validate that the adduct detection correctly identifies each adduct type on a reference feature set and reports no false positives."
- [other] Generate a labeled feature table with adduct annotations and produce a verification report listing assigned labels and their accuracy: "Generate a labeled feature table with adduct annotations and produce a verification report listing assigned labels and their accuracy."
- [other] FERMO implements adduct detection to recognize [M+NH4]+, [M+K]+, [M+H2O+H]+, and [M-H2O+H]+ as ionization adducts for feature mass labeling: "FERMO implements adduct detection to recognize [M+NH4]+, [M+K]+, [M+H2O+H]+, and [M-H2O+H]+ as ionization adducts for feature mass labeling."
