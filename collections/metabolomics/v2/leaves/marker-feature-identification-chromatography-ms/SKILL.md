---
name: marker-feature-identification-chromatography-ms
description: Use when when processing raw chromatography–mass spectrometry data (GC–MS
  or LC–MS) as a 2D m/z vs retention time map and you need to identify and visualize
  marker features for analyte discrimination without relying on conventional peak
  picking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - XCMS
  - NPFimg
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c03163?ref=
  title: NPFimg
- doi: 10.1021/acs.analchem.1c03163
  title: ''
evidence_spans:
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg,
  in that it has lower error rates of signal acquisition and marker identification.
- github.com__poomcj__NPFimg
- We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker
  features of analytes in chromatography–mass spectrometry (MS) data by combining
  image processing and
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

# marker-feature-identification-chromatography-ms

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automatically identify multivariate chemo-/biomarker features in chromatography–mass spectrometry data by combining image processing and machine learning on 2D MS maps (m/z vs retention time), bypassing conventional peak picking to reduce false detections. Designed for GC–MS and LC–MS workflows at ppb-level sensitivity.

## When to use

When processing raw chromatography–mass spectrometry data (GC–MS or LC–MS) as a 2D m/z vs retention time map and you need to identify and visualize marker features for analyte discrimination without relying on conventional peak picking. Apply this skill when false peak detection is a concern in untargeted metabolomics or chemometrics workflows, especially at low concentration levels (parts-per-billion sensitivity).

## When NOT to use

- Input is already a processed feature table or peak matrix; NPFimg requires raw 2D m/z vs retention time data.
- Peak picking and retention time alignment have already been completed successfully; NPFimg replaces rather than supplements conventional peak picking.
- Analysis requires targeted quantification of pre-defined metabolites; NPFimg is designed for untargeted multivariate marker discovery.

## Inputs

- Raw chromatography–mass spectrometry data files (GC–MS or LC–MS)
- Two-dimensional MS map (m/z vs retention time matrix)
- Sample metadata (e.g., aroma odor, human breath, or other analyte classes)

## Outputs

- Discriminated analytes with spatial signatures in m/z–retention time plane
- Identified marker features for each analyte
- Visualized 2D MS map with annotated marker features
- Signal acquisition and marker identification error rates
- Feature table or marker list suitable for downstream metabolomics analysis

## How to apply

Load raw chromatography–mass spectrometry data in 2D m/z vs retention time format. Apply image processing techniques to enhance signal-to-noise ratio and suppress noise across the 2D map. Use machine learning classification to discriminate individual analytes based on their spatial signatures in the m/z–retention time plane without performing conventional peak picking. Identify and extract marker features for each discriminated analyte directly from the processed 2D map. Quantify error rates for signal acquisition and marker identification, optionally benchmarking against XCMS baseline to verify improvement in reliability and reduction of false positives.

## Related tools

- **NPFimg** (Primary image processing and machine learning pipeline for discriminating analytes and identifying marker features from 2D MS maps) — https://github.com/poomcj/NPFimg
- **XCMS** (Baseline comparison tool for signal acquisition and marker identification; NPFimg demonstrates lower error rates than XCMS on the same datasets)

## Evaluation signals

- Marker features are successfully identified and visualized on the 2D MS map for all discriminated analytes without conventional peak picking artifacts or false peak detections.
- Signal acquisition and marker identification error rates computed for NPFimg are lower than XCMS baseline on the same GC–MS or LC–MS dataset.
- Marker identification feasibility is demonstrated at parts-per-billion concentration levels with quantified sensitivity and specificity metrics.
- Analytes are correctly discriminated based on spatial signatures in the m/z–retention time plane, confirmed by case study results on aroma odor and human breath samples.
- Output feature table or marker list is compatible with downstream untargeted metabolomics workflows and shows chemical interpretability (plausible m/z and retention time ranges for known compound classes).

## Limitations

- Limited applications demonstrated; case studies focus on aroma odor and human breath GC–MS at ppb level; broader applicability to diverse sample types or higher-mass LC–MS data requires additional validation.
- Potential applicability to untargeted metabolomics of human breath is noted but not fully established; generalization to other biological matrices or sample types may require method tuning.
- No changelog or version history provided in repository documentation; reproducibility across different code versions or parameter settings is not explicitly addressed.

## Evidence

- [readme] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [readme] Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [readme] The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [readme] Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification.: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [readme] NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
