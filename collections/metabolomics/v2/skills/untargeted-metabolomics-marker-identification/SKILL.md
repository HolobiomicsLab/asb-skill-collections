---
name: untargeted-metabolomics-marker-identification
description: Use when when you have untargeted GC–MS or LC–MS data in the form of a two-dimensional m/z vs retention time map and need to identify marker features without conventional peak picking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2269
  tools:
  - NPFimg
  - XCMS
  techniques:
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# untargeted-metabolomics-marker-identification

## Summary

Automated identification of multivariate chemo-/biomarker features in untargeted metabolomics data by processing two-dimensional chromatography–mass spectrometry maps (m/z vs retention time) using image processing and machine learning, without conventional peak picking. This skill is particularly suited for human breath GC–MS analysis and other low-abundance analyte detection scenarios where false peak detection is a concern.

## When to use

When you have untargeted GC–MS or LC–MS data in the form of a two-dimensional m/z vs retention time map and need to identify marker features without conventional peak picking. Specifically applicable when: (1) you are analyzing human breath or aroma samples at parts per billion sensitivity levels, (2) you want to avoid false peak detections inherent in conventional peak picking, (3) you need multivariate marker discrimination rather than simple peak lists, and (4) you seek automated rather than manual feature annotation.

## When NOT to use

- Input data are already peak-picked, aligned, and formatted as a feature abundance table; use this skill on raw 2D m/z vs retention time maps, not pre-processed feature matrices.
- You require targeted metabolomics with predefined compound lists and MS/MS fragmentation matching; NPFimg is designed for untargeted discovery.
- Your MS instrument produces very high noise or baseline artifacts that are inseparable from signal by image processing alone; preprocessing or instrument optimization may be needed first.

## Inputs

- Two-dimensional MS map (m/z vs retention time) from GC–MS or LC–MS acquisition
- Raw chromatography–mass spectrometry data in a format compatible with NPFimg import (e.g., NetCDF or vendor-neutral formats)

## Outputs

- Structured table of marker feature predictions with m/z values, retention times, and feature scores
- Visualization of identified marker features overlaid on the m/z–retention time space
- Discriminated analyte feature set suitable for downstream metabolomics or chemometrics analysis

## How to apply

Load the two-dimensional MS map (m/z vs retention time) from your chromatography–MS dataset into NPFimg. Apply the NPFimg image processing and machine learning pipeline, which treats the MS map as an image and applies automated detection algorithms to discriminate analytes and identify marker features across the m/z–retention time space. The method avoids conventional peak picking by processing the full 2D structure, reducing false positives. Automated detection yields marker features with associated m/z values, retention times, and feature scores. Export predictions to a structured table and visualize identified marker features on the m/z–retention time space to confirm spatial coherence and biological plausibility. Comparison with XCMS or other tools can validate reliability, particularly for signal acquisition and marker identification error rates.

## Related tools

- **NPFimg** (Core image processing and machine learning pipeline for automated marker feature identification from 2D m/z vs retention time maps) — https://github.com/poomcj/NPFimg
- **XCMS** (Comparison benchmark tool for conventional peak picking and marker identification; used to validate NPFimg's lower error rates)

## Evaluation signals

- Marker features identified by NPFimg exhibit lower false positive rates and signal acquisition errors compared to XCMS on the same dataset.
- Identified m/z values and retention times cluster spatially on the 2D map without fragmentation across the time or m/z axis, indicating genuine analyte signals rather than noise artifacts.
- Exported feature scores correlate with known analyte concentrations or show expected abundance patterns across sample groups (e.g., human breath vs. blank).
- Visualization of marker features on the m/z–retention time map shows coherent, localized 2D regions rather than scattered isolated points.
- Downstream statistical or classification models using NPFimg-identified features show comparable or improved performance relative to conventional peak-picked features.

## Limitations

- Method feasibility is demonstrated primarily on GC–MS case studies of aroma odor and human breath; generalization to other sample matrices or LC–MS platforms requires additional validation.
- Effectiveness depends on data quality; very high baseline noise, instrumental drift, or poor peak resolution may compromise feature discrimination.
- Image processing heuristics (e.g., morphological operations, threshold parameters) are tuned for the case studies shown; transfer to different instrument types, columns, or MS scan rates may require parameter retuning.
- Repository documentation is minimal; the full methodological details are available only in the published article, which may hinder reproducibility or extension without access to the paper.

## Evidence

- [intro] NPFimg automatically identifies multivariate chemo-/biomarker features in chromatography–mass spectrometry data by combining image processing and machine learning: "We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
- [intro] NPFimg processes a 2D m/z vs retention time map to discriminate analytes and identify marker features without conventional peak picking: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features. Our approach allows us to comprehensively characterize the"
- [intro] Marker identification is demonstrated in human breath GC–MS case studies at parts per billion level sensitivity: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] NPFimg shows lower error rates than XCMS in signal acquisition and marker identification: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] NPFimg is applicable to untargeted metabolomics of human breath and diverse metabolomics/chemometrics using GC–MS and LC–MS: "In addition, we show the potential applicability of NPFimg to the untargeted metabolomics of human breath. While this study shows the limited applications, NPFimg is potentially applicable to data"
- [other] Workflow: load 2D MS map, apply image processing and machine learning pipeline, identify and export marker features with m/z, retention time, and scores: "Load the two-dimensional MS map (m/z vs retention time) from the breath GC–MS dataset into NPFimg. Apply NPFimg image processing and machine learning pipeline to process the MS map and discriminate"
