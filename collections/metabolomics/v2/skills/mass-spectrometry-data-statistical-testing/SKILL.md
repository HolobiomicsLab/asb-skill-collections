---
name: mass-spectrometry-data-statistical-testing
description: Use when you have a normalized abundance matrix from LC-MS/MS profiling with sample class assignments (e.g., phenotypic groups, disease states, treatment conditions) and need to filter metabolic features for downstream pathway analysis or biological validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - margheRita
  - R
  - notame
  - MS-DIAL
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
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
---

# mass-spectrometry-data-statistical-testing

## Summary

Apply univariate statistical tests (parametric ANOVA or non-parametric alternatives) to LC-MS/MS metabolomic feature tables to identify metabolites with statistically significant abundance differences across sample classes, followed by multiple-testing correction and feature selection based on q-value thresholds.

## When to use

You have a normalized abundance matrix from LC-MS/MS profiling with sample class assignments (e.g., phenotypic groups, disease states, treatment conditions) and need to filter metabolic features for downstream pathway analysis or biological validation. Use this skill when you have ≥3 sample classes to compare and wish to reduce the feature set to those with q-values (FDR-corrected p-values) below a predefined significance cutoff (e.g., q < 0.05).

## When NOT to use

- Input is already a filtered list of known biomarkers or curated metabolites; re-testing may inflate false-positive rates.
- Sample class groups are highly imbalanced (e.g., n=1 vs n=100) without appropriate variance-stabilization; consider post-hoc power analysis.
- Feature abundance data are raw, unnormalized counts; apply normalization and quality control filtering (e.g., mass defect filtering, CV thresholding) before statistical testing.

## Inputs

- Normalized LC-MS/MS feature abundance matrix (e.g., Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt)
- Sample metadata with class/group assignments (e.g., phenotype labels AA, DD, MM)

## Outputs

- Filtered feature table with Feature_ID, metabolite names, ANOVA F-statistics, p-values, q-values, and effect sizes
- List of significant metabolic features passing the q-value threshold

## How to apply

Load the normalized feature abundance table (e.g., Urine_RP_NEG_norm.txt) into margheRita as a data object with sample metadata annotated with class assignments (AA, DD, MM). Apply the univariate() function to compute ANOVA F-statistics and p-values across all class levels for each metabolite feature; Benjamini–Hochberg FDR correction is applied automatically during this step to yield q-values. Use select_sign_features() to filter significant features by specifying a q-value threshold (commonly 0.05 or 0.01). Extract the resulting table containing Feature_ID, metabolite names, ANOVA statistics, p-values, q-values, and effect sizes for downstream interpretation. The choice between parametric (ANOVA) and non-parametric tests depends on whether feature abundance distributions meet normality assumptions, which should be assessed prior to testing.

## Related tools

- **margheRita** (R package providing univariate() and select_sign_features() functions for ANOVA testing and q-value-based feature filtering on normalized LC-MS/MS data) — https://github.com/emosca-cnr/margheRita
- **R** (Programming language in which margheRita is implemented)
- **notame** (Alternative R workflow package for non-targeted LC-MS metabolic profiling with statistical analysis functions; compatible via margheRita export functions) — https://github.com/hanhineva-lab/notame
- **MS-DIAL** (Peak picking and feature detection software upstream of margheRita; output processed by statistical testing workflow)

## Examples

```
univariate(data_object, metadata_col='class') |> select_sign_features(q_threshold=0.05)
```

## Evaluation signals

- Q-value distribution shows expected enrichment of small values (< 0.05) in features with biological effect, and q-values increase monotonically with increasing p-values after FDR correction.
- Number of significant features (q < threshold) is interpretable relative to study design and metabolite coverage; extreme counts (e.g., >90% of features or <1%) warrant review of threshold or data quality.
- Effect sizes (e.g., fold-change, eta-squared) for significant features are consistent with magnitude of class-level differences visible in exploratory plots (e.g., PCA, box plots by group).
- Replicate runs of univariate() on the same input data yield identical p-values and q-values.
- Tabulated results include all expected columns (Feature_ID, metabolite name, ANOVA F-statistic, p-value, q-value) with no missing or infinite values for passing features.

## Limitations

- ANOVA assumes homogeneity of variance across groups; violations may inflate Type I error rates. Consider Welch's ANOVA or non-parametric tests (Kruskal–Wallis) when variances differ substantially.
- Multiple-testing correction (Benjamini–Hochberg FDR) controls false-discovery rate but not family-wise error; choice of q-value threshold (0.05 vs 0.01) is arbitrary and should be justified a priori or validated by independent cohort.
- Statistical significance does not imply biological significance; effect sizes and fold-changes must be examined in context of biological plausibility and prior knowledge.
- Feature abundance distributions may not meet normality assumptions, especially after preprocessing (e.g., log-transformation, imputation of missing values); visualize distributions and consider rank-based tests if violations are severe.

## Evidence

- [other] Apply univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature.: "Apply univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature."
- [other] Use select_sign_features() to filter significant features based on q-value threshold (Benjamini–Hochberg FDR correction applied during univariate or select_sign_features step).: "Use select_sign_features() to filter significant features based on q-value threshold (Benjamini–Hochberg FDR correction applied during univariate or select_sign_features step)."
- [other] Extract and tabulate the results including feature identifiers, ANOVA statistics, p-values, q-values, and effect sizes.: "Extract and tabulate the results including feature identifiers, ANOVA statistics, p-values, q-values, and effect sizes."
- [readme] simplified execution of parametric and non-parametric statistical tests over a large number of features: "simplified execution of parametric and non-parametric statistical tests over a large number of features"
- [other] ANOVA testing across AA, DD, and MM class levels in the Urine dataset identified significant metabolic features, with results reported in a table including Feature_ID, metabolite names, and associated q-values for filtering at specified cutoffs.: "ANOVA testing across AA, DD, and MM class levels in the Urine dataset identified significant metabolic features, with results reported in a table including Feature_ID, metabolite names, and"
