---
name: breath-biomarker-discovery
description: Use when you have GC–MS data from human breath samples and need to identify marker metabolites for disease diagnosis, phenotyping, or biomarker discovery without a predefined target list. Your data is noisy or conventional peak picking has produced high false-positive rates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# breath-biomarker-discovery

## Summary

Automated identification of multivariate chemo-/biomarker features in untargeted GC–MS analysis of human breath samples using image processing and machine learning on two-dimensional MS maps (m/z vs retention time). This skill bypasses conventional peak picking to reduce false detections and enable detection at parts per billion levels.

## When to use

You have GC–MS data from human breath samples and need to identify marker metabolites for disease diagnosis, phenotyping, or biomarker discovery without a predefined target list. Your data is noisy or conventional peak picking has produced high false-positive rates. You want to detect signals at very low abundance (ppb level) across the full m/z–retention time space simultaneously rather than targeting known compounds.

## When NOT to use

- Your input is already a curated feature table or peak list; NPFimg operates on raw or minimally processed MS maps.
- You are performing targeted metabolomics with a predefined analyte list; NPFimg is designed for untargeted discovery.
- Your breath samples are from a disease or condition outside the validation scope (aroma odor and human breath); generalization to other matrices is untested.

## Inputs

- GC–MS dataset from human breath samples (raw or processed as two-dimensional m/z vs retention time map)
- NetCDF or vendor-native MS data format containing chromatographic and mass spectrometric dimensions

## Outputs

- Structured table of marker feature predictions with m/z values, retention times, and feature scores
- Visualization of identified marker features on the m/z–retention time space
- Discriminated analyte profiles without conventional peak picking artifacts

## How to apply

Load the two-dimensional MS map (m/z vs retention time axes) from your breath GC–MS dataset into NPFimg. Apply the image processing and machine learning pipeline to process the MS map and discriminate analytes, which treats the chromatogram–MS space as an image rather than performing conventional peak picking. Use NPFimg's automated detection algorithm to identify marker features, outputting m/z values, retention times, and feature scores for each candidate biomarker. Visualize the identified markers on the m/z–retention time plane to confirm spatial coherence. Compare results against XCMS or other standard tools to validate lower error rates in both signal acquisition and marker identification; the paper reports NPFimg achieves superior reliability in this comparison.

## Related tools

- **NPFimg** (Primary tool for image processing and machine learning-based marker feature identification on two-dimensional MS maps) — github.com/poomcj/NPFimg
- **XCMS** (Reference/comparison tool for conventional peak picking and marker identification; NPFimg demonstrates lower error rates in head-to-head evaluation)

## Evaluation signals

- Identified marker features cluster spatially on the m/z–retention time plane, indicating they represent distinct analytes rather than noise artifacts.
- Feature scores and retention times are reproducible across replicate breath samples from the same subject.
- Comparison with XCMS output shows NPFimg produces fewer false-positive peaks and false-negative marker omissions, quantified by error rates.
- Detected m/z values and retention times match known breath metabolites or literature references at ppb-level sensitivity.
- Marker features export as a well-formed table with non-null m/z, retention time, and feature score columns; no missing values in critical fields.

## Limitations

- Feasibility is demonstrated only on GC–MS breath data and aroma odor case studies; generalization to other breath disease states or sample matrices is not yet validated.
- The method requires well-resolved two-dimensional MS maps; highly complex mixtures with severe co-elution may degrade discrimination.
- No changelog or version history is available in the repository, limiting traceability of method refinements.
- The README indicates further details will be updated; current documentation is minimal and relies on the full published paper for methodology.

## Evidence

- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion level.: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification.: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] NPFimg shows potential applicability to untargeted metabolomics of human breath.: "NPFimg shows potential applicability to untargeted metabolomics of human breath."
- [intro] NPFimg automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning.: "NPFimg automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning."
- [readme] We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning.: "We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
