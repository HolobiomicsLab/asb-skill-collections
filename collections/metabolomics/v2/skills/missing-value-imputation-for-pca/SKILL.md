---
name: missing-value-imputation-for-pca
description: Use when your metabolomic dataset contains missing values (common in untargeted or targeted mass spectrometry data) and you need to perform PCA for outlier detection at multiple standard deviation thresholds (e.g., 3 SD, 4 SD, 5 SD) on principal component scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# missing-value-imputation-for-pca

## Summary

Impute missing values to the median prior to principal component analysis in metabolomic datasets to enable PCA-based outlier detection and dimensionality reduction. This preprocessing step is essential because PCA requires a complete data matrix and median imputation preserves the distributional properties needed for downstream SD-based outlier thresholding.

## When to use

Your metabolomic dataset contains missing values (common in untargeted or targeted mass spectrometry data) and you need to perform PCA for outlier detection at multiple standard deviation thresholds (e.g., 3 SD, 4 SD, 5 SD) on principal component scores. This is particularly relevant when quality control workflows require identification of sample outliers in PC space before or after batch normalization.

## When NOT to use

- Your data contains no missing values and you wish to avoid unnecessary imputation that might alter PC loadings.
- You have strong prior biological knowledge that missingness is non-random (MNAR) and requires domain-specific imputation (e.g., values below LOD); median imputation assumes data are missing at random (MAR) or completely at random (MCAR).
- Your workflow requires preservation of the original missing data structure for sensitivity analysis or comparison of imputation methods; use this skill only after such comparisons are complete.

## Inputs

- Metaboprep object containing metabolomic data with potential missing values
- source_layer parameter specifying the data layer to impute (e.g., 'input')
- optional sample_ids and feature_ids filters to subset the data before imputation

## Outputs

- Complete (non-missing) data matrix with missing values replaced by feature medians
- data.frame containing PC eigenvectors for the top 10 PCs
- outlier count vector for samples at 3 SD, 4 SD, and 5 SD thresholds on top two PCs
- attributes: variance explained vector, acceleration factor result, parallel analysis result

## How to apply

Before calling pc_and_outliers() or performing PCA within the quality_control() pipeline, the metaboprep package automatically imputes missing data to the median of each feature. This median imputation is applied after loading the data into a Metaboprep object and prior to acceleration analysis and parallel analysis to determine the number of significant PCs. The rationale is that median imputation is robust to skewed distributions common in metabolomics data and avoids bias introduced by mean imputation. After imputation, the complete data matrix is then subjected to PCA, with sample outlier counts computed on the top two PCs at 3 SD, 4 SD, and 5 SD thresholds. The choice of median over other imputation methods (e.g., mean, KNN, MICE) is justified by its simplicity and stability in high-dimensional omics contexts.

## Related tools

- **metaboprep** (Implements median imputation internally within pc_and_outliers() and quality_control() workflows) — https://github.com/MRCIEU/metaboprep
- **R** (Computational environment for executing imputation and PCA operations)

## Examples

```
mydata <- mydata |> quality_control(source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2, pc_outlier_sd = 5)
```

## Evaluation signals

- Check that the output data matrix contains zero missing values (NA count = 0) after imputation.
- Verify that imputed values fall within the range [min, max] of observed feature values and equal the median of each feature's non-missing data.
- Confirm that PCA variance explained by the top 2 PCs is reasonable (typically >30% for metabolomic data) and that PC scores are finite (no NaN or Inf).
- Validate that outlier counts at 3 SD, 4 SD, and 5 SD thresholds form a nested hierarchy (outliers_3SD ≥ outliers_4SD ≥ outliers_5SD).
- Compare PC eigenvector magnitudes before and after imputation to ensure the imputation does not artificially inflate or suppress PC loadings.

## Limitations

- Median imputation assumes data are missing at random (MAR) or completely at random (MCAR); it is inappropriate for missing-not-at-random (MNAR) data such as values below a detection limit that are systematically missing.
- Median imputation does not account for feature correlations and may underestimate variance in high-dimensional spaces; more sophisticated methods (KNN, MICE) may be preferable if missingness exceeds ~30% of the matrix.
- The metaboprep implementation uses a fixed imputation strategy (median only); no option to select or compare alternative imputation methods (e.g., mean, minimum, KNN) is exposed via the pc_and_outliers() interface.
- If a feature has >50% missing values, its median is unstable and may not represent the true central tendency; extreme feature missingness should be filtered before imputation (metaboprep provides feature_missingness threshold for this purpose).

## Evidence

- [other] The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs, and computes sample outlier counts at 3 SD, 4 SD, and 5 SD thresholds on the top two PCs.: "The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs, and computes sample outlier counts at 3"
- [readme] Run QC example showing the quality_control pipeline which calls pc_and_outliers internally: mydata <- mydata |> quality_control( source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2, total_peak_area_sd = 5, outlier_udist = 5, outlier_treatment = "leave_be", winsorize_quantile = 1.0, tree_cut_height = 0.5, pc_outlier_sd = 5, sample_ids = NULL, feature_ids = NULL): "mydata <- mydata |> quality_control( source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2, total_peak_area_sd = 5, outlier_udist = 5, outlier_treatment = "leave_be","
- [other] The metaboprep package provides data filtering capabilities using a standard pipeline with user-defined thresholds, which includes outlier detection mechanisms applied to principal components at configurable standard deviation cutoffs.: "The metaboprep package provides data filtering capabilities using a standard pipeline with user-defined thresholds, which includes outlier detection mechanisms applied to principal components at"
- [other] Load a Metaboprep object containing metabolomic data (or subset by sample_ids and/or feature_ids). Call pc_and_outliers() with the Metaboprep object, specify source_layer (e.g., 'input'), and optional sample/feature ID filters.: "Load a Metaboprep object containing metabolomic data (or subset by sample_ids and/or feature_ids). Call pc_and_outliers() with the Metaboprep object, specify source_layer (e.g., 'input'), and"
