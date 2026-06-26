---
name: quantitative-mode-metabolomics-configuration
description: Use when when you have metabolomics results from multiple studies reporting
  compound identifiers, p-values, fold-changes, and study sizes (N), and you need
  to prepare them for quantitative meta-analysis using weighted Fisher's method and
  logarithmic fold-change combination.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3957
  tools:
  - R
  - amanida
  - webchem
  techniques:
  - mass-spectrometry
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

# quantitative-mode-metabolomics-configuration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure and validate the input data structure for quantitative metabolomics meta-analysis by specifying column mappings, selecting mode='quan', and handling missing and negative fold-change values. This skill ensures metabolomics datasets from heterogeneous sources (xls/xlsx/csv/txt) conform to the required tibble schema before statistical combination.

## When to use

When you have metabolomics results from multiple studies reporting compound identifiers, p-values, fold-changes, and study sizes (N), and you need to prepare them for quantitative meta-analysis using weighted Fisher's method and logarithmic fold-change combination. This skill is required before computing global significance and effect size estimates across studies.

## When NOT to use

- Input dataset already contains error/variance or standard deviation columns—use standard meta-analysis tools (e.g., metafor) instead, as amanida is specifically designed for metabolomics studies lacking variance data.
- You only have compound identifiers and trend labels (up/down regulation) without p-values and fold-changes—use qualitative vote-counting mode (mode='qual') instead.
- Raw individual-level data is available—aggregate it to study-level summary statistics (p-value, fold-change, N) before using this skill.

## Inputs

- metabolomics results file (xls, xlsx, csv, or txt format)
- column name mapping vector specifying: compound identifier, p-value, fold-change, N, reference
- file separator specification (e.g., semicolon, comma, tab)

## Outputs

- tibble data structure with columns: compound identifier, p-value, fold-change (positive values), N, reference
- S4 object suitable for input to compute_amanida() quantitative meta-analysis function

## How to apply

Call amanida_read() with mode='quan' and specify the coln parameter as a vector listing column names in this exact order: [compound identifier, p-value, fold-change, N (study size), reference]. The function will parse the input file (xls/xlsx/csv/txt format), map columns accordingly, ignore any rows with missing data, and transform negative fold-change values to positive using the reciprocal formula (1/value). Validate the output tibble structure and data types before passing to compute_amanida() for meta-analysis. This transformation is necessary because metabolomics reports relative change via fold-change (not difference of means), and negative fold-changes represent down-regulation but must be expressed as positive reciprocals to maintain directionality in the weighted combination step.

## Related tools

- **amanida** (R package implementing amanida_read() function for quantitative metabolomics data import and configuration; handles column mapping, missing data, and fold-change reciprocal transformation) — https://github.com/mariallr/amanida
- **webchem** (optional tool for downstream compound ID harmonization via PubChem lookup (used in check_names() after amanida_read()))
- **R** (execution environment for amanida package and tibble data structure operations)

## Examples

```
coln = c("Compound Name", "P-value", "Fold-change", "N total", "References"); datafile <- amanida_read("colorectal_cancer_urine.csv", mode = "quan", coln, separator=";")
```

## Evaluation signals

- Output tibble has exactly 5 columns with correct names and data types: character (identifier, reference), numeric (p-value, fold-change, N)
- All fold-change values are positive; any original negative values have been transformed via 1/value reciprocal
- No rows with missing data appear in output (NA handling verified by row count comparison with input)
- P-value range is [0, 1] and N values are positive integers ≥ 1
- Output tibble is compatible with compute_amanida() function signature without errors or type coercion warnings

## Limitations

- Missing data is silently ignored (rows dropped); no reporting of how many records were excluded due to incompleteness
- Negative fold-change transformation via 1/value assumes bidirectional symmetry around 1.0; extreme values (e.g., FC < 0.01) may produce very large reciprocals
- Column order in coln parameter is strict and position-dependent; misspecification silently maps wrong columns and corrupts analysis
- Only supports xls/xlsx/csv/txt formats; does not read JSON, XML, or proprietary mass spectrometry data formats
- Does not validate biological plausibility of fold-change or p-value ranges before meta-analysis (garbage-in, garbage-out)

## Evidence

- [intro] Dataset to analyse must include the following columns: identifier, p-value, fold-change, study size (N) and reference: "Dataset to analyse must include the following columns: identifier, p-value, fold-change, study size (N) and reference"
- [readme] Supported files are csv, xls/xlsx and txt. For quantitative meta-analysis include the following parameters: Indicate mode = "quan": "Supported files are csv, xls/xlsx and txt. For quantitative meta-analysis include the following parameters: Indicate mode = "quan""
- [readme] coln: vector containing the column names, which need to be in this order: Id: compound name or unique identification, P-value, Fold-change, N: number of individuals in the study, Reference: "coln: vector containing the column names, which need to be in this order: Id: compound name, P-value, Fold-change, N: number of individuals, Reference"
- [other] During import, missing data is ignored and negative fold-change values are transformed to positive using the reciprocal formula (1/value): "missing data is ignored and negative fold-change values are transformed to positive using the reciprocal formula (1/value)"
- [intro] negative values of fold-change are transformed to positive (1/value): "negative values of fold-change are transformed to positive (1/value)"
- [readme] only using p-value and fold-change, global significance and effect size for compounds or metabolites are obtained: "only using p-value and fold-change, global significance and effect size for compounds are obtained"
- [readme] coln = c("Compound Name", "P-value", "Fold-change", "N total", "References"); datafile <- amanida_read(input_file, mode = "quan", coln, separator=";"): "coln = c("Compound Name", "P-value", "Fold-change", "N total", "References"); amanida_read(input_file, mode = "quan", coln, separator=";")"
