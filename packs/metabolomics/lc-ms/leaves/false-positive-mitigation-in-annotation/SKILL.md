---
name: false-positive-mitigation-in-annotation
description: Use when you have implemented an automated feature annotation or adduct detection module and need to verify that assigned labels (e.g., [M+NH4]+, [M+K]+, [M+H2O+H]+, [M-H2O+H]+) are accurate and do not produce erroneous assignments on a reference feature set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - pytest
  - FERMO (fermo_core)
  techniques:
  - LC-MS
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

# false-positive-mitigation-in-annotation

## Summary

Systematic validation of feature annotation and adduct labeling in metabolomics workflows to eliminate incorrect ion type assignments and false identifications. This skill applies unit testing and reference validation to ensure that adduct detection modules correctly identify ionization species without spurious matches.

## When to use

Apply this skill when you have implemented an automated feature annotation or adduct detection module and need to verify that assigned labels (e.g., [M+NH4]+, [M+K]+, [M+H2O+H]+, [M-H2O+H]+) are accurate and do not produce erroneous assignments on a reference feature set. Essential before deploying annotation logic to production metabolomics dashboards.

## When NOT to use

- Input feature table already contains validated adduct annotations from orthogonal mass spectrometry expertise — this skill is redundant.
- Mass spectrometry data lacks sufficient mass accuracy (e.g., >50 ppm error) to reliably match theoretical adduct masses — mass tolerance windows become too broad.
- Reference dataset is unavailable or too small to provide statistically meaningful validation of annotation accuracy.

## Inputs

- feature table with m/z values (CSV format with columns including observed mass-to-charge ratio)
- reference feature set with ground-truth adduct labels and identities
- adduct mass offset definitions and mass tolerance parameters

## Outputs

- labeled feature table with adduct annotations assigned to each feature
- pytest unit test results confirming correct identification and absence of false positives
- verification report listing assigned adduct labels and per-feature accuracy metrics

## How to apply

Define reference feature sets with known true adduct assignments and run pytest unit tests against the annotation module to validate correct identification of each adduct type while confirming the absence of false positives. Configure mass-matching logic with appropriate mass tolerance windows (e.g., comparing observed m/z values against theoretical adduct masses like [M+NH4]+ at +17.0266 Da, [M+K]+ at +38.9815 Da, [M+H2O+H]+ at +19.0184 Da, and [M-H2O+H]+ at +1.0078 Da). Generate a verification report listing assigned labels, their accuracy metrics, and any discrepancies between expected and observed annotations. The rationale is that mass spectrometry feature tables contain numerous m/z values that may coincidentally match multiple adduct hypotheses; rigorous testing isolates true signal from numerical artifacts and ensures downstream hypothesis prioritization is built on reliable annotations.

## Related tools

- **pytest** (Unit testing framework to validate that adduct detection correctly identifies each adduct type and reports no false positives on reference feature sets)
- **FERMO (fermo_core)** (Metabolomics data analysis platform implementing adduct detection module for feature mass labeling in LC-MS/MS workflows) — https://github.com/fermo-metabolomics/FERMO

## Evaluation signals

- All reference features with known adducts are correctly assigned their expected ion type labels without exceptions
- No false positive adduct assignments reported on the reference feature set (0% spurious labeling rate)
- Mass-matching logic consistently respects the specified mass tolerance window (e.g., within ±X ppm of theoretical adduct mass)
- pytest test suite passes all unit tests for each adduct type ([M+NH4]+, [M+K]+, [M+H2O+H]+, [M-H2O+H]+) individually
- Verification report documents label accuracy for each adduct type and identifies any edge cases or marginal assignments requiring human review

## Limitations

- Adduct detection accuracy is bounded by input mass spectrometry resolution and calibration quality; high-resolution instruments (e.g., Orbitrap) will yield fewer ambiguous assignments than low-resolution ones (e.g., quadrupole).
- Reference feature set must be representative of the sample types and ionization conditions in the production workflow; validation on one organism or LC method may not generalize to others.
- FERMO 0.8.8.3 recognizes only four specific adduct ion types; other common adducts (e.g., [M+Na]+, [M+Cl]−, or in-source water losses [M−H2O]+ in negative mode) are not covered by this module.

## Evidence

- [other] FERMO implements adduct detection to recognize [M+NH4]+, [M+K]+, [M+H2O+H]+, and [M-H2O+H]+ as ionization adducts for feature mass labeling.: "FERMO implements adduct detection to recognize [M+NH4]+, [M+K]+, [M+H2O+H]+, and [M-H2O+H]+ as ionization adducts for feature mass labeling."
- [other] Define adduct mass offsets for [M+NH4]+ (+17.0266 Da), [M+K]+ (+38.9815 Da), [M+H2O+H]+ (+19.0184 Da), and [M-H2O+H]+ (+1.0078 Da) in the adduct detection module.: "Define adduct mass offsets for [M+NH4]+ (+17.0266 Da), [M+K]+ (+38.9815 Da), [M+H2O+H]+ (+19.0184 Da), and [M-H2O+H]+ (+1.0078 Da) in the adduct detection module."
- [other] Run pytest unit tests to validate that the adduct detection correctly identifies each adduct type on a reference feature set and reports no false positives.: "Run pytest unit tests to validate that the adduct detection correctly identifies each adduct type on a reference feature set and reports no false positives."
- [other] Generate a labeled feature table with adduct annotations and produce a verification report listing assigned labels and their accuracy.: "Generate a labeled feature table with adduct annotations and produce a verification report listing assigned labels and their accuracy."
- [other] Implement mass-matching logic to scan an input feature table and assign adduct labels by comparing observed m/z values against theoretical adduct masses within a specified mass tolerance window.: "Implement mass-matching logic to scan an input feature table and assign adduct labels by comparing observed m/z values against theoretical adduct masses within a specified mass tolerance window."
