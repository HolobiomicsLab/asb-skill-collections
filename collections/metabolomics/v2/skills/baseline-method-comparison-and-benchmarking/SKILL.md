---
name: baseline-method-comparison-and-benchmarking
description: Use when you have developed or adapted an analytical method (e.g., NPFimg for GC–MS marker identification) and need to demonstrate its reliability or superiority over a widely-used reference method (e.g., XCMS). Apply this skill when you have access to both the same raw input data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - NPFimg
  - XCMS
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03163?ref=
  title: NPFimg
- doi: 10.1021/acs.analchem.1c03163
  title: ''
evidence_spans:
- github.com__poomcj__NPFimg
- We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npfimg_cq
    doi: 10.1021/acs.analchem.1c03163?ref=
    title: NPFimg
  dedup_kept_from: coll_npfimg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03163?ref=
  all_source_dois:
  - 10.1021/acs.analchem.1c03163?ref=
  - 10.1021/acs.analchem.1c03163
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# baseline-method-comparison-and-benchmarking

## Summary

Quantitatively compare a novel analytical method against an established baseline tool by computing error metrics on the same input dataset, enabling objective evaluation of performance improvements in signal detection and feature identification. This skill is essential for validating whether new approaches reduce false positives, false negatives, or other systematic errors relative to conventional pipelines.

## When to use

You have developed or adapted an analytical method (e.g., NPFimg for GC–MS marker identification) and need to demonstrate its reliability or superiority over a widely-used reference method (e.g., XCMS). Apply this skill when you have access to both the same raw input data (e.g., two-dimensional m/z vs retention time chromatography–mass spectrometry data) and ground truth or validated reference results, and when error rates of signal acquisition (false positives, false negatives, detection accuracy) and feature identification accuracy are the key performance criteria.

## When NOT to use

- The input datasets differ between methods (e.g., different preprocessing, normalization, or filtering steps applied before baseline comparison) — this confounds the comparison.
- Ground truth or validated reference results are unavailable or unreliable — error rates cannot be computed without a standard to measure against.
- The baseline method has not been published or its parameters are not reproducible — you cannot ensure a fair and transparent comparison.

## Inputs

- Raw two-dimensional chromatography–mass spectrometry data (m/z vs retention time)
- Ground truth or validated reference annotations (signal locations, marker identities)
- Method-specific parameter configurations (peak detection thresholds, machine learning model settings)

## Outputs

- Error rate tabulation for signal acquisition (false positive rate, false negative rate, detection accuracy per method)
- Error rate tabulation for marker identification accuracy per method
- Comparative summary table showing relative performance improvement of novel method over baseline
- Error metrics in absolute counts and percentages suitable for statistical comparison

## How to apply

Load the same raw analytical dataset (e.g., GC–MS two-dimensional MS map) into both the novel method and the baseline tool using their standard or published parameter settings. Process the dataset through each pipeline independently without cross-contamination. For each method, extract signal detection outcomes (peaks identified, m/z and retention time coordinates, intensities) and marker feature assignments. Compute error metrics for both: false positive rate (signals detected by the method but absent in ground truth), false negative rate (signals in ground truth but missed by the method), and marker identification accuracy (percentage of detected features correctly classified). Tabulate the error metrics side-by-side and calculate the relative improvement (e.g., percentage reduction in false positives or increase in accuracy). The rationale is that identical input data removes confounding factors, allowing error differences to reflect genuine algorithmic or pipeline improvements rather than data preprocessing artifacts.

## Related tools

- **NPFimg** (Novel method combining image processing and machine learning for automated marker identification in chromatography–mass spectrometry data; the subject of comparison.) — github.com/poomcj/NPFimg
- **XCMS** (Widely-used baseline method for peak detection and feature identification in mass spectrometry data; provides reference performance metrics for comparison.)

## Evaluation signals

- Both methods process identical raw input data (same m/z vs retention time chromatogram) without prior filtering or preprocessing differences that would bias the comparison.
- Error metrics are computed using the same ground truth or validated reference standard for both methods, ensuring comparability.
- False positive rate, false negative rate, and marker identification accuracy are reported as absolute counts and percentages for each method, with numerical differences substantiated.
- The novel method exhibits lower error rates (e.g., fewer false positives, fewer false negatives, or higher accuracy percentage) compared to the baseline across both signal acquisition and marker identification tasks.
- Relative improvement is quantified (e.g., 'NPFimg reduces false positive rate by X%' or 'improves marker accuracy from Y% to Z%') with statistical significance noted if applicable.

## Limitations

- Comparison validity depends on both methods receiving identical preprocessing and parameter tuning effort; if the baseline method is run with outdated or non-optimal parameters, the comparison may not reflect true algorithmic differences.
- Error rates alone do not capture computational efficiency, scalability, or practical usability; a method with lower error rates but prohibitive runtime or memory requirements may not be preferable in practice.
- Ground truth availability and reliability are critical; if the reference standard is incomplete, biased, or contaminated with false annotations, computed error rates will be misleading.
- The skill demonstrates improvement on specific case studies (e.g., aroma odor and human breath GC–MS at parts per billion level) and may not generalize to other matrices, instruments, or concentration ranges without additional validation.

## Evidence

- [intro] Comparison rationale and baseline choice: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] Input data type and processing pipeline: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] Error metrics definition: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] Case study scope and validation context: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] Method generalizability boundary: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
