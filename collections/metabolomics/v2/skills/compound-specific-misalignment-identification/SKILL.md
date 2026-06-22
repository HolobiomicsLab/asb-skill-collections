---
name: compound-specific-misalignment-identification
description: Use when you have completed XCMS grouping on LC-MS data and suspect misaligned features due to long acquisition periods (>1 week) or large sample cohorts (hundreds of samples).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-specific-misalignment-identification

## Summary

Identifies misaligned feature groups produced by XCMS grouping using ncGTW's misalignDetect() function, which compares two XCMS results with different bandwidth parameters to detect retention time (RT) drift artifacts. This skill enables correction of alignment errors that arise when XCMS assumes all m/z bins in a sample share a single warping function, improving accuracy for downstream peak-regrouping and peak-filling.

## When to use

Apply this skill when you have completed XCMS grouping on LC-MS data and suspect misaligned features due to long acquisition periods (>1 week) or large sample cohorts (hundreds of samples). Specifically, when you observe inconsistent RT drift structures across different m/z bins or have re-grouped XCMS results with different bandwidth (bw) parameters and need to systematically identify which feature groups were misaligned by XCMS's uniform warping assumption.

## When NOT to use

- XCMS grouping has not yet been performed or only a single grouping result is available (misalignDetect requires two grouping results for comparison)
- Retention time drift is expected to be uniform across all m/z bins in your samples (misalignment detection assumes compound-specific RT drift structures; uniform drift does not require ncGTW)
- Your LC-MS dataset is small (single session, <10 samples) with minimal RT variation—ncGTW misalignment detection is designed for large cohorts where drift artifacts accumulate

## Inputs

- XCMS grouping result object with large bandwidth parameter (xcmsSet or XCMSnExp)
- XCMS grouping result object with small bandwidth parameter (xcmsSet or XCMSnExp)
- ppm tolerance value (numeric, matching peak detection ppm)

## Outputs

- excluGroups table (data.frame) containing detected misaligned feature groups with p-values and sample subset information

## How to apply

Load two XCMS grouping result objects into R: one produced with a large bw parameter (set to the expected maximal RT drift) and one with a small bw parameter (matching the RT sampling resolution). Call ncGTW's misalignDetect() function with both grouping results and supply the ppm tolerance parameter—matching the ppm value used during peak detection—to ensure consistent mass accuracy thresholds. The function estimates p-values for each feature under the null hypothesis of accurate alignment (from the high-resolution result), identifies features with sufficiently small p-values and disjoint sample subsets, and matches neighboring features across the two grouping results. The output excluGroups table lists all detected misaligned feature groups, which can then be passed to ncGTW's realignment function for correction.

## Related tools

- **ncGTW** (provides misalignDetect() function to identify misaligned feature groups from XCMS and realign them using compound-specific graphical time warping) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (produces the two grouping result objects that are compared as input to misalignDetect(); ncGTW is a plug-in that detects and corrects XCMS misalignment artifacts)
- **R** (environment for loading XCMS objects, calling misalignDetect(), and extracting the excluGroups output table)

## Examples

```
misalignDetect(xcmsRes_largeBW, xcmsRes_smallBW, ppm = 25)
```

## Evaluation signals

- excluGroups table is non-empty and contains feature groups with p-values well below a significance threshold (e.g., p < 0.05), indicating robust statistical evidence of misalignment
- Misaligned features map to a contiguous or clustered subset of samples (disjoint sample subsets) rather than being randomly scattered—validates the algorithm's ability to detect structured RT drift artifacts
- m/z values and retention times in excluGroups align with known ion properties and expected chromatographic behavior for those compounds
- Realignment of excluGroups via ncGTW's alignment function produces improved downstream metrics (e.g., reduced peak width variance, higher peak intensity consistency, or better feature detection in peak-filling)
- ppm tolerance used in misalignDetect() matches or is compatible with the ppm tolerance from XCMS peak detection step (audit parameter consistency)

## Limitations

- misalignDetect() requires two XCMS grouping results with carefully chosen bw parameters; suboptimal parameter selection (e.g., bw values too close together or mismatched to actual RT drift) may result in missed or spurious detections
- The algorithm assumes that high-resolution alignment (small bw) produces statistically valid p-values under the null hypothesis of accurate alignment; if the small bw grouping is itself misaligned, p-value estimates may be unreliable
- No changelog or version history is available, making it difficult to assess the stability and evolution of the misalignDetect() function across different ncGTW releases
- The skill detects misalignment but does not guarantee that the excluGroups table will be complete; features that are misaligned but do not meet the statistical and disjoint sample set criteria may not be reported

## Evidence

- [other] misalignDetect() function inputs and parameters: "misalignDetect() requires two XCMS grouping results with different bw values (one set to expected maximal RT drift, one to RT sampling resolution) and a ppm parameter matching the peak detection ppm"
- [intro] XCMS misalignment root cause: "the assumption that all m/z bins in the same sample share the same warping function, which often fails with hundreds of samples or data acquisition longer than a week"
- [intro] ncGTW detection and correction workflow: "Due to the same warping function assumption or bad parameter settings, `xcms` may have some misaligned features, and there is a function in `ncGTW` to identify such misalignments"
- [readme] misalignment detection algorithm overview: "ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result"
- [readme] ncGTW as XCMS plug-in: "ncGTW can detect the misaligned feature groups from XCMS and realign them. After that, XCMS can use the realigned data from XCMS for more accurate grouping and peak-filling"
