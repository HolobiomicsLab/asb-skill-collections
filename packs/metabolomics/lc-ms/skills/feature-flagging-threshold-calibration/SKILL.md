---
name: feature-flagging-threshold-calibration
description: Use when after drift correction in non-targeted LC-MS metabolomics workflows, when you need to decide which molecular features are sufficiently reproducible (low instrument/QC variance) and biologically informative (high QC-versus-biological signal ratio) to retain for downstream statistical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - notame
  - R
  - Biobase
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-flagging-threshold-calibration

## Summary

Systematically apply quality-metric thresholds to identify and mark low-quality metabolic features in LC-MS data using relative standard deviation (RSD), robust RSD variants, and detection ratios. This skill bridges preprocessing and statistical analysis by deciding which features to retain, flag, or exclude based on reproducibility and biological signal strength.

## When to use

After drift correction in non-targeted LC-MS metabolomics workflows, when you need to decide which molecular features are sufficiently reproducible (low instrument/QC variance) and biologically informative (high QC-versus-biological signal ratio) to retain for downstream statistical analysis. Use this skill when you have computed RSD, RSD* (robust median absolute deviation variant), and D-ratio metrics for all features and must choose thresholds that balance data retention against quality.

## When NOT to use

- Before drift correction has been applied; quality metrics are unreliable on uncorrected data.
- When QC samples are absent or too few to estimate reproducibility reliably.
- If your study design lacks replicate injections or technical replicates; RSD and D-ratio cannot be computed meaningfully.

## Inputs

- MetaboSet object (drift-corrected, post-cubic-spline-regression)
- Feature abundance matrix (exprs slot)
- Feature metadata (fData slot) with computed RSD, RSD*, and D-ratio columns
- Quality control (QC) sample designations

## Outputs

- MetaboSet object with updated Flag column in fData marking low-quality features
- Quality metric distribution visualizations (RSD, D-ratio, detection rate histograms or density plots)
- Summary table of flagged features and their specific quality violations

## How to apply

Load the drift-corrected MetaboSet object and apply the flag_quality function with explicit threshold parameters: RSD limit (default 0.2, but conservatively 0.1 to be strict), RSD* limit (robust variant, default 0.2, conservatively 0.1), and D-ratio limit (default 0.4, conservatively 0.1). The function compares each feature's internal spread (RSD, RSD*) and QC-to-biological variance ratio (D-ratio) against these cutoffs, marking features that violate any threshold in a Flag column within fData. After flagging, inspect the fData table to tally newly flagged features and their specific quality metric violations, then visualize the distributions of RSD, D-ratio, and detection rate across all features to assess the proportion flagged and verify the thresholds are appropriate for your instrument, sample type, and analysis goals.

## Related tools

- **notame** (Provides flag_quality function to apply quality thresholds; bundles quality metrics (RSD, RSD*, D-ratio) and flagging logic for LC-MS metabolomics) — https://github.com/hanhineva-lab/notame
- **Biobase** (Provides ExpressionSet and MetaboSet data structures; stores feature metadata (fData) and abundance matrix (exprs) that hold quality metrics and Flag column)
- **R** (Statistical programming environment in which MetaboSet objects are manipulated and thresholds are applied)

## Examples

```
mset_flagged <- flag_quality(mset, rsd_limit = 0.1, rsd_abs_limit = 0.1, d_ratio_limit = 0.1); head(fData(mset_flagged)$Flag)
```

## Evaluation signals

- Flag column in fData contains boolean or categorical values (0/1, TRUE/FALSE, or descriptive labels) for all features; no NA values where metrics are defined.
- Proportion of flagged features is consistent with threshold severity: conservative thresholds (RSD/D-ratio 0.1) should flag more features than recommended thresholds (RSD 0.2, D-ratio 0.4).
- Quality metric distributions show clear separation between flagged and unflagged features; flagged features cluster in the tail of RSD/D-ratio distributions.
- Flagged feature count is nonzero (threshold is stringent enough to catch low-quality data) but not >90% (threshold is not so strict it removes too much data).
- Manual spot-check: inspect fData rows for 5–10 flagged features and verify that their RSD, RSD*, or D-ratio values exceed the stated threshold parameters.

## Limitations

- Threshold choice is data- and instrument-dependent; recommended thresholds (RSD 0.2, D-ratio 0.4) are not universal and may require calibration per platform, method, or metabolite class.
- D-ratio is meaningful only when QC samples and biological replicates are present and properly annotated; mislabeled samples will produce unreliable ratios.
- RSD* (robust version) assumes sufficient sample size to compute median absolute deviation reliably; sparse or very small datasets may yield unstable robust estimates.
- Features flagged as low-quality are marked but not automatically removed; downstream decisions (retain, filter, or exclude) remain with the analyst.
- Package API is experimental and subject to breaking changes; example: threshold parameter names or default values may shift between notame versions.

## Evidence

- [other] flag_quality function with conservative thresholds (RSD 0.1, D-ratio 0.1): "Apply flag_quality function with conservative limit of 0.1 for classic RSD, RSD* (robust version using median absolute deviation), and basic D-ratio to flag features where internal spread or"
- [other] Inspect flagged features and quality metric violations: "Inspect the Flag column in fData to identify newly flagged features and their quality metric violations."
- [other] Visualize quality metric distributions: "Visualize quality metric distributions (RSD, D-ratio, detection rate) across all features to assess the proportion flagged."
- [other] flag_quality is used to flag features based on quality metrics: "```flag_quality``` is used to flag features based on the other quality metrics"
- [other] Recommended vs. conservative thresholds: "using conservative limits of 0.1 for classic RSD, RSD*, and basic D-ratio (compared to recommended thresholds of 0.2 for RSD and 0.4 for D-ratio)"
