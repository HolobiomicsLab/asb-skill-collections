---
name: sample-quality-assessment-using-pca
description: Use when after loading and basic filtering of (un)targeted metabolomic data (sample/feature missingness, peak area filters) but before aggregation or statistical modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - ggplot2
  - metaboprep
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
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
---

# sample-quality-assessment-using-pca

## Summary

Identify metabolomic sample outliers by performing principal component analysis on filtered metabolite data and flagging samples that deviate >3, 4, or 5 standard deviations from the mean on top principal components. This detects samples with atypical metabolic profiles that may compromise downstream analysis.

## When to use

After loading and basic filtering of (un)targeted metabolomic data (sample/feature missingness, peak area filters) but before aggregation or statistical modeling. Use this skill when you have a Metaboprep object with metabolite measurements across multiple samples and need to identify and flag samples with anomalous multivariate metabolite patterns that could bias batch effects, associations, or clustering.

## When NOT to use

- Input data has >80% missing values per sample or feature without prior filtering—imputation to median will inflate noise and reduce outlier detection power.
- Sample size is very small (<10 samples)—PC stability and robust distance estimation become unreliable.
- Data are already known to contain strong, expected batch structure or biological subgroups—PCA outlier detection may flag legitimate group differences rather than technical anomalies.

## Inputs

- Metaboprep object (containing metabolomic data matrix, sample metadata, feature metadata)
- source_layer parameter (character: 'input', 'qc', or other layer name)
- optional sample_ids filter (character vector of sample identifiers to subset)
- optional feature_ids filter (character vector of feature identifiers to subset)

## Outputs

- data.frame with PC eigenvectors for top 10 principal components
- outlier count vector (samples flagged at 3 SD, 4 SD, 5 SD thresholds)
- attribute: variance_explained (numeric vector, proportion of variance per PC)
- attribute: acceleration_factor_result (result from acceleration analysis)
- attribute: parallel_analysis_result (result from parallel analysis for PC retention)

## How to apply

Call pc_and_outliers() on a Metaboprep object after specifying a source_layer (e.g., 'input' or 'qc'). The function imputes missing values to the median, performs acceleration analysis and parallel analysis to determine the optimal number of significant principal components, then computes PCA on the retained components. For each sample, it calculates the Mahalanobis or Euclidean distance on the top 2 principal components and flags samples exceeding ±3 SD, ±4 SD, and ±5 SD thresholds as outliers. Return a data.frame with PC eigenvectors (top 10 PCs) and outlier counts at each threshold, plus attributes containing variance explained per PC, acceleration factor, and parallel analysis result. Use the results to decide on a pc_outlier_sd threshold (commonly 5 SD) for exclusion in quality_control().

## Related tools

- **metaboprep** (provides pc_and_outliers() function and Metaboprep object for organizing and filtering metabolomic data; orchestrates median imputation, PCA, parallel analysis, and multivariate outlier flagging) — https://github.com/MRCIEU/metaboprep
- **R** (execution environment for metaboprep and underlying PCA/statistical computations)
- **ggplot2** (optional visualization of PC scores and outlier highlights post-analysis)

## Examples

```
mydata <- mydata |> quality_control(source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2, pc_outlier_sd = 5)
```

## Evaluation signals

- PC eigenvectors and variance explained vector sum to ≤1.0 (normalized) and are ordered by decreasing variance; parallel analysis and acceleration factor results are non-null and logically consistent with retained PC count.
- Outlier counts at 3, 4, 5 SD thresholds form a monotonically decreasing sequence (more stringent threshold → fewer flagged samples); no sample flagged at 3 SD unless also flagged at lower threshold.
- Outlier flagged samples show visually distinct position in PC1 vs. PC2 scatter plot (>3 SD from centroid); confirm by re-running on subset data without those samples and verifying PC structure stabilizes.
- Variance explained by top 2 PCs is reasonable for metabolomic data (typically 20–60% combined); if <10%, check that data were properly scaled and that imputation did not artificially dominate.
- Outlier removal via quality_control(..., pc_outlier_sd=5) yields a sample exclusion count matching the 5 SD threshold from pc_and_outliers() output (excluding other filter effects).

## Limitations

- Median imputation prior to PCA can bias distances if missingness is non-random or systematic by group; consider multiple imputation or separate PCA per sample stratum for sensitive applications.
- Parallel analysis and acceleration analysis may be unstable or over-retain PCs when sample size is very small relative to feature count; manual inspection of scree plots recommended.
- Outlier detection is relative to the current dataset; if a true biological subgroup is present, samples from that subgroup may be incorrectly flagged as outliers. Advisable to inspect metadata and replicate data before exclusion.
- No changelog available in the repository; version-to-version changes in imputation, parallelization, or PC selection criteria are not explicitly documented, limiting reproducibility across package updates.

## Evidence

- [methods] The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs, and computes sample outlier counts at 3 SD, 4 SD, and 5 SD thresholds on the top two PCs.: "The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs, and computes sample outlier counts at 3"
- [methods] Return a data.frame with PC eigenvectors for the top 10 PCs and outlier counts, plus attributes containing variance explained vector, acceleration factor result, and parallel analysis result.: "Return a data.frame with PC eigenvectors for the top 10 PCs and outlier counts, plus attributes containing variance explained vector, acceleration factor result, and parallel analysis result."
- [readme] Running sample data PCA outlier analysis at +/- 5 Sdev: "Running sample data PCA outlier analysis at +/- 5 Sdev"
- [readme] Perform data filtering on the data set using a standard pipeline and according to user-defined thresholds: "Perform data filtering on the data set using a standard pipeline and according to user-defined thresholds"
