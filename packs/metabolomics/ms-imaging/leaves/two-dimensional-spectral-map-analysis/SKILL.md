---
name: two-dimensional-spectral-map-analysis
description: Use when you have GC–MS or LC–MS data represented as a two-dimensional map with m/z values on one axis and retention time on the other, and you need to identify analyte signals and chemo-/biomarker features while minimizing false positive and false negative peak detections.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - NPFimg
  - XCMS
  techniques:
  - LC-MS
  - GC-MS
  - MS-imaging
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# two-dimensional-spectral-map-analysis

## Summary

Analyze two-dimensional chromatography–mass spectrometry maps (m/z vs retention time) using image processing and machine learning to discriminate analytes and identify marker features without conventional peak picking. This approach reduces false peak detections and achieves lower error rates than traditional methods like XCMS.

## When to use

You have GC–MS or LC–MS data represented as a two-dimensional map with m/z values on one axis and retention time on the other, and you need to identify analyte signals and chemo-/biomarker features while minimizing false positive and false negative peak detections. This is particularly suitable when working with complex matrices (aroma, breath) at parts per billion sensitivity levels where conventional peak picking produces unacceptable error rates.

## When NOT to use

- Input is already a 1D peak list or feature table; the skill operates on raw 2D spectral maps and would require deconvolution.
- The analyte mixture is simple (few well-resolved peaks) and conventional peak picking already achieves acceptable error rates; additional complexity may not be justified.
- Data are from imaging mass spectrometry or spatial MS where spatial resolution and pixel-level interpretation differ fundamentally from chromatographic 2D maps.

## Inputs

- Two-dimensional MS map data (m/z vs retention time matrix; e.g., NetCDF, mzML, or proprietary GC–MS format)
- Raw GC–MS or LC–MS chromatography–mass spectrometry dataset

## Outputs

- Identified analyte signals and discriminated analyte locations in 2D spectral space
- Multivariate chemo-/biomarker features (marker feature map or feature list)
- Visualization of marker features overlaid on the 2D spectral map
- Error rate metrics (signal acquisition error rates and marker identification accuracy)

## How to apply

Load the two-dimensional MS map (m/z vs retention time chromatography–mass spectrometry data) into an image-processing pipeline such as NPFimg. Apply image processing and machine learning algorithms to the map to discriminate analytes and identify marker features directly from the spectral image without invoking conventional peak picking. The method exploits spatial structure in the 2D map to reduce false detections inherent in 1D peak-picking approaches. Compute error metrics (false positives, false negatives, detection accuracy) for signal acquisition and marker identification accuracy. Compare these metrics to a baseline (e.g., XCMS with standard peak detection parameters) to quantify the reduction in error rates achieved by avoiding conventional peak picking.

## Related tools

- **NPFimg** (Primary implementation: applies image processing and machine learning to 2D MS maps (m/z vs retention time) to identify analyte signals and marker features without conventional peak picking.) — https://github.com/poomcj/NPFimg
- **XCMS** (Comparison baseline: conventional peak detection method used to benchmark NPFimg's error rates for signal acquisition and marker identification.)

## Evaluation signals

- Quantified error rates for signal acquisition (false positives, false negatives) are lower than the baseline (XCMS) method.
- Marker identification accuracy is higher than the baseline; cross-validate identified features against independently confirmed markers or external reference standards.
- Visual overlay of identified marker features on the original 2D spectral map shows coherent spatial clustering and absence of scattered noise artifacts.
- The method successfully detects analytes at target sensitivity (parts per billion level for aroma and breath studies) without false peak picking artifacts.
- Reproducibility: independent runs on the same dataset or dataset replicates produce consistent marker feature identification and error metrics.

## Limitations

- The README states 'For the other details, I will update soon', indicating incomplete documentation of parameters, hyperparameters, and edge-case handling.
- Feasibility is demonstrated only on GC–MS case studies (aroma odor and human breath); applicability to other chromatography–mass spectrometry modalities (e.g., targeted LC–MS/MS) remains untested in the presented work.
- The method requires two-dimensional spectral structure; it is not applicable to pre-picked feature tables or 1D chromatograms alone.

## Evidence

- [intro] Processing workflow and output.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] Avoidance of conventional peak picking and rationale.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] Error rate comparison to baseline.: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] Demonstrated application domain and sensitivity level.: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] Broader applicability scope.: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
- [readme] README statement on core method.: "NPFimg automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning."
