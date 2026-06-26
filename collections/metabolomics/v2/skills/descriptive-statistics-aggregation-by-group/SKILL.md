---
name: descriptive-statistics-aggregation-by-group
description: Use when after lipid matching is complete and you have a table of matched
  lipid abundances with sample annotations (e.g., experimental condition, disease
  state, or treatment group).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3365
  tools:
  - Python (pandas, NumPy, SciPy)
  - R (base stats, tidyverse, or similar)
  - pandas
  - NumPy
  - R base stats / tidyverse
  - Lipid_MRM_parser.ipynb
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

# descriptive-statistics-aggregation-by-group

## Summary

Compute group-wise descriptive statistics (mean, standard deviation, median) on matched lipid abundance measurements, stratified by experimental condition or sample category. This intermediate aggregation step prepares data for comparative statistical testing and enables rapid assessment of central tendency and variability within cohorts.

## When to use

After lipid matching is complete and you have a table of matched lipid abundances with sample annotations (e.g., experimental condition, disease state, or treatment group). Use this skill when you need to summarize lipid expression patterns within each cohort before performing statistical hypothesis tests or generating visualizations stratified by group.

## When NOT to use

- Lipid matching has not yet been completed; abundances are still raw or unaligned.
- No group/condition metadata is available or all samples belong to a single cohort.
- Output is intended to be directly published without further statistical testing or multiple-hypothesis correction.

## Inputs

- matched lipid abundance table (CSV, TSF, or in-memory data frame)
- sample metadata with experimental condition/group assignment
- lipid identifier column

## Outputs

- group-wise descriptive statistics table (CSV or data frame)
- one row per lipid–group combination
- columns: lipid identifier, group label, mean, standard deviation, median

## How to apply

Load the matched lipid abundance table (a data frame with lipids as rows and samples as columns, plus metadata) into Python (pandas) or R. Group measurements by the experimental condition or sample category column. For each lipid and each group, calculate mean, standard deviation, and median using built-in aggregation functions (e.g., pandas.groupby().agg() or R's aggregate() or dplyr::group_by() %>% summarise()). Return a structured table with one row per lipid–group combination, containing the lipid identifier, group label, and the three descriptive statistics. This workflow ensures consistent, reproducible summarization prior to formal statistical testing.

## Related tools

- **pandas** (DataFrame grouping and aggregation (groupby, agg) for descriptive statistics computation)
- **NumPy** (Backend for mean, standard deviation, and median calculations)
- **R base stats / tidyverse** (Aggregation and grouping (aggregate, group_by, summarise) for descriptive statistics)
- **Lipid_MRM_parser.ipynb** (Python Jupyter notebook providing the full CLAW-MRM workflow including data loading and grouping) — github.com/chopralab/CLAW

## Examples

```
import pandas as pd; df_matched = pd.read_csv('Pre_EdgeR/matched_lipids.csv'); grouped_stats = df_matched.groupby('experimental_condition')[['abundance_col1', 'abundance_col2']].agg(['mean', 'std', 'median']); grouped_stats.to_csv('Pre_EdgeR/descriptive_stats_by_group.csv')
```

## Evaluation signals

- Descriptive statistics table has one row per unique lipid–group combination; no duplicate lipid–group pairs.
- All three summary statistics (mean, SD, median) are non-null for each group and lipid.
- Group labels in the output match the unique values in the input metadata condition column.
- Mean and median values fall within the observed range of raw abundances for each lipid–group pair.
- Standard deviation is ≥ 0 and is non-zero for groups with >1 replicate per lipid.

## Limitations

- Descriptive statistics alone do not provide inferential evidence; must be followed by formal statistical testing (t-test, Mann–Whitney U, ANOVA) for comparative claims.
- Median and mean can mask bimodal or skewed distributions; consider paired visualization (e.g., box plots, violin plots) to assess distribution shape.
- If group sample sizes are very unbalanced or extremely small (<2 replicates per group), SD estimates may be unstable or undefined.
- No multiple-hypothesis correction is applied at this stage; p-values and adjusted thresholds come later in the pipeline.

## Evidence

- [other] Group lipid measurements by experimental condition or sample category.: "Group lipid measurements by experimental condition or sample category."
- [other] Calculate descriptive statistics (mean, standard deviation, median) for each lipid within each group.: "Calculate descriptive statistics (mean, standard deviation, median) for each lipid within each group."
- [other] Load the matched lipid abundance table (output from the matching step) into a data frame.: "Load the matched lipid abundance table (output from the matching step) into a data frame."
- [other] Python (pandas, NumPy, SciPy), R (base stats, tidyverse, or similar): "Python (pandas, NumPy, SciPy), R (base stats, tidyverse, or similar)"
- [other] statistical analysis step as part of its workflow that operates on matched lipid data, positioned after the matching phase and before visualization: "statistical analysis step as part of its workflow that operates on matched lipid data, positioned after the matching phase and before visualization"
