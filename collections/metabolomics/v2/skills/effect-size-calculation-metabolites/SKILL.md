---
name: effect-size-calculation-metabolites
description: Use when after applying statistical tests (e.g., Student's t-test) to identify differentially abundant metabolites between two or more sample groups in a MultiAssayExperiment object.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDiff
  - R
  - MultiAssayExperiment
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty344
  all_source_dois:
  - 10.1093/bioinformatics/bty344
  - 10.1158/0008-5472.can-14-1490
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Effect Size Calculation for Metabolites

## Summary

Quantify the magnitude of differential abundance between sample groups in metabolomic studies by computing effect sizes (difference in means) alongside statistical significance. This skill enables detection of biologically meaningful metabolic signatures beyond p-value thresholds.

## When to use

After applying statistical tests (e.g., Student's t-test) to identify differentially abundant metabolites between two or more sample groups in a MultiAssayExperiment object. Use this skill when you need to distinguish between statistically significant but small-magnitude changes and large-magnitude shifts in metabolite abundance that are clinically or biologically relevant.

## When NOT to use

- Input lacks replicate measurements within groups—effect size estimation requires group-level abundance statistics.
- Metabolite abundances have not been normalized and imputed—effect sizes computed on raw or partially missing data are unreliable.
- Single-group or cross-sectional studies with no comparator group to define 'difference in means'.

## Inputs

- MultiAssayExperiment object with normalized and imputed metabolite measurements
- Differential test results metadata (p-values from diff_test function)
- Group factor assignments (e.g., tumor_groups with AKT1-high and MYC-high levels)

## Outputs

- Summary table: metabolite names × unadjusted p-values × adjusted p-values × effect sizes (difference in means)
- Ranked metabolite list ordered by effect size magnitude
- Effect size annotations (significance symbols: **, *, or ns)

## How to apply

Extract effect sizes (difference in means) from the metadata slot of the diff_test output alongside unadjusted and Benjamini-Hochberg adjusted p-values. Calculate or retrieve the mean metabolite abundance for each group being compared (e.g., AKT1-high vs. MYC-high samples) and compute their difference. Generate a summary table mapping metabolite names to effect sizes, unadjusted p-values, and adjusted p-values, then rank metabolites by effect size magnitude to prioritize those with both statistical significance and biological relevance. The rationale is that metabolites with large effect sizes represent robust, reproducible metabolic signatures less prone to technical variability.

## Related tools

- **MetaboDiff** (Executes diff_test function to compute p-values and extract effect sizes from metabolite differential abundance test results) — https://github.com/andreasmock/MetaboDiff
- **MultiAssayExperiment** (Container object that stores normalized metabolite measurements and group metadata required for effect size calculation)
- **R** (Statistical environment for extracting metadata, computing differences in means, and generating summary tables)

## Examples

```
met_results <- diff_test(met, group_factors='tumor_groups'); summary_table <- data.frame(metabolite=rownames(met_results), p_value=met_results$pvalue, p_adjusted=met_results$pvalue_adj, effect_size=met_results$mean_diff)
```

## Evaluation signals

- Effect sizes are numeric (difference in means), not NA, and have interpretable magnitude (e.g., log-fold or absolute concentration units).
- Metabolites with adjusted p-value < 0.05 also show non-negligible effect sizes (e.g., |difference| > 0 or dataset-specific threshold); conversely, metabolites with large effect sizes but p > 0.05 are flagged for underpowered comparison.
- Summary table row count equals the number of metabolites analyzed; no metabolites are dropped without explicit justification.
- Effect sizes and p-values are positively correlated (larger magnitude changes tend toward lower p-values); if not, investigate normalization or imputation artifacts.
- Oleic acid, Arachidonic acid, and Docohexaenoic acid in the Priolo dataset reproducibly appear with reported significance levels (**, *, *) matching effect size ranks.

## Limitations

- Effect size magnitude is sample-size-dependent; small sample sizes or high variance inflate confidence intervals around point estimates without reducing the reported effect size.
- Benjamini-Hochberg correction controls false discovery rate for p-values but does not adjust effect size estimates; large effects observed by chance in high-dimensional searches may not replicate.
- Missing metabolites imputed via k-nearest neighbor (cutoff=0.4) contribute reduced variance and potentially deflated effect sizes; compare imputed vs. non-imputed metabolites separately if replication fidelity is critical.
- Effect size calculation assumes group-wise normality post-variance-stabilizing normalization (vsn); violations (e.g., skewed distributions after vsn) may bias difference-in-means estimates.

## Evidence

- [methods] Extract effect sizes for metabolite comparison: "Extract test results (p-values and difference in means) from the metadata slot and verify that Oleic acid, Arachidonic acid, and Docohexaenoic acid appear with significance thresholds"
- [methods] Normalize abundances before effect size computation: "Variance stabilizing normalization (vsn) is used to ensure that the variance remains nearly constant over the measured spectrum"
- [methods] Apply multiple testing correction to p-values alongside effect sizes: "The p-values are corrected for multiple testing by the Benjamini-Hochberg procedure."
- [readme] MetaboDiff enables differential analysis from measurement tables: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
