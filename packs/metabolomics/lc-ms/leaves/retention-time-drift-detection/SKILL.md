---
name: retention-time-drift-detection
description: Use when you have LC-MS data processed through XCMS grouping that shows signs of RT drift (e.g., data acquired over extended periods or across many samples) and you suspect misalignment of feature groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ncGTW
  - R
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

# retention-time-drift-detection

## Summary

Detect misaligned feature groups in LC-MS data caused by retention time (RT) drift and incorrect XCMS grouping parameters by comparing two XCMS grouping results with different bandwidth settings. This skill identifies features that failed to align correctly due to RT drift structures or suboptimal parameter choices, enabling targeted realignment before downstream analysis.

## When to use

Apply this skill when you have LC-MS data processed through XCMS grouping that shows signs of RT drift (e.g., data acquired over extended periods or across many samples) and you suspect misalignment of feature groups. This is particularly relevant when XCMS assumes all m/z bins share a single warping function, which often fails at scale (hundreds of samples or acquisition longer than a week). Use this skill if you want to verify grouping accuracy before peak-regrouping or peak-filling steps.

## When NOT to use

- Data has not yet been processed through XCMS grouping — misalignDetect() operates only on XCMS output.
- You have only a single XCMS grouping result or cannot generate two results with different bw parameters.
- Your LC-MS data is from a single sample or a single short acquisition with minimal RT drift — misalignment detection is most relevant at scale (hundreds of samples or week-long acquisitions).

## Inputs

- XCMS grouping result object (large bandwidth parameter set)
- XCMS grouping result object (small bandwidth parameter set)
- ppm tolerance value (numeric, matching peak detection ppm)

## Outputs

- excluGroups table (data frame listing misaligned feature groups with p-values and sample subset information)

## How to apply

Generate two XCMS grouping results from the same raw data using different bandwidth (bw) parameters: one set to the expected maximal RT drift and one to the RT sampling resolution. Load both grouping result objects into R alongside the ppm parameter value used during peak detection (matching the mass tolerance). Call misalignDetect() from the ncGTW package with both grouping results and the ppm tolerance. The function applies two statistical criteria: it estimates p-values for each feature group using the higher-resolution (smaller bw) alignment result under the null hypothesis of accurate alignment, then identifies features with sufficiently small p-values and disjoint sample subsets as misaligned. Extract the returned excluGroups table, which lists all detected misaligned feature groups for downstream realignment.

## Related tools

- **ncGTW** (Provides misalignDetect() function to detect and fix misaligned feature groups from XCMS; operates as a plug-in for XCMS alignment refinement) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Generates the two grouping results (with different bw parameters) that serve as inputs to misalignDetect())
- **R** (Execution environment for ncGTW and XCMS packages)

## Examples

```
misalignDetect(xcms_result_large_bw, xcms_result_small_bw, ppm=5)
```

## Evaluation signals

- excluGroups table is non-empty and contains feature groups with p-values meeting the significance threshold, indicating detected misalignments.
- Detected misaligned features show disjoint sample subsets (i.e., the misalignment is localized to specific samples or sample groups, not globally random).
- Feature groups in excluGroups correspond to m/z and RT ranges where the two XCMS grouping results diverge most significantly.
- After realignment using ncGTW on the detected misaligned groups, downstream peak-regrouping or peak-filling produces more consistent intensity patterns or fewer gaps than before correction.
- The number and m/z distribution of detected misaligned groups is consistent with the expected RT drift magnitude and data acquisition duration.

## Limitations

- Requires two separate XCMS grouping runs with different bw parameters; computationally expensive for large datasets.
- Detection accuracy depends on correct choice of bw parameters: one must reflect the expected maximal RT drift, the other the RT sampling resolution.
- The ppm parameter must match the peak detection ppm value used in the original XCMS run; mismatches reduce sensitivity.
- misalignDetect() assumes that at least some features are correctly aligned in the high-resolution (small bw) grouping result; if the high-resolution grouping is also poor, detection may fail.
- No changelog available; version compatibility and algorithm updates are not documented.

## Evidence

- [other] Two XCMS grouping results with different bw parameters are required, and the ppm tolerance must be specified: "misalignDetect() requires two XCMS grouping results with different bw values (one set to expected maximal RT drift, one to RT sampling resolution) and a ppm parameter matching the peak detection ppm"
- [intro] ncGTW detects misalignment due to RT drift structures and incorrect XCMS assumptions: "Due to the same warping function assumption or bad parameter settings, `xcms` may have some misaligned features, and there is a function in `ncGTW` to identify such misalignments"
- [other] The excluGroups table output contains the detected misaligned feature groups: "Extract and return the excluGroups table containing the detected misaligned feature groups"
- [readme] Detection uses two statistical criteria with p-values from high-resolution alignment: "ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result, where the p-value is given by the"
- [readme] Identified misaligned features have disjoint sample subsets: "identifies all features with sufficiently small p-values and disjoint sample subsets"
