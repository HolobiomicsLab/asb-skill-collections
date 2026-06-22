---
name: ppb-level-marker-detection-and-sensitivity-assessment
description: Use when you have raw GC–MS or LC–MS data in two-dimensional m/z vs retention time format and need to identify marker features at parts-per-billion sensitivity without relying on conventional peak picking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
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

# ppb-level marker detection and sensitivity assessment

## Summary

Automated identification of multivariate chemo-/biomarker features in GC–MS data at parts-per-billion concentration levels using image processing and machine learning on two-dimensional m/z vs retention time maps. This skill replaces conventional peak picking with a comprehensive signal characterization approach that reduces false detections and enables detection at ultra-trace concentrations.

## When to use

Apply this skill when you have raw GC–MS or LC–MS data in two-dimensional m/z vs retention time format and need to identify marker features at parts-per-billion sensitivity without relying on conventional peak picking. Suitable when false peak detection is a concern or when you need to validate marker identification error rates against baseline methods like XCMS on complex biological or chemical samples such as breath metabolomics or aroma compound profiling.

## When NOT to use

- Input is already a feature table or peak-picked dataset; use this skill on raw, unprocessed chromatography–mass spectrometry data only.
- Analysis does not require ppb-level detection sensitivity; conventional peak picking may suffice for higher concentration ranges.
- Data is from instruments or formats not compatible with two-dimensional m/z vs retention time representation (e.g., ion mobility spectrometry without time-of-flight calibration).

## Inputs

- Raw GC–MS data in two-dimensional m/z vs retention time format
- Chromatography–mass spectrometry raw files (aroma odor or biological breath samples)
- Baseline peak-picking results (e.g., from XCMS) for comparison

## Outputs

- Identified and visualized marker features with multivariate coordinates (m/z, retention time)
- Signal acquisition error rate quantification
- Marker identification error rate (comparison vs. XCMS baseline)
- Feature table with marker annotations at parts-per-billion sensitivity

## How to apply

Load raw GC–MS data as a two-dimensional map in m/z vs retention time format. Apply NPFimg's image processing and machine learning pipeline to process the 2D MS map and discriminate analytes without conventional peak picking. The method identifies and visualizes marker features by combining morphological image operations with pattern recognition. Quantify signal acquisition and marker identification error rates using NPFimg, then benchmark against XCMS or equivalent baseline on the same dataset to confirm feasibility at parts-per-billion detection level. The approach is justified by its avoidance of false peak detections inherent in conventional methods and demonstrated performance on ppb-level aroma odor and human breath case studies.

## Related tools

- **NPFimg** (Image processing and machine learning pipeline for automatic multivariate marker feature identification from two-dimensional MS maps; core tool for this skill) — github.com/poomcj/NPFimg
- **XCMS** (Baseline comparison tool for signal acquisition and marker identification error rates; standard against which NPFimg performance is benchmarked)

## Evaluation signals

- Error rates for signal acquisition and marker identification from NPFimg are lower than or comparable to XCMS baseline on identical datasets.
- Identified marker features are visualizable on the two-dimensional m/z vs retention time map without false peak artifacts.
- Marker identification is reproducible at parts-per-billion concentration levels across replicate samples (aroma odor and human breath case studies).
- Absence of spurious peaks characteristic of conventional peak picking; signal characterization covers the full 2D feature space.
- Quantified error metrics include both false positive and false negative rates, with explicit reporting of detection sensitivity threshold.

## Limitations

- Method is demonstrated on GC–MS case studies (aroma odor and human breath); applicability to other LC–MS workflows or sample types requires validation.
- Comparison is limited to XCMS as baseline; performance against other peak-picking or deconvolution methods not reported.
- Repository documentation is incomplete ('For the other details, I will update soon'); full implementation details and parameter tuning guidance are not publicly available.
- No changelog or version history found, limiting assessment of method stability and reproducibility across releases.

## Evidence

- [intro] NPFimg automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry data by combining image processing and machine learning: "We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize marker features: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] NPFimg avoids conventional peak picking, which suffers from false peak detections: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] Marker identification feasibility is demonstrated at parts-per-billion level on GC–MS of aroma odor and human breath samples: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] NPFimg has lower error rates of signal acquisition and marker identification compared to XCMS: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] NPFimg is potentially applicable to diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
- [readme] README confirms the two-dimensional MS map processing and parts-per-billion detection level: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features. Our approach allows us to comprehensively characterize the"
