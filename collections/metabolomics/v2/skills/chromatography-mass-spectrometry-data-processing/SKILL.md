---
name: chromatography-mass-spectrometry-data-processing
description: Use when when you have raw GC–MS or LC–MS data (m/z vs retention time chromatography-mass spectrometry maps) and need to identify analyte signals and marker features without conventional peak picking;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0625
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

# chromatography-mass-spectrometry-data-processing

## Summary

Automated identification of multivariate chemo-/biomarker features in GC–MS and LC–MS data by combining image processing and machine learning on two-dimensional m/z–retention time maps, bypassing conventional peak picking to reduce false positives and false negatives.

## When to use

When you have raw GC–MS or LC–MS data (m/z vs retention time chromatography-mass spectrometry maps) and need to identify analyte signals and marker features without conventional peak picking; especially when dealing with low-abundance targets (parts per billion level) or when conventional peak detection introduces unacceptable false positives and false negatives.

## When NOT to use

- Input is already a feature table or processed peak list (prior conventional peak picking has already been applied).
- Analysis requires targeted monitoring of pre-defined m/z values with known retention times (use targeted methods instead).
- Data is from mass spectrometry modalities other than GC–MS or LC–MS (method scope is chromatography-coupled MS only).

## Inputs

- Two-dimensional MS map (m/z vs retention time, GC–MS or LC–MS format)
- Raw chromatography-mass spectrometry data

## Outputs

- Identified marker features with m/z values, retention times, and feature scores
- Signal acquisition error metrics (false positives, false negatives, detection accuracy)
- Marker identification accuracy scores
- Visualized marker features on m/z–retention time space

## How to apply

Load the two-dimensional MS map (m/z vs retention time) into NPFimg. Apply the image processing and machine learning pipeline to process the MS map and discriminate analytes without conventional peak picking. Run the automated detection algorithm to identify marker features and compute signal acquisition metrics (false positives, false negatives, detection accuracy) and marker identification accuracy. Visualize identified marker features on the m/z–retention time space and export predictions with m/z values, retention times, and feature scores. Optionally compare error rates against XCMS or other baseline methods to validate lower error rates achieved by the image-processing approach.

## Related tools

- **NPFimg** (Primary tool for two-dimensional MS map processing, image analysis, and automated marker feature identification via machine learning) — https://github.com/poomcj/NPFimg
- **XCMS** (Baseline comparison tool for conventional peak detection and signal acquisition; used to benchmark error rates against NPFimg's approach)

## Evaluation signals

- Marker features are identified without conventional peak picking; verify that output includes m/z, retention time, and feature score for each detected feature.
- Signal acquisition error rates (false positives, false negatives, detection accuracy) are computed and lower than XCMS baseline when both methods process the same dataset.
- Marker identification accuracy is quantified and reported; comparison with XCMS shows measurable reduction in false detections.
- Visualizations on m/z–retention time space show clustered or connected feature regions, indicating spatial coherence of identified analyte signals.
- Feature predictions are exported as structured tables with consistent schema (m/z, retention time, feature score columns).

## Limitations

- Currently demonstrated on GC–MS case studies (aroma odor and human breath); LC–MS applicability is stated as potential but not exhaustively validated in the presented work.
- Performance at parts per billion level is shown for the tested case studies; absolute limit of detection for arbitrary metabolites is not systematically characterized.
- Repository README indicates 'limited applications' and notes 'I will update soon', suggesting method is still under active development and documentation is incomplete.

## Evidence

- [intro] NPFimg automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry data by combining image processing and machine learning: "NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify marker features without conventional peak picking: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features"
- [intro] Avoidance of conventional peak picking which suffers from false peak detections is a key methodological advantage: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] NPFimg has lower error rates of signal acquisition and marker identification compared to XCMS: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] Method is potentially applicable to diverse metabolomics and chemometrics using GC–MS and LC–MS: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
- [readme] Repository documentation confirms the core workflow and applicability scope: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
