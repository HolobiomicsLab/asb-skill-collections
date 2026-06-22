---
name: chromatographic-peak-detection-and-grouping
description: Use when when you have processed LC-MS data through XCMS alignment but suspect misaligned features due to retention-time drift over long acquisition periods (>1 week) or large sample batches (hundreds of samples), or when peak-filling produces unexpectedly high coefficient-of-variation (CV > 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
  tools:
  - ncGTW
  - R
  - xcms
  - graphical time warping (GTW)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`'
- ncGTW is an R package developed as a plug-in of xcms
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ncgtw_cq
    doi: 10.1093/bioinformatics/btaa037
    title: ncGTW
  dedup_kept_from: coll_ncgtw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaa037
  all_source_dois:
  - 10.1093/bioinformatics/btaa037
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-peak-detection-and-grouping

## Summary

Detect and group chromatographic peaks across LC-MS samples, then identify and correct misaligned feature groups using compound-specific warping functions. This skill bridges XCMS peak detection with ncGTW realignment to reduce coefficient-of-variation in aligned retention times.

## When to use

When you have processed LC-MS data through XCMS alignment but suspect misaligned features due to retention-time drift over long acquisition periods (>1 week) or large sample batches (hundreds of samples), or when peak-filling produces unexpectedly high coefficient-of-variation (CV > 0.3) for specific m/z features. Apply this skill after XCMS grouping but before downstream statistical analysis or peak-regrouping.

## When NOT to use

- Input data has already been processed through ncGTW or another specialized retention-time correction tool — applying this skill would introduce redundant warping.
- Coefficient-of-variation for all features is already < 0.15 after XCMS peak-filling — misalignment is unlikely and ncGTW realignment will not improve downstream analysis.
- Sample count is small (< 10–20 samples) or acquisition time is short (< 1 day) — ncGTW's constraint-based neighbor warping is optimized for large, long-duration studies where retention-time drift structures are pronounced.

## Inputs

- XCMS-aligned LC-MS feature table (xcmsSet object or equivalent)
- Raw LC-MS data in mzML, mzXML, or NetCDF format
- Baseline coefficient-of-variation values per feature (numeric vector)
- Sample metadata with temporal or batch structure

## Outputs

- ncGTW-realigned feature table with individualized retention-time warping functions
- Updated coefficient-of-variation values per feature after peak-filling
- Warping function curves for each compound across sample pairs
- Comparison table (XCMS CV vs. ncGTW CV for each misaligned feature)

## How to apply

First, load the XCMS-aligned dataset and compute CV values for each detected feature using compCV to establish a baseline (e.g., feature 1 CV = 0.369). Next, apply ncGTW's misalignment detection algorithm, which estimates p-values for each feature using higher-resolution alignment and identifies features with sufficiently small p-values and disjoint sample subsets. For misaligned features, invoke ncGTW's reference-free multiple alignment method, which performs pairwise alignments between samples while constraining warping functions on neighboring samples to estimate individualized warping functions for each compound. After ncGTW realignment, apply fillPeaks and recompute CV values to verify improvement (target: CV reduction to <0.25 for feature 1, <0.15 for feature 2). The realignment succeeds if CV values decrease substantially and remain consistent across the realigned feature set.

## Related tools

- **ncGTW** (Detects misaligned features from XCMS and realigns them using individualized compound-specific warping functions with neighbor-wise constraints) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Performs initial peak detection, grouping, and alignment; ncGTW operates as a plug-in to correct misaligned feature groups identified by XCMS)
- **R** (Host language for ncGTW and xcms packages; required for executing workflow steps (compCV, fillPeaks, alignment functions))
- **graphical time warping (GTW)** (Foundational dynamic time warping method upon which ncGTW improves by adding compound-specificity and neighbor constraints)

## Examples

```
library(ncGTW); library(xcms); xs_aligned <- xcmsSet(...); cv_before <- compCV(xs_aligned); xs_realigned <- ncGTW(xs_aligned); xs_realigned <- fillPeaks(xs_realigned); cv_after <- compCV(xs_realigned);
```

## Evaluation signals

- Coefficient-of-variation for realigned features decreases by ≥ 30% after ncGTW processing and peak-filling (e.g., 0.369 → 0.229 for feature 1, 0.351 → 0.119 for feature 2).
- P-values computed by ncGTW misalignment detection algorithm identify only a small, interpretable subset of features (not all features are flagged as misaligned).
- Warping function curves estimated for each compound are smooth and consistent across neighboring sample pairs (no sharp discontinuities or wild oscillations).
- Peak-regrouping accuracy (if evaluated) improves downstream or fragmentation pattern consistency is preserved for the realigned features.
- CV values remain stable and low when recomputed on an independent holdout sample set, indicating generalization of the learned warping functions.

## Limitations

- ncGTW assumes misalignment is driven by retention-time drift and compound-specific peak shifts; it will not correct for m/z calibration errors or ionization efficiency changes.
- The algorithm requires sufficient sample density and temporal structure (neighboring samples should be similar) for constraint-based warping to work; sparse or randomly ordered samples may not benefit.
- No changelog is available in the repository, so version-specific behavior and bug fixes are difficult to track.
- ncGTW's misalignment detection relies on p-value thresholding; results are sensitive to the choice of resolution used in higher-resolution alignment and the p-value cutoff.

## Evidence

- [other] ncGTW realignment reduced CV after peak-filling from 0.369 to 0.229 for feature 1 and from 0.351 to 0.119 for feature 2: "ncGTW realignment reduced CV after peak-filling from 0.369 to 0.229 for feature 1 and from 0.351 to 0.119 for feature 2, compared to XCMS warping functions."
- [intro] ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples: "ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples. That is, ncGTW avoids the popular but not accurate"
- [intro] xcms may have some misaligned features, and there is a function in ncGTW to identify such misalignments: "Due to the same warping function assumption or bad parameter settings, `xcms` may have some misaligned features, and there is a function in `ncGTW` to identify such misalignments. After identifying"
- [readme] ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result, where the p-value is given by the null hypothesis with accurate alignment. Second, we identifies all features with sufficiently small p-values and disjoint sample subsets.: "ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result, where the p-value is given by the"
- [readme] ncGTW performs all possible pairwise alignments between each two sample with the structure information in the dataset: "First, instead of set a certain reference, ncGTW performs all possible pairwise alignments between each two sample with the structure information in the dataset."
- [intro] ncGTW is an R package developed as a plug-in of xcms, a popular LC-MS data analysis R package: "`ncGTW` is an R package developed as a plug-in of `xcms`, a popular LC-MS data analysis R package"
