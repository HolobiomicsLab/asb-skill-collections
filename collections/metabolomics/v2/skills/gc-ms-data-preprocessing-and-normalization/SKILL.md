---
name: gc-ms-data-preprocessing-and-normalization
description: Use when you have raw GC-MS data (aroma, breath, or other volatile analyte samples) in NetCDF or vendor-native format and need to identify multivariate chemo-/biomarker features without conventional peak picking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0769
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

# gc-ms-data-preprocessing-and-normalization

## Summary

Convert raw GC-MS data into a two-dimensional m/z versus retention time map suitable for image processing and machine learning-based marker identification. This preprocessing step replaces conventional peak picking to avoid false peak detections and enables parts-per-billion level sensitivity in metabolomics workflows.

## When to use

You have raw GC-MS data (aroma, breath, or other volatile analyte samples) in NetCDF or vendor-native format and need to identify multivariate chemo-/biomarker features without conventional peak picking. Use this when your analysis goal is marker discovery at parts-per-billion concentration levels and you want to leverage image processing and machine learning on the full 2D chromatographic–mass spectrometric signal.

## When NOT to use

- Input is already a peak table or feature matrix (preprocessing already complete).
- Analysis requires targeted quantification at specific known m/z and retention time coordinates (use conventional peak picking instead).
- Data is from non-volatile analytes analyzed by liquid chromatography–MS; this skill is optimized for GC–MS.

## Inputs

- Raw GC-MS data file (NetCDF or vendor format: .raw, .d, etc.)
- Sample metadata (sample type: aroma odor, human breath, or similar volatile analyte source)
- Expected concentration range or sensitivity target (e.g., parts-per-billion level)

## Outputs

- Two-dimensional m/z vs retention time intensity map
- Preprocessed image matrix suitable for machine learning input
- Marker feature map with localized analyte signals

## How to apply

Load raw GC-MS data and construct a two-dimensional intensity map indexed by m/z (mass-to-charge) on one axis and retention time on the other. This 2D map serves as the input to image processing pipelines (e.g., NPFimg) that discriminate analytes and identify marker features across the full signal space. The approach avoids traditional peak picking, which is prone to false positives. After preprocessing, apply machine learning classification or feature extraction to the 2D map to localize and quantify marker signals. The method is grounded in the rationale that comprehensive signal characterization without peak-picking thresholds improves detection reliability at low concentrations and reduces manual parameter tuning.

## Related tools

- **NPFimg** (Processes 2D m/z vs retention time maps to discriminate analytes and identify marker features via image processing and machine learning) — https://github.com/poomcj/NPFimg
- **XCMS** (Baseline peak picking and feature detection tool used for error-rate comparison in marker identification)

## Evaluation signals

- Verify that the output 2D map has correct dimensionality (m/z bins × retention time bins) and spans the expected range for the sample type (e.g., m/z 30–300 for volatile compounds).
- Confirm that signal intensity is preserved: sum of intensities in the 2D map matches the total ion current or known calibration standard.
- Compare marker identification error rates (false positives, false negatives) against XCMS baseline on the same dataset; NPFimg should show lower error rates at parts-per-billion sensitivity.
- Visually inspect the 2D map for expected analyte clusters: peaks should localize to distinct m/z × retention time regions without artifacts or noise spreading.
- Validate that marker features are reproducible across replicate samples of the same type (e.g., multiple aroma odor or breath samples).

## Limitations

- Method is demonstrated only on GC–MS; applicability to LC–MS has not been experimentally validated in the cited work.
- Requires tuning of image processing parameters and machine learning model selection; no automated parameter recommendation is provided in the article.
- Detection limit validation is limited to aroma odor and human breath case studies; generalization to other volatile analyte matrices is not established.
- Repository README indicates that 'For the other details, I will update soon', suggesting incomplete documentation of implementation and parameter settings.

## Evidence

- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion level.: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification.: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS.: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
- [readme] We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning.: "We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
