---
name: adduct-mass-offset-parameterization
description: Use when when processing LC-MS metabolomics feature tables where adduct
  annotation is absent or incomplete, and you need to identify which ionization adducts
  are present in your mass spectrometry data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - pytest
  - FERMO
  - fermo_core
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

# adduct-mass-offset-parameterization

## Summary

Define and implement mass offset parameters for common ionization adducts ([M+NH4]+, [M+K]+, [M+H2O+H]+, [M-H2O+H]+) to enable accurate adduct detection and labeling in LC-MS metabolomics feature tables. This skill ensures that observed m/z values are correctly annotated with their ionization form, critical for downstream metabolite identification and abundance quantification.

## When to use

When processing LC-MS metabolomics feature tables where adduct annotation is absent or incomplete, and you need to identify which ionization adducts are present in your mass spectrometry data. This is particularly important when integrating multiple samples or datasets where different ionization modes may produce the same molecular species in different adduct forms.

## When NOT to use

- Input feature table already contains reliable adduct annotations from the mass spectrometer or upstream processing.
- Your LC-MS instrument uses non-standard ionization adducts not covered by the four defined offsets (e.g., [M+Na]+, [M+Cl]−, or exotic multiply-charged species).
- Mass tolerance window is too tight relative to your instrument's mass accuracy, risking missed assignments and false negatives.

## Inputs

- LC-MS feature table (CSV format with m/z and intensity columns)
- Mass tolerance threshold (ppm or Da)
- Reference feature set with known adducts (for validation)

## Outputs

- Adduct-labeled feature table with assigned ionization forms
- Verification report listing assigned adduct labels and accuracy metrics
- Unit test results (pytest log) confirming correct identification with no false positives

## How to apply

First, define the exact mass offset (Δm/z in Da) for each target adduct: [M+NH4]+ = +17.0266 Da, [M+K]+ = +38.9815 Da, [M+H2O+H]+ = +19.0184 Da, and [M-H2O+H]+ = +1.0078 Da. Implement mass-matching logic in your feature detection module that scans the input feature table and assigns adduct labels by comparing each observed m/z value against theoretical adduct masses within a specified mass tolerance window (typically ±5–10 ppm depending on instrument resolution). Execute unit tests using pytest or equivalent to validate that each adduct type is correctly identified on a reference feature set with no false positives. Generate a labeled feature table with adduct annotations and produce a verification report documenting assigned labels and their assignment accuracy.

## Related tools

- **pytest** (Unit testing framework for validating adduct detection correctness and reporting false positive/negative rates)
- **FERMO** (Metabolomics dashboard integrating adduct detection module for feature mass labeling and annotation) — https://github.com/fermo-metabolomics/FERMO
- **fermo_core** (Core library providing adduct detection and feature table processing logic) — https://github.com/fermo-metabolomics/fermo_core

## Evaluation signals

- All reference features with known adducts are correctly identified (100% recall on validation set).
- No false positive adduct assignments are reported (zero or negligible false positives on negative control features).
- Adduct labels in output feature table match expected ionization forms within the specified mass tolerance.
- Unit test suite passes all pytest assertions without errors or warnings.
- Verification report documents assignment accuracy and mass error distribution (mean and std dev) for each adduct type.

## Limitations

- Only detects the four explicitly parameterized adduct ions; additional or instrument-specific adducts require definition of new mass offsets.
- Accuracy depends critically on mass tolerance window setting: too-tight windows cause false negatives; too-loose windows increase false positives, especially for high-complexity samples.
- Does not account for isotope patterns or multiply-charged adducts, which may co-elute and complicate assignment.
- Performance on low-resolution or degraded mass spectrometry data may be poor if mass accuracy exceeds the tolerance threshold.

## Evidence

- [other] FERMO implements adduct detection to recognize [M+NH4]+, [M+K]+, [M+H2O+H]+, and [M-H2O+H]+ as ionization adducts for feature mass labeling.: "FERMO implements adduct detection to recognize [M+NH4]+, [M+K]+, [M+H2O+H]+, and [M-H2O+H]+ as ionization adducts for feature mass labeling."
- [other] Define adduct mass offsets for [M+NH4]+ (+17.0266 Da), [M+K]+ (+38.9815 Da), [M+H2O+H]+ (+19.0184 Da), and [M-H2O+H]+ (+1.0078 Da) in the adduct detection module.: "Define adduct mass offsets for [M+NH4]+ (+17.0266 Da), [M+K]+ (+38.9815 Da), [M+H2O+H]+ (+19.0184 Da), and [M-H2O+H]+ (+1.0078 Da)"
- [other] Implement mass-matching logic to scan an input feature table and assign adduct labels by comparing observed m/z values against theoretical adduct masses within a specified mass tolerance window.: "Implement mass-matching logic to scan an input feature table and assign adduct labels by comparing observed m/z values against theoretical adduct masses within a specified mass tolerance window."
- [other] Run pytest unit tests to validate that the adduct detection correctly identifies each adduct type on a reference feature set and reports no false positives.: "Run pytest unit tests to validate that the adduct detection correctly identifies each adduct type on a reference feature set and reports no false positives."
- [readme] FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization.: "FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization."
