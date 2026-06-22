---
name: signal-acquisition-error-quantification
description: Use when you have processed the same GC–MS dataset (m/z vs retention time) through two independent signal acquisition pipelines and need to compute and compare their detection accuracy. Use this skill when one method (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - NPFimg
  - XCMS
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
---

# signal-acquisition-error-quantification

## Summary

Quantify and compare error rates of signal acquisition and marker identification between two chromatography–mass spectrometry processing methods (e.g., NPFimg vs. XCMS) on the same GC–MS dataset to validate algorithmic reliability. This skill surfaces when conventional peak picking is suspected of introducing false positives or false negatives, and a reference method is available for comparison.

## When to use

You have processed the same GC–MS dataset (m/z vs retention time) through two independent signal acquisition pipelines and need to compute and compare their detection accuracy. Use this skill when one method (e.g., image processing + machine learning) claims to reduce false peak detections compared to a standard baseline (e.g., conventional peak picking in XCMS), and you have ground truth or consensus annotations for true positive signals.

## When NOT to use

- Only one signal acquisition method has been applied to the dataset; comparison requires at least two independent pipelines.
- The dataset is already a feature table or consensus peak list; this skill operates on raw/processed signals before marker identification, not on downstream feature matrices.
- Ground truth annotations are unavailable and no reference standard or independent validation is possible; error rates cannot be computed without a true positive baseline.

## Inputs

- GC–MS dataset in two-dimensional form (m/z vs retention time chromatography-mass spectrometry data)
- Results from signal acquisition method 1 (e.g., NPFimg: detected signals and marker features)
- Results from signal acquisition method 2 (e.g., XCMS with standard peak detection parameters)
- Ground truth or consensus annotation of true analyte signals (optional but strengthens validation)

## Outputs

- Error rate table comparing both methods (false positives, false negatives, detection accuracy)
- Quantitative comparison showing lower error rates for the target method (e.g., NPFimg)
- Visualization of error metric distributions or summary statistics

## How to apply

For each method, compute error metrics for signal acquisition and marker identification: false positives, false negatives, and detection accuracy (or precision/recall). Apply both methods to the same GC–MS dataset without changing preprocessing parameters between runs. Tabulate the error metrics side-by-side and calculate relative performance (e.g., percentage reduction in error rate). The rationale is that NPFimg avoids conventional peak picking, which suffers from false peak detections; by comparing error distributions on identical data, you isolate the algorithmic advantage. Ensure the ground truth or reference annotation is applied consistently to both results.

## Related tools

- **NPFimg** (Automatically identifies multivariate chemo-/biomarker features in chromatography–mass spectrometry data using image processing and machine learning; processes two-dimensional MS map (m/z vs retention time) to discriminate analytes without conventional peak picking) — github.com/poomcj/NPFimg
- **XCMS** (Widely used baseline method for peak detection and signal acquisition in chromatography–mass spectrometry; generates conventional peak picking results used as comparison standard)

## Evaluation signals

- Error rates (false positive, false negative, detection accuracy) are computed reproducibly for both methods on the same dataset.
- The target method (NPFimg) shows quantitatively lower error rates than the baseline (XCMS) across false positive and false negative metrics.
- Error metrics are computed with the same ground truth or reference annotation applied consistently to both methods' results.
- Marker identification accuracy (true positives for chemo-/biomarker detection) is higher or equal in the target method compared to the baseline.
- Results are tabulated and annotated with the case study context (e.g., aroma odor or human breath GC–MS data, parts per billion level sensitivity).

## Limitations

- Comparison validity depends on using identical or comparable peak detection parameters for XCMS; suboptimal XCMS tuning may artificially inflate its error rate.
- Ground truth or consensus annotation of true signals is often unavailable in untargeted metabolomics; error rates may be estimated indirectly (e.g., via precision/recall on a subset of validated markers).
- The skill is demonstrated on GC–MS data in the aroma odor and human breath case studies; applicability to other chromatography–mass spectrometry modalities (e.g., liquid chromatography–MS) or non-biological matrices is not explicitly validated in the article.
- No changelog or version tracking provided for NPFimg; reproducibility of error quantification may be affected by algorithm updates or parameter drift over time.

## Evidence

- [intro] Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification.: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion level.: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [readme] We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning.: "automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning."
