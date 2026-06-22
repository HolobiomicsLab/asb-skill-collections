---
name: untargeted-lc-ms-data-preprocessing
description: Use when when you have raw untargeted LC-MS metabolomics data and need to detect low-quality or mis-integrated peaks in an XCMS-processed xcmsSet object before performing metabolite annotation, statistical analysis, or biomarker discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaClean
  - R
  - XCMS
  - caret
  techniques:
  - LC-MS
derived_from:
- doi: 10.1007/s11306-020-01738-3
  title: MetaClean
- doi: 10.1186/1471-2105-15-s11-s5
  title: ''
evidence_spans:
- MetaClean is a package for building classifiers to identify low quality integrations in untargeted metabolomics data.
- '`MetaClean` provides 8 classification algorithms (implemented with the R package `caret`) for building a predictive model.'
- getEvalObj is called to extract the relevant data from the three objects provided by ther user and store them in an object of class evalObj
- It is an R package and can be easily incorporated
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaclean_cq
    doi: 10.1007/s11306-020-01738-3
    title: MetaClean
  dedup_kept_from: coll_metaclean_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01738-3
  all_source_dois:
  - 10.1007/s11306-020-01738-3
  - 10.1186/1471-2105-15-s11-s5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# untargeted-lc-ms-data-preprocessing

## Summary

Preprocessing of untargeted LC-MS metabolomics data using XCMS to extract ion chromatograms (EICs) and fill missing peaks, followed by computation of 12 peak-quality metrics via MetaClean to detect and flag low-quality peaks for downstream quality assessment and machine learning classification.

## When to use

When you have raw untargeted LC-MS metabolomics data and need to detect low-quality or mis-integrated peaks in an XCMS-processed xcmsSet object before performing metabolite annotation, statistical analysis, or biomarker discovery. Apply this skill if you want to leverage both XCMS preprocessing and automated quality flagging to reduce false positives in downstream analysis.

## When NOT to use

- Input is already a manually curated, high-confidence peak table or feature matrix — preprocessing is redundant.
- Raw data has not been preprocessed by XCMS (e.g., already baseline-corrected or de-noised by another pipeline) — getEvalObj expects XCMS-specific object structure.
- Your goal is targeted analysis of known metabolites with pre-defined m/z and retention time windows — untargeted EIC extraction and 12-metric quality scoring is unnecessary overhead.

## Inputs

- raw untargeted LC-MS data in NetCDF or mzML format
- xcmsEIC object from XCMS getEIC() function
- filled xcmsSet object from XCMS fillPeaks() function
- optional EIC labels CSV file with class labels
- optional RSD filtering threshold (percentage)

## Outputs

- M×13 or M×12 peak-quality metrics matrix (M = number of peaks; columns: 12 metrics + EIC number ± class label)
- evalObj with slots eicPts, eicPeakData, eicNos
- filtered EIC list (if RSD filter applied)

## How to apply

First, use XCMS to perform standard preprocessing: run getEIC() to extract ion chromatograms from the raw data, then use fillPeaks() to fill missing peak data across samples, producing a filled xcmsSet object. Next, optionally apply RSD filtering using rsdFilter() to remove high-variance EICs by relative standard deviation threshold. Then call getEvalObj() on the xcmsEIC and filled xcmsSet objects to extract retention time, intensity, and peak characteristic data into an evalObj with slots eicPts, eicPeakData, and eicNos. Finally, call getPeakQualityMetrics() with the evalObj and flatness.factor parameter (default sensitivity to noise) to compute the 12 peak-quality metrics: Apex Max-Boundary Ratio, Elution Shift, FWHM2Base, Jaggedness, Modality, Retention-Time Consistency, Symmetry, Gaussian Similarity, Sharpness, Triangle Peak Area Similarity Ratio, Zig-Zag Index, and EIC number. The output is an M×13 matrix (with optional class labels) or M×12 matrix (without labels), where M is the number of peaks, enabling downstream classifier training or quality thresholding.

## Related tools

- **XCMS** (performs peak detection and retention time alignment on raw LC-MS data; provides xcmsEIC and xcmsSet objects required as input to getEvalObj) — https://github.com/sneumann/xcms
- **MetaClean** (computes 12 peak-quality metrics via getEvalObj and getPeakQualityMetrics; enables RSD filtering and downstream machine learning classification of peak quality) — https://github.com/KelseyChetnik/MetaClean
- **caret** (R package used by MetaClean to implement 8 machine learning classification algorithms for peak quality prediction)
- **R** (scripting environment for executing XCMS and MetaClean functions)

## Examples

```
library(MetaClean); evalObj <- getEvalObj(xcmsEIC, xcmsSet_filled); pqm <- getPeakQualityMetrics(evalObj, flatness.factor = 0.5)
```

## Evaluation signals

- evalObj contains non-empty eicPts, eicPeakData, and eicNos slots with matching dimensions across samples
- Peak-quality metrics matrix M has M rows equal to the total number of detected peaks and exactly 12 metric columns (or 13 with EIC number, or 14 with labels)
- All 12 peak-quality metric columns contain numerical values (no NAs or infinities) within expected ranges (e.g., 0–1 for normalized metrics, non-negative for counts)
- Optional RSD filtering reduces EIC count; remaining EICs have RSD below the specified threshold
- Metric distributions show multimodality or bimodality consistent with high-quality vs. low-quality peak separation (verifiable via downstream classifier training accuracy or ROC-AUC)

## Limitations

- The getEvalObj and getPeakQualityMetrics functions require XCMS-compliant xcmsEIC and xcmsSet objects; incompatible peak detection outputs or preprocessing pipelines will cause function failure.
- Flatness.factor parameter (sensitivity to noise) is user-defined; suboptimal choice may lead to over- or under-flagging of borderline peaks.
- The 12 metrics are adapted from literature and may not capture all sources of peak degradation in novel instrument platforms or non-standard ionization modes.
- RSD filtering is optional and can remove biologically valid peaks with high intrinsic variance; thresholds should be validated against biological replicates or pooled QC samples.

## Evidence

- [readme] MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data"
- [readme] can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS: "can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS"
- [methods] The function getEvalObj is called to extract the relevant data from the three objects provided by ther user: "The function getEvalObj is called to extract the relevant data from the three objects"
- [methods] The function getPeakQualityMetrics uses the evalObj objects to calculate each of the 11 peak quality metrics.: "The function getPeakQualityMetrics uses the evalObj objects to calculate each of the 11 peak quality metrics"
- [methods] the user can optionally filter out EICs by RSD % using the rsdFilter() function: "the user can optionally filter out EICs by RSD % using the rsdFilter() function"
- [other] Return an M×13 (with labels) or M×12 (without labels) matrix where M is the number of peaks, with columns for each metric, EIC number, and optionally class label.: "Return an M×13 (with labels) or M×12 (without labels) matrix where M is the number of peaks"
