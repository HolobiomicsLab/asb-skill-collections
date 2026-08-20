---
name: outlier-detection-via-multivariate-distance
description: Use when after batch normalization when you have a Metaboprep object
  with metabolomic feature data and need to identify samples that are statistical
  outliers in the high-dimensional feature space. Use it when you want to detect unusual
  sample profiles before downstream multivariate analyses (e.
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
  license_tier: restricted
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

# outlier-detection-via-multivariate-distance

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and enumerate sample outliers in metabolomic data using multivariate distance metrics (Mahalanobis or Euclidean) computed on principal component scores, applied at configurable standard deviation thresholds (typically 3–5 SD). This skill integrates missing-data imputation, PC selection via acceleration and parallel analysis, and systematic outlier flagging to support quality control workflows.

## When to use

Apply this skill after batch normalization when you have a Metaboprep object with metabolomic feature data and need to identify samples that are statistical outliers in the high-dimensional feature space. Use it when you want to detect unusual sample profiles before downstream multivariate analyses (e.g., PCA, clustering, or case–control studies), or when you require reproducible outlier counts at predefined SD thresholds for quality control reporting.

## When NOT to use

- Data have not yet been batch-normalized or have not undergone initial QC filtering (apply batch_normalise and quality_control first).
- Input layer contains >80% missing values per sample or feature (pre-filter using quality_control with extreme_missingness parameters).
- Sample size is very small (< 10 samples) — PC-based distance metrics require sufficient degrees of freedom; parallel analysis may fail or be unreliable.

## Inputs

- Metaboprep object (containing feature matrix, sample metadata, feature metadata)
- source_layer parameter (character: 'input', 'qc', or other layer name)
- optional sample_ids filter (character vector)
- optional feature_ids filter (character vector)

## Outputs

- data.frame with PC eigenvectors (top 10 PCs) and sample-level outlier flags/counts at 3 SD, 4 SD, 5 SD thresholds
- attributes: variance_explained (numeric vector), acceleration_factor_result (object), parallel_analysis_result (object)

## How to apply

Load your Metaboprep object containing normalized metabolomic data. Call `pc_and_outliers()` with the object, specify the source layer (e.g., 'input' or 'qc'), and optionally filter by sample_ids or feature_ids. The function internally imputes missing values to the median, performs acceleration analysis and parallel analysis to determine the number of significant principal components, computes PCA scores on the top two (or more) PCs, and then flags samples as outliers where their multivariate distance (SD units) from the origin exceeds 3 SD, 4 SD, and 5 SD thresholds. Return a data frame containing PC eigenvectors for the top 10 PCs, outlier counts at each threshold, and attributes storing variance explained, acceleration factor results, and parallel analysis outcomes. Choose your SD threshold based on the stringency needed: 5 SD is more conservative (few false positives), while 3 SD is more sensitive (catches more borderline deviants).

## Related tools

- **metaboprep** (provides Metaboprep class, pc_and_outliers() function, and integrated PCA/parallel analysis infrastructure for outlier detection) — https://github.com/MRCIEU/metaboprep
- **R** (execution environment for statistical computing and PCA calculations)
- **ggplot2** (optional visualization of PC scores and outlier flags (referenced in metaboprep vignette))

## Examples

```
mydata |> pc_and_outliers(source_layer = "qc", sample_ids = NULL, feature_ids = NULL)
```

## Evaluation signals

- Verify that the returned data.frame has one row per sample and columns for each of the top 10 PC eigenvectors plus outlier count columns; row count matches input sample count (minus any pre-filtered samples).
- Check that variance_explained attribute is a numeric vector in descending order and sums to ≤ 100% (should sum to <100% after PCA truncation to top PCs).
- Confirm that outlier counts at 3 SD ≥ outlier counts at 4 SD ≥ outlier counts at 5 SD (monotonic decrease in stringency).
- Validate that all imputed missing values are present in the PC computation (no samples dropped due to remaining NA values); compare input sample count to output row count.
- Check parallel_analysis_result and acceleration_factor_result attributes are non-NULL and contain valid results indicating the number of significant PCs (should be ≤ min(n_samples, n_features)).

## Limitations

- If the number of informative PCs detected by parallel analysis is less than max_num_pcs (default 10), the function will only return eigenvectors for the detected PCs and may issue a warning; users must handle variable output dimensions.
- Outlier detection on only the top 2 PCs (as noted in the workflow) may miss outliers that manifest primarily in higher PCs; consider increasing max_num_pcs or re-running with different PC selections if suspected.
- Median imputation assumes missing data are missing at random (MAR) and does not account for systematic missingness patterns; users should inspect missingness mechanisms before applying this function.
- SD-based thresholds (3, 4, 5) are absolute and do not adapt to the sample-specific distribution of distances; they may flag too many or too few outliers if the underlying data are highly skewed or have heavy tails.

## Evidence

- [methods] The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs, and computes sample outlier counts at 3 SD, 4 SD, and 5 SD thresholds on the top two PCs.: "The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs, and computes sample outlier counts at 3"
- [methods] Call pc_and_outliers() with the Metaboprep object, specify source_layer (e.g., 'input'), and optional sample/feature ID filters.: "Call pc_and_outliers() with the Metaboprep object, specify source_layer (e.g., 'input'), and optional sample/feature ID filters"
- [methods] Return a data.frame with PC eigenvectors for the top 10 PCs and outlier counts, plus attributes containing variance explained vector, acceleration factor result, and parallel analysis result.: "Return a data.frame with PC eigenvectors for the top 10 PCs and outlier counts, plus attributes containing variance explained vector"
- [intro] Perform data filtering on the data set using a standard pipeline and according to user-defined thresholds: "Perform data filtering on the data set using a standard pipeline and according to user-defined thresholds"
- [readme] Running sample data PCA outlier analysis at +/- 5 Sdev: "Running sample data PCA outlier analysis at +/- 5 Sdev"
