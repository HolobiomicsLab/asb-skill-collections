---
name: unique-compound-enumeration
description: Use when you have a GC-MS results table with a Match.Factor column (representing identification confidence) and you need to understand how many distinct compounds survive at different quality cutoffs (e.g., ≥65, ≥80, ≥90).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0654
  tools:
  - R
  - uafR
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with simple modifications
- any software or utility that generates the necessary information can be used with simple modifications (e.g. changing the column names)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unique-compound-enumeration

## Summary

Enumerate and count unique chemical compounds in a mass spectrometry dataset after applying quality-based filtering thresholds. This skill isolates high-confidence identifications from GC-MS outputs by retaining only compounds that meet specified Match.Factor criteria, enabling comparison of compound set size across threshold levels.

## When to use

Apply this skill when you have a GC-MS results table with a Match.Factor column (representing identification confidence) and you need to understand how many distinct compounds survive at different quality cutoffs (e.g., ≥65, ≥80, ≥90). Use it to characterize the trade-off between stringency and compound retention, or to subset a compound library for downstream cheminformatics analysis.

## When NOT to use

- Input data lacks a Match.Factor column or Match.Factor values are not numeric or populated.
- You need to retain all compounds (including low-confidence hits) without filtering; use the raw dataset instead.
- Your goal is to compare compounds across files or samples rather than subset by quality; use aggregation or retention-time sorting instead.

## Inputs

- GC-MS results CSV file with columns: Compound.Name, Match.Factor, and standard fields (Component.RT, Base.Peak.MZ, Component.Area, File.Name)
- Numeric threshold values (e.g., 65, 80, 90) representing minimum acceptable Match.Factor values

## Outputs

- Summary table (data.frame or CSV) with rows for each threshold and columns: threshold_value, unique_compound_count
- Filtered compound name vectors corresponding to each threshold condition

## How to apply

Load the GC-MS CSV file (with required columns: Compound.Name, Match.Factor) into R. Apply independent Match.Factor filters at each threshold (e.g., >= 65, >= 80, >= 90), retaining unique compound names for each condition. Count the number of distinct compounds passing each threshold using unique() and length(). Construct a summary table with one row per threshold level and columns for the threshold value and the count of unique compounds retained. Save the comparison table as CSV for reporting. The rationale is that Match.Factor is a reliability metric; higher thresholds remove lower-confidence identifications and reduce the compound set size, allowing you to quantify this effect and choose an appropriate balance for your analysis goals.

## Related tools

- **R** (Primary language for loading CSV, filtering by Match.Factor threshold, counting unique compounds with unique() and length(), and constructing summary tables)
- **uafR** (R package providing spreadOut() and mzExacto() functions to prepare and extract query chemicals from GC-MS datasets; integrates with this skill for filtered compound list handling) — https://github.com/castratton/uafR

## Examples

```
query_chems_65 = unique(input_dat$Compound.Name[input_dat$Match.Factor >= 65]); query_chems_80 = unique(input_dat$Compound.Name[input_dat$Match.Factor >= 80]); query_chems_90 = unique(input_dat$Compound.Name[input_dat$Match.Factor >= 90]); summary_table = data.frame(threshold = c(65, 80, 90), count = c(length(query_chems_65), length(query_chems_80), length(query_chems_90))); write.csv(summary_table, 'compound_summary.csv', row.names = FALSE)
```

## Evaluation signals

- The summary table contains exactly N rows (one per threshold) with columns threshold_value and unique_compound_count, no missing values.
- Compound counts are monotonically non-increasing as threshold increases (e.g., count_mf65 >= count_mf80 >= count_mf90).
- Each count matches manual verification: length(unique(input_dat$Compound.Name[input_dat$Match.Factor >= threshold])).
- No duplicate compound names within a threshold's filtered set (unique() removes duplicates correctly).
- Output CSV parses without errors and threshold values match the input specification (e.g., 65, 80, 90).

## Limitations

- Match.Factor cutoffs are arbitrary; the article does not provide domain justification for specific thresholds (65, 80, 90). Threshold selection should be guided by method validation or downstream analysis needs.
- This skill counts unique compound names only; it does not account for structural identity (e.g., different isomers with the same name or same chemical with variant names).
- The approach assumes Match.Factor is available and trustworthy; if the underlying GC-MS data quality is poor or the matching algorithm is biased, filtering on Match.Factor alone may not ensure true identifications.
- Compound name standardization is not performed; spelling variations or capitalization differences may cause the same chemical to be counted as multiple unique compounds.

## Evidence

- [other] How many query chemicals are retained in the standard_data.csv compound list when applying Match.Factor filter thresholds of ≥65, ≥80, and ≥90?: "research_question from task_004"
- [other] Apply three independent filters: Match.Factor >= 65, Match.Factor >= 80, and Match.Factor >= 90, retaining unique compound names for each filter.: "workflow step 2 from task_004"
- [other] Count the number of unique compounds retained under each threshold condition (COND-mf65, COND-mf80, COND-mf90).: "workflow step 3 from task_004"
- [methods] query_chems = standard_dat$Compound.Name[standard_dat$Match.Factor >= 65]: "Match.Factor filtering example demonstrating threshold-based subsetting"
- [readme] The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "Required input columns for uafR workflows"
- [readme] query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]: "Example R code showing Match.Factor-based filtering to extract query chemicals"
