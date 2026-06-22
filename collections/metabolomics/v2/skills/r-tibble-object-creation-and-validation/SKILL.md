---
name: r-tibble-object-creation-and-validation
description: Use when when you have raw metabolomics results from multiple studies in heterogeneous file formats (xls/xlsx, csv, or txt) and need to harmonize them into a single, machine-readable tibble structure with required columns (compound identifier, p-value, fold-change, study size N, reference) for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - R
  - amanida
  - webchem
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions for computing a weighted meta-analysis
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

# R tibble object creation and validation

## Summary

Convert raw metabolomics datasets from multiple file formats (xls/xlsx/csv/txt) into a validated R tibble structure suitable for downstream quantitative meta-analysis, including standardized column mapping, missing data handling, and fold-change transformation.

## When to use

When you have raw metabolomics results from multiple studies in heterogeneous file formats (xls/xlsx, csv, or txt) and need to harmonize them into a single, machine-readable tibble structure with required columns (compound identifier, p-value, fold-change, study size N, reference) for quantitative meta-analysis combining significance and effect size across studies.

## When NOT to use

- Input data already contains standard deviations or variance measures — use standard meta-analysis tools instead of amanida's adapted approach
- You are performing qualitative (vote-counting) meta-analysis only — use mode='qual' and omit fold-change/p-value columns
- Your dataset requires preservation of negative fold-change directionality as original values — the reciprocal transformation is irreversible

## Inputs

- Raw metabolomics dataset file (xls/xlsx/csv/txt format)
- Column name mapping vector specifying: identifier, p-value, fold-change, N, reference
- File separator specification (for csv/txt; e.g. ';' or ',')

## Outputs

- R tibble with harmonized structure suitable for quantitative meta-analysis
- Validated tibble with columns: compound identifier (character), p-value (numeric), fold-change (numeric, all positive), N/study size (integer), reference (character)

## How to apply

Use the `amanida_read()` function with mode='quan' to import your dataset, specifying the column name mapping via the `coln` parameter in the required order: identifier, p-value, fold-change, N (study size), and reference. The function automatically ignores missing data during import. After import, validate that negative fold-change values have been transformed to positive using the reciprocal formula (1/value) to ensure all fold-changes are comparable as upregulation ratios. Inspect the resulting tibble's structure and data types (numeric columns for p-values and fold-changes, integer for N, character for identifiers and references) to confirm it meets requirements for downstream meta-analysis functions. The tibble must have no rows with missing values in critical quantitative columns and fold-change values should all be ≥1 after transformation.

## Related tools

- **amanida** (Provides the amanida_read() function for importing and parsing metabolomics datasets into tibbles with automatic missing data handling and fold-change transformation) — https://github.com/mariallr/amanida
- **R** (Host language for tibble objects and amanida package)
- **webchem** (Optional downstream tool for harmonizing compound identifiers via PubChem lookup using check_names() after tibble creation)

## Examples

```
coln = c("Compound Name", "P-value", "Fold-change", "N total", "References")
input_file <- "colorectal_urine.csv"
datafile <- amanida_read(input_file, mode = "quan", coln, separator=";")
```

## Evaluation signals

- Resulting object is a valid R tibble with expected number of rows (one per study result) and exactly 5 columns in correct order
- All p-value entries are numeric in range [0, 1] with no NAs
- All fold-change entries are numeric ≥ 1 with no NAs (confirming negative values were transformed via 1/value)
- Study size (N) column contains positive integers with no NAs
- Compound identifier and reference columns are character vectors with no NAs
- No rows present with any missing values in the five core columns

## Limitations

- The function ignores missing data entirely during import — rows or cells with missing critical values are silently dropped, potentially reducing sample size without explicit warning
- Negative fold-change values are irreversibly transformed to positive reciprocals, preventing later recovery of original directionality or asymmetric analysis
- The function does not validate biological plausibility of fold-change values; extremely large fold-changes (e.g. >1000) are accepted without flagging
- No built-in quality control for duplicate compound identifiers or inconsistent formatting across studies — must be handled separately via check_names()
- Tibble creation requires exact column name matching in the coln parameter; typos or reordering will cause function failure

## Evidence

- [other] amanida_read function accepts metabolomics datasets in xls/xlsx, csv, or txt formats with required columns for compound identifier, p-value, fold-change, study size (N), and reference: "Dataset to analyse must include the following columns: identifier, p-value, fold-change, study size (N) and reference"
- [other] Missing data is handled by ignoring missing values; negative fold-change values are transformed to positive using reciprocal formula: "missing data is ignored... negative values of fold-change are transformed to positive (1/value)"
- [readme] amanida_read function with mode='quan' and coln parameter maps input columns; produces tibble data structure: "For quantitative meta-analysis include the following parameters: Indicate mode = "quan", coln: vector containing the column names, which need to be in this order: Id: compound name or unique"
- [other] Tibble structure is validated for downstream meta-analysis consumption: "Validate the resulting tibble structure and data types for consumption by downstream meta-analysis functions"
- [readme] Example R invocation showing amanida_read() with mode, column names, and separator parameters: "coln = c("Compound Name", "P-value", "Fold-change", "N total", "References")
input_file <- system.file("extdata", "dataset2.csv", package = "amanida")
datafile <- amanida_read(input_file, mode ="
