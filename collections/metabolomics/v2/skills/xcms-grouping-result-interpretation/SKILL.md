---
name: xcms-grouping-result-interpretation
description: Use when xCMS grouping has been performed on LC-MS data from studies with hundreds of samples or data acquisition periods longer than a week, where retention time drift structures are complex and the single-warping-function assumption is likely violated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ncGTW
  - xcms
  - R
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`, a popular LC-MS data analysis R package'
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
---

# xcms-grouping-result-interpretation

## Summary

Interpret and validate XCMS grouping results by detecting misaligned feature groups using ncGTW's misalignDetect() function with dual bandwidth parameters. This skill identifies alignment artifacts that arise when XCMS assumes a single warping function across all m/z bins, enabling targeted realignment of problematic features before downstream analysis.

## When to use

Apply this skill when XCMS grouping has been performed on LC-MS data from studies with hundreds of samples or data acquisition periods longer than a week, where retention time drift structures are complex and the single-warping-function assumption is likely violated. Use specifically when you suspect misaligned feature groups may compromise peak-regrouping, peak-filling, or quantification accuracy.

## When NOT to use

- XCMS grouping has been performed on small, short-duration studies (< 100 samples, < 1 week acquisition) where RT drift is minimal and single-warping assumptions are reasonable.
- You lack two independent XCMS grouping results with systematically different bandwidth parameters.
- The ppm tolerance parameter for misalignDetect() does not match the ppm threshold used in the original XCMS peak detection step.

## Inputs

- XCMS grouping result object (large bandwidth parameter set)
- XCMS grouping result object (small bandwidth parameter set)
- ppm tolerance parameter (numeric, matching peak detection ppm)

## Outputs

- excluGroups table (detected misaligned feature groups)
- p-value estimates for each feature (from higher-resolution alignment)

## How to apply

Load two XCMS grouping results into R: one with a large bandwidth (bw) parameter set to the expected maximal RT drift, and one with a small bw parameter set to the RT sampling resolution. Call misalignDetect() from the ncGTW package, providing both grouping objects and a ppm tolerance parameter that matches the ppm value used during initial peak detection. The function estimates p-values for each feature under the null hypothesis of accurate alignment (higher resolution result) and identifies features with sufficiently small p-values and disjoint sample subsets as misaligned. Extract the returned excluGroups table, which lists all detected misaligned feature groups as candidates for realignment with ncGTW's reference-free pairwise alignment method.

## Related tools

- **ncGTW** (Provides misalignDetect() function to identify misaligned feature groups from XCMS and realign them using neighbor-wise compound-specific graphical time warping) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Produces grouping results (with different bandwidth parameters) that serve as input to misalignDetect() for misalignment detection)
- **R** (Runtime environment for executing ncGTW and XCMS functions)

## Examples

```
result <- misalignDetect(xcmsGrouping_largeBW, xcmsGrouping_smallBW, ppm=5)
```

## Evaluation signals

- excluGroups table is non-empty and contains feature groups with p-values below the statistical significance threshold, indicating detected misalignments
- Detected misaligned features show disjoint sample subsets (not random distribution across all samples), confirming structured misalignment rather than noise
- Feature m/z values and retention times in excluGroups match entries in the original XCMS grouping objects, validating traceability
- After realignment with ncGTW on detected misaligned features, subsequent peak-regrouping or peak-filling operations yield improved quantification consistency or reduced artifactual peak intensity variance across the sample cohort

## Limitations

- misalignDetect() requires careful parameterization: bandwidth values must be chosen to represent both maximal RT drift and sampling resolution; incorrect bw selection will either miss true misalignments or generate false positives.
- The ppm parameter must exactly match the peak detection ppm threshold used in the original XCMS analysis; mismatches will produce unreliable p-value estimates.
- Requires two separate XCMS grouping runs with different parameters, adding computational and storage overhead.
- The method assumes that misaligned features will exhibit sufficiently small p-values and disjoint sample subsets; features with gradual or diffuse misalignment patterns across many samples may not be detected.

## Evidence

- [other] misalignDetect() input requirements and parameters: "misalignDetect() requires two XCMS grouping results with different bw values (one set to expected maximal RT drift, one to RT sampling resolution) and a ppm parameter matching the peak detection ppm"
- [intro] XCMS limitation that motivates misalignment detection: "ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples. That is, ncGTW avoids the popular but not accurate"
- [intro] Problem statement: misaligned features from XCMS: "Due to the same warping function assumption or bad parameter settings, `xcms` may have some misaligned features, and there is a function in `ncGTW` to identify such misalignments"
- [readme] ncGTW misalignment detection algorithm overview: "ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result, where the p-value is given by the"
- [other] Workflow: extract and return excluGroups table: "Extract and return the excluGroups table containing the detected misaligned feature groups"
