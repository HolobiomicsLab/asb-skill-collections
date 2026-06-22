---
name: marker-feature-identification-and-validation
description: Use when when processing GC–MS or LC–MS data as m/z vs retention time chromatograms and you need to identify biomarker or chemical marker features without conventional peak picking, particularly when false positive detection rates from peak detection algorithms are problematic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
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

# marker-feature-identification-and-validation

## Summary

Automated identification of multivariate chemo-/biomarker features from two-dimensional chromatography–mass spectrometry maps using image processing and machine learning, bypassing conventional peak picking to reduce false detections. This skill combines visual feature extraction with quantitative marker discrimination to detect analytes at parts-per-billion sensitivity.

## When to use

When processing GC–MS or LC–MS data as m/z vs retention time chromatograms and you need to identify biomarker or chemical marker features without conventional peak picking, particularly when false positive detection rates from peak detection algorithms are problematic. Applicable to metabolomics workflows on human breath, aroma, or similar complex mixture samples where marker visualization and discrimination are key outputs.

## When NOT to use

- Input is already a processed feature table or peak list; apply this skill to raw or minimally processed 2D MS data only.
- Targeted metabolomics with a predefined list of expected m/z values and retention times; this skill is designed for multivariate marker discovery, not validation of known markers.
- Data from instruments or workflows already employing robust peak picking that has been validated for your specific matrix; conventional peak picking may be sufficient.

## Inputs

- GC–MS or LC–MS data in m/z vs retention time format (e.g., NetCDF chromatography-mass spectrometry raw data or processed 2D maps)
- Case study dataset with known analyte composition or reference markers
- Optional: comparison baseline results (e.g., XCMS peak detection output for the same dataset)

## Outputs

- Identified marker features with m/z and retention time coordinates
- Visualized chemo-/biomarker feature map
- Signal acquisition error rate (false positives, false negatives, detection accuracy)
- Marker identification accuracy metric
- Tabulated comparison with baseline methods (XCMS, etc.)

## How to apply

Load a two-dimensional MS map (m/z vs retention time) into NPFimg. Apply the image processing and machine learning pipeline to process the entire map as an image rather than applying peak picking to individual traces. The algorithm discriminates analytes and identifies marker features by learning visual patterns in the 2D space. Compute error rates (false positives, false negatives, detection accuracy) for signal acquisition and marker identification accuracy by comparing against a reference standard or known markers. Validate that NPFimg achieves lower error rates than baseline methods (e.g., XCMS with standard peak detection parameters) before adopting results for downstream analysis.

## Related tools

- **NPFimg** (Primary tool for image processing and machine learning-based marker feature identification from 2D MS maps) — github.com/poomcj/NPFimg
- **XCMS** (Baseline comparison tool for conventional peak detection; used to benchmark error rates of signal acquisition and marker identification)

## Evaluation signals

- Error rates (false positives, false negatives, detection accuracy) for NPFimg are quantitatively lower than XCMS on the same dataset.
- Marker features are visualized and discriminable in the m/z vs retention time space without ambiguous or overlapping identifications.
- Identified markers match known reference compounds or ground truth markers from case study datasets (aroma odor, human breath).
- Signal acquisition is successful at parts-per-billion sensitivity levels as demonstrated in the source case studies.
- Comparison table shows consistent improvement across both signal acquisition and marker identification metrics relative to peak-picking baselines.

## Limitations

- The method is demonstrated on GC–MS and LC–MS data; applicability to other MS modalities (e.g., MALDI, direct infusion) is not established.
- Performance depends on the quality of the 2D MS map (resolution, dynamic range, noise); degraded or heavily noisy maps may reduce reliability.
- Currently demonstrated on aroma and human breath case studies; generalization to other matrices or untargeted metabolomics workflows may require revalidation.
- Requires access to reference standards or known marker ground truth for error rate computation; performance without such references is unclear.
- No changelog or versioning information provided in the repository, limiting reproducibility tracking.

## Evidence

- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize marker features.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] The method avoids conventional peak picking, which suffers from false peak detections.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] NPFimg has lower error rates of signal acquisition and marker identification compared to XCMS.: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] The method automatically identifies multivariate chemo-/biomarker features by combining image processing and machine learning.: "We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
- [intro] Marker identification is demonstrated in case studies of aroma odor and human breath on GC–MS at parts per billion level.: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] NPFimg is potentially applicable to diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS.: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
- [readme] Repository description emphasizes combining image processing and machine learning without conventional peak picking.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
