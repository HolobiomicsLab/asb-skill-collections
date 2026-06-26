---
name: missing-data-handling-in-metabolite-datasets
description: Use when when importing metabolomics datasets with multiple studies into
  amanida_read for quantitative or qualitative meta-analysis, and some studies report
  missing values for p-values, fold-changes, sample sizes, or other effect size metrics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - amanida
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted
  meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions
  for computing a weighted meta-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# missing-data-handling-in-metabolite-datasets

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A strategy for handling missing values in metabolomics datasets during import and meta-analysis preparation. Missing data is ignored during the amanida_read import step, allowing incomplete compound records to be retained without imputation, which is appropriate when metabolomics studies report sparse or incomplete effect size information across multiple studies.

## When to use

When importing metabolomics datasets with multiple studies into amanida_read for quantitative or qualitative meta-analysis, and some studies report missing values for p-values, fold-changes, sample sizes, or other effect size metrics. This is common in metabolomics meta-analyses because studies vary in what statistics they report and whether they disclose all required parameters.

## When NOT to use

- If your dataset requires imputation (e.g., expectation-maximization, k-nearest neighbor) rather than listwise deletion — amanida_read does not support imputation methods.
- If missing data occurs in the compound identifier column, as compounds cannot be matched or aggregated without a unique ID.
- If the majority of studies have missing effect size metrics (e.g., >50% of rows missing p-values or fold-changes), indicating that the dataset may be too sparse for reliable meta-analysis.

## Inputs

- CSV, TSV, XLS, or XLSX file with columns for compound identifier, p-value, fold-change, study sample size (N), and bibliographic reference
- Column name mapping vector (coln) specifying the order and names of required columns
- Separator character (e.g., ';' or '\t') if not auto-detected

## Outputs

- R tibble with compound identifiers, p-values, fold-changes, study sizes, and references; rows with complete data retained, rows with any missing values in required columns silently excluded
- Data types validated for downstream meta-analysis (numeric for p-values and fold-changes, integer for N, character for identifier and reference)

## How to apply

During the amanida_read import step with mode='quan' or mode='qual', the function automatically ignores missing data without requiring explicit imputation parameters. Specify the column mapping via the coln parameter for the columns present in your dataset (identifier, p-value, fold-change, N, reference for quantitative analysis; identifier, trend, reference for qualitative analysis). Missing values in any of these columns are silently skipped, and rows with any missing required field are handled gracefully by the downstream compute_amanida or amanida_vote functions, which operate on complete pairs. This approach is justified because metabolomics meta-analysis weights studies by their sample size and statistical significance, so incomplete reporting in one study does not invalidate analysis of studies with complete data.

## Related tools

- **amanida** (Performs missing data handling during import via amanida_read function; also computes weighted meta-analysis on complete-case data) — https://github.com/mariallr/amanida
- **R** (Language and runtime environment for executing amanida and data manipulation functions)

## Examples

```
coln = c("Compound Name", "P-value", "Fold-change", "N total", "References")
input_file <- system.file("extdata", "dataset2.csv", package = "amanida")
datafile <- amanida_read(input_file, mode = "quan", coln, separator=";")
```

## Evaluation signals

- Check that the output tibble has fewer rows than the input file if any rows contained missing values in required columns; use nrow() to compare.
- Verify that all remaining rows have non-NA values in the required columns (identifier, p-value, fold-change, N, reference for quantitative analysis) using complete.cases() or is.na() checks.
- Confirm that numeric columns (p-value, fold-change, N) are stored as numeric or integer types, not character, using str() or class().
- Run compute_amanida on the resulting tibble without errors; if errors occur, investigate whether required columns are present and correctly named.
- Compare the number of compounds in the meta-analysis output with the number of unique identifiers in the cleaned tibble; they should match if no further filtering was applied.

## Limitations

- amanida_read silently removes rows with missing data without logging which rows or columns were affected; users cannot easily audit the exclusion.
- No support for multiple imputation or sensitivity analysis to assess impact of missing data mechanism (MCAR vs. MAR vs. MNAR).
- If missing data is not missing completely at random (MCAR), the resulting meta-analysis estimates may be biased, but amanida does not warn or test for this.
- Missing data handling is hard-coded in amanida_read; users cannot select alternative strategies (e.g., pairwise deletion or indicator variables).

## Evidence

- [intro] missing data is ignored: "During import, missing data is ignored and negative fold-change values are transformed to positive using the reciprocal formula (1/value)"
- [intro] Missing data ignored during workflow: "Apply missing data handling by ignoring missing values during import."
- [readme] amanida_read function processes required columns: "The amanida_read function accepts metabolomics datasets in xls/xlsx, csv, or txt formats with required columns for compound identifier, p-value, fold-change, study size (N), and reference."
- [readme] Column specification for quantitative meta-analysis: "coln: vector containing the column names, which need to be in this order: Id: compound name or unique identification, P-value, Fold-change, N: number of individuals in the study, Reference:"
