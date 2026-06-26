---
name: metabolomics-data-quality-control
description: Use when after loading raw metabolomics data (e.g., from Metabolon, Nightingale,
  Olink, or SomaLogic platforms) into a Metaboprep object and before statistical analysis
  or modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - rmarkdown
  - knitr
  - ggplot2
  - metaboprep
  - dendextend
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
- '%\VignetteEngine{knitr::rmarkdown}'
- library(ggplot2)
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

# metabolomics-data-quality-control

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A systematic pipeline for filtering untargeted and targeted metabolomics datasets by applying user-defined thresholds on sample missingness, feature missingness, total peak area outliers, and principal component outliers. This skill removes low-quality samples and features while preserving data integrity for downstream analysis.

## When to use

Apply this skill after loading raw metabolomics data (e.g., from Metabolon, Nightingale, Olink, or SomaLogic platforms) into a Metaboprep object and before statistical analysis or modeling. Use it when your dataset contains missing values, potential outlier samples, or features with low signal quality that could bias downstream results. Trigger this skill if you have raw abundance data with both sample-level (missingness, total peak area anomalies) and feature-level (detection rate, correlated metabolites) quality concerns.

## When NOT to use

- Input data is already a pre-filtered or aggregated feature table (e.g., from published databases); re-filtering may lose valid signal.
- Sample size is very small (<10 samples) or feature count is very low (<20 features); outlier detection thresholds may be unstable.
- Data comes from a highly curated, vendor-processed format (e.g., post-vendor QC report); verify vendor filtering does not conflict with user thresholds.

## Inputs

- Metaboprep object containing raw abundance matrix, sample metadata, and feature metadata
- user-defined numeric thresholds: sample_missingness, feature_missingness, total_peak_area_sd, outlier_udist, pc_outlier_sd, winsorize_quantile, tree_cut_height

## Outputs

- Metaboprep object with new 'qc' data layer containing filtered abundance matrix
- Sample exclusion codes and counts (e.g., user_defined_sample_missingness, user_defined_sample_pca_outlier)
- Feature exclusion codes and counts (e.g., user_defined_feature_missingness)
- Feature dendrogram (hierarchical clustering tree) from correlational analysis
- Summary statistics for retained samples and features

## How to apply

Load the raw metabolomics data into a Metaboprep object, then invoke quality_control() with user-defined numeric thresholds for sample_missingness (e.g., 0.2 = exclude samples with ≥20% missing values), feature_missingness (e.g., 0.2 = exclude features detected in <80% of samples), total_peak_area_sd (e.g., 5 = exclude samples with total abundance >±5 standard deviations from mean), and outlier_udist (e.g., 5 = threshold for multivariate distance-based outlier detection). The function performs hierarchical clustering of features to identify correlated metabolite groups, runs principal component analysis to detect sample-level outliers via pc_outlier_sd threshold (e.g., 5 standard deviations), and optionally applies winsorization at a specified quantile. Optionally exclude predefined feature sets (e.g., xenobiotics) from QC filtering while retaining them in the output via features_exclude_but_keep. The filtered dataset is stored in a new 'qc' layer within the Metaboprep object, with exclusion reasons and counts recorded for transparency.

## Related tools

- **metaboprep** (R package providing Metaboprep object class, quality_control() function, and hierarchical clustering/PCA infrastructure for metabolomics QC) — https://github.com/MRCIEU/metaboprep
- **R** (runtime environment for executing metaboprep workflows)
- **ggplot2** (visualization of QC summary plots and outlier distributions)
- **dendextend** (dendrogram manipulation and visualization of feature clustering trees)

## Examples

```
mydata <- mydata |> quality_control(source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2, total_peak_area_sd = 5, outlier_udist = 5, outlier_treatment = "leave_be", winsorize_quantile = 1.0, tree_cut_height = 0.5, pc_outlier_sd = 5)
```

## Evaluation signals

- Verify that the 'qc' layer exists in the output Metaboprep object and contains non-null abundance data with fewer rows (samples) and/or columns (features) than the 'input' layer.
- Check exclusion summary table: confirm sample and feature counts for each exclusion code match the applied thresholds (e.g., sample_missingness=0.2 should exclude samples with ≥20% missing values).
- Confirm that feature dendrograms can be extracted and plotted without error, indicating successful hierarchical clustering.
- Validate that all retained samples have missingness <sample_missingness threshold and all retained features have missingness <feature_missingness threshold.
- Verify that total peak area values for retained samples fall within ±total_peak_area_sd standard deviations of the dataset mean.

## Limitations

- Threshold selection is data- and platform-dependent; no single set of thresholds is universally optimal across all metabolomics studies.
- PCA-based outlier detection may be unstable when the number of available informative PCs is much smaller than max_num_pcs parameter (e.g., only 2 PCs available but max_num_pcs=10).
- Hierarchical clustering and PCA can be computationally intensive for very large feature sets (>5000 metabolites) or samples (>1000).
- Winsorization and tree cut height parameters require prior knowledge or pilot tuning; inappropriate settings may obscure real biology or retain spurious noise.
- No changelog is available; version stability and reproducibility of results across metaboprep versions are not formally documented.

## Evidence

- [other] quality_control function applies data filtering using a standard pipeline with user-defined parameters including sample_missingness, feature_missingness, total_peak_area_sd, and outlier_udist thresholds: "The quality_control function applies data filtering using a standard pipeline with user-defined parameters including sample_missingness, feature_missingness, total_peak_area_sd, and outlier_udist"
- [other] Quality control pipeline performs hierarchical clustering and principal component analysis on features to identify correlated metabolites and sample outliers: "Perform hierarchical clustering and principal component analysis on features to identify correlated metabolites and sample outliers."
- [other] Optionally exclude features from QC filtering while retaining them in the final dataset using features_exclude_but_keep parameter: "Optionally exclude features from QC filtering (e.g., xenobiotics) using the features_exclude_but_keep parameter while retaining them in the final dataset."
- [readme] Core goal is to perform data filtering on the dataset using a standard pipeline and according to user-defined thresholds: "Perform data filtering on the data set using a standard pipeline and according to user-defined thresholds."
- [other] quality_control function with specified thresholds returns filtered Metaboprep object with QC-filtered data stored in the 'qc' layer: "Return the filtered Metaboprep object with QC-filtered data stored in the 'qc' layer and summary statistics appended."
- [readme] quality_control records exclusion codes for samples including user_defined_sample_missingness and user_defined_sample_pca_outlier: "user_defined_sample_missingness   | 2
user_defined_sample_pca_outlier   | 0"
