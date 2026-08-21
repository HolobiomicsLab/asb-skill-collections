---
name: p-value-computation-and-multiple-testing-correction
description: Use when after matched lipid abundances have been grouped by experimental
  condition and descriptive statistics (mean, SD, median) calculated per group.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python (pandas, NumPy, SciPy)
  - R (base stats, tidyverse, or similar)
  - pandas
  - NumPy
  - SciPy
  - R base stats
  - tidyverse
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c05039
  title: CLAW-MRM
evidence_spans:
- statistical analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_claw_mrm_cq
    doi: 10.1021/acs.analchem.4c05039
    title: CLAW-MRM
  dedup_kept_from: coll_claw_mrm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05039
  all_source_dois:
  - 10.1021/acs.analchem.4c05039
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# p-value-computation-and-multiple-testing-correction

## Summary

Compute statistical test p-values for lipid abundance comparisons between experimental groups, then apply multiple-hypothesis correction (e.g., Benjamini–Hochberg FDR) to control false discovery rate across all tested lipids. This skill produces adjusted p-values and effect sizes suitable for identifying significantly altered lipid features.

## When to use

After matched lipid abundances have been grouped by experimental condition and descriptive statistics (mean, SD, median) calculated per group. Apply this skill when you have paired or unpaired abundance measurements across two or more sample categories and need to identify lipids with statistically significant differences while controlling for multiple comparisons.

## When NOT to use

- Input data are not grouped by experimental condition or sample category; statistical grouping must be defined before testing.
- Lipid abundances have not been matched across samples; unmatched or inconsistently annotated lipids will produce spurious comparisons.
- Sample size is very small (n < 3 per group); statistical power will be severely limited and corrections may be overly conservative.

## Inputs

- matched lipid abundance table (data frame with lipid identifiers, sample/replicate IDs, abundance values, and experimental group/condition labels)

## Outputs

- statistical results table (CSV or data frame with one row per lipid: lipid identifier, group means, test statistics, unadjusted p-values, adjusted p-values, effect sizes/fold-change)

## How to apply

Partition the matched lipid abundance table by experimental condition or sample category. Select an appropriate statistical test based on study design and data distribution: use t-test for two-group comparisons, Mann–Whitney U for non-parametric pairwise comparisons, or ANOVA for ≥3 groups. Compute a p-value for each lipid's test statistic. Calculate effect sizes (fold-change between group means, Cohen's d, or similar). Apply multiple-hypothesis correction (e.g., Benjamini–Hochberg FDR procedure) to the full set of p-values to derive adjusted p-values controlling false discovery rate. Compile all results—lipid ID, group means, test statistics, unadjusted p-values, adjusted p-values, and fold-change—into a structured results table, typically exported as CSV.

## Related tools

- **pandas** (data frame construction, grouping by experimental condition, row/column manipulation for test results compilation)
- **NumPy** (numerical computation and array operations supporting statistical calculations)
- **SciPy** (statistical test functions (t-test, Mann–Whitney U, ANOVA) and p-value computation)
- **R base stats** (alternative statistical test library (t.test, wilcox.test, aov) for comparative analysis)
- **tidyverse** (R-based data manipulation and grouping operations for preparing grouped abundance data and formatting results)

## Evaluation signals

- All lipids in the matched abundance table appear exactly once in the results table (row count equivalence).
- p-values and adjusted p-values are numeric, in range [0, 1], and unadjusted p-values ≥ adjusted p-values for each lipid (correction monotonicity).
- Effect sizes (fold-change, Cohen's d) are computed for every lipid and match the direction and magnitude of observed group mean differences.
- Benjamini–Hochberg adjusted p-values reflect the cumulative distribution of unadjusted p-values (sorted p-values should show increasing adjusted values when properly applied).
- Test statistics (t-statistic, U-statistic, F-statistic) are consistent with the corresponding p-values given the sample size and degrees of freedom.

## Limitations

- Multiple-hypothesis correction becomes more conservative as the number of tested lipids increases; large-scale lipidomics may require very stringent adjusted p-value thresholds (e.g., q < 0.001).
- Benjamini–Hochberg FDR control assumes independence or positive dependence between tests; highly correlated lipid abundance measurements may invalidate assumption.
- Choice of statistical test (parametric vs. non-parametric) depends on unknown distribution properties; misspecification can inflate or deflate p-values.
- No changelog provided in repository; implementation details of test selection and correction may differ between versions or instances.

## Evidence

- [other] Perform statistical tests (e.g., t-test, Mann–Whitney U, or ANOVA as appropriate to study design) to compare lipid abundances between groups, computing p-values and effect sizes (e.g., fold-change, Cohen's d).: "Perform statistical tests (e.g., t-test, Mann–Whitney U, or ANOVA as appropriate to study design) to compare lipid abundances between groups, computing p-values and effect sizes (e.g., fold-change,"
- [other] Apply multiple-hypothesis correction (e.g., Benjamini–Hochberg FDR) to control false discovery rate.: "Apply multiple-hypothesis correction (e.g., Benjamini–Hochberg FDR) to control false discovery rate."
- [other] Compile results into a structured table with one row per lipid, including lipid identifier, group means, test statistics, adjusted p-values, and fold-change values.: "Compile results into a structured table with one row per lipid, including lipid identifier, group means, test statistics, adjusted p-values, and fold-change values."
- [other] Group lipid measurements by experimental condition or sample category.: "Group lipid measurements by experimental condition or sample category."
- [intro] streamline various tasks such as data parsing, matching, statistical analysis, and visualization: "streamline various tasks such as data parsing, matching, statistical analysis, and visualization"
