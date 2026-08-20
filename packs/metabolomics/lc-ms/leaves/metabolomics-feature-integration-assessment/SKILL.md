---
name: metabolomics-feature-integration-assessment
description: Use when after XCMS peak picking and fillPeaks() when you have xcmsEIC and filled xcmsSet objects and need to systematically flag low-quality or unreliable peak integrations prior to statistical modeling or machine learning classification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-feature-integration-assessment

## Summary

Compute 12 peak-quality metrics from XCMS-derived EIC and peak objects to systematically assess the quality of integrated chromatographic peaks in untargeted LC-MS metabolomics data. This skill enables automated detection of low-quality peak integrations before downstream analysis.

## When to use

Apply this skill after XCMS peak picking and fillPeaks() when you have xcmsEIC and filled xcmsSet objects and need to systematically flag low-quality or unreliable peak integrations prior to statistical modeling or machine learning classification. Use it as a prerequisite step when building quality-assessment classifiers or filtering EICs by retention-time consistency and peak shape integrity.

## When NOT to use

- Input data have not been processed through XCMS getEIC() and fillPeaks(); the skill requires xcmsEIC and filled xcmsSet objects as prerequisites.
- You are working with targeted or data-independent acquisition (DIA) LC-MS; this skill is designed for untargeted metabolomics with extracted ion chromatograms.
- Peak integrations have already been manually curated or filtered by other quality criteria; this skill is most valuable when applied systematically to unfiltered XCMS output.

## Inputs

- xcmsEIC object (from XCMS getEIC())
- filled xcmsSet object (from XCMS fillPeaks())
- optional EIC labels CSV dataframe
- flatness.factor parameter (default sensitivity to noise)

## Outputs

- M×12 or M×13 peak-quality metrics matrix (M = number of peaks)
- evalObj with slots eicPts, eicPeakData, eicNos
- columns for each of 12 metrics, EIC number, and optionally class label

## How to apply

Load the xcmsEIC object (from XCMS getEIC()) and filled xcmsSet object (from fillPeaks()), optionally along with an EIC labels CSV. Call getEvalObj() on the xcmsEIC and filled objects to extract retention time, intensity, and peak characteristic data into an evalObj with slots eicPts, eicPeakData, and eicNos. Then invoke getPeakQualityMetrics() with the evalObj, optional eicLabels dataframe, and flatness.factor parameter (default sensitivity to noise) to compute 12 metrics: Apex Max-Boundary Ratio, Elution Shift, FWHM2Base, Jaggedness, Modality, Retention-Time Consistency, Symmetry, Gaussian Similarity, Sharpness, Triangle Peak Area Similarity Ratio, Zig-Zag Index, and one additional metric. The function returns an M×13 matrix (with labels) or M×12 (without labels) where M is the number of peaks, with columns for each metric, EIC number, and optionally class label. Use the resulting metric matrix as input to downstream classifiers or as a feature set for quality filtering.

## Related tools

- **MetaClean** (R package that implements getEvalObj() and getPeakQualityMetrics() functions to compute 12 peak-quality metrics from XCMS EIC and peak objects) — https://github.com/KelseyChetnik/MetaClean
- **XCMS** (Upstream preprocessing software that generates xcmsEIC objects via getEIC() and filled xcmsSet objects via fillPeaks(), which are direct inputs to this skill)
- **R** (Programming language and environment in which MetaClean is implemented and executed)
- **caret** (Optional downstream R package for training machine learning classifiers on the computed peak-quality metrics)

## Examples

```
evalObj <- getEvalObj(xcmsEIC = xcmsEIC_obj, xcmsSet = filled_xcmsSet); pqm <- getPeakQualityMetrics(evalObj = evalObj, eicLabels = labels_df, flatness.factor = 1.0)
```

## Evaluation signals

- The returned matrix has dimensions M×12 (without labels) or M×13 (with labels), where M equals the total number of peaks in the xcmsSet; verify row count matches expected peak count.
- All 12 metric columns (Apex Max-Boundary Ratio, Elution Shift, FWHM2Base, Jaggedness, Modality, Retention-Time Consistency, Symmetry, Gaussian Similarity, Sharpness, TPASR, Zig-Zag Index, and one additional) contain numeric values without missing values across all rows.
- EIC number column values match the range of EIC indices in the input xcmsEIC object and are unique per row.
- Metric values fall within plausible ranges (e.g., ratios near 0–1, consistency scores within expected variance bounds); spot-check a subset of peaks to verify metrics are not extreme or NaN.
- Optional class labels (if provided) appear in the final column and match the eicLabels input dataframe; verify no label misalignment or row duplication.

## Limitations

- The skill depends entirely on upstream XCMS preprocessing quality; poor peak picking or retention time alignment in XCMS will propagate into the metric calculations.
- The flatness.factor parameter controls sensitivity to noise; no explicit guidance is provided in the article for tuning this parameter for specific instrument or data characteristics.
- The 12-metric set is adapted from published literature but may not capture all sources of peak integration artifacts; validation against independent manual curation is recommended for each new dataset or instrument.
- The skill does not perform clustering or outlier detection on the metrics themselves; users must apply downstream classification, filtering, or statistical methods to act on the metric matrix.
- EIC labels (optional) must be provided externally as a CSV or dataframe; the skill does not infer or validate label consistency with the XCMS objects.

## Evidence

- [other] MetaClean computes 12 peak-quality metrics (Apex Max-Boundary Ratio, Elution Shift, FWHM2Base, Jaggedness, Modality, Symmetry, Sharpness, Gaussian Similarity, Retention-Time Consistency, TPASR, Zig-Zag Index, and one additional metric) from XCMS-derived EIC and peak objects using getEvalObj followed by getPeakQualityMetrics functions.: "MetaClean computes 12 peak-quality metrics...from XCMS-derived EIC and peak objects using getEvalObj followed by getPeakQualityMetrics functions."
- [other] Call getEvalObj on the xcmsEIC and fill objects to extract retention time, intensity, and peak characteristic data into an evalObj with slots eicPts, eicPeakData, and eicNos.: "Call getEvalObj on the xcmsEIC and fill objects to extract retention time, intensity, and peak characteristic data into an evalObj with slots eicPts, eicPeakData, and eicNos."
- [other] Call getPeakQualityMetrics with the evalObj, optional eicLabels dataframe, and flatness.factor parameter (default sensitivity to noise) to compute the 11 metrics.: "Call getPeakQualityMetrics with the evalObj, optional eicLabels dataframe, and flatness.factor parameter (default sensitivity to noise)"
- [other] Return an M×13 (with labels) or M×12 (without labels) matrix where M is the number of peaks, with columns for each metric, EIC number, and optionally class label.: "Return an M×13 (with labels) or M×12 (without labels) matrix where M is the number of peaks, with columns for each metric, EIC number, and optionally class label."
- [readme] MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data.: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data."
- [readme] It is an R package and can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS.: "It is an R package and can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS."
