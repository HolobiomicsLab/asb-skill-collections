---
name: warping-function-comparison-across-algorithms
description: 'Use when after applying two or more LC-MS alignment algorithms (such as XCMS and ncGTW) to the same dataset, use this skill to determine which produces warping functions. Specifically, apply this when: (1) you have detected or suspect misaligned features in XCMS output (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - ncGTW
  - R
  - XCMS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# warping-function-comparison-across-algorithms

## Summary

Compare retention time (RT) warping functions produced by different LC-MS alignment algorithms (e.g., ncGTW vs. XCMS) by measuring their impact on coefficient of variation (CV) before and after peak-filling. This skill identifies which algorithm produces lower CV values and more accurate feature alignment for downstream quantitative analysis.

## When to use

After applying two or more LC-MS alignment algorithms (such as XCMS and ncGTW) to the same dataset, use this skill to determine which produces superior warping functions. Specifically, apply this when: (1) you have detected or suspect misaligned features in XCMS output (e.g., features with inconsistent RT across samples or high CV); (2) you want to benchmark ncGTW's individualized compound-specific warping functions against XCMS's global warping assumption; (3) downstream peak-filling or peak-regrouping accuracy is critical to your quantitative analysis; (4) your dataset has hundreds of samples or extended acquisition times (> 1 week) where RT drift structures vary by compound.

## When NOT to use

- Input data are already processed through peak-filling and regrouping; CV comparison at this stage may conflate alignment quality with peak-detection and statistical artifacts.
- Only one alignment algorithm has been applied; warping-function comparison requires at least two independent algorithms.
- Dataset contains fewer than ~10 samples or RT drift is negligible; both XCMS and ncGTW will produce similar CV values, making comparison inconclusive.

## Inputs

- XCMS-aligned LC-MS feature table with RT warping functions applied
- ncGTW-aligned LC-MS feature table with individualized compound-specific warping functions applied
- Detected misaligned feature groups (identified by ncGTW's two-criterion detection: p-value and sample subset disjointness)
- Raw LC-MS data in NetCDF, mzXML, or mzML format (for re-alignment if needed)

## Outputs

- Tabulated CV comparison table: XCMS CV (pre-fill, post-fill) vs. ncGTW CV (pre-fill, post-fill) for each feature
- CV reduction ratio for each algorithm and feature
- Verification of improvement: ratio of ncGTW CV reduction to XCMS CV reduction
- Qualitative assessment of which algorithm's warping functions better preserve or recover feature intensity relationships across samples

## How to apply

Load both the XCMS-aligned dataset and the ncGTW-aligned dataset into R. For each algorithm's output, apply the fillPeaks function to reconstruct missing peak intensities across samples. Then compute the coefficient of variation (CV) for each feature of interest using the compCV function, recording CV values before and after peak-filling. Compare the CV reduction ratios: calculate (CV_before − CV_after) / CV_before × 100% for each algorithm and feature pair. Interpret lower CV values and higher reduction ratios as evidence of superior warping function quality; ncGTW's individualized warping functions per compound with constraint edges on neighboring samples should yield better CV metrics than XCMS's single global warping function when RT drift structures differ across the dataset.

## Related tools

- **ncGTW** (Performs individualized compound-specific graphical time warping with constraint edges on neighboring samples; produces realigned RT warping functions for misaligned features detected by XCMS.) — https://github.com/ChiungTingWu/ncGTW
- **XCMS** (Performs initial LC-MS alignment using a single global warping function per sample across all m/z bins; serves as baseline algorithm for comparison.)
- **R** (Scripting environment in which ncGTW is implemented as a plug-in to XCMS; used to execute fillPeaks and compCV functions for CV computation.)

## Examples

```
# Load XCMS and ncGTW aligned results, compute CV before/after peak-filling
library(ncGTW); xcms_aligned <- readRDS('xcms_result.rds'); ncgtw_aligned <- readRDS('ncgtw_result.rds'); xcms_fill <- fillPeaks(xcms_aligned); ncgtw_fill <- fillPeaks(ncgtw_aligned); cv_xcms_f1 <- compCV(xcms_fill, featureID='feature_1'); cv_ncgtw_f1 <- compCV(ncgtw_fill, featureID='feature_1'); print(data.frame(Algorithm=c('XCMS','ncGTW'), CV_PostFill=c(cv_xcms_f1, cv_ncgtw_f1)))
```

## Evaluation signals

- CV values decrease after peak-filling for both algorithms; ncGTW's post-fill CV should be lower than XCMS's (e.g., ncGTW feature 1: 0.229 vs. XCMS: 0.369).
- ncGTW's CV reduction ratio (%) exceeds XCMS's for the same features; improvement is quantifiable and reproducible across replicate runs.
- Feature-level CV improvement correlates with ncGTW's detection of RT drift structure variation across samples; features with higher drift heterogeneity show larger gaps between algorithms.
- Realigned peak intensities from ncGTW align better with known spike-in or internal standard concentrations than XCMS-aligned intensities (if reference data are available).
- No increase in false positives (spurious feature groups) after ncGTW realignment; feature count and group size remain stable or improve.

## Limitations

- ncGTW relies on higher-resolution alignment to compute p-values for misalignment detection; computational cost scales with dataset size (hundreds of samples).
- ncGTW's constraint-edge graph structure assumes neighboring samples have correlated RT drift; this assumption may fail in datasets with large acquisition gaps or instrument maintenance periods.
- CV comparison is sensitive to peak-filling algorithm parameters and noise; low signal-to-noise ratios may produce unreliable CV estimates for both algorithms.
- ncGTW detects misaligned features but does not guarantee recovery of all true features; some severely misaligned features may remain undetected if p-values do not meet significance thresholds.
- No changelog found in repository documentation; version-specific behavior and parameter stability are undocumented.

## Evidence

- [other] ncGTW realignment reduced CV after peak-filling from 0.369 to 0.229 for feature 1 and from 0.351 to 0.119 for feature 2, compared to XCMS warping functions.: "ncGTW realignment reduced CV after peak-filling from 0.369 to 0.229 for feature 1 and from 0.351 to 0.119 for feature 2, compared to XCMS warping functions."
- [readme] ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples.: "ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples"
- [intro] ncGTW can detect misaligned features produced by xcms due to the assumption that all m/z bins in the same sample share the same warping function, which often fails with hundreds of samples or data acquisition longer than a week: "ncGTW can detect misaligned features produced by xcms due to the assumption that all m/z bins in the same sample share the same warping function, which often fails with hundreds of samples or data"
- [other] Apply fillPeaks to the XCMS-aligned results and compute CV values for feature 1 and feature 2 using compCV.: "Apply fillPeaks to the XCMS-aligned results and compute CV values for feature 1 and feature 2 using compCV"
- [readme] The purpose of ncGTW is to detect and fix the bad alignments in the LC-MS data. Currently, ncGTW is implemented in a R-package as a plug-in for XCMS.: "The purpose of ncGTW is to detect and fix the bad alignments in the LC-MS data. Currently, ncGTW is implemented in a R-package as a plug-in for XCMS"
