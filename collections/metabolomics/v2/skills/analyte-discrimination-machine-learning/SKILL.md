---
name: analyte-discrimination-machine-learning
description: Use when you have raw chromatography–mass spectrometry data (GC-MS or LC-MS) in 2D m/z–retention time format and need to identify and discriminate multiple analytes while avoiding false peak detections inherent in conventional peak picking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - XCMS
  - NPFimg
derived_from:
- doi: 10.1021/acs.analchem.1c03163?ref=
  title: NPFimg
- doi: 10.1021/acs.analchem.1c03163
  title: ''
evidence_spans:
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification.
- github.com__poomcj__NPFimg
- We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and
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

# analyte-discrimination-machine-learning

## Summary

Use machine learning classifiers to discriminate individual analytes in a two-dimensional MS map (m/z vs retention time) based on their spatial signatures, enabling automated marker feature identification without conventional peak picking. This skill is applied within the NPFimg pipeline to replace error-prone peak detection with multivariate chemo-/biomarker feature discovery.

## When to use

You have raw chromatography–mass spectrometry data (GC-MS or LC-MS) in 2D m/z–retention time format and need to identify and discriminate multiple analytes while avoiding false peak detections inherent in conventional peak picking. Apply this skill particularly when working with low-concentration analytes (ppb level) where conventional peak picking suffers high error rates, or when you require comprehensive, multivariate characterization of marker features rather than isolated m/z or retention time values.

## When NOT to use

- Input is already a peak table or feature matrix (i.e., peaks have already been picked); this skill operates on raw 2D MS maps, not on downstream feature tables.
- You require targeted identification of known metabolites with reference spectra; this skill is designed for untargeted, multivariate discovery of novel marker features.
- Your data has already been processed through conventional peak picking and you only have peak centroids; the skill requires the full 2D m/z–retention time image to learn spatial analyte signatures.

## Inputs

- raw chromatography–mass spectrometry data (GC-MS or LC-MS) in NetCDF or vendor format
- two-dimensional m/z vs retention time MS map (image-like array)
- image-processed 2D MS map with enhanced signal-to-noise ratio

## Outputs

- discriminated analyte labels/clusters mapped to 2D m/z–retention time space
- multivariate marker features identified for each analyte (m/z, retention time, and spatial co-occurrence patterns)
- visualized 2D map with analyte discrimination and marker feature annotations
- error rates for signal acquisition and marker identification (quantitative evaluation)

## How to apply

After loading raw MS data and applying image processing (noise suppression, signal-to-noise ratio enhancement) to the 2D m/z–retention time map, train a machine learning classifier on the spatially encoded analyte signatures in the processed 2D plane. The classifier discriminates individual analytes by learning their characteristic patterns in m/z–retention time space. Following classification, extract marker features for each discriminated analyte directly from the spatial patterns in the 2D map without performing separate peak picking. Validate discrimination success by comparing error rates (signal acquisition and marker identification) against a baseline (e.g., XCMS) on the same datasets. The rationale is that analytes exhibit distinct spatial 'signatures' in the 2D MS map; machine learning on these signatures captures multivariate structure that conventional univariate peak picking misses.

## Related tools

- **NPFimg** (Implements the complete pipeline (image processing + machine learning classification) for 2D MS map processing and analyte discrimination; the primary tool implementing this skill.) — github.com/poomcj/NPFimg
- **XCMS** (Baseline comparator for conventional peak picking and marker identification error rates; used to validate NPFimg discrimination performance.)

## Evaluation signals

- Quantitative error rates for signal acquisition and marker identification are lower than XCMS baseline on identical datasets (the article reports 'lower error rates of signal acquisition and marker identification' as the validation metric).
- Marker features are successfully identified and visualized in the 2D m/z–retention time space without invoking conventional peak picking; verify that output marker features are NOT derived from a separate peak-picking step.
- At parts-per-billion (ppb) concentration levels, the discriminated analytes and their marker features are correctly identified in case study samples (aroma odor and human breath); confirm feasibility in low-concentration regimes.
- Discriminated analyte clusters in 2D space do not overlap spuriously; spatial separation of analyte signatures in m/z–retention time should be clear and interpretable.
- Output marker features are multivariate (capturing both m/z and retention time co-occurrence patterns) rather than univariate peak centroids; verify that the marker feature representation includes spatial context from the 2D map.

## Limitations

- The skill has been demonstrated only on GC-MS data (aroma odor and human breath case studies) and limited LC-MS applications; generalization to all MS platforms and sample matrices is not yet established.
- Machine learning performance depends on the quality of image preprocessing (noise suppression, signal enhancement); poor preprocessing will degrade classification accuracy.
- The article and README provide no details on hyperparameter tuning, classifier choice (algorithm type), training data requirements, or convergence criteria; practitioners must refer to the full publication (10.1021/acs.analchem.1c03163) or source code for implementation specifics.
- No changelog or version history is available in the repository documentation; reproducibility across different NPFimg versions is not documented.

## Evidence

- [readme] NPFimg automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning: "NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning"
- [readme] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features"
- [readme] comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections: "comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections"
- [readme] Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification"
- [readme] feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion level: "feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion level"
- [readme] potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS: "potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
