---
name: principal-component-analysis-for-metabolomics
description: 'Use when after loading a Metaboprep object containing metabolomic abundance data when you need to: (1) identify samples that are statistical outliers in multivariate metabolite space; (2) determine the number of statistically significant principal components;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
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

# principal-component-analysis-for-metabolomics

## Summary

Apply principal component analysis (PCA) to metabolomics abundance matrices to identify and enumerate sample outliers in reduced principal component space at user-specified standard deviation thresholds. This skill enables detection of multivariate outliers and assessment of data quality before downstream statistical analysis.

## When to use

Apply this skill after loading a Metaboprep object containing metabolomic abundance data when you need to: (1) identify samples that are statistical outliers in multivariate metabolite space; (2) determine the number of statistically significant principal components; (3) evaluate sample quality across multiple SD cutoffs (3, 4, 5 SD) to decide on exclusion thresholds; or (4) assess whether samples cluster appropriately by known experimental variables before proceeding to association analysis.

## When NOT to use

- Input is already a pre-filtered feature table without access to the original Metaboprep object structure
- You have fewer samples than features after median imputation (PCA may be unstable)
- Your metabolomics dataset has been heavily pre-filtered such that only 1–2 informative PCs remain, limiting sensitivity to multivariate outliers

## Inputs

- Metaboprep object with metabolite abundance matrix (samples × features)
- source_layer parameter specifying which data layer to analyze (e.g., 'input', 'qc')
- optional sample_ids filter to subset samples
- optional feature_ids filter to subset features

## Outputs

- data.frame with PC eigenvectors for top 10 principal components
- outlier count vector at 3 SD, 4 SD, and 5 SD thresholds on top 2 PCs
- variance explained vector (attribute)
- acceleration factor result (attribute)
- parallel analysis result (attribute)

## How to apply

Load a Metaboprep object containing metabolomic data and call pc_and_outliers() with a specified source_layer (e.g., 'input' or 'qc'). The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant principal components automatically, then computes eigenvectors for the top 10 PCs. Sample outliers are counted at 3 SD, 4 SD, and 5 SD thresholds on the top two PCs. The choice of SD threshold depends on your tolerance for false positive exclusions: lower thresholds (3 SD) are more stringent; higher thresholds (5 SD) are more conservative. Return values include PC eigenvectors, variance explained per PC, and outlier counts at each threshold, which can inform downstream QC filtering decisions via the quality_control function.

## Related tools

- **metaboprep** (R package providing pc_and_outliers() function and Metaboprep object container for metabolomics data) — https://github.com/MRCIEU/metaboprep
- **R** (Statistical computing environment in which metaboprep and PCA functions execute)
- **ggplot2** (Visualization library for plotting PCA scores and outlier distributions)

## Examples

```
pc_result <- pc_and_outliers(metaboprep = mydata, source_layer = "input", sample_ids = NULL, feature_ids = NULL)
```

## Evaluation signals

- PC eigenvectors are non-zero and ordered by decreasing variance explained; first two PCs capture the dominant axes of metabolite variation
- Outlier counts at 3 SD ≥ counts at 4 SD ≥ counts at 5 SD (monotonic ordering enforced by stricter thresholds)
- Variance explained per PC decreases monotonically; sum of explained variance for top 2 PCs is typically 30–60% for metabolomics data
- Samples identified as outliers at 5 SD threshold align with known problematic samples (failed QC, extreme missingness, or known batch effects) when cross-checked against sample metadata
- Number of statistically significant PCs returned by acceleration/parallel analysis is ≤ min(samples, features) and is consistent across repeated calls on the same data

## Limitations

- Missing data imputation is performed only to the median; systematic or non-random missingness may inflate variance and bias PC estimates
- The function assumes that metabolite features are reasonably independent before PCA; highly correlated features (e.g., from the same pathway or isotopologue series) can inflate specific PC axes
- Outlier detection is performed on only the top 2 PCs; rare outliers that deviate along lower-variance PCs (PC 3+) may be missed
- SD thresholds (3, 4, 5) are fixed; no adaptive threshold selection based on the empirical distribution is performed
- If the number of available informative PCs is smaller than max_num_pcs (default 10), a warning is issued but analysis proceeds; this may reduce outlier detection power if samples are similar

## Evidence

- [methods] The pc_and_outliers function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs, and computes sample outlier counts at 3 SD, 4 SD, and 5 SD thresholds on the top two PCs.: "The function internally imputes missing data to the median, performs acceleration analysis and parallel analysis to determine the number of significant PCs, and computes sample outlier counts at 3"
- [methods] The metaboprep package provides data filtering capabilities including outlier detection mechanisms applied to principal components at configurable standard deviation cutoffs.: "The metaboprep package provides data filtering capabilities using a standard pipeline with user-defined thresholds, which includes outlier detection mechanisms applied to principal components at"
- [methods] Return a data.frame with PC eigenvectors for the top 10 PCs and outlier counts, plus attributes containing variance explained vector, acceleration factor result, and parallel analysis result.: "Return a data.frame with PC eigenvectors for the top 10 PCs and outlier counts, plus attributes containing variance explained vector, acceleration factor result, and parallel analysis result."
- [readme] Running sample data PCA outlier analysis at +/- 5 Sdev with re-identification of feature independence and PC outliers.: "Running sample data PCA outlier analysis at +/- 5 Sdev - re-identify feature independence and PC outlier analysis"
