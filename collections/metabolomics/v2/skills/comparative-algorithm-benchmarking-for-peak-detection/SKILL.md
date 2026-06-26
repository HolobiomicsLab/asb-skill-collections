---
name: comparative-algorithm-benchmarking-for-peak-detection
description: 'Use when you have developed or adapted a peak detection method for chromatography–mass
  spectrometry and need to validate its reliability against an established baseline
  on the same raw GC–MS dataset. Specifically when: (1) the input is raw GC–MS data
  in m/z vs retention time format;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - NPFimg
  - XCMS
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c03163?ref=
  title: NPFimg
- doi: 10.1021/acs.analchem.1c03163
  title: ''
evidence_spans:
- github.com__poomcj__NPFimg
- We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker
  features of analytes in chromatography–mass spectrometry (MS) data by combining
  image processing and
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg,
  in that it has lower error rates of signal acquisition and marker identification.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Comparative Algorithm Benchmarking for Peak Detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematic comparison of peak detection algorithms on the same chromatography–mass spectrometry dataset to quantify and rank error rates in signal acquisition and marker identification. This skill validates whether a novel method (e.g., NPFimg) outperforms established baseline tools (e.g., XCMS) on real GC–MS data.

## When to use

You have developed or adapted a peak detection method for chromatography–mass spectrometry and need to validate its reliability against an established baseline on the same raw GC–MS dataset. Specifically when: (1) the input is raw GC–MS data in m/z vs retention time format; (2) you need to identify marker features at parts-per-billion sensitivity; (3) you want to quantify error rates in signal acquisition and feature identification to demonstrate feasibility or superiority; (4) you have access to both the novel method and a recognized reference tool (e.g., XCMS).

## When NOT to use

- Input data is already a curated feature table or peak matrix (feature extraction has already been performed); comparison should occur at the raw spectrum level to be meaningful.
- Only one algorithm is available; benchmarking requires ≥ 2 methods on identical data.
- The baseline tool (e.g., XCMS) is not designed for the same instrument type or data format (e.g., comparing a GC–MS method against an LC–MS-only tool introduces confounds unrelated to algorithm quality).

## Inputs

- Raw GC–MS data in two-dimensional m/z vs retention time format (e.g., NetCDF, mzML, or vendor-specific chromatography–mass spectrometry files)
- Sample metadata (e.g., sample type: aroma odor, human breath, or other analyte class)
- Detection sensitivity target (e.g., parts-per-billion concentration level)

## Outputs

- Error rate table: signal acquisition error rates (false positive rate, false negative rate, intensity estimation error) per algorithm
- Marker identification performance metrics: precision, recall, F-score, or false discovery rate per algorithm
- Comparative summary: ranked algorithms by error rate or reliability
- Visualization: side-by-side comparison of detected features and marker locations

## How to apply

Load the same raw GC–MS dataset (e.g., aroma odor or human breath samples in two-dimensional m/z vs retention time format) into both the novel algorithm and the baseline tool. Apply each method's complete pipeline without modification to preserve comparability. Quantify error rates for signal acquisition (false positives, false negatives, intensity estimation errors) and marker identification (precision, recall, false discovery rate) for each algorithm on the same data. Tabulate results side-by-side and report relative performance metrics—e.g., 'NPFimg achieved lower error rates compared to XCMS.' The rationale is that direct comparison on identical input eliminates confounds from preprocessing or dataset differences and allows reliable assessment of algorithmic superiority, particularly at low (ppb-level) detection thresholds where false peaks are common.

## Related tools

- **NPFimg** (novel peak detection and marker identification method combining image processing and machine learning; primary subject of benchmarking) — https://github.com/poomcj/NPFimg
- **XCMS** (established baseline peak detection tool for chromatography–mass spectrometry; reference standard for comparison)

## Evaluation signals

- Error rate table is complete and consistent: all algorithms report the same error metrics (false positive rate, false negative rate, intensity error) on the same dataset; no missing values.
- Detected features and marker locations are reproducible within each algorithm across independent runs (stability check).
- Relative performance ranking is defensible: the 'winner' algorithm achieves statistically lower error rates (or higher precision/recall) on the same sample set; differences are not due to data leakage or parameter tuning bias.
- Marker identification results at ppb sensitivity level are validated against independent ground truth (e.g., spiked standards, orthogonal analytical confirmation) or domain expert review.
- Comparison controls for confounds: both algorithms process identical raw input; no preprocessing, filtering, or parameter optimization is applied differentially.

## Limitations

- Benchmarking results are specific to the sample types and concentration ranges tested (e.g., aroma odor and human breath at ppb levels); generalization to other matrices, higher concentrations, or non-GC–MS instruments requires separate validation.
- Error rate definitions and calculation methods must be explicitly stated and consistent across both algorithms; ambiguity in metric definition can lead to misleading comparisons.
- Baseline tool performance is sensitive to parameter choice (e.g., peak width, noise threshold in XCMS); unfavorable parameter tuning of the baseline artificially inflates the novel method's apparent advantage. Fair comparison requires either consensus parameters or independent optimization of each method.
- Comparison is limited to the same raw dataset; results do not guarantee generalization to new sample matrices or instruments without additional benchmarking.

## Evidence

- [intro] Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification.: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [other] Quantify error rates for signal acquisition and marker identification using NPFimg. Compare NPFimg error rates against XCMS baseline on the same datasets.: "Quantify error rates for signal acquisition and marker identification using NPFimg. Compare NPFimg error rates against XCMS baseline on the same datasets."
- [intro] The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion level.: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
