---
name: compound-data-subsetting-by-threshold
description: Use when you have a GC-MS dataset with a Match.Factor column (or equivalent quality metric) and need to evaluate how many unique compounds are retained at different confidence thresholds, or when you must subset the compound list to a user-defined quality level before downstream cheminformatics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - R
  - uafR
  - Agilent Unknowns Analysis
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

# compound-data-subsetting-by-threshold

## Summary

This skill filters a compound list from GC-MS data by applying quantitative quality thresholds (e.g., Match.Factor ≥65, ≥80, ≥90) to retain only compounds meeting specified matching criteria. It is essential for reducing false positives and focusing analysis on high-confidence chemical identifications.

## When to use

Use this skill when you have a GC-MS dataset with a Match.Factor column (or equivalent quality metric) and need to evaluate how many unique compounds are retained at different confidence thresholds, or when you must subset the compound list to a user-defined quality level before downstream cheminformatics analysis.

## When NOT to use

- Input data lacks a Match.Factor or equivalent quality/confidence column.
- Analysis goal is to retain ALL compounds regardless of quality score (no filtering needed).
- Compound identifications are already validated by orthogonal methods and do not require further quality-based subsetting.

## Inputs

- GC-MS data CSV file with columns: Compound.Name, Match.Factor (and optionally Component.RT, Base.Peak.MZ, Component.Area, File.Name)
- Threshold specification(s) (numeric values, e.g., 65, 80, 90)

## Outputs

- Filtered unique compound name vector(s) for each threshold
- Summary table (rows = threshold levels; columns = threshold value, unique compound count)
- CSV file containing the comparison table

## How to apply

Load the GC-MS CSV file (with required columns including 'Compound.Name' and 'Match.Factor') into R. Apply independent logical filters at each threshold level (e.g., Match.Factor >= 65, >= 80, >= 90), extracting the unique compound names that meet each condition. Count unique compounds retained under each threshold to quantify the trade-off between stringency and dataset size. The rationale is that higher Match.Factor thresholds reduce chemical identifications to high-confidence matches, but may exclude valid compounds; comparing counts across thresholds helps users choose an appropriate cutoff for their analysis goals. Construct a summary table documenting threshold value and compound count for each condition, and export as CSV for reporting.

## Related tools

- **R** (Primary language for loading CSV, applying logical filters, counting unique compounds, and constructing summary table)
- **uafR** (R package providing spreadOut() function to prepare raw GC-MS CSV for intelligent sorting and downstream filtering operations) — https://github.com/castratton/uafR
- **Agilent Unknowns Analysis** (Recommended software to generate the GC-MS data in the correct default format with required column names (Compound.Name, Match.Factor))

## Examples

```
query_chemicals_mf65 <- input_dat$Compound.Name[input_dat$Match.Factor >= 65]; query_chemicals_mf80 <- input_dat$Compound.Name[input_dat$Match.Factor >= 80]; query_chemicals_mf90 <- input_dat$Compound.Name[input_dat$Match.Factor >= 90]; summary_table <- data.frame(Threshold = c('>=65', '>=80', '>=90'), Compound_Count = c(length(unique(query_chemicals_mf65)), length(unique(query_chemicals_mf80)), length(unique(query_chemicals_mf90)))); write.csv(summary_table, 'threshold_comparison.csv', row.names = FALSE)
```

## Evaluation signals

- Verify that the output compound list contains only unique Compound.Name values (no duplicates).
- Check that compound counts are monotonically non-increasing as threshold increases (e.g., count at ≥90 ≤ count at ≥80 ≤ count at ≥65).
- Confirm that all compounds in the ≥90 subset also appear in the ≥80 and ≥65 subsets (proper nesting).
- Validate that the summary table has exactly 3 rows (one per threshold) and 2 columns (threshold value and compound count).
- Spot-check a sample of retained compounds to confirm their Match.Factor values meet or exceed the declared threshold.

## Limitations

- The skill assumes Match.Factor is the only quality metric; compounds with high Match.Factor may still represent false positives if other metrics (e.g., retention time, peak area) are anomalous.
- Optimal threshold values (65, 80, 90) are dataset- and application-dependent; no universal cutoff is recommended by the paper.
- The skill does not account for isotope patterns, fragmentation consistency, or database cross-validation, which may be necessary for rigorous compound identification.
- If the input CSV has missing or invalid Match.Factor values, they will be excluded silently; no imputation or handling is specified.

## Evidence

- [other] Match.Factor filtering can be applied to standard_data.csv at multiple threshold levels (≥65, ≥80, ≥90) to subset the compound list based on matching quality criteria.: "Match.Factor filtering can be applied to standard_data.csv at multiple threshold levels (≥65, ≥80, ≥90) to subset the compound list"
- [other] Load standard_data.csv into R and extract the Compound.Name and Match.Factor columns. Apply three independent filters: Match.Factor >= 65, Match.Factor >= 80, and Match.Factor >= 90, retaining unique compound names for each filter.: "Load standard_data.csv into R and extract the Compound.Name and Match.Factor columns. Apply three independent filters: Match.Factor >= 65, Match.Factor >= 80, and Match.Factor >= 90"
- [readme] The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"
- [readme] query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]: "query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]"
- [readme] spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses): "spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses)"
