---
name: outlier-detection-and-treatment
description: Use when when you have a Metaboprep object with raw or batch-normalized
  metabolomics abundance data and need to detect samples that deviate significantly
  from the central distribution due to technical artifacts, processing errors, or
  biological extremes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - metaboprep
  - ggplot2
  - dendextend
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboprep_cq
    doi: 10.1093/bioinformatics/btac059/6522114
    title: Metaboprep
  dedup_kept_from: coll_metaboprep_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac059/6522114
  all_source_dois:
  - 10.1093/bioinformatics/btac059/6522114
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# outlier-detection-and-treatment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and handle statistical outliers in metabolomics datasets using hierarchical clustering, principal component analysis, and user-defined distance thresholds. This skill applies multiple complementary detection methods (total peak area, PCA-based, and feature correlation) to flag anomalous samples for exclusion or treatment before downstream analysis.

## When to use

When you have a Metaboprep object with raw or batch-normalized metabolomics abundance data and need to detect samples that deviate significantly from the central distribution due to technical artifacts, processing errors, or biological extremes. Apply this skill before statistical modeling or biomarker discovery when outliers could bias results or violate normality assumptions.

## When NOT to use

- Input has already been manually curated and outliers removed by the analyst—re-running detection risks double-filtering.
- Study design intentionally retains extreme phenotypes (e.g., case–control study where cases cluster separately)—outlier removal may discard signal.
- Sample size is very small (n < 20)—statistical thresholds (e.g., ±5 SD) may be unstable or remove too many observations.

## Inputs

- Metaboprep object containing metabolomics abundance matrix, sample metadata, and feature metadata

## Outputs

- Filtered Metaboprep object with outlier-flagged samples and exclusion codes in sample metadata
- Sample summary statistics including outlier assignments and reasons for exclusion
- Feature hierarchical clustering tree (dendrogram) used for correlation-based outlier detection

## How to apply

Within the quality_control pipeline, configure three complementary outlier detection strategies: (1) total peak area outliers using the total_peak_area_sd threshold (e.g., ±5 SD) to flag samples with extreme summed abundance; (2) PCA-based outlier detection using pc_outlier_sd (e.g., 5 SD) on principal components to identify multivariate anomalies; and (3) feature correlation outliers via hierarchical clustering (tree_cut_height parameter, e.g., 0.5) to identify samples misaligned with feature dependencies. Specify outlier_treatment ('leave_be', 'exclude', or 'winsorize') to control whether flagged samples are retained with metadata tags, removed entirely, or intensity-capped at winsorize_quantile thresholds. The function automatically re-assesses feature independence after each filtering step and returns a Metaboprep object with exclusion codes and summary statistics appended, allowing traceability of which samples were flagged and why.

## Related tools

- **metaboprep** (R package implementing the quality_control function with integrated outlier detection, feature clustering, and PCA analysis; provides Metaboprep object structure for managing data layers and exclusion tracking) — https://github.com/MRCIEU/metaboprep
- **ggplot2** (Visualization of PCA scores and outlier assignments)
- **dendextend** (Enhancement and manipulation of hierarchical clustering dendrograms for feature tree visualization and interpretation)

## Examples

```
mydata <- mydata |> quality_control(source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2, total_peak_area_sd = 5, outlier_udist = 5, outlier_treatment = "leave_be", tree_cut_height = 0.5, pc_outlier_sd = 5)
```

## Evaluation signals

- Exclusion codes in sample metadata correctly map to detection method (user_defined_sample_totalpeakarea, user_defined_sample_pca_outlier) and match the number of flagged samples reported by quality_control.
- Dendrogram tree structure reflects expected feature dependencies; samples assigned to mis-clustered branches should be flagged and excluded when tree_cut_height is tuned appropriately.
- Summary statistics before/after filtering show expected changes: sample count decreases by the number of excluded samples; mean/SD of total peak area and PC scores shrink toward central distribution.
- Outlier_treatment parameter behavior is consistent: 'leave_be' retains flagged samples with 'excluded=TRUE'; 'exclude' removes them entirely from data layer; 'winsorize' caps intensities at specified quantile.
- PCA re-assessment loop correctly re-computes feature independence after sample exclusion, confirming max_num_pcs reported matches the number of informative components in the filtered dataset.

## Limitations

- Outlier detection thresholds (total_peak_area_sd, pc_outlier_sd, tree_cut_height) are user-specified and not data-adaptive; inappropriate thresholds may over-filter or under-filter depending on the distribution and study design.
- PCA-based detection assumes linear independence; non-linear or compositional artifacts may not be captured by standard PC outlier tests.
- Hierarchical clustering depends on the choice of linkage method and distance metric; the README does not specify which are used, so results may vary with different clustering configurations.
- Feature exclusion via features_exclude_but_keep parameter (e.g., xenobiotics) is retained in the final dataset but excluded from QC filtering, potentially masking sample-level anomalies driven by those features.
- Very small sample sizes (n < 20) or highly skewed missing data patterns can make statistical thresholds unreliable; the function does not provide automated guidance on threshold selection.

## Evidence

- [abstract] The quality_control function applies data filtering using a standard pipeline with user-defined parameters including sample_missingness, feature_missingness, total_peak_area_sd, and outlier_udist thresholds to filter the metabolite dataset.: "quality_control function applies data filtering using a standard pipeline with user-defined parameters including sample_missingness, feature_missingness, total_peak_area_sd, and outlier_udist"
- [abstract] Perform hierarchical clustering and principal component analysis on features to identify correlated metabolites and sample outliers.: "Perform hierarchical clustering and principal component analysis on features to identify correlated metabolites and sample outliers."
- [intro] Perform data filtering on the data set using a standard pipeline and according to user-defined thresholds.: "Perform data filtering on the data set using a standard pipeline and according to user-defined thresholds"
- [readme] mydata <- mydata |> quality_control( source_layer = 'input', sample_missingness = 0.2, feature_missingness = 0.2, total_peak_area_sd = 5, outlier_udist = 5, outlier_treatment = 'leave_be', winsorize_quantile = 1.0, tree_cut_height = 0.5, pc_outlier_sd = 5, sample_ids = NULL, feature_ids = NULL): "quality_control( source_layer = 'input', sample_missingness = 0.2, feature_missingness = 0.2, total_peak_area_sd = 5, outlier_udist = 5, outlier_treatment = 'leave_be', winsorize_quantile = 1.0,"
- [readme] Calculating total peak abundance outliers at +/- 5 Sdev - excluding 0 sample(s): "Calculating total peak abundance outliers at +/- 5 Sdev - excluding"
- [readme] Running sample data PCA outlier analysis at +/- 5 Sdev: "Running sample data PCA outlier analysis at +/- 5 Sdev"
