---
name: differential-metabolite-abundance-testing
description: Use when you have preprocessed and normalized metabolite measurements
  from two or more distinct biological groups (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
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

# differential-metabolite-abundance-testing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply statistical hypothesis testing to identify metabolites with significantly different abundance between two or more sample groups in a preprocessed MultiAssayExperiment object. This skill detects disease-specific or condition-specific metabolic signatures using Student's t-test with Benjamini-Hochberg multiple-testing correction.

## When to use

You have preprocessed and normalized metabolite measurements from two or more distinct biological groups (e.g., tumor vs. normal, AKT1-high vs. MYC-high) in a MultiAssayExperiment object, and you want to identify which individual metabolites show statistically significant differences in abundance between groups. This is the appropriate entry point after quality control, imputation, and normalization are complete.

## When NOT to use

- Metabolite measurements have not yet been normalized and imputed — apply normalize_met and knn_impute first.
- You are analyzing a single group or unpaired samples without a clear control or comparison group.
- The input is already a filtered feature table of pre-selected metabolites; this skill is for unbiased testing across all measured metabolites.

## Inputs

- MultiAssayExperiment object containing normalized metabolite measurements
- Sample group annotations (colData with group factor, e.g., 'tumor_groups')
- Metabolite rowData with valid identifiers (metabolite names or IDs)

## Outputs

- Differential abundance test results table (metabolite name, unadjusted p-value, Benjamini-Hochberg adjusted p-value, difference in means, significance notation)
- Ranked list of significantly different metabolites at chosen threshold

## How to apply

Load the preprocessed MultiAssayExperiment object and subset samples to the groups of interest using the group factor (e.g., tumor_groups). Apply the MetaboDiff diff_test function with group_factors parameter set to the relevant column name and perform Student's t-test to compute p-values and mean differences for each metabolite. Apply Benjamini-Hochberg correction to all p-values to control for false discovery rate across the multiple metabolites tested. Extract the test results (unadjusted p-values, adjusted p-values, and effect sizes) from the metadata slot. Use standard significance thresholds (e.g., adjusted p < 0.05 or * / ** notation) to rank and report metabolites with the strongest evidence of differential abundance.

## Related tools

- **MetaboDiff** (Primary R package providing diff_test function for Student's t-test and p-value extraction from MultiAssayExperiment objects) — https://github.com/andreasmock/MetaboDiff
- **MultiAssayExperiment** (Data container for storing and subsetting normalized metabolite assay data with associated sample and feature annotations)
- **R** (Statistical computing environment for executing differential metabolomic analysis workflow)

## Examples

```
diff_test(met, group_factors='tumor_groups')
```

## Evaluation signals

- Metabolites with known biological relevance to the comparison (e.g., Oleic acid, Arachidonic acid, Docohexaenoic acid in lipid metabolism studies) appear with expected significance thresholds (p < 0.05 adjusted).
- Benjamini-Hochberg adjusted p-values are all ≥ unadjusted p-values and number of adjusted p-values < 0.05 is ≤ number of unadjusted p-values < 0.05.
- Difference in means effect sizes are in the same direction and magnitude as biological expectations (e.g., higher abundance in one group vs. the other).
- Summary table is complete with no missing p-values or effect size entries for tested metabolites.
- Test results include both raw and adjusted p-values to enable two-level filtering (e.g., unadjusted p < 0.05 for exploratory review, adjusted p < 0.05 for stringent significance).

## Limitations

- Student's t-test assumes approximately normal distributions within groups; if normality is violated, results may be unreliable — check quality_plot and pca_plot before proceeding.
- Benjamini-Hochberg correction assumes independence of metabolite tests; violation (e.g., correlated metabolites in same pathway) may inflate false discovery rate.
- Small sample sizes per group reduce statistical power; effect sizes should be reported alongside p-values to distinguish true biological differences from noise.
- Missing data imputed via knn_impute with cutoff=0.4 may introduce bias if missingness is non-random; results should be validated with sensitivity analysis.

## Evidence

- [methods] diff_test function application: "Apply diff_test function with group_factors='tumor_groups' to perform Student's t-test between the two groups with Benjamini-Hochberg p-value correction."
- [methods] expected output format: "Extract test results (p-values and difference in means) from the metadata slot and verify that Oleic acid, Arachidonic acid, and Docohexaenoic acid appear with significance thresholds"
- [intro] purpose of differential testing: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
- [methods] Benjamini-Hochberg procedure: "The p-values are corrected for multiple testing by the Benjamini-Hochberg procedure."
- [methods] MultiAssayExperiment data structure: "The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis."
