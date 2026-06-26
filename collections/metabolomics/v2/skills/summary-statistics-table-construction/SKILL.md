---
name: summary-statistics-table-construction
description: Use when when you need to quantify and compare the effect of multiple
  filtering thresholds (e.g., Match.Factor ≥65, ≥80, ≥90) on the size of a retained
  compound set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - R
  - uafR
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with
  simple modifications
- any software or utility that generates the necessary information can be used with
  simple modifications (e.g. changing the column names)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_uafr
    doi: 10.1371/journal.pone.0306202
    title: uafr
  dedup_kept_from: coll_uafr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pone.0306202
  all_source_dois:
  - 10.1371/journal.pone.0306202
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# summary-statistics-table-construction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct a summary table that aggregates counts or statistics across multiple filter conditions applied to a compound dataset. This skill is used to compare how data volume changes when different threshold criteria are applied to mass spectrometry results.

## When to use

When you need to quantify and compare the effect of multiple filtering thresholds (e.g., Match.Factor ≥65, ≥80, ≥90) on the size of a retained compound set. This is appropriate when the analysis goal is to demonstrate filter sensitivity or to select an optimal threshold that balances data retention with quality criteria.

## When NOT to use

- The input data does not contain a Match.Factor column or equivalent quality metric.
- The goal is to retain all compounds without filtering; threshold comparison is not relevant.
- You need to summarize properties of individual compounds (e.g., molecular weight, retention time) rather than counts across threshold conditions.

## Inputs

- CSV file with columns 'Compound.Name' and 'Match.Factor' (e.g., standard_data.csv)
- One or more numeric threshold values for Match.Factor filtering

## Outputs

- Summary table (data frame or CSV) with columns for threshold condition label, threshold value, and compound count
- Optionally: a saved CSV file containing the summary comparison

## How to apply

Load the data file (standard_data.csv) into R and extract the relevant columns (Compound.Name and Match.Factor). Apply each filter threshold independently—for example, Match.Factor >= 65, >= 80, and >= 90—and extract unique compound names satisfying each condition (labeled COND-mf65, COND-mf80, COND-mf90). Count the number of unique compounds retained under each threshold. Construct a summary table with one row per threshold condition and columns for the threshold value and the corresponding compound count. Save the result as a CSV file. The rationale is that visualizing counts side-by-side allows rapid assessment of how stringent each threshold is and supports informed selection of the most appropriate filter level for downstream analysis.

## Related tools

- **R** (Language and environment for loading CSV, filtering by Match.Factor threshold, counting unique compounds, and constructing the summary table)
- **uafR** (R package providing helper functions (spreadOut, mzExacto) for preprocessing and filtering mass spectrometry data; filtering logic can be applied before or after using these functions) — https://github.com/castratton/uafR

## Examples

```
input_dat = read.csv('standard_data.csv'); counts = c(length(unique(input_dat$Compound.Name[input_dat$Match.Factor >= 65])), length(unique(input_dat$Compound.Name[input_dat$Match.Factor >= 80])), length(unique(input_dat$Compound.Name[input_dat$Match.Factor >= 90]))); summary_tbl = data.frame(Threshold = c('>=65', '>=80', '>=90'), Compound.Count = counts); write.csv(summary_tbl, 'match_factor_summary.csv', row.names = FALSE)
```

## Evaluation signals

- The summary table contains exactly one row per threshold condition tested (e.g., three rows for thresholds ≥65, ≥80, ≥90).
- Compound counts decrease monotonically as the threshold becomes more stringent (count at ≥65 ≥ count at ≥80 ≥ count at ≥90).
- All compound names extracted under each filter are unique (no duplicates within a condition group).
- The threshold values in the summary table match the filter criteria applied (e.g., 65, 80, 90).
- The summary table is saved in a standard format (CSV or tabular object) with named columns and human-readable headers.

## Limitations

- The quality of the summary depends on the quality and consistency of the Match.Factor values in the input file; missing or non-numeric Match.Factor entries will cause filtering errors.
- The threshold values must be selected a priori; the skill does not suggest optimal thresholds automatically.
- If compounds have multiple rows (e.g., from different files or runs), the 'unique' counting step may mask important sample-level variation.
- The summary table alone does not validate whether the filtered compounds are biologically or chemically meaningful; it only quantifies retention.

## Evidence

- [methods] Match.Factor filtering can be applied at multiple threshold levels: "Apply three independent filters: Match.Factor >= 65, Match.Factor >= 80, and Match.Factor >= 90, retaining unique compound names for each filter."
- [methods] Counting compounds per threshold: "Count the number of unique compounds retained under each threshold condition (COND-mf65, COND-mf80, COND-mf90)."
- [methods] Summary table structure and output: "Construct a summary table with three rows (one per threshold) and two columns (threshold value and compound count). Save the comparison table as a CSV file."
- [readme] Example R filter invocation: "query_chems = standard_dat$Compound.Name[standard_dat$Match.Factor >= 65]"
