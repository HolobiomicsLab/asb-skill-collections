---
name: automated-peak-detection-without-conventional-picking
description: Use when you have a two-dimensional GC–MS or LC–MS dataset (m/z vs retention time) and need to identify discriminative analyte features without relying on conventional peak picking algorithms. This is especially valuable when analyzing complex, low-abundance samples (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - NPFimg
  - XCMS
  techniques:
  - LC-MS
  - GC-MS
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

# Automated Peak Detection Without Conventional Picking

## Summary

This skill applies image processing and machine learning to chromatography–mass spectrometry data to automatically identify multivariate marker features directly from two-dimensional MS maps (m/z vs retention time), bypassing conventional peak picking which suffers from false detections. It is particularly suited for untargeted metabolomics of complex samples like human breath at parts per billion sensitivity levels.

## When to use

Apply this skill when you have a two-dimensional GC–MS or LC–MS dataset (m/z vs retention time) and need to identify discriminative analyte features without relying on conventional peak picking algorithms. This is especially valuable when analyzing complex, low-abundance samples (e.g., human breath, aroma compounds) where conventional peak detection generates false positives, or when untargeted marker discovery is the goal rather than targeted quantitation.

## When NOT to use

- When input has already been processed through conventional peak picking and stored as a feature matrix or peak list—the method is designed to work directly on raw or minimally processed 2D MS maps.
- When high-throughput targeted quantitation with predefined compound libraries is the primary goal; this skill prioritizes marker discovery and multivariate discrimination over absolute quantitation.
- When retention time shifts are severe and unaligned across samples; the method assumes retention time consistency or requires pre-alignment of the 2D MS maps.

## Inputs

- Two-dimensional MS map (m/z vs retention time) from GC–MS or LC–MS instrument
- Chromatography–mass spectrometry raw data or processed intensity matrix
- Sample metadata (control vs. case grouping for multivariate feature extraction)

## Outputs

- Structured feature table with m/z values, retention times, and feature scores
- Visualization of identified marker features overlaid on m/z–retention time space
- Classification results discriminating analyte signals from background

## How to apply

Load the two-dimensional MS map into NPFimg as a gridded intensity image. Apply the image processing pipeline to enhance signal-to-noise contrast and normalize the spatial representation of m/z and retention time axes. Deploy the machine learning classifier to discriminate true analyte signals from noise and baseline artifacts across the entire map without pre-specifying peak boundaries. The algorithm automatically outputs marker features with associated m/z values, retention times, and feature scores. Validate results by comparing with conventional peak-picking tools (e.g., XCMS) and examining signal acquisition error rates and marker identification reliability.

## Related tools

- **NPFimg** (Primary tool implementing image processing and machine learning pipeline for automated marker feature detection from 2D MS maps without conventional peak picking) — https://github.com/poomcj/NPFimg
- **XCMS** (Benchmark comparison tool for conventional peak picking; used to validate NPFimg's lower error rates in signal acquisition and marker identification)

## Evaluation signals

- Error rates in signal acquisition and marker identification are lower or comparable to XCMS when applied to the same dataset, as documented in the article's comparison study.
- Identified marker features exhibit m/z and retention time values consistent with expected analyte properties and avoid false detections known to plague conventional peak picking.
- Visualization of marker features on the m/z–retention time space shows spatial coherence and discrimination between control and case groups; features cluster in distinct regions rather than scattered randomly.
- Feature scores output by the algorithm are reproducible across replicate analyses and correlate with analyte abundance or biomarker relevance in downstream validation (e.g., ROC analysis).
- The method successfully identifies multivariate chemo-/biomarker features at parts per billion sensitivity levels in complex matrices (e.g., human breath) without manual peak boundary definition.

## Limitations

- Method requires that the two-dimensional MS map be properly registered and aligned across samples; severe retention time drifts or m/z calibration errors will degrade performance.
- Limited documentation and update history noted in the repository; external users may encounter undocumented edge cases or parameter sensitivities not fully described in the primary publication.
- Applicability is demonstrated primarily for GC–MS and LC–MS at parts per billion levels; performance on other chromatographic platforms or at different dynamic ranges has not been systematically evaluated.
- The machine learning classifier is trained and validated on aroma odor and human breath datasets; generalization to substantially different metabolite classes or sample matrices requires independent validation.

## Evidence

- [intro] NPFimg automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning: "We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
- [intro] Bypasses conventional peak picking which suffers from false peak detections: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] Process two-dimensional MS map to identify and visualize marker features: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] Lower error rates compared to XCMS in signal acquisition and marker identification: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] Successfully demonstrated on human breath at parts per billion level: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] Potential applicability to untargeted metabolomics of human breath: "In addition, we show the potential applicability of NPFimg to the untargeted metabolomics of human breath."
- [intro] Broadly applicable to diverse metabolomics/chemometrics using GC–MS and LC–MS: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
- [readme] README confirms automated identification without conventional peak picking: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
