---
name: sample-missingness-filtering
description: Use when when you have loaded (un)targeted metabolite data into a Metaboprep object and need to exclude samples with excessive missing values before quality control or statistical analysis. This is typically applied early in the QC pipeline when sample-level data completeness is a concern (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - metaboprep
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-missingness-filtering

## Summary

Filter metabolomics samples from a Metaboprep object based on user-defined thresholds for missing data proportion. This step removes samples exceeding a missingness cutoff (e.g., ≥20%) to ensure adequate feature coverage before downstream analysis.

## When to use

When you have loaded (un)targeted metabolite data into a Metaboprep object and need to exclude samples with excessive missing values before quality control or statistical analysis. This is typically applied early in the QC pipeline when sample-level data completeness is a concern (e.g., when some samples have incomplete LC-MS runs or systematic acquisition failures). Use this skill if your research question depends on reliable per-sample metabolite measurements across a consistent feature set.

## When NOT to use

- Input data is already a feature table or sparse matrix not wrapped in a Metaboprep object — use Metaboprep() constructor first.
- You require all samples to be retained (e.g., in a small exploratory cohort) — adjust sample_missingness to 1.0 or skip this filter.
- Missing data patterns are informative and should be preserved for downstream imputation or pattern analysis — consider deferring this filter or using a less aggressive threshold.

## Inputs

- Metaboprep object containing raw or preprocessed metabolite abundance matrix, sample metadata, and feature annotations

## Outputs

- Filtered Metaboprep object with QC-flagged data in the 'qc' layer
- Updated sample metadata with exclusion codes (e.g., 'user_defined_sample_missingness')
- Summary statistics indicating number of samples excluded by missingness threshold

## How to apply

Within the quality_control() function, set the sample_missingness parameter to your chosen threshold (as a decimal; e.g., 0.2 for samples with ≥20% missing values). The function calculates the proportion of missing (zero or NA) metabolite abundances for each sample and flags samples exceeding the threshold for exclusion. Before applying, decide whether to exclude specific features from this calculation using the features_exclude_but_keep parameter (e.g., to keep xenobiotics out of missingness calculations but retain them in the final dataset). After QC completes, inspect the exclusion summary to confirm how many samples were removed and verify that the exclusion codes match your intent (e.g., 'user_defined_sample_missingness'). This threshold is typically set conservatively (0.2–0.5) to balance data completeness with sample retention.

## Related tools

- **metaboprep** (R package providing the quality_control() function and Metaboprep object class for metabolite data filtering and QC reporting) — https://github.com/MRCIEU/metaboprep
- **R** (Programming language environment for executing the quality_control pipeline and Metaboprep workflows)

## Examples

```
mydata <- mydata |> quality_control(source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2, total_peak_area_sd = 5, outlier_udist = 5, outlier_treatment = "leave_be", winsorize_quantile = 1.0, tree_cut_height = 0.5, pc_outlier_sd = 5)
```

## Evaluation signals

- Verify the number of samples excluded matches the count in the exclusion summary (e.g., 'user_defined_sample_missingness | 2').
- Confirm excluded samples had missingness proportions ≥ the specified threshold (e.g., ≥0.2); spot-check a few flagged samples.
- Check that the remaining samples (those not excluded) all have missingness < threshold; no false negatives.
- Inspect the Metaboprep summary() output showing 'excluded' flags and exclusion codes to ensure the QC layer reflects the filtering.
- Verify that features marked in features_exclude_but_keep were not used to calculate sample missingness but are still present in the final output.

## Limitations

- The filter is applied independently per sample and does not account for missing-data correlations or batch patterns; extreme missingness may still result from technical factors not captured by threshold alone.
- Setting sample_missingness too stringently (e.g., <0.1) may over-remove samples and reduce statistical power, especially in small cohorts.
- The function assumes missing data are represented as zero or NA in the abundance matrix; alternative missingness encodings (e.g., negative values, sentinel values) may not be detected.
- This filter does not impute missing values; samples are excluded entirely. If metabolite patterns are informative, consider batch-specific or feature-specific thresholds instead.

## Evidence

- [methods] sample_missingness filter applied during quality_control pipeline: "Assessing for sample missingness at specified level of >=20% - excluding 0 sa"
- [methods] sample_missingness parameter in quality_control function: "quality_control(source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2)"
- [intro] Perform data filtering according to user-defined thresholds: "Perform data filtering on the data set using a standard pipeline and according to user-defined thresholds"
- [methods] Exclusion summary reports sample_missingness exclusions: "user_defined_sample_missingness   | 2"
- [methods] Option to exclude features from QC filtering while retaining them: "features_exclude_but_keep parameter while retaining them in the final dataset"
