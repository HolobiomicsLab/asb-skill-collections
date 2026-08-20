---
name: t-test-interpretation-metabolomics
description: Use when you have preprocessed, normalized, and imputed metabolite measurements
  organized in a MultiAssayExperiment object with two or more clearly defined sample
  groups (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDiff
  - R
  - MultiAssayExperiment
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# t-test-interpretation-metabolomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply Student's t-test with Benjamini-Hochberg multiple testing correction to identify differentially abundant metabolites between sample groups in a MultiAssayExperiment object, then extract and interpret p-values and effect sizes to detect statistically significant metabolic signatures.

## When to use

You have preprocessed, normalized, and imputed metabolite measurements organized in a MultiAssayExperiment object with two or more clearly defined sample groups (e.g., tumor phenotypes, disease states, or treatment conditions) and need to identify which individual metabolites show statistically significant differential abundance between those groups at a chosen significance threshold (e.g., p < 0.05 or adjusted p < 0.1).

## When NOT to use

- Input metabolite data has not been normalized (e.g., raw peak intensities or counts without variance-stabilizing transformation)
- Missing value imputation has not been performed or cutoff threshold (e.g., cutoff=0.4 for knn_impute) has not been justified
- Sample groups are not discrete/categorical (e.g., comparing along a continuous phenotype; use correlation-based methods instead)
- Comparing more than two groups without post-hoc pairwise testing framework

## Inputs

- Preprocessed MultiAssayExperiment object with normalized and imputed metabolite measurements
- Sample metadata with group factor (e.g., tumor_groups: AKT1-high, MYC-high)
- Subset specification identifying which groups to compare

## Outputs

- Test results table with metabolite names, unadjusted p-values, and adjusted p-values
- Effect sizes (difference in means between groups)
- Summary of significantly differential metabolites at chosen threshold

## How to apply

Load the MultiAssayExperiment object containing normalized and imputed metabolite measurements and sample group annotations (e.g., 'tumor_groups' column in colData). Subset the object to include only the groups of interest using the group factor. Apply MetaboDiff's diff_test function with the group_factors parameter set to your grouping variable and specify the statistical test (Student's t-test is standard for two-group comparisons). The function automatically applies Benjamini-Hochberg p-value correction for multiple testing to control false discovery rate. Extract the test results (unadjusted p-values, adjusted p-values, and difference in means/effect sizes) from the metadata slot. Compare adjusted p-values against your chosen significance threshold (typically p < 0.05 or p < 0.1) and generate a summary table mapping metabolite names to both unadjusted and adjusted p-values and effect sizes. Verify that metabolites of biological interest meet the threshold and that the direction of fold-change aligns with expected biology.

## Related tools

- **MetaboDiff** (Provides diff_test function to perform Student's t-test with Benjamini-Hochberg correction and extract p-values and effect sizes from metabolite abundance data) — https://github.com/andreasmock/MetaboDiff
- **R** (Statistical computing environment for differential metabolomic analysis and t-test implementation)
- **MultiAssayExperiment** (Bioconductor class for organizing preprocessed metabolite measurements, sample metadata, and group annotations required as input to diff_test)

## Examples

```
diff_test(met, group_factors='tumor_groups') %>% extract_metadata() %>% filter(p.adj < 0.05) %>% select(metabolite_name, p.value, p.adj, estimate)
```

## Evaluation signals

- Adjusted p-values reflect correct Benjamini-Hochberg correction: verify that adjusted p ≥ unadjusted p for all metabolites and that FDR rate is controlled at chosen threshold
- Effect sizes (difference in means) show plausible direction and magnitude given biological hypotheses (e.g., fatty acids elevated in AKT1-high samples reflect known AKT1-driven lipogenic metabolism)
- Key metabolites of interest (e.g., Oleic acid, Arachidonic acid, Docohexaenoic acid) appear in results with expected significance levels (*, **, or ns) matching prior knowledge from the literature or validation cohorts
- Summary table is complete with no missing values for p-values or effect sizes, and row count matches the number of metabolites in the input object
- Adjusted p-values are monotonically increasing when metabolites are sorted by unadjusted p-value (Benjamini-Hochberg property)

## Limitations

- Student's t-test assumes approximately normal distribution of metabolite abundances after normalization; violation may reduce statistical power or inflate false positives—consider exploring distribution via normality plots before interpretation
- Benjamini-Hochberg correction controls FDR but may be conservative when metabolite abundance patterns show strong correlation structures; biweight midcorrelation or network-aware methods may be more appropriate for exploring modular metabolic signatures
- Effect sizes (raw difference in means) are not standardized and depend on metabolite measurement units and normalization scale; interpretation of biological significance requires comparison to biological replicability and external validation cohorts
- Two-group t-test comparisons do not account for continuous sample traits (age, BMI, treatment dose) that may confound metabolite abundance; consider adding covariates to linear models if available
- The choice of significance threshold (p < 0.05 vs. p < 0.1) is context-dependent and affects discovery rate; exploratory analyses may warrant higher thresholds, while validation cohorts should use stricter thresholds

## Evidence

- [methods] Apply diff_test function enables differential metabolomic analysis: "Apply diff_test function with group_factors='tumor_groups' to perform Student's t-test between the two groups with Benjamini-Hochberg p-value correction."
- [methods] Extract and verify significance results for target metabolites: "Extract test results (p-values and difference in means) from the metadata slot and verify that Oleic acid, Arachidonic acid, and Docohexaenoic acid appear with significance thresholds of **, *, and *"
- [methods] Benjamini-Hochberg procedure for multiple testing correction: "The p-values are corrected for multiple testing by the Benjamini-Hochberg procedure."
- [intro] MetaboDiff enables differential metabolomic analysis from metabolite tables: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
- [methods] MultiAssayExperiment object as standard container for metabolite data: "The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis."
- [methods] Variance stabilizing normalization ensures constant variance across metabolite spectrum: "Variance stabilizing normalization (vsn) is used to ensure that the variance remains nearly constant over the measured spectrum"
