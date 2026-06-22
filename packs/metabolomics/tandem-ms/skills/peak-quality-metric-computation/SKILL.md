---
name: peak-quality-metric-computation
description: Use when you have completed XCMS preprocessing (getEIC() and fillPeaks()) on untargeted LC-MS metabolomics data and need to assign per-peak quality scores prior to manual curation, classifier training, or downstream statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - MetaClean
  - R
  - XCMS
  techniques:
  - LC-MS
  - tandem-MS
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

# peak-quality-metric-computation

## Summary

Compute 12 chromatographic peak-quality metrics from XCMS-derived extracted ion chromatograms (EICs) and peak objects to quantify peak morphology, consistency, and noise resilience in untargeted LC-MS metabolomics data. These metrics serve as input features for machine learning classifiers that detect low-quality peak integrations.

## When to use

You have completed XCMS preprocessing (getEIC() and fillPeaks()) on untargeted LC-MS metabolomics data and need to assign per-peak quality scores prior to manual curation, classifier training, or downstream statistical analysis. Apply this skill when peak integration quality is uncertain and you need objective, morphology-based descriptors to distinguish true peaks from noise artifacts, baseline distortions, or mis-integrated boundaries.

## When NOT to use

- Your LC-MS data have not yet been preprocessed by XCMS (getEIC and fillPeaks) — this skill requires XCMS-derived peak and EIC objects as input.
- You are working with targeted MS/MS data or selected reaction monitoring (SRM) rather than untargeted full-scan LC-MS — MetaClean is designed for untargeted metabolomics workflows.
- Your peaks have already been manually curated or validated by an expert and you need only summary statistics; computing quality metrics is unnecessary overhead in that case.

## Inputs

- xcmsEIC object (from XCMS getEIC() function)
- filled xcmsSet object (from XCMS fillPeaks() function)
- optional: EIC labels CSV (dataframe mapping EIC numbers to class labels for supervised evaluation)

## Outputs

- Peak quality metrics matrix (M × 12 or M × 13 numeric matrix where M = number of peaks; columns are the 12 metrics plus EIC number, optionally plus class label)
- evalObj (R S4 object with slots eicPts, eicPeakData, eicNos; intermediate data structure)

## How to apply

Load the xcmsEIC object (output from XCMS getEIC() function) and the filled xcmsSet object (from fillPeaks()) into the MetaClean pipeline. Call getEvalObj() on these objects to extract retention time, intensity, and peak characteristic data into an evalObj with slots eicPts, eicPeakData, and eicNos. Then invoke getPeakQualityMetrics() with the evalObj, optional eicLabels dataframe, and a flatness.factor parameter (default sensitivity to noise) to compute the 12 metrics: Apex Max-Boundary Ratio, Elution Shift, FWHM2Base, Jaggedness, Modality, Retention-Time Consistency, Symmetry, Gaussian Similarity, Sharpness, Triangle Peak Area Similarity Ratio, Zig-Zag Index, and one additional metric. The function returns an M×13 matrix (with class labels) or M×12 matrix (without labels), where M is the number of peaks, with one column per metric plus an EIC number column. Optionally apply rsdFilter() beforehand to exclude EICs with high retention-time variance (>user-defined RSD %) to reduce computational load and exclude inherently unreliable peaks.

## Related tools

- **MetaClean** (Provides getEvalObj() and getPeakQualityMetrics() functions to extract XCMS data and compute the 12 peak-quality metrics) — https://github.com/KelseyChetnik/MetaClean
- **XCMS** (Produces xcmsEIC and xcmsSet objects (via getEIC() and fillPeaks()) that serve as input to peak-quality metric computation)
- **R** (Execution environment for MetaClean; caret package provides underlying machine learning infrastructure)

## Examples

```
getEvalObj(xcmsEIC = eic_obj, xcmsSet = filled_set) %>% getPeakQualityMetrics(eicLabels = labels_df, flatness.factor = 1.0)
```

## Evaluation signals

- Output matrix has M rows (one per peak) and exactly 12 or 13 columns (depending on label inclusion); no NaN or Inf values except where explicitly permitted by metric definition.
- Each metric column contains numeric values within expected ranges documented in Zhang & Zhao (2014) (e.g., Symmetry and Gaussian Similarity in [0, 1], FWHM2Base and Elution Shift typically < 1 for well-formed peaks).
- EIC number column contains unique integer identifiers matching the input xcmsSet; no duplicate or missing EIC assignments.
- Peaks with high Jaggedness, Zig-Zag Index, or low Gaussian Similarity scores correspond visually to noisy, irregular chromatograms; peaks with low values correspond to smooth, Gaussian-like traces (manual spot-check on a subset).
- If optional RSD filtering was applied beforehand, all retained EICs pass the RSD threshold; if rsdFilter() was not used, all EICs from the input xcmsSet are represented.

## Limitations

- The 12 metrics are adapted from published literature but are not universally validated across all instrument platforms, ionization methods, or compound classes; performance may vary for atypical metabolites or extreme retention-time ranges.
- Computation requires accurate peak boundary detection and retention-time alignment from XCMS; garbage-in, garbage-out: poorly fitted XCMS parameters will propagate into unreliable metric values.
- The flatness.factor parameter (noise sensitivity) is a tuning knob; no automated method is provided to select an optimal value; users must either accept the default or empirically validate on their own data.
- The skill produces only per-peak descriptors; it does not classify peaks as 'good' or 'bad' — classification requires a separately trained machine learning model and is a distinct skill.
- Retention-Time Consistency metric requires replicate injections or repeated acquisitions; for single-run data, this metric will be uninformative or require external reference standards.

## Evidence

- [intro] MetaClean computes 12 peak-quality metrics adapted from literature to detect low-quality peaks in untargeted LC-MS metabolomics data: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data"
- [methods] getEvalObj extracts retention time, intensity, and peak characteristics; getPeakQualityMetrics computes the 11 named metrics from the evalObj: "The function getEvalObj is called to extract the relevant data from the three objects provided by ther user"
- [methods] The 11 metrics include Apex Max-Boundary Ratio, Elution Shift, FWHM2Base, Jaggedness, Modality, Retention-Time Consistency, Symmetry, Gaussian Similarity, Sharpness, Triangle Peak Area Similarity Ratio, and Zig-Zag Index: "The function getPeakQualityMetrics uses the evalObj objects to calculate each of the 11 peak quality metrics."
- [methods] Output is an M×13 matrix with labels or M×12 without labels, where M is the number of peaks and columns include each metric, EIC number, and optionally class label: "Return an M×13 (with labels) or M×12 (without labels) matrix where M is the number of peaks, with columns for each metric, EIC number, and optionally class label."
- [intro] Integration with XCMS preprocessing: can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize XCMS: "can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS"
- [readme] The 12 peak-quality metrics used by MetaClean are adapted from Zhang & Zhao (2014) and Eshghi et al. (2018): "The 12 peak-quality metrics used by MetaClean are adapted from the following publications"
