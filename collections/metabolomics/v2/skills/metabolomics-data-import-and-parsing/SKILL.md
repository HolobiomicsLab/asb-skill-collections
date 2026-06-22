---
name: metabolomics-data-import-and-parsing
description: Use when when you have metabolomics comparison results from one or more studies in tabular format (spreadsheet or text file) with columns for compound name/identifier, statistical p-value, relative fold-change (including negative values indicating down-regulation), study sample size (N), and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0625
  tools:
  - R
  - amanida
  - webchem
  - metaboprep
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
- doi: 10.1093/bioinformatics/btac059/6522114
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions for computing a weighted meta-analysis
- library(metaboprep)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  - build: coll_metaboprep_cq
    doi: 10.1093/bioinformatics/btac059/6522114
    title: Metaboprep
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  - 10.1093/bioinformatics/btac059/6522114
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-import-and-parsing

## Summary

Import metabolomics datasets from standard file formats (xls/xlsx, csv, txt) into a structured tibble suitable for meta-analysis, handling column mapping, missing data, and fold-change sign normalization. This is the critical first step that prepares raw study results (compound identifiers, p-values, fold-changes, sample sizes, references) for downstream quantitative or qualitative meta-analysis workflows.

## When to use

When you have metabolomics comparison results from one or more studies in tabular format (spreadsheet or text file) with columns for compound name/identifier, statistical p-value, relative fold-change (including negative values indicating down-regulation), study sample size (N), and bibliographic reference, and you need to ingest them into R for meta-analysis. Typically triggered when aggregating results across multiple independent metabolomics studies to derive global effect sizes and significance.

## When NOT to use

- Input file is already a properly formatted and normalized tibble or data frame in R memory — skip directly to compute_amanida or check_names.
- Data lacks required columns (e.g., only p-values and identifiers, no fold-change or study N) — quantitative meta-analysis cannot proceed without fold-change and sample size for weighting.
- Study results are reported as raw individual-level data (individual measurements per participant) rather than summary statistics — use alternative preprocessing to compute p-values and fold-changes first.

## Inputs

- File path to metabolomics results (xls, xlsx, csv, or txt format)
- Column name vector in order: [identifier, p-value, fold-change, N, reference]
- File separator character (';' or ',')
- Analysis mode flag ('quan' or 'qual')

## Outputs

- R tibble with columns: compound identifier, p-value, fold-change (positive normalized), study N, reference
- Missing data removed; negative fold-changes converted to positive reciprocals

## How to apply

Use the amanida_read function to load your dataset, specifying the file path, the analysis mode (mode='quan' for quantitative meta-analysis with p-values and fold-changes, or mode='qual' for vote-counting with trend labels), a named column vector (coln) mapping input column names to the required order [identifier, p-value/trend, fold-change/reference, study N, reference], and the field separator (separator=';' or ',') appropriate to your file format. During parsing, the function automatically ignores missing data entries. Crucially, any negative fold-change values are transformed to positive via the reciprocal formula (1/value) to normalize direction, since metabolomics typically reports relative change rather than absolute differences and down-regulated metabolites should be represented as fractional fold-changes (e.g., -2 becomes 0.5). The output is a tibble data structure with normalized columns ready for compute_amanida or check_names functions.

## Related tools

- **amanida** (Performs the import via amanida_read function; subsequent meta-analysis via compute_amanida) — https://github.com/mariallr/amanida
- **webchem** (Used by check_names (post-import) to harmonize compound identifiers against PubChem)
- **R** (Runtime environment for amanida package and tibble data structures)

## Examples

```
coln = c("Compound Name", "P-value", "Fold-change", "N total", "References")
input_file <- system.file("extdata", "dataset2.csv", package = "amanida")
datafile <- amanida_read(input_file, mode = "quan", coln, separator=";")
```

## Evaluation signals

- Output tibble has exactly 5 columns with correct names and data types (character for identifier/reference, numeric for p-value/fold-change/N).
- No missing values remain in critical columns (identifier, p-value, fold-change, N); rows with missing entries are removed.
- All fold-change values are positive; verify by checking min(datafile$fold_change) > 0 and inspect original negative entries to confirm reciprocal transformation (1/original_value) was applied.
- Row count equals or is less than input file rows (some rows removed if incomplete); no rows duplicated.
- Tibble is compatible with downstream amanida functions: compute_amanida(datafile) and check_names(datafile) execute without schema errors.

## Limitations

- Function ignores (silently removes) rows with missing data in any required column; if >10% of rows are incomplete, investigate data quality upstream.
- Negative fold-change transformation assumes the reciprocal model (1/value) is biologically appropriate for your metabolomics context; if fold-changes are on a different scale, verify the formula aligns with study design.
- File format support limited to xls/xlsx/csv/txt; binary or proprietary metabolomics formats (e.g., .raw, .d) must be pre-converted to tabular format.
- Column mapping is positional and rigid: coln must be in exact order [identifier, p-value, fold-change, N, reference]; order errors silently produce incorrect assignments. Validate coln order before running.
- No built-in validation of p-value range (0–1) or fold-change range (>0 post-transformation); implausible values (e.g., p > 1) are accepted; use downstream checks (e.g., summary statistics) to detect import errors.

## Evidence

- [intro] Import data from supported formats (xls/xlsx, csv or txt) using amanida_read function with columns: identifier, p-value, fold-change, study size (N) and reference: "Dataset to analyse must include the following columns: identifier, p-value, fold-change, study size (N) and reference"
- [intro] Missing data handling during import; negative fold-change transformation: "missing data is ignored; negative values of fold-change are transformed to positive (1/value)"
- [readme] amanida_read function accepts mode and coln parameters for quantitative analysis: "For quantitative meta-analysis include the following parameters: Indicate mode = "quan"; coln: vector containing the column names, which need to be in this order: Id, P-value, Fold-change, N,"
- [intro] Output is a tibble data structure for downstream meta-analysis: "producing a tibble data structure for downstream meta-analysis"
- [readme] Supported file formats for amanida_read: "Supported files are csv, xls/xlsx and txt."
