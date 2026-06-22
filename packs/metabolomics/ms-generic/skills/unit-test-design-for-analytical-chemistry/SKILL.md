---
name: unit-test-design-for-analytical-chemistry
description: Use when when implementing or modifying metabolomics feature detection pipelines (e.g., adduct detection, m/z matching, feature labeling) where correctness directly impacts downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0599
  tools:
  - pytest
  - fermo_core
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unit-test-design-for-analytical-chemistry

## Summary

Design and implement pytest unit tests to validate mass spectrometry feature detection and annotation modules, ensuring correctness of adduct labeling, ion mass matching, and feature table outputs against reference datasets with quantified false-positive and false-negative rates.

## When to use

When implementing or modifying metabolomics feature detection pipelines (e.g., adduct detection, m/z matching, feature labeling) where correctness directly impacts downstream analysis. Unit tests are essential when mass-matching logic, adduct offset calculations, or ion type recognition could introduce systematic errors in feature annotation.

## When NOT to use

- Feature table is already manually curated and does not require algorithmic validation of adduct assignments.
- Adduct detection module has not yet been implemented or is still in exploratory prototyping phase without stable mass-matching logic.
- Input data lacks ground-truth or reference annotations needed to establish expected test outcomes.

## Inputs

- Feature table (CSV or compatible format) with observed m/z values
- Reference adduct mass offsets (e.g., [M+NH4]+ = +17.0266 Da)
- Mass tolerance threshold (e.g., ppm window for m/z matching)
- Expected feature annotations or ground-truth adduct labels

## Outputs

- Pytest test suite with passing/failing cases for each adduct type
- Unit test report quantifying accuracy, false positives, and false negatives
- Labeled feature table with validated adduct annotations
- Verification report listing assigned labels and their correctness

## How to apply

Define reference feature sets with known adduct types and their theoretical m/z values. Construct pytest test cases that compare observed adduct labels against expected labels for each ion species (e.g., [M+NH4]+ at +17.0266 Da, [M+K]+ at +38.9815 Da). Implement mass-matching validation tests that verify correct assignment within a specified mass tolerance window (e.g., ppm threshold). Run pytest to execute all test cases and generate a report documenting assigned labels, their accuracy, and quantification of false positives. Use test output to validate that the detection module correctly identifies all adduct types without spurious assignments before deploying to production feature tables.

## Related tools

- **pytest** (Execute unit tests to validate adduct detection, mass-matching logic, and feature labeling correctness; report test results and accuracy metrics) — https://github.com/fermo-metabolomics/FERMO
- **fermo_core** (Provides the adduct detection and mass-matching implementation being validated by unit tests) — https://github.com/fermo-metabolomics/fermo_core

## Examples

```
pytest tests/test_adduct_detection.py -v --tb=short
```

## Evaluation signals

- All adduct types ([M+NH4]+, [M+K]+, [M+H2O+H]+, [M-H2O+H]+) are correctly identified in test reference set with 100% recall on known features.
- False-positive rate on reference feature set is zero or below acceptable threshold (no spurious adduct assignments).
- Mass-matching validation confirms observed m/z values fall within the specified tolerance window of theoretical adduct masses.
- Test report quantifies accuracy as a percentage and explicitly lists features where adduct labels match expected ground-truth annotations.
- Pytest output shows no test failures and all assertions for mass offset calculations pass.

## Limitations

- Unit tests can only validate behavior on reference datasets; performance on unseen, real-world feature tables may differ if data distribution or noise characteristics are not represented in test set.
- Adduct detection accuracy depends critically on mass tolerance parameter; tests must be re-run if tolerance is adjusted, and results may not generalize across different MS instruments or acquisition modes.
- False-negative detection (missed adducts due to weak signal or co-elution) is difficult to test without comprehensive ground-truth that itself requires independent validation.

## Evidence

- [other] Run pytest unit tests to validate that the adduct detection correctly identifies each adduct type on a reference feature set and reports no false positives.: "Run pytest unit tests to validate that the adduct detection correctly identifies each adduct type on a reference feature set and reports no false positives."
- [other] Implement mass-matching logic to scan an input feature table and assign adduct labels by comparing observed m/z values against theoretical adduct masses within a specified mass tolerance window.: "Implement mass-matching logic to scan an input feature table and assign adduct labels by comparing observed m/z values against theoretical adduct masses within a specified mass tolerance window."
- [other] Define adduct mass offsets for [M+NH4]+ (+17.0266 Da), [M+K]+ (+38.9815 Da), [M+H2O+H]+ (+19.0184 Da), and [M-H2O+H]+ (+1.0078 Da) in the adduct detection module.: "Define adduct mass offsets for [M+NH4]+ (+17.0266 Da), [M+K]+ (+38.9815 Da), [M+H2O+H]+ (+19.0184 Da), and [M-H2O+H]+ (+1.0078 Da) in the adduct detection module."
- [other] Generate a labeled feature table with adduct annotations and produce a verification report listing assigned labels and their accuracy.: "Generate a labeled feature table with adduct annotations and produce a verification report listing assigned labels and their accuracy."
