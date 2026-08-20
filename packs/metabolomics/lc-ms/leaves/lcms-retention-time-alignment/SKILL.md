---
name: lcms-retention-time-alignment
description: Use when when XCMS-aligned LC-MS data shows coefficient of variation (CV) above expected thresholds for known features, or when analyzing long-duration experiments (>1 week) or large cohorts (>100 samples) where global warping functions are known to fail due to compound-specific RT drift structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ncGTW
  - R
  - graphical time warping (GTW)
  - dynamic time warping (DTW)
  - xcms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`'
- ncGTW is an R package developed as a plug-in of xcms
- This algorithm is improved from graphical time warping (GTW) [@gtw16], a popular dynamic time warping (DTW)
- graphical time warping (GTW) [@gtw16], a popular dynamic time warping (DTW) based alignment method
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-MS retention time alignment

## Summary

Detect and correct misaligned retention time (RT) features in LC-MS data by applying neighbor-wise compound-specific graphical time warping (ncGTW) to generate individualized warping functions that replace XCMS global warping assumptions. This skill reduces coefficient of variation in peak-filled features and improves downstream grouping and quantification accuracy.

## When to use

When XCMS-aligned LC-MS data shows coefficient of variation (CV) above expected thresholds for known features, or when analyzing long-duration experiments (>1 week) or large cohorts (>100 samples) where global warping functions are known to fail due to compound-specific RT drift structures. Use this skill when you suspect misaligned feature groups despite XCMS preprocessing, particularly if features exhibit disjoint sample subsets or systematically deviate from baseline alignment at different m/z values.

## When NOT to use

- XCMS alignment already produces CV values within acceptable range (< 0.15) for all features of interest — ncGTW is designed for refinement of suboptimal alignments, not routine preprocessing.
- Sample cohort is small (< 20 samples) and acquisition duration is short (< 24 hours) — global XCMS warping functions are generally adequate in low-drift scenarios.
- Input data is not LC-MS or does not have retention time dimension — ncGTW is specific to chromatographic alignment.

## Inputs

- xcmsSet object (XCMS-aligned LC-MS feature groups)
- ncGTWinputs object (preprocessed profile data and metadata)
- Retention time structure metadata for samples

## Outputs

- Refined RT warping functions (replacing XCMS corrected RT)
- Realigned xcmsSet object with adjusted retention times
- Coefficient of variation (CV) comparisons for realigned features
- Peak-filled feature matrix with improved alignment accuracy

## How to apply

Load preprocessed LC-MS data into R with XCMS alignment results (xcmsSet object) and metadata in ncGTWinputs format. Execute ncGTWalign() with individualized warping functions for each compound and constraint edges on neighboring samples, specifying parallel sample grouping (parSamp) and worker processes (bpParam) to handle large datasets. Pass the ncGTWalign() output through adjustRT() to refine RT warping functions, replacing the original XCMS corrected RT values (xcmsLargeWin@rt$corrected) with ncGTW-derived coefficients. Apply fillPeaks to the realigned results and compute coefficient of variation (CV) values for previously misaligned features using compCV(). Compare CV before and after ncGTW realignment to quantify improvement; expect reductions in CV (e.g., feature 1: 0.369 → 0.229; feature 2: 0.351 → 0.119 in typical cases).

## Related tools

- **ncGTW** (Core alignment engine; computes neighbor-wise compound-specific graphical time warping functions and generates refined RT corrections) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Upstream preprocessing and initial feature detection; provides xcmsSet object and baseline warping functions that ncGTW refines and replaces)
- **R** (Execution environment for ncGTW, xcms, and CV computation functions)

## Examples

```
ncGTW_result <- ncGTWalign(ncGTWinputs, xcmsSet_obj, parSamp=TRUE, bpParam=BiocParallel::SerialParam()); xcmsSet_adjusted <- adjustRT(xcmsSet_obj, ncGTW_result); xcmsSet_filled <- fillPeaks(xcmsSet_adjusted); cv_values <- compCV(xcmsSet_filled, feature_ids=c('feature_1', 'feature_2'))
```

## Evaluation signals

- Coefficient of variation (CV) for realigned features decreases after ncGTW peak-filling compared to XCMS peak-filling (target: CV reduction > 30% for affected features).
- ncGTWalign() output passes adjustRT() without errors and produces new warping coefficients that differ from original XCMS corrected RT values.
- Feature retention times across samples show tighter clustering post-realignment when plotted against sample order or acquisition time (visual or quantitative alignment quality metric).
- Peak-regrouping or peak-filling downstream of ncGTW realignment does not produce duplicate or conflicting feature assignments, indicating correct warping function replacement.
- Misaligned features identified by ncGTW (those with sufficiently small p-values and disjoint sample subsets) show systematic RT offset patterns that are corrected after adjustRT() application.

## Limitations

- ncGTW assumes XCMS has already performed initial feature detection and grouping; it does not replace the entire XCMS pipeline, only refines RT alignment.
- Identification of misaligned features relies on p-value thresholds and higher-resolution alignment results; performance degrades if initial XCMS feature detection is severely compromised.
- ncGTW requires sufficient sample diversity and neighboring sample relationships to enforce constraint edges; very sparse or highly heterogeneous experiments may limit effectiveness.
- Computational cost scales with sample count and compound complexity; parallel processing (bpParam) is recommended but requires sufficient memory and CPU availability.
- No changelog is provided in the repository; version compatibility with xcms and R versions must be verified independently.

## Evidence

- [intro] ncGTW can identify and realign misaligned features due to XCMS assumption: "ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples. That is, ncGTW avoids the popular but not accurate"
- [other] ncGTW produces lower CV than XCMS after peak-filling for two misaligned features: "ncGTW realignment reduced CV after peak-filling from 0.369 to 0.229 for feature 1 and from 0.351 to 0.119 for feature 2, compared to XCMS warping functions."
- [other] ncGTWalign() and adjustRT() workflow generates new RT warping functions: "ncGTWalign() accepts loaded profile data (ncGTWinputs) and an xcmsSet object, applies alignment with configurable parallel sample grouping (parSamp parameter) and workers (bpParam parameter), then"
- [readme] ncGTW purpose and role as XCMS plug-in: "The purpose of ncGTW is to detect and fix the bad alignments in the LC-MS data. Currently, ncGTW is implemented in a R-package as a plug-in for XCMS."
- [readme] ncGTW identifies misaligned features using p-value and sample subset criteria: "ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result"
