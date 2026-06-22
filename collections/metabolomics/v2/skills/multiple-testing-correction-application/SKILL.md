---
name: multiple-testing-correction-application
description: Use when when performing statistical tests (e.g., t-tests, ANOVA) across many metabolites in a MultiAssayExperiment object to identify differentially abundant metabolites between sample groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2885
  - http://edamontology.org/topic_3047
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multiple-testing-correction-application

## Summary

Application of Benjamini-Hochberg false discovery rate correction to p-values from differential metabolite abundance tests to control for multiple comparisons across many metabolites. This skill ensures that significance claims in metabolomic differential abundance remain valid when testing hundreds of metabolites simultaneously.

## When to use

When performing statistical tests (e.g., t-tests, ANOVA) across many metabolites in a MultiAssayExperiment object to identify differentially abundant metabolites between sample groups. Multiple testing correction is mandatory when testing dozens or hundreds of metabolite features simultaneously; without it, false positives accumulate rapidly. Apply this skill after computing unadjusted p-values from diff_test but before reporting or filtering metabolites as 'significant'.

## When NOT to use

- When testing only a single metabolite or a small handful of pre-specified hypotheses (Bonferroni or no correction may be more appropriate)
- When p-values have already been adjusted by another multiple-testing procedure in upstream analysis
- When the input p-values violate assumptions of the correction method (e.g., non-uniform null distribution due to severe confounding or batch effects not accounted for in the model)

## Inputs

- MultiAssayExperiment object with normalized and imputed metabolite measurements
- Vector or data.frame of unadjusted p-values from diff_test function
- Sample group annotations (e.g., tumor_groups factor)
- Effect sizes (difference in means between groups)

## Outputs

- Summary table mapping metabolite names to unadjusted p-values, Benjamini-Hochberg adjusted p-values, and effect sizes
- Filtered list of metabolites meeting adjusted p-value significance threshold
- Annotated results with significance symbols (**, *, or ns) based on adjusted p-values

## How to apply

After executing diff_test with group_factors to perform Student's t-tests between sample groups, extract the unadjusted p-values from the metadata slot. Apply the Benjamini-Hochberg procedure to correct these p-values for multiple testing, controlling the false discovery rate rather than the family-wise error rate. This is more appropriate for exploratory metabolomics where you expect some true signals among many tests. Extract both unadjusted and adjusted p-values along with effect sizes (difference in means) into a summary table. Filter metabolites using the adjusted p-value threshold (e.g., adjusted p < 0.05) to identify metabolites with statistically significant differential abundance, and verify that expected metabolites (e.g., Oleic acid, Arachidonic acid, Docohexaenoic acid in the AKT1-high vs MYC-high comparison) achieve target significance levels.

## Related tools

- **MetaboDiff** (Provides diff_test function that computes unadjusted p-values from Student's t-tests between sample groups; outputs p-values to metadata slot for subsequent multiple-testing correction) — https://github.com/andreasmock/MetaboDiff
- **R** (Language and environment for implementing Benjamini-Hochberg correction (via p.adjust function) and generating summary tables of corrected p-values)
- **MultiAssayExperiment** (Data container storing metabolite measurements, sample metadata, and test results that enables organized extraction and annotation of p-values and effect sizes)

## Examples

```
# After diff_test: results <- diff_test(met, group_factors='tumor_groups'); adjusted_p <- p.adjust(results$pvalue, method='BH'); summary_table <- data.frame(metabolite=names(results), unadjusted_p=results$pvalue, adjusted_p=adjusted_p, effect_size=results$mean_diff)
```

## Evaluation signals

- Adjusted p-values are monotonically non-decreasing when sorted by rank of unadjusted p-values (i.e., smaller unadjusted p ≤ larger unadjusted p implies smaller adjusted p ≤ larger adjusted p)
- All adjusted p-values are ≥ their corresponding unadjusted p-values
- Expected metabolites (Oleic acid, Arachidonic acid, Docohexaenoic acid in AKT1-high vs MYC-high) appear in the summary table with adjusted p-values < 0.05 and correct significance symbols (**=p<0.01, *=p<0.05)
- The number of metabolites passing the adjusted p < 0.05 threshold is substantially smaller than the number passing unadjusted p < 0.05, reflecting conservative control of false discovery
- Summary table contains exactly three columns per metabolite: metabolite name, unadjusted p-value, adjusted p-value, and effect size (difference in means)

## Limitations

- Benjamini-Hochberg correction assumes independence or weak positive dependence between tests; metabolites in a common pathway may violate this, potentially underestimating true discoveries
- Correction is conservative when the proportion of true nulls is very high (common in exploratory metabolomics); alternative methods (e.g., q-value) may be more powerful but require assumptions about the null distribution
- Effectiveness depends critically on the upstream statistical model (diff_test parameters, group definitions, normalization quality); confounding, batch effects, or poor sample grouping will inflate p-values and reduce power regardless of correction method
- The article does not discuss handling of ties or missing p-values in the correction procedure; implementation details may vary by software version

## Evidence

- [methods] The p-values are corrected for multiple testing by the Benjamini-Hochberg procedure.: "The p-values are corrected for multiple testing by the Benjamini-Hochberg procedure."
- [other] diff_test function can be applied to identify differentially abundant metabolites between AKT1-high and MYC-high sample groups with significance thresholds: "Apply diff_test function with group_factors='tumor_groups' to perform Student's t-test between the two groups with Benjamini-Hochberg p-value correction."
- [other] Extract test results and verify that Oleic acid, Arachidonic acid, and Docohexaenoic acid appear with significance thresholds: "Extract test results (p-values and difference in means) from the metadata slot and verify that Oleic acid, Arachidonic acid, and Docohexaenoic acid appear with significance thresholds of **, *, and *"
- [intro] MetaboDiff enables differential metabolomic analysis starting from metabolite measurement tables: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
