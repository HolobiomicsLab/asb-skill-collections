---
name: peak-picking-avoidance-ms-analysis
description: Use when analyzing raw 2D MS data (m/z vs. retention time maps) where conventional peak picking introduces unacceptable error rates, particularly in untargeted metabolomics or chemometrics studies requiring sensitive marker identification at trace levels (e.g., parts per billion).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - XCMS
  - NPFimg
  techniques:
  - LC-MS
  - CE-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-picking-avoidance-ms-analysis

## Summary

A workflow that bypasses conventional peak picking in chromatography–mass spectrometry analysis by combining image processing and machine learning to directly identify multivariate marker features on the m/z vs. retention time plane, reducing false positive peak detections.

## When to use

Apply this skill when analyzing raw 2D MS data (m/z vs. retention time maps) where conventional peak picking introduces unacceptable error rates, particularly in untargeted metabolomics or chemometrics studies requiring sensitive marker identification at trace levels (e.g., parts per billion). Use when you have chromatography–MS data and need to discriminate analytes and identify marker features without relying on peak detection algorithms.

## When NOT to use

- When input data are already in feature table or pre-picked peak format — the skill targets raw 2D MS maps.
- When targeted analysis with known m/z and retention time windows is sufficient — peak picking avoidance adds complexity without benefit.
- When conventional peak picking error rates are acceptable for the downstream application (e.g., rough screening with high tolerance for false positives).

## Inputs

- raw chromatography–mass spectrometry data file (NetCDF or vendor format)
- two-dimensional MS map (m/z vs. retention time plane)

## Outputs

- discriminated analytes with spatial signatures in m/z–retention time plane
- multivariate marker features (chemo-/biomarker signatures) per analyte
- visualization of analytes and marker features on processed 2D MS map

## How to apply

Load raw chromatography–MS data as a 2D map (m/z vs. retention time coordinates). Apply image processing techniques to enhance signal-to-noise ratio and suppress background noise in the 2D plane. Use machine learning classification to discriminate individual analytes based on their spatial signatures in the m/z–retention time domain. Identify marker features for each discriminated analyte directly from the processed 2D map without performing conventional peak picking. Visualize the discriminated analytes and their associated marker features on the processed map to confirm correct analyte discrimination and feature localization. The rationale is that spatial signature-based discrimination in image space avoids cascading errors from peak detection thresholds and false positive peak assignments.

## Related tools

- **NPFimg** (implements the complete workflow of image processing and machine learning-based marker identification on 2D MS maps without conventional peak picking) — https://github.com/poomcj/NPFimg
- **XCMS** (benchmark tool for conventional peak picking and signal acquisition; NPFimg comparison demonstrates lower error rates)

## Evaluation signals

- Signal acquisition error rate is lower than conventional peak picking (e.g., XCMS); count false positives and false negatives in marker identification against a reference set.
- Marker identification accuracy is higher than baseline methods; verify by independent confirmation or external validation (e.g., comparison with authentic standards).
- Visualization of discriminated analytes on the 2D MS map shows coherent spatial clustering in m/z–retention time space without spurious fragmented signatures.
- The method preserves detection sensitivity at trace levels (parts per billion range) as demonstrated in GC–MS case studies; verify signal-to-noise ratio of recovered markers exceeds detection threshold.
- Marker features are reproducible across replicate analyses; consistency of m/z and retention time coordinates within acceptable tolerance confirms stable machine learning discrimination.

## Limitations

- Applicability demonstrated primarily on GC–MS data; generalization to liquid chromatography–MS and other modalities requires validation.
- Method performance depends on quality of image processing preprocessing steps (noise suppression, signal enhancement); poor input signal quality may degrade machine learning discrimination.
- Machine learning classification requires sufficient training or annotation data to learn analyte spatial signatures; performance not established for completely novel analyte classes.
- No changelog or version history provided; reproducibility and evolution of the method may be difficult to track across updates.

## Evidence

- [intro] Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections.: "comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections"
- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features.: "processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features"
- [intro] Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification.: "lower error rates of signal acquisition and marker identification compared to XCMS"
- [intro] NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS: "potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
- [readme] We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning.: "automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning"
