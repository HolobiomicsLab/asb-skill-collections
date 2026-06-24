---
name: lipid-abundance-statistical-comparison
description: Use when after lipid matching is complete and you have a table of normalized
  lipid abundances aligned across samples, grouped into distinct experimental conditions
  or phenotypic categories (e.g., diseased vs. control, treated vs. untreated).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - Python (pandas, NumPy, SciPy)
  - R (base stats, tidyverse, or similar)
  - pandas
  - NumPy
  - SciPy
  - R tidyverse / base stats
  - edgeR
  license_tier: open
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

# lipid-abundance-statistical-comparison

## Summary

Statistical comparison of lipid abundances across experimental groups or sample categories to identify differentially abundant lipids. This skill applies hypothesis testing, effect size estimation, and multiple-hypothesis correction to matched lipid abundance tables to generate publication-ready comparative statistics.

## When to use

After lipid matching is complete and you have a table of normalized lipid abundances aligned across samples, grouped into distinct experimental conditions or phenotypic categories (e.g., diseased vs. control, treated vs. untreated). Use this skill when your research question asks which lipids show significant differences in abundance between groups.

## When NOT to use

- Input lipid abundance table has not yet been matched across samples — perform matching step first.
- Samples are not clearly assigned to experimental groups or conditions.
- Study contains only a single sample or condition — no inter-group comparison is possible.

## Inputs

- matched lipid abundance table (data frame with lipids as rows, samples as columns, normalized intensity values)
- sample metadata/labels defining experimental group assignments
- study design specification (paired/unpaired, number of groups)

## Outputs

- statistical results table (CSV) with columns: lipid identifier, group means, test statistics, p-values, adjusted p-values (FDR), fold-change, effect size
- summary statistics report

## How to apply

Load the matched lipid abundance table into a data frame, grouping measurements by experimental condition. Calculate descriptive statistics (mean, standard deviation, median) for each lipid within each group. Select and apply an appropriate statistical test based on study design and data distribution: t-test for two normally distributed groups, Mann–Whitney U for non-normal data, or ANOVA for multiple groups. Compute p-values and effect sizes (fold-change or Cohen's d). Apply multiple-hypothesis correction (Benjamini–Hochberg FDR is standard) to control false discovery rate. Compile results into a structured table with one row per lipid, including lipid identifier, group means, test statistics, adjusted p-values, and fold-change values. Export as CSV.

## Related tools

- **pandas** (data frame manipulation, grouping by condition, calculating descriptive statistics)
- **NumPy** (numerical computation supporting statistical operations)
- **SciPy** (statistical testing (t-test, Mann–Whitney U, ANOVA) and p-value computation)
- **R tidyverse / base stats** (alternative platform for grouping, descriptive statistics, and statistical testing)
- **edgeR** (differential abundance analysis and summary/full results generation in CLAW-MRM workflow) — github.com/chopralab/CLAW

## Evaluation signals

- Output table contains one row per unique lipid identifier with no duplicates.
- All group means are numeric and non-null for lipids present in all groups; missing values are documented.
- Adjusted p-values (FDR) are monotonically non-decreasing when sorted by unadjusted p-values.
- Fold-change values are non-zero and effect sizes are within expected biological or statistical ranges (e.g., Cohen's d typically between −3 and +3 for reasonable group separation).
- CSV schema matches specification: lipid ID, group means, test statistic, p-value, adjusted p-value, fold-change, and optionally effect size columns are all present and properly formatted.

## Limitations

- No guidance provided on minimum group sample size requirements or statistical power calculations.
- Choice of multiple-hypothesis correction method (e.g., Benjamini–Hochberg vs. Bonferroni) affects false discovery rate control; context recommends FDR but does not discuss trade-offs.
- No changelog documented in repository; reproducibility of specific statistical method versions or parameter changes over time is unclear.

## Evidence

- [other] Perform statistical tests (e.g., t-test, Mann–Whitney U, or ANOVA as appropriate to study design) to compare lipid abundances between groups, computing p-values and effect sizes (e.g., fold-change, Cohen's d).: "Perform statistical tests (e.g., t-test, Mann–Whitney U, or ANOVA as appropriate to study design) to compare lipid abundances between groups, computing p-values and effect sizes (e.g., fold-change,"
- [other] Apply multiple-hypothesis correction (e.g., Benjamini–Hochberg FDR) to control false discovery rate.: "Apply multiple-hypothesis correction (e.g., Benjamini–Hochberg FDR) to control false discovery rate."
- [other] statistical analysis step as part of its workflow that operates on matched lipid data, positioned after the matching phase and before visualization: "statistical analysis step as part of its workflow that operates on matched lipid data, positioned after the matching phase and before visualization"
- [other] Calculate descriptive statistics (mean, standard deviation, median) for each lipid within each group.: "Calculate descriptive statistics (mean, standard deviation, median) for each lipid within each group."
- [readme] Utilize the main components of CLAW-MRM, such as the Python notebook Lipid_MRM_parser.ipynb and the R script edgeR.R, to perform data analysis, visualization, and statistical tests on lipidomics datasets.: "Utilize the main components of CLAW-MRM, such as the Python notebook Lipid_MRM_parser.ipynb and the R script edgeR.R, to perform data analysis, visualization, and statistical tests on lipidomics"
