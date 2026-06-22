---
name: mass-error-calculation
description: 'Use when when screening LC-HRMS datasets for suspect compounds: you have detected features with measured m/z values and a database of reference compounds with theoretical m/z values, and you need to rank candidate matches by mass accuracy before proceeding to retention time and fragmentation.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - Scannotation
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.est.3c04764
  title: Scannotation
evidence_spans:
- Scannotation is an automated and user-friendly suspect screening tool for the rapid pre-annotation of LC-HRMS datasets.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scannotation_cq
    doi: 10.1021/acs.est.3c04764
    title: Scannotation
  dedup_kept_from: coll_scannotation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.est.3c04764
  all_source_dois:
  - 10.1021/acs.est.3c04764
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-error-calculation

## Summary

Calculate absolute or relative mass error between observed m/z values from LC-HRMS features and theoretical m/z values of suspect compounds to assess mass accuracy and enable feature-suspect matching within defined tolerance windows.

## When to use

When screening LC-HRMS datasets for suspect compounds: you have detected features with measured m/z values and a database of reference compounds with theoretical m/z values, and you need to rank candidate matches by mass accuracy before proceeding to retention time and fragmentation pattern scoring.

## When NOT to use

- When input features lack m/z information or are already matched to compounds with high confidence via orthogonal methods (e.g., standards or MS/MS validation).
- When the mass accuracy of the instrument is unknown or cannot be reliably estimated—mass error thresholds must be calibrated to instrument performance.
- When screening low-resolution mass spectra (e.g., unit-resolution MS1)—mass error calculation assumes sufficient mass resolution to discriminate between isobars.

## Inputs

- Feature table (m/z values from LC-HRMS detection)
- Suspect compound database (reference m/z values, chemical formulas)
- Mass accuracy tolerance threshold (Da or ppm)

## Outputs

- Filtered feature-suspect candidate pairs (within mass error tolerance)
- Mass error values (absolute or relative) for each pair
- Ranked candidate list ordered by mass error magnitude

## How to apply

For each detected feature, compute the mass error as the difference between observed m/z and suspect compound reference m/z, expressed either as absolute mass error (Da) or relative mass error (ppm). Apply mass accuracy tolerance thresholds (typically instrument-dependent, e.g., ±5 ppm for HRMS) to filter candidate suspects; retain only those within the acceptable deviation window. The mass error calculation serves as the first screening layer in the Scannotation scoring pipeline—candidates failing this step are eliminated before more computationally expensive isotopic pattern and neutral loss scoring. Order remaining candidates by mass error magnitude to prioritize best matches.

## Related tools

- **Scannotation** (Implements mass error calculation as the first MS1 predictor in the multi-stage feature-suspect proximity scoring pipeline for automated suspect screening) — https://github.com/scannotation/Scannotation_software

## Evaluation signals

- Mass error values for all feature-suspect pairs fall within expected instrument accuracy range (e.g., ±5 ppm for HRMS) for true positives.
- Candidates filtered by mass error threshold show higher subsequent match rates in isotopic pattern and neutral loss scoring, indicating successful pre-filtering.
- Distribution of mass errors for retained candidates is centered near zero with low variance; systematic bias suggests calibration drift.
- Downstream proximity scores are higher for feature-suspect pairs with smaller mass errors, confirming mass error is a meaningful component of the composite scoring function.
- False positive rate decreases when stricter mass error thresholds are applied, demonstrating threshold-dependent specificity trade-off.

## Limitations

- Mass error calculation alone does not distinguish isobars or isomers; retention time and fragmentation scoring are required for chemical differentiation.
- Mass accuracy tolerance must be instrument-specific and may vary with m/z range, ionization mode, and sample matrix; fixed thresholds may be suboptimal across diverse acquisition conditions.
- Systematic mass calibration errors or drift during long analytical runs can inflate apparent mass error and reduce sensitivity; frequent recalibration is recommended.
- Relative mass error (ppm) varies nonlinearly with absolute m/z; low-mass compounds may appear to have disproportionately large ppm errors even when absolute error is acceptable.

## Evidence

- [other] Compute m/z distance between each feature and suspect using absolute or relative mass error tolerance: "Compute m/z distance between each feature and suspect using absolute or relative mass error tolerance."
- [readme] Four MS1 chemical predictors integrated for proximity scoring: "This software combines several MS1 chemical predictors: m/z, retention times, isotopic patterns and neutral loss patterns, to score the proximity between features and suspects"
- [intro] Efficient prioritization workflow enabled by mass-based filtering: "Scannotation is an automated and user-friendly suspect screening tool for the rapid pre-annotation of LC-HRMS datasets."
