---
name: metabolite-feature-anova-analysis
description: Use when you have normalized abundance data from LC-MS/MS for multiple samples classified into three or more discrete groups (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - margheRita
  - R
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

# metabolite-feature-anova-analysis

## Summary

Perform univariate ANOVA across sample class groups (e.g., AA, DD, MM) to identify metabolic features with statistically significant abundance differences, followed by multiple-testing correction and feature selection. This skill is essential when comparing metabolite profiles across three or more distinct phenotypic or clinical classes in untargeted LC-MS/MS metabolomics studies.

## When to use

You have normalized abundance data from LC-MS/MS for multiple samples classified into three or more discrete groups (e.g., disease states, genotypes, treatment conditions), and you need to discover which metabolic features show significant variation across those groups rather than random noise. This is typically applied after quality control, filtering, and normalization steps have been completed, and the normalized feature matrix is ready for statistical testing.

## When NOT to use

- If you have only two sample groups (use a two-sample t-test or Mann–Whitney U test instead of ANOVA).
- If the normalized data contains many missing values that have not been imputed or handled; missing data can bias ANOVA estimates.
- If sample classes are not well-balanced and no correction for unequal group sizes or variance heterogeneity has been considered, particularly when Levene's test indicates significant violations of homogeneity of variance.

## Inputs

- Normalized feature abundance matrix (e.g., Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt)
- Sample metadata with discrete class assignments (e.g., AA, DD, MM phenotype labels)
- margheRita data object created via data import with class annotations

## Outputs

- Table of significant metabolic features with Feature_ID, metabolite name, ANOVA F-statistic, p-value, q-value, and effect size
- Filtered feature set meeting q-value threshold criterion
- Statistical summary report for downstream pathway analysis or metabolite identification

## How to apply

Load the normalized feature abundance matrix (e.g., Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt) into margheRita as a data object with sample metadata containing class assignments. Apply the univariate() function to compute ANOVA F-statistics and p-values for each metabolic feature across the class levels. The function automatically performs Benjamini–Hochberg false-discovery rate (FDR) correction to obtain q-values. Filter significant features using select_sign_features() with a specified q-value cutoff threshold (commonly 0.05 or 0.1). Extract and tabulate results including Feature_ID, metabolite names, ANOVA statistics, raw p-values, adjusted q-values, and effect sizes to create the final output report of significant metabolic features.

## Related tools

- **margheRita** (Executes univariate() and select_sign_features() functions to compute ANOVA F-statistics, p-values, FDR-corrected q-values, and filter significant metabolic features) — https://github.com/emosca-cnr/margheRita
- **R** (Programming environment and runtime for margheRita package execution)
- **MS-DIAL** (Upstream peak-picking and feature detection software; margheRita processes MS-DIAL output)

## Examples

```
univariate(data = urine_mrobj, group_var = 'class'); significant_features <- select_sign_features(univariate_results, q_cutoff = 0.05)
```

## Evaluation signals

- ANOVA F-statistics and raw p-values are calculated for every feature without missing values; count and range match the total number of features in the input matrix.
- Benjamini–Hochberg FDR correction has been applied: q-values are monotonically non-decreasing as raw p-values increase, and at least some q-values equal 1.0 (features with highest raw p-values).
- Selected features at a specified q-value threshold (e.g., q < 0.05) are a strict subset of all tested features; each selected feature has a q-value ≤ the cutoff.
- Feature table includes metabolite identifiers (Feature_ID, m/z, retention time, or metabolite name) allowing cross-reference with spectral libraries or MS/MS databases.
- Summary statistics (e.g., count of significant features, range of q-values, median effect size) are consistent with biological expectations for the sample classes tested.

## Limitations

- ANOVA assumes normality of residuals within each group; violations may require non-parametric alternatives (Kruskal–Wallis test) available in margheRita.
- ANOVA assumes homogeneity of variance across groups; severely imbalanced group sizes or high variance heterogeneity may reduce statistical power or inflate Type I error rates.
- Multiple-testing correction via Benjamini–Hochberg FDR controls the expected proportion of false discoveries but does not provide absolute confidence in individual feature calls; validation in an independent cohort or via orthogonal methods is recommended.
- Missing values in the feature abundance matrix must be handled (imputation or exclusion) prior to ANOVA; the univariate() function typically excludes features with incomplete data for a given group.

## Evidence

- [other] Apply univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature.: "Apply univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature."
- [other] Use select_sign_features() to filter significant features based on q-value threshold (Benjamini–Hochberg FDR correction applied during univariate or select_sign_features step).: "Use select_sign_features() to filter significant features based on q-value threshold (Benjamini–Hochberg FDR correction applied during univariate or select_sign_features step)."
- [readme] simplified execution of parametric and non-parametric statistical tests over a large number of features: "simplified execution of parametric and non-parametric statistical tests over a large number of features"
- [other] ANOVA testing across AA, DD, and MM class levels in the Urine dataset identified significant metabolic features, with results reported in a table including Feature_ID, metabolite names, and associated q-values for filtering at specified cutoffs.: "ANOVA testing across AA, DD, and MM class levels in the Urine dataset identified significant metabolic features, with results reported in a table including Feature_ID, metabolite names, and"
- [other] Load the normalized Urine dataset (Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt) into margheRita as a data object with sample metadata including AA/DD/MM class assignments.: "Load the normalized Urine dataset (Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt) into margheRita as a data object with sample metadata including AA/DD/MM class assignments."
