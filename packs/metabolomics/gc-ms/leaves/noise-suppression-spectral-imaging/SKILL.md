---
name: noise-suppression-spectral-imaging
description: Use when your input is a raw two-dimensional MS map (m/z vs retention time) derived from chromatography–mass spectrometry data with poor signal-to-noise characteristics, and you need to discriminate individual analytes and identify marker features reliably.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - XCMS
  - NPFimg
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03163?ref=
  title: NPFimg
- doi: 10.1021/acs.analchem.1c03163
  title: ''
evidence_spans:
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

# Noise Suppression in Spectral Imaging

## Summary

Apply image processing techniques to enhance signal-to-noise ratio and suppress noise in two-dimensional chromatography–mass spectrometry maps (m/z vs retention time) prior to analyte discrimination and feature identification. This step is critical for reducing false peak detections inherent in conventional peak picking.

## When to use

Your input is a raw two-dimensional MS map (m/z vs retention time) derived from chromatography–mass spectrometry data with poor signal-to-noise characteristics, and you need to discriminate individual analytes and identify marker features reliably. Apply this skill before machine learning classification or feature extraction steps when visual inspection reveals background noise, baseline drift, or low-intensity signal artifacts that risk false peak detection.

## When NOT to use

- Input is already a feature table or peak list; noise suppression on spectral imaging is not applicable to post-processed tabular data.
- The MS data is from a targeted analysis with pre-defined peak regions and known analytes; conventional peak picking may be more appropriate than image-based suppression.
- Signal intensity is already very high relative to background noise (SNR >> 10); additional noise suppression may risk over-smoothing and loss of fine spectral detail.

## Inputs

- Raw two-dimensional MS map (m/z vs retention time) from gas chromatography–mass spectrometry or liquid chromatography–mass spectrometry
- NetCDF or mzML format chromatography–mass spectrometry data files

## Outputs

- Noise-suppressed 2D MS map (m/z vs retention time) with enhanced signal-to-noise ratio
- Preprocessed image suitable for machine learning classification and marker feature identification

## How to apply

Load the raw 2D MS map (m/z vs retention time plane) from NetCDF or mzML chromatography–mass spectrometry output. Apply image processing techniques—such as Gaussian smoothing, morphological operations, or wavelet denoising—to enhance the signal-to-noise ratio across the entire 2D surface. The rationale is to suppress noise artifacts while preserving true analyte signals that span distinct spatial signatures in the m/z–retention time plane. This preprocessing step precedes machine learning classification and avoids the error-prone conventional peak picking process, which suffers from false positive and false negative detections. Validate the processed map visually and quantitatively (e.g., peak intensity distribution, background level reduction) before proceeding to analyte discrimination.

## Related tools

- **NPFimg** (Integrated image processing and machine learning pipeline that incorporates noise suppression of 2D MS maps as a preprocessing step for multivariate chemo-/biomarker feature identification) — github.com/poomcj/NPFimg
- **XCMS** (Conventional peak picking and signal processing tool; NPFimg's noise suppression approach is designed as a superior alternative to XCMS for automated marker feature identification with lower error rates)

## Evaluation signals

- Visual inspection confirms that background noise is reduced across the 2D m/z–retention time map while true analyte signals (spatial clusters) remain sharp and localized.
- Quantitative metric: Signal-to-noise ratio measured at known marker feature locations increases by at least 2–5×, or background root-mean-square intensity decreases measurably.
- Comparison with XCMS output demonstrates fewer false positive peaks (spurious noise artifacts misclassified as analytes) and fewer false negative peaks (true low-intensity analytes preserved).
- Downstream machine learning classification achieves higher discrimination accuracy (e.g., lower misclassification rate) on the noise-suppressed map compared to raw input.
- Marker features identified post-suppression are reproducible across replicate MS acquisitions and align with known reference analytes in case studies (e.g., aroma compounds, breath metabolites at ppb level).

## Limitations

- Over-aggressive noise suppression (e.g., excessive Gaussian smoothing) can broaden peak profiles and blur fine spectral features, reducing analyte discrimination precision.
- Image processing parameters (kernel size, threshold levels, morphological structuring element) are data-dependent and may require optimization for different MS platforms, ionization modes, or chromatographic methods.
- The approach is demonstrated primarily on GC–MS and breath MS datasets; generalization to other untargeted metabolomics workflows (e.g., lipidomics, proteomics) is stated as potential but not yet validated in the article.
- Noise suppression alone does not address systematic effects such as batch drift, instrument calibration errors, or chemical background; additional preprocessing steps may be needed.
- No formal changelog or versioning scheme was found in the repository, limiting reproducibility of historical analyses.

## Evidence

- [other] Apply image processing techniques to enhance signal-to-noise ratio and suppress noise in the 2D map: "Apply image processing techniques to enhance signal-to-noise ratio and suppress noise in the 2D map."
- [intro] Comprehensively characterize signals in MS data without the conventional peak picking process, which suffers from false peak detections: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] NPFimg has lower error rates of signal acquisition and marker identification compared to XCMS: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [readme] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize marker features: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
