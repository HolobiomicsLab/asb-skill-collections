---
name: metabolite-cv-ratio-calculation
description: Use when after normalizing a metabolomic feature matrix when you have both non-QC (study) samples and QC (quality-control) replicates in the same experiment. Use it to remove features that are poorly reproducible or show inconsistent signal across samples relative to instrument/technical variation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - margheRita
  - notame
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-cv-ratio-calculation

## Summary

Calculate and apply coefficient-of-variation (CV) ratios between sample and QC groups to filter metabolomic features by reproducibility. This skill identifies features with elevated variability in real samples relative to quality-control replicates, retaining only those exceeding a ratio threshold (typically CV_non-QC / CV_QC > 1.0).

## When to use

Apply this skill after normalizing a metabolomic feature matrix when you have both non-QC (study) samples and QC (quality-control) replicates in the same experiment. Use it to remove features that are poorly reproducible or show inconsistent signal across samples relative to instrument/technical variation. This is especially valuable when you need to identify genuine biological signals amid high noise or batch effects typical of LC-MS/MS profiling.

## When NOT to use

- Input is already a feature table filtered by other QC metrics (e.g., mass defect, missing value thresholds) — combine CV filtering into a unified QC pipeline rather than applying sequentially.
- Study design lacks QC replicates or has fewer than 3 QC samples per instrument run — CV calculation requires sufficient replication to estimate reproducibility reliably.
- Features are sparse or zero-inflated across samples — CV calculation may be unstable for rare features; consider imputation or alternative distributional assumptions first.

## Inputs

- Normalized metabolomic feature abundance matrix (e.g., Urine_RP_NEG_norm.txt)
- Sample metadata identifying QC vs. non-QC sample group membership
- Feature annotations (m/z, retention time, metabolite name)

## Outputs

- Filtered feature abundance matrix with retained features only
- CV ratio values (one per feature)
- Feature count summary (n_initial, n_retained, n_removed)
- CV ratio distribution statistics (mean, median, min, max, quantiles)

## How to apply

Load the normalized feature abundance matrix (e.g., Urine_RP_NEG_norm.txt) and sample metadata identifying QC vs. non-QC sample groups into R. For each metabolomic feature, separately calculate the coefficient of variation (CV = standard deviation / mean) within the non-QC sample group and within the QC sample group. Compute the CV ratio as (CV_non-QC / CV_QC) for each feature. Apply a threshold filter, retaining only features where CV_ratio exceeds the default cutoff of 1.0; features below this threshold are likely noise or artifacts. Output the filtered feature table and generate summary statistics including count of features before and after filtering, mean/median CV ratio of retained features, and the full distribution of CV ratios to assess filtering stringency.

## Related tools

- **margheRita** (Implements CV_ratio() function for coefficient-of-variation filtering of metabolomic features post-normalization) — https://github.com/emosca-cnr/margheRita
- **R** (Execution environment for CV calculation, ratio computation, and statistical filtering)
- **notame** (Alternative R package for non-targeted LC-MS preprocessing with built-in quality-control and feature-filtering workflows) — https://github.com/hanhineva-lab/notame

## Examples

```
# In R with margheRita:
library(margheRita)
data_filtered <- CV_ratio(feature_matrix = urine_norm, sample_metadata = metadata, group_col = 'sample_type', qc_label = 'QC', threshold = 1.0)
```

## Evaluation signals

- Feature count decreases from initial set (e.g., 539 → 303 metabolites), with count reduction proportional to CV ratio threshold stringency.
- Retained features have median CV ratio > 1.0 and distribution mean > 1.0 (e.g., median 1.1032 in the reference dataset), confirming biological signal enrichment.
- CV ratio histogram shows bimodal or right-skewed distribution with modal peak at or above threshold, indicating clear separation of high-variance (retained) from low-variance (removed) features.
- Removed features cluster at CV ratios ≤ 1.0, consistent with features whose variation in samples matches or is less than QC instrument noise.
- Subsequent statistical tests (e.g., ANOVA, Mann–Whitney U) on retained features show lower multiple-testing burden and higher effect sizes, validating improved signal-to-noise ratio.

## Limitations

- CV ratio filtering is sensitive to outlier samples or QC replicates with anomalously high/low intensity; consider flagging or removing outliers before CV calculation.
- Threshold of CV_ratio > 1.0 is heuristic and may be too stringent (retaining few features) or too lenient (retaining noisy features) depending on sample complexity, ionization efficiency, and LC-MS instrument stability; consider adjusting based on downstream statistical power.
- Features with zero or near-zero mean abundance in either QC or non-QC groups will have undefined or inflated CV values; pre-filter features by minimum abundance or presence threshold.
- CV ratio does not account for biological covariance or clustering; features with high CV ratio may reflect genuine sample heterogeneity rather than true metabolite abundance differences.

## Evidence

- [other] The CV_ratio() function retains only features with a CV ratio (non-QC samples / QC samples) exceeding the default threshold of 1, producing a distribution with median 1.1032 and resulting in 303 metabolites retained out of 539 initial features.: "The CV_ratio() function retains only features with a CV ratio (non-QC samples / QC samples) exceeding the default threshold of 1, producing a distribution with median 1.1032 and resulting in 303"
- [other] Calculate the coefficient of variation (CV) for each feature separately within the non-QC sample group and within the QC sample group.: "Calculate the coefficient of variation (CV) for each feature separately within the non-QC sample group and within the QC sample group."
- [other] Compute the CV ratio (CV_non-QC / CV_QC) for each feature. Apply the threshold filter, retaining only features where CV_ratio > 1.0.: "Compute the CV ratio (CV_non-QC / CV_QC) for each feature. Apply the threshold filter, retaining only features where CV_ratio > 1.0."
- [readme] filtering by coefficient of variation (samples vs QCs) and probabilistic quotient normalization: "filtering by coefficient of variation (samples vs QCs) and probabilistic quotient normalization"
