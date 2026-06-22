---
name: two-dimensional-ms-image-processing
description: Use when you have raw GC–MS or LC–MS data represented as a two-dimensional map (m/z axis vs. retention time axis) and need to identify chemo-/biomarker features across multiple analytes simultaneously, especially when conventional peak picking produces high false-positive or false-negative rates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# two-dimensional-ms-image-processing

## Summary

Apply image processing and machine learning to two-dimensional chromatography–mass spectrometry maps (m/z vs. retention time) to automatically discriminate analytes and identify multivariate marker features without conventional peak picking. This skill avoids false peak detections inherent in traditional workflows and is demonstrable at parts per billion sensitivity levels.

## When to use

You have raw GC–MS or LC–MS data represented as a two-dimensional map (m/z axis vs. retention time axis) and need to identify chemo-/biomarker features across multiple analytes simultaneously, especially when conventional peak picking produces high false-positive or false-negative rates, or when you require comprehensive signal characterization across untargeted metabolomics workflows.

## When NOT to use

- Input is already a one-dimensional feature matrix or peak table; this skill requires raw 2D spectral data.
- The analysis goal is targeted metabolomics with pre-defined compound lists; this skill is designed for untargeted marker discovery.
- Conventional peak picking has already been applied successfully with low false-positive rates; this skill's value is primarily in avoiding peak-picking artifacts.

## Inputs

- raw chromatography–mass spectrometry data (GC–MS or LC–MS format)
- two-dimensional MS map (m/z vs. retention time plane)

## Outputs

- discriminated analyte identities and spatial extents in the 2D map
- multivariate marker features per analyte (m/z and retention time coordinates)
- visualized 2D map with annotated analytes and marker features
- signal acquisition and marker identification error rates

## How to apply

Load the raw chromatography–mass spectrometry data and construct a two-dimensional map with m/z on one axis and retention time on the other. Apply image processing techniques (e.g., filtering, enhancement) to increase signal-to-noise ratio and suppress noise artifacts in the 2D plane. Use machine learning classification to discriminate individual analytes based on their spatial signatures (contiguous regions of high intensity) in the m/z–retention time plane. Identify marker features for each discriminated analyte by analyzing the spatial topology of the processed 2D map, rather than applying threshold-based peak picking. Visualize the discriminated analytes and their associated marker features on the processed map to confirm spatial coherence and separation. Compare error rates of signal acquisition and marker identification against a reference tool (e.g., XCMS) to validate reliability.

## Related tools

- **NPFimg** (implements image processing and machine learning classification to process 2D MS maps and automatically identify multivariate marker features) — github.com/poomcj/NPFimg
- **XCMS** (baseline reference tool for conventional peak picking; comparison demonstrates lower error rates of NPFimg in signal acquisition and marker identification)

## Evaluation signals

- Discriminated analytes are spatially contiguous (no fragmentation) and separated in the m/z–retention time plane without overlap artifacts.
- Error rates of signal acquisition and marker identification are lower than or comparable to XCMS or other conventional peak-picking tools on the same dataset.
- Marker features are recoverable at or near the sensitivity threshold demonstrated in the article (parts per billion level for GC–MS).
- Visual inspection of the annotated 2D map shows clear correspondence between machine-learning-derived spatial regions and expected analyte locations; no false positive regions at noise baseline.
- The number and identity of identified markers remain stable across multiple independent runs (if stochasticity is present in the ML classifier).

## Limitations

- The method is sensitive to the quality of image processing steps; inadequate noise suppression or signal enhancement can degrade discriminative power.
- Machine learning classification requires sufficient training signal (spatial extent and intensity) per analyte; very low-abundance analytes may not be reliably discriminated.
- Performance has been demonstrated primarily on GC–MS and breath/aroma samples; generalization to other ionization methods or sample matrices is not explicitly characterized in the article.
- No changelog or versioning information is available in the repository; reproducibility across code versions is uncertain.

## Evidence

- [other] NPFimg combines image processing and machine learning to automatically identify multivariate chemo-/biomarker features and comprehensively characterize signals in MS data without the conventional peak picking process, which suffers from false peak detections.: "automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning"
- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify marker features without performing conventional peak picking.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] The method avoids false peak detections inherent in conventional workflows.: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] Performance is demonstrated at parts per billion sensitivity on GC–MS.: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [intro] Error rates of signal acquisition and marker identification are lower with NPFimg than XCMS.: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] The method is applicable to diverse metabolomics and chemometrics workflows using GC–MS and LC–MS.: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
- [readme] README confirms method combines image processing and machine learning on 2D MS maps to discriminate analytes and identify marker features.: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
