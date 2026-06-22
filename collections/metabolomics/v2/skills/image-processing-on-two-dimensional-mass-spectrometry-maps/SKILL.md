---
name: image-processing-on-two-dimensional-mass-spectrometry-maps
description: Use when when you have raw GC–MS data in two-dimensional m/z × retention time format (NetCDF or proprietary binary) and need to identify marker features across aroma or breath samples at parts-per-billion concentration levels, particularly when conventional peak picking introduces false positives.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
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

# image-processing-on-two-dimensional-mass-spectrometry-maps

## Summary

Apply image processing and machine learning to two-dimensional mass spectrometry maps (m/z vs. retention time) to automatically identify and visualize multivariate chemo-/biomarker features without conventional peak picking. This skill enables marker identification in GC–MS data at parts-per-billion sensitivity levels with lower error rates than traditional peak-picking workflows.

## When to use

When you have raw GC–MS data in two-dimensional m/z × retention time format (NetCDF or proprietary binary) and need to identify marker features across aroma or breath samples at parts-per-billion concentration levels, particularly when conventional peak picking introduces false positives or when you lack predefined peak models.

## When NOT to use

- Input data is already a processed feature table or peak list (skip to statistical analysis).
- Target analytes have very high m/z variability or retention time drift that exceeds the image registration assumptions.
- Analysis requires targeted quantitation with predefined MS/MS fragmentation patterns; image processing alone may miss structured spectral relationships.

## Inputs

- raw GC–MS data in two-dimensional m/z vs. retention time format (NetCDF, proprietary binary)
- two-dimensional MS map (m/z × retention time image array)
- reference marker annotations or ground-truth peak positions (for validation)

## Outputs

- identified marker feature coordinates (m/z, retention time pairs)
- visualized marker features overlaid on 2D MS map
- signal acquisition error rates
- marker identification error rates
- quantified analyte abundance or intensity values

## How to apply

Load raw GC–MS data as a two-dimensional image array where axes represent m/z and retention time. Apply NPFimg's image processing pipeline to segment and discriminate analytes within the 2D MS map without invoking traditional peak detection algorithms. The method combines spatial filtering, connected-component analysis, and machine learning classifiers trained on reference marker positions to reduce false signal artifacts. Quantify error rates for both signal acquisition and marker identification against a baseline (e.g., XCMS) on the same dataset. The workflow avoids peak picking altogether, instead leveraging pixel-level image features to directly extract marker coordinates and intensities.

## Related tools

- **NPFimg** (Primary implementation: combines image processing and machine learning to process 2D MS maps and identify marker features without peak picking) — github.com/poomcj/NPFimg
- **XCMS** (Baseline comparison tool: traditional peak-picking workflow used to benchmark NPFimg error rates on the same GC–MS datasets)

## Evaluation signals

- Error rates for signal acquisition and marker identification are lower than or comparable to XCMS on the same dataset.
- Marker feature coordinates (m/z, retention time) align with visually inspected 2D MS map features and known reference compounds.
- No false peaks are introduced by conventional peak-picking artifacts (e.g., baseline noise spikes).
- Parts-per-billion level marker sensitivity is achieved and documented in results table.
- Marker features are successfully visualized on the 2D MS map without conventional peak picking step.

## Limitations

- Method has been demonstrated only on aroma odor and human breath GC–MS case studies; generalization to other sample types or LC–MS workflows requires further validation.
- Image registration and spatial alignment assumptions may fail if retention time or m/z calibration drifts significantly across a batch.
- No changelog or version history provided in repository; reproducibility and software maintenance status uncertain.

## Evidence

- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] Marker identification feasibility is demonstrated in case studies of aroma odor and human breath on GC–MS at parts per billion level: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] NPFimg has lower error rates of signal acquisition and marker identification compared to XCMS: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [readme] NPFimg automatically identifies multivariate chemo-/biomarker features by combining image processing and machine learning: "automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning"
