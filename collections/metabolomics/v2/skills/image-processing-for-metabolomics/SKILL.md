---
name: image-processing-for-metabolomics
description: Use when you have GC–MS or LC–MS data represented as a two-dimensional map (m/z vs retention time) and need to identify analyte signals and marker features while minimizing false peak detections.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0769
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

# image-processing-for-metabolomics

## Summary

Apply image processing and machine learning to two-dimensional chromatography–mass spectrometry maps (m/z vs retention time) to automatically identify multivariate chemo-/biomarker features without conventional peak picking. This skill reduces false positive and false negative detection rates compared to traditional peak detection methods like XCMS.

## When to use

You have GC–MS or LC–MS data represented as a two-dimensional map (m/z vs retention time) and need to identify analyte signals and marker features while minimizing false peak detections. Particularly useful when conventional peak picking introduces high error rates or when working with low-abundance analytes (parts per billion level) in untargeted metabolomics workflows.

## When NOT to use

- Input data is already a peak-picked feature table or pre-processed peak list; the skill is designed to replace, not follow, conventional peak picking.
- Targeted analysis with predefined m/z and retention time windows where traditional peak picking methods are already reliable.
- Data from instruments or workflows where the m/z vs retention time map representation is not available or not applicable.

## Inputs

- Two-dimensional MS map (m/z vs retention time)
- GC–MS raw chromatography-mass spectrometry data
- LC–MS raw chromatography-mass spectrometry data

## Outputs

- Identified analyte signals with reduced false detection rates
- Marker feature assignments with visualization
- Error rate metrics (false positives, false negatives, detection accuracy)
- Multivariate chemo-/biomarker feature matrix

## How to apply

Load the two-dimensional MS map (m/z vs retention time chromatography-mass spectrometry data) into NPFimg. Apply the image processing and machine learning pipeline to process the map and discriminate analytes without conventional peak picking, which suffers from false positives and negatives. The method identifies and visualizes marker features across the m/z and retention time dimensions simultaneously. Compute error metrics for signal acquisition (false positives, false negatives, detection accuracy) and marker identification accuracy. Compare error rates against a baseline method (e.g., XCMS with standard peak detection parameters) to quantify improvement in reliability.

## Related tools

- **NPFimg** (Primary tool implementing image processing and machine learning pipeline to process two-dimensional MS maps and identify marker features without conventional peak picking) — https://github.com/poomcj/NPFimg
- **XCMS** (Baseline comparison tool for quantifying error rate improvement; runs standard peak detection for benchmarking against NPFimg performance)

## Evaluation signals

- Error rates (false positives, false negatives) for signal acquisition are lower in NPFimg compared to XCMS baseline.
- Marker identification accuracy is higher in NPFimg compared to XCMS, particularly at parts per billion detection levels.
- Visualized marker features align with known analyte compounds in the case study (aroma odor, human breath).
- No conventional peak picking artifacts (e.g., false peaks from baseline noise) appear in the final feature set.
- Output marker feature matrix contains multivariate features spanning both m/z and retention time dimensions without reduction to univariate peak lists.

## Limitations

- Method is demonstrated on GC–MS case studies of aroma odor and human breath; generalization to other biological matrices or analytical conditions may require validation.
- Requires two-dimensional MS map representation; not applicable to data formats lacking m/z and retention time information.
- The README notes 'For the other details, I will update soon', suggesting incomplete documentation of parameters, thresholds, and edge cases.
- Performance comparison is limited to XCMS; robustness against other peak picking algorithms (e.g., MZmine, OpenMS) is not reported.

## Evidence

- [readme] NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize marker features: "NPFimg processes a two-dimensional MS map (m/z vs retention time) to discriminate analytes and identify and visualize the marker features."
- [readme] Avoids conventional peak picking process which suffers from false peak detections: "Our approach allows us to comprehensively characterize the signals in MS data without the conventional peak picking process, which suffers from false peak detections."
- [readme] Lower error rates compared to XCMS: "Comparison with the widely used XCMS shows the excellent reliability of NPFimg, in that it has lower error rates of signal acquisition and marker identification."
- [readme] Demonstrated on GC–MS case studies at parts per billion level: "The feasibility of marker identification is successfully demonstrated in case studies of aroma odor and human breath on gas chromatography–mass spectrometry (GC–MS) even at the parts per billion"
- [readme] Combines image processing and machine learning for multivariate feature identification: "We present a method named NPFimg, which automatically identifies multivariate chemo-/biomarker features of analytes in chromatography–mass spectrometry (MS) data by combining image processing and"
