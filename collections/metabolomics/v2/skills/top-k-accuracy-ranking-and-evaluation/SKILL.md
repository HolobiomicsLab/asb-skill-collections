---
name: top-k-accuracy-ranking-and-evaluation
description: Use when a machine learning model produces multiple ranked predictions
  (each with an associated confidence score) for a single input, and you need to quantify
  how often the correct answer appears in the top-k predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  tools:
  - NMR2Struct transformer + CNN model
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmr2struct
    doi: 10.1021/acscentsci.4c01132
    title: NMR2Struct
  dedup_kept_from: coll_nmr2struct
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.4c01132
  all_source_dois:
  - 10.1021/acscentsci.4c01132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# top-k-accuracy-ranking-and-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate model predictions by ranking outputs by confidence score and computing top-1, top-3, and top-5 accuracy metrics, where a prediction is considered correct if the ground-truth result appears within the top-k ranked candidates. This skill is essential for assessing generalization performance of structure prediction models across different molecular size regimes.

## When to use

Apply this skill when a machine learning model produces multiple ranked predictions (each with an associated confidence score) for a single input, and you need to quantify how often the correct answer appears in the top-k predictions. Specifically use it when testing out-of-distribution or out-of-scope inputs (e.g., molecules larger than the training domain) to measure absolute and relative accuracy degradation compared to in-scope baseline performance.

## When NOT to use

- When the model produces only a single prediction per input without a ranked confidence distribution; use this skill only if multiple scored candidates are available.
- When ground-truth labels are unavailable or not aligned with the prediction format (e.g., regression targets rather than discrete structure classes).
- When predictions are already binary (correct/incorrect) with no ranking information; top-k ranking presupposes a ranked candidate list.

## Inputs

- Ranked prediction list with confidence scores per test sample
- Ground-truth labels (e.g., correct molecular connectivity graph)
- In-scope baseline accuracy metrics for comparison

## Outputs

- Top-1 accuracy (scalar, 0–1)
- Top-3 accuracy (scalar, 0–1)
- Top-5 accuracy (scalar, 0–1)
- Absolute accuracy degradation vs. baseline
- Relative accuracy degradation percentage
- Error distribution summary report

## How to apply

For each test sample, (1) obtain the model's ranked list of predictions sorted by confidence score in descending order; (2) identify which rank position the ground-truth result occupies (if present); (3) record whether ground truth appears in the top-1, top-3, and top-5 positions; (4) compute the fraction of samples where ground truth appears within each k threshold (top-1 accuracy = fraction where rank ≤ 1; top-3 accuracy = fraction where rank ≤ 3; top-5 accuracy = fraction where rank ≤ 5); (5) compare out-of-scope accuracy metrics directly against the reported in-scope baseline (e.g., molecules ≤19 heavy atoms vs. >19 heavy atoms) to quantify absolute difference and relative degradation percentage; (6) document error distribution and failure modes in a summary report stratified by molecular complexity or other relevant attributes.

## Related tools

- **NMR2Struct transformer + CNN model** (Generates ranked predictions of molecular structure (formula and connectivity) with confidence scores from 1D NMR spectra; outputs feed directly into top-k evaluation)

## Evaluation signals

- Top-k accuracy values are bounded between 0 and 1; top-1 ≤ top-3 ≤ top-5 (monotonic non-decreasing property holds).
- Accuracy degradation on out-of-scope molecules (>19 heavy atoms) is quantified as an absolute difference and percentage relative to in-scope baseline; report includes both metrics.
- Error distribution can be stratified by molecular property (size, heavy atom count, functional group) to identify systematic failure modes.
- Confidence scores are properly ordered in ranked predictions such that rank position 1 has highest confidence; spot-check that top predictions are indeed ordered by decreasing confidence.
- Sample size is sufficient to compute stable estimates (e.g., n ≥ 30 per evaluation set); confidence intervals or error bars on accuracy estimates are reported.

## Limitations

- Accuracy is bounded by the underlying model's training scope; the NMR2Struct framework's effectiveness is established only up to 19 heavy atoms, and generalization beyond this threshold is uncharacterized.
- Top-k metrics assume that exactly one ground-truth answer exists per sample; behavior is undefined if multiple correct answers are possible or if the true structure is not in the candidate pool.
- Confidence scores reflect model calibration on the training distribution; out-of-distribution inputs may exhibit poorly calibrated scores, making ranking less meaningful.
- Top-k accuracy does not penalize how far down the ranked list the correct answer appears; a correct answer at rank 5 and rank 3 both contribute equally to top-5 accuracy.

## Evidence

- [other] Rank predictions by confidence score and compute top-1, top-3, and top-5 structure recovery accuracy: "Rank predictions by confidence score and compute top-1, top-3, and top-5 structure recovery accuracy (fraction of predictions matching ground-truth connectivity)."
- [other] Compare out-of-scope accuracy against in-scope baseline and quantify degradation: "Compare out-of-scope accuracy metrics against the reported in-scope baseline (molecules ≤19 heavy atoms) and quantify the absolute and relative degradation."
- [other] Framework effectiveness is bounded to molecules with up to 19 heavy atoms: "The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized."
- [other] Document accuracy loss, error distribution, and failure modes: "Document accuracy loss, error distribution, and failure modes in a summary report."
