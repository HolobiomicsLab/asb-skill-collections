---
name: blank-sample-feature-filtering
description: Use when you have a feature quantification table exported from MZmine3 processing of non-targeted LC-MS/MS data and your experimental design includes blank (negative control) samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MZmine3
  - Jupyter Notebook
  - FBMN-STATS
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

# blank-sample-feature-filtering

## Summary

Blank sample feature filtering removes features from LC-MS/MS feature quantification tables whose intensity in blank (control) samples exceeds a defined threshold relative to biological samples. This procedural step eliminates contaminants and instrumental artifacts before downstream statistical analysis of feature-based molecular networks.

## When to use

Apply this skill when you have a feature quantification table exported from MZmine3 processing of non-targeted LC-MS/MS data and your experimental design includes blank (negative control) samples. Use it after data cleanup and before batch correction if you need to eliminate features attributable to contamination, instrument carryover, or background noise that appear in blanks at intensities comparable to or exceeding biological samples.

## When NOT to use

- Your experimental design does not include blank or negative control samples.
- Input is already a pre-processed feature table with blanks already removed by upstream software.
- You are analyzing targeted metabolomics data where all features are a priori validated and unlikely to be contaminants.

## Inputs

- Feature quantification table (CSV) exported from MZmine3 processing of non-targeted LC-MS/MS data
- Sample metadata identifying which columns correspond to blank samples

## Outputs

- Filtered feature quantification table (CSV) with blank-associated features removed
- Optional: QC report documenting number of features removed and intensity statistics in blanks

## How to apply

Load the feature quantification table (CSV format from MZmine3) into R or Jupyter Notebook. Identify and extract blank sample columns from the feature table. Calculate feature intensity statistics in blank samples (e.g., mean or median intensity per feature). Apply a blank removal criterion—typically a ratio threshold comparing blank intensity to biological sample intensity (e.g., sample/blank > 3 or similar user-defined cutoff)—to identify features that fail this criterion. Remove identified blank-associated features from the feature table and export the filtered result as CSV. The rationale is that genuine biological features should show substantially higher intensity in samples than in blanks; features with elevated blank intensity are likely instrumental artifacts or contamination and should be excluded before univariate and multivariate analyses.

## Related tools

- **MZmine3** (Upstream peak detection and feature quantification; generates the input feature table)
- **R** (Environment for loading, filtering, and exporting feature tables using data frame operations)
- **Jupyter Notebook** (Interactive computational environment for executing filtering workflow in R or Python)
- **FBMN-STATS** (Complete workflow implementation including blank removal as a procedural step) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Examples

```
setwd('/My_TestData'); feature_table <- read.csv('feature_quantification.csv', row.names=1); blank_cols <- c('blank_1', 'blank_2', 'blank_3'); blank_means <- rowMeans(feature_table[, blank_cols]); sample_cols <- setdiff(colnames(feature_table), blank_cols); sample_means <- rowMeans(feature_table[, sample_cols]); ratio <- sample_means / (blank_means + 1e-6); filtered_table <- feature_table[ratio > 3, ]; write.csv(filtered_table, 'feature_quantification_blank_removed.csv')
```

## Evaluation signals

- Number of features removed is reasonable relative to total feature count and aligns with expected contamination burden.
- Blank intensity statistics (mean, median, max) are lower for retained features than for removed features.
- Downstream univariate and multivariate statistical analyses show improved effect sizes or reduced noise after blank removal (validate using principal component analysis or volcano plots).
- Output feature table retains expected biological features and removes known contaminants or artifacts (e.g., siloxanes, plasticizers if present in blanks).
- Output CSV conforms to expected schema: rows = features, columns = samples, numeric intensity values; metadata row/column structure unchanged.

## Limitations

- Blank removal criterion (intensity ratio threshold) is user-defined; no universal threshold is specified in the article. Threshold choice depends on instrumental sensitivity, sample complexity, and contamination severity.
- If blank samples are absent or poorly replicated, the statistical basis for filtering is weak and may remove genuine low-abundance biological features.
- The skill assumes blank samples and biological samples are run under identical LC-MS/MS conditions; systematic differences in instrument state or timing may confound blank intensity.
- Features with identical or near-identical intensities in blanks and samples cannot be distinguished as contaminant vs. biological without additional validation (e.g., cross-sample correlation or reference standards).

## Evidence

- [other] The FBMN-STATS workflow implements blank removal as a procedural step applied to non-targeted LC-MS/MS data and Feature-based Molecular Networks, positioned after data cleanup and before batch correction in the analysis pipeline.: "The FBMN-STATS workflow implements blank removal as a procedural step applied to non-targeted LC-MS/MS data and Feature-based Molecular Networks, positioned after data cleanup and before batch"
- [other] Identify and extract blank sample columns from the feature table. Calculate feature intensity statistics in blank samples (e.g., mean or median intensity per feature). Apply blank removal criterion to filter features with intensity in blanks above a defined threshold relative to biological samples.: "Identify and extract blank sample columns from the feature table. Calculate feature intensity statistics in blank samples (e.g., mean or median intensity per feature). Apply blank removal criterion"
- [readme] Using the notebooks provided here, one can perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks.: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks"
- [other] Load the feature quantification table exported from MZmine3 processing of MSV000082312 and MSV000085786 into R or Jupyter Notebook.: "Load the feature quantification table exported from MZmine3 processing of MSV000082312 and MSV000085786 into R or Jupyter Notebook."
