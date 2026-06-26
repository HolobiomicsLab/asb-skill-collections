---
name: bandwidth-parameter-effect-comparison
description: Use when you suspect XCMS grouping contains misaligned features due to
  suboptimal parameter settings or insufficient samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - ncGTW
  - R
  - xcms
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an
  alignment algorithm
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

# bandwidth-parameter-effect-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare XCMS grouping results produced with different bandwidth (bw) parameters to detect misaligned feature groups in retention time. This skill identifies features that fail to align consistently across parameter settings, revealing systematic alignment failures in LC-MS data.

## When to use

Apply this skill when you suspect XCMS grouping contains misaligned features due to suboptimal parameter settings or insufficient samples. Use it as a prerequisite diagnostic before attempting realignment: generate two XCMS grouping results with contrasting bw values (one large, capturing expected maximal RT drift; one small, matching RT sampling resolution) and compare them to identify inconsistent feature groupings.

## When NOT to use

- Input XCMS results were generated with identical bandwidth parameters—comparison requires contrasting parameter sets to reveal divergent groupings.
- Peak detection ppm value is unknown or unavailable—the ppm parameter must match the original peak detection tolerance for valid p-value estimation.
- You are seeking to align individual samples rather than identify systematic feature grouping errors—this skill diagnoses grouping-level misalignment, not sample-level warping.

## Inputs

- XCMS grouping result object (large bandwidth parameter set)
- XCMS grouping result object (small bandwidth parameter set)
- ppm tolerance value (numeric, matching peak detection ppm)

## Outputs

- excluGroups table (data frame containing detected misaligned feature groups with p-values and sample subset information)

## How to apply

Load two XCMS grouping results into R—one generated with a large bw parameter (representing expected maximal retention time drift across your sample set) and one with a small bw parameter (matching your peak detection resolution). Call misalignDetect() from the ncGTW package, providing both grouping results and a ppm tolerance parameter that matches your peak detection ppm threshold. The function estimates p-values using the high-resolution (small bw) result as the null hypothesis of accurate alignment, then identifies features with sufficiently small p-values and disjoint sample subsets. Extract the excluGroups table, which lists feature groups detected as misaligned. This comparative approach exploits the principle that accurate alignment should produce consistent groupings regardless of parameter resolution; divergence signals systematic misalignment.

## Related tools

- **ncGTW** (Executes misalignDetect() function to compare grouping results and identify misaligned feature groups) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Generates the two grouping results (with different bw parameters) that serve as inputs to the comparison)
- **R** (Execution environment for ncGTW and data object manipulation)

## Examples

```
misalign_result <- misalignDetect(xcms_grouping_large_bw, xcms_grouping_small_bw, ppm = 5); excluGroups <- misalign_result@excluGroups
```

## Evaluation signals

- excluGroups table is non-empty and contains feature groups with p-values below a significance threshold, indicating detected misalignments.
- Detected misaligned features show disjoint sample subsets—the affected samples differ across misaligned groups, demonstrating systematic rather than random divergence.
- Features in the excluGroups table can be matched to neighboring features in the low-resolution grouping result, confirming they represent real grouping inconsistencies.
- The excluGroups table has expected row/column structure matching ncGTW output schema (feature group identifiers, p-values, sample information).
- Re-running misalignDetect() with the same inputs reproduces identical excluGroups, confirming reproducibility.

## Limitations

- The skill requires careful selection of the two bw parameters: the large bw must be set to expected maximal RT drift across all samples, and the small bw to RT sampling resolution. Inappropriate parameter choice may fail to reveal actual misalignments.
- Detection accuracy depends on sufficient samples and adequate RT drift structure; datasets with fewer samples or uniform RT drift may not produce reliable misalignment signals.
- The method assumes the high-resolution (small bw) grouping is closer to ground truth; if both groupings are substantially incorrect, the comparison may fail to identify true misalignments.
- No changelog is available, limiting reproducibility tracking across ncGTW versions.

## Evidence

- [other] misalignDetect() parameter requirements: "misalignDetect() requires two XCMS grouping results with different bw values (one set to expected maximal RT drift, one to RT sampling resolution) and a ppm parameter matching the peak detection ppm"
- [readme] misalignment detection rationale: "ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result, where the p-value is given by the"
- [intro] XCMS misalignment cause: "Due to the same warping function assumption or bad parameter settings, `xcms` may have some misaligned features, and there is a function in `ncGTW` to identify such misalignments."
- [other] output specification: "Extract and return the excluGroups table containing the detected misaligned feature groups."
