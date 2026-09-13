---
name: image-based-feature-extraction-ms-maps
description: Use when you have a two-dimensional MS map (m/z vs retention time) from
  GC–MS or LC–MS data and need to discriminate analytes and identify marker features
  without false positives from peak picking; particularly useful for untargeted metabolomics
  at ppb sensitivity (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - NPFimg
  - XCMS
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c03163?ref=
  title: NPFimg
- doi: 10.1021/acs.analchem.1c03163
  title: ''
evidence_spans:
- github.com__poomcj__NPFimg
- We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker
  features of analytes in chromatography–mass spectrometry (MS) data by combining
  image processing and
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg
- Comparison with the widely used XCMS shows the excellent reliability of NPFimg,
  in that it has lower error rates of signal acquisition and marker identification.
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

# image-based-feature-extraction-ms-maps

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automatically identify multivariate chemo-/biomarker features in chromatography–mass spectrometry data by treating the m/z vs retention time plane as a two-dimensional image and applying image processing combined with machine learning, avoiding conventional peak picking errors.

## When to use

You have a two-dimensional MS map (m/z vs retention time) from GC–MS or LC–MS data and need to discriminate analytes and identify marker features without false positives from peak picking; particularly useful for untargeted metabolomics at ppb sensitivity (e.g., breath samples, aroma analysis) where conventional peak picking introduces errors.

## When NOT to use

- Input is already a peak table or feature matrix (feature extraction already complete).
- The analysis requires targeted detection of known compounds with predefined m/z windows; use targeted methods instead.
- MS data are in high-dimensional or sparse formats not amenable to 2D image representation (e.g., very wide m/z ranges with minimal signal).

## Inputs

- Two-dimensional MS map (m/z vs retention time image from GC–MS or LC–MS)
- Raw chromatography–mass spectrometry data in a format compatible with NPFimg

## Outputs

- Identified marker features with m/z values, retention times, and feature scores
- Visualization of marker features on the m/z–retention time plane
- Structured feature table with automated detection predictions

## How to apply

Load the two-dimensional MS map (m/z vs retention time) from your chromatography–MS dataset into NPFimg as a raw image. Apply NPFimg's image processing and machine learning pipeline to process the map and automatically discriminate analytes without invoking conventional peak picking. The algorithm detects marker features directly from the image representation, generating automated detection scores. Visualize the identified marker features back onto the m/z–retention time space to verify spatial coherence. Export predictions as a structured table with m/z values, retention times, and feature scores. Validate by comparing error rates and feature recovery against a reference method such as XCMS.

## Related tools

- **NPFimg** (Core image processing and machine learning pipeline for automated marker feature identification from 2D MS maps) — github.com/poomcj/NPFimg
- **XCMS** (Reference baseline for comparison of signal acquisition error rates and marker identification reliability)

## Evaluation signals

- Identified marker features cluster spatially on the m/z–retention time map without fragmentation or spurious isolated points.
- Error rates for signal acquisition and marker identification are lower than or comparable to XCMS (the established reference method).
- Feature scores are consistent across replicate MS maps from the same sample class.
- Marker features exhibit m/z and retention time values within expected ranges for known or putative analytes in the sample matrix.
- Exported feature table is non-empty, schema-valid (contains m/z, retention time, and score columns), and contains no NaN or infinite values in core columns.

## Limitations

- The method requires two-dimensional MS map data; sparse or fragmented chromatographic signals may not form coherent image structures suitable for image processing.
- Performance at very low abundance (sub-ppb) or in extremely complex backgrounds is not explicitly demonstrated beyond the case studies (aroma odor, human breath at ppb level).
- The README notes 'limited applications' and indicates the method is 'potentially applicable' to diverse metabolomics/chemometrics, suggesting validation is not yet complete for all MS modalities (GC–MS and LC–MS are confirmed).
- No formal comparison with other image-based or machine learning–based peak picking alternatives beyond XCMS is provided.

## Evidence

- [intro] NPFimg automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning: "NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
- [intro] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [intro] Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [intro] Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [intro] The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion level: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [readme] We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and machine learning: "We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
- [intro] NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS: "NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
- [readme] While this study shows the limited applications, NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS: "While this study shows the limited applications, NPFimg is potentially applicable to data processing in diverse metabolomics/chemometrics using GC–MS and liquid chromatography–MS"
