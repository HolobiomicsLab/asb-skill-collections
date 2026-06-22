---
name: feature-abundance-threshold-comparison
description: Use when after loading an MZmine3-exported feature quantification table and identifying blank sample columns, when you need to remove features with significant intensity in procedural blanks before proceeding to batch correction and statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Jupyter Notebook
  - MZmine3
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41596-024-01046-3
  title: FBMN-STATS
evidence_spans:
- To easily install and run Jupyter Notebook in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
  dedup_kept_from: coll_fbmn_stats_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-024-01046-3
  all_source_dois:
  - 10.1038/s41596-024-01046-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-abundance-threshold-comparison

## Summary

A filtration method that removes features from non-targeted LC-MS/MS feature quantification tables by comparing feature intensity in blank samples against biological samples using a defined threshold ratio. This step prevents false-positive feature assignments attributable to contamination or background noise.

## When to use

Apply this skill after loading an MZmine3-exported feature quantification table and identifying blank sample columns, when you need to remove features with significant intensity in procedural blanks before proceeding to batch correction and statistical analysis. Use when blank samples are part of your experimental design and you want to filter out features likely representing contamination or instrument carryover rather than true biological signal.

## When NOT to use

- Input data do not include procedural blank samples (no blank columns to compare against).
- Feature table has already undergone blank removal or quality filtering in upstream processing.
- Analysis goal is to characterize contamination or background — in which case you would retain blank-associated features intentionally.

## Inputs

- Feature quantification table (CSV) exported from MZmine3 processing of non-targeted LC-MS/MS data
- Sample metadata or column annotations identifying which columns correspond to blank samples
- Threshold parameter (ratio or absolute intensity cutoff) for blank-to-sample comparison

## Outputs

- Filtered feature quantification table (CSV) with blank-associated features removed
- Optional: log of removed features and their blank intensities for quality assurance

## How to apply

Extract blank sample columns from the feature quantification table and calculate feature intensity statistics (mean or median) within the blank sample group. Define a threshold that represents the maximum acceptable intensity in blanks relative to biological samples (e.g., a ratio or absolute cutoff). For each feature, compare its blank intensity to this threshold; features exceeding the threshold are marked for removal. Remove identified blank-associated features from the feature table and export the filtered result as CSV. The rationale is that features with high blank intensity are likely background or contamination, not true metabolites of interest.

## Related tools

- **R** (Programming environment for loading, filtering, and exporting feature tables; used to calculate blank intensity statistics and apply threshold-based feature removal) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (Computational notebook interface for interactive feature filtration, threshold parameter tuning, and result visualization) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **MZmine3** (Upstream tool that generates the feature quantification table input; defines the format and quality of features before blank removal)

## Examples

```
# In R: blank_intensity <- apply(feature_table[, blank_cols], 1, mean); retained_features <- feature_table[blank_intensity < threshold, ]; write.csv(retained_features, 'filtered_feature_table.csv')
```

## Evaluation signals

- Number and percentage of features removed matches expected contamination level (e.g., if 10–30% of features are typically blank-associated in your analytical platform).
- Blank samples in the filtered table have near-zero intensity across all remaining features, confirming successful removal of high-blank-intensity features.
- Biological samples retain statistically significant signal across features, demonstrating that true metabolite features were preserved.
- Downstream univariate and multivariate statistical analyses show improved effect sizes and reduced noise after blank removal, compared to unfiltered data.
- Visual inspection of feature intensity distributions shows separation between biological sample and blank sample intensities for retained features.

## Limitations

- Threshold selection is empirical and dataset-dependent; an inappropriately high threshold may retain contamination, while a too-low threshold may remove true low-abundance features present in both blanks and samples.
- Features with bimodal or highly variable intensity distributions across biological replicates may not be reliably classified as blank-associated using a single threshold.
- Does not account for features that are genuinely elevated in blanks due to experimental design (e.g., internal standards or spiked controls), which may be incorrectly removed if threshold is not manually adjusted.
- The method assumes blank samples are run under identical or similar instrumental conditions as biological samples; systematic differences in blank acquisition may lead to misleading intensity comparisons.

## Evidence

- [other] blank removal procedural step: "The FBMN-STATS workflow implements blank removal as a procedural step applied to non-targeted LC-MS/MS data and Feature-based Molecular Networks, positioned after data cleanup and before batch"
- [other] blank intensity calculation and threshold: "Calculate feature intensity statistics in blank samples (e.g., mean or median intensity per feature). Apply blank removal criterion to filter features with intensity in blanks above a defined"
- [readme] workflow implementation in FBMN-STATS: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks"
- [other] input data format: "Load the feature quantification table exported from MZmine3 processing of MSV000082312 and MSV000085786 into R or Jupyter Notebook."
