---
name: tabular-data-parsing-and-structure-conversion
description: Use when you have a txt or tabular export file from a liquid chromatography–mass
  spectrometry (LC-MS) instrument (e.g., Sciex MultiQuant > v3.0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Sciex Multiquant (>v3.0.3)
  - QComics
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c03660
  title: QComics
evidence_spans:
- The goal of the `QComics` package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcomics_cq
    doi: 10.1021/acs.analchem.3c03660
    title: QComics
  dedup_kept_from: coll_qcomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c03660
  all_source_dois:
  - 10.1021/acs.analchem.3c03660
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tabular-data-parsing-and-structure-conversion

## Summary

Parse unstructured or semi-structured tabular export files (e.g., Sciex MultiQuant txt) into a standardized, machine-readable data frame with validated column names, data types, and metadata fields suitable for downstream analytical workflows. This skill is essential when integrating instrument-specific export formats into reproducible data pipelines.

## When to use

You have a txt or tabular export file from a liquid chromatography–mass spectrometry (LC-MS) instrument (e.g., Sciex MultiQuant > v3.0.3) containing QCpool sample identifiers, measurement values, timestamps, and metadata, and you need to ingest it into an R-based quality assessment workflow such as QComics. Apply this skill when the raw export format does not match your downstream tool's expected schema and requires column name standardization, data type coercion, and validation before use in quality overview analysis.

## When NOT to use

- Input data is already in a structured, validated format (e.g., an R data frame or pre-parsed CSV with correct column names and types) — proceed directly to quality assessment.
- The txt export is from a different instrument vendor or software version with a fundamentally incompatible tabular structure — consult vendor documentation or adapt the parser for that format.
- Your workflow does not require validation or standardization of data types and column names — a simple raw file read may suffice, but this sacrifices reproducibility and robustness.

## Inputs

- txt export file from Sciex MultiQuant (>v3.0.3) containing tabular QCpool sample data with columns for identifiers, measurement values, timestamps, and metadata

## Outputs

- R data frame or tibble with standardized column names and validated data types (numeric measurements, POSIXct timestamps, character identifiers)
- CSV file or R serialized object (.rds) containing the parsed and structured table

## How to apply

Load the txt file exported from the instrument using base R file I/O or tidyverse functions (e.g., `readr::read_delim()` or `read.table()`), then inspect the tabular structure to identify and extract columns containing QCpool sample identifiers, measurement values, timestamps, and metadata fields. Validate that required columns are present and coerce data types to the correct format (numeric for measurements, POSIXct for timestamps). Rename columns to match the standardized schema expected by downstream QComics functions using consistent naming conventions. Finally, serialize the parsed data frame as a CSV or R object (`.rds`) for reproducible input to the quality assessment pipeline. Success is confirmed when all required columns are present with correct types and no parsing errors or missing critical values are detected.

## Related tools

- **Sciex Multiquant (>v3.0.3)** (Upstream instrument software that generates the txt export file containing pooled QCpool sample measurements, timestamps, and metadata to be parsed)
- **R** (Programming language and environment used to load, parse, validate, and convert the txt export into a structured data frame for downstream QComics quality assessment)
- **QComics** (Downstream R package that accepts the parsed and structured data frame to provide a quick overview of the quality of a metabolomics or lipidomics study) — https://github.com/ricoderks/QComics

## Examples

```
# Load and parse Sciex MultiQuant txt export, validate columns and types, output structured R data frame for QComics
qcpool_df <- readr::read_delim('qcpool_export.txt', delim='\t') %>% dplyr::rename(sample_id = SampleID, value = MassFragmentIntensity, timestamp = InjectionTime) %>% dplyr::mutate(value = as.numeric(value), timestamp = as.POSIXct(timestamp))
readr::write_csv(qcpool_df, 'qcpool_parsed.csv')
```

## Evaluation signals

- All required columns (QCpool sample identifiers, measurement values, timestamps, metadata) are present in the output data frame and match the standardized schema.
- Data types are correct: numeric columns for measurements, POSIXct or Date for timestamps, and character for identifiers and metadata strings.
- No parsing errors, warnings, or NA values introduced unexpectedly; row count matches the input txt file (accounting for header row).
- The serialized output (CSV or .rds) can be successfully re-imported and used as input to QComics functions without schema or type errors.
- Column names are consistent with QComics documentation or downstream tool expectations; no missing or duplicate columns.

## Limitations

- Parser is specific to Sciex MultiQuant (>v3.0.3) txt format; outputs from older versions or different vendors will require format-specific adapter code.
- Validation assumes standard column presence and structure; malformed or incomplete txt files (e.g., missing headers, inconsistent delimiters, corrupted rows) may cause parsing to fail or produce invalid output.
- No changelog is available for the QComics package, limiting visibility into breaking changes to the expected data frame schema across versions.

## Evidence

- [intro] Required column and format validation: "Validate that required columns are present and data types are correct (numeric values, date/time format)."
- [intro] Standardization and structured output: "Convert parsed data into a structured R data frame or tibble with standardized column names and formats. Output the structured table in a machine-readable format (CSV or R serialized object)"
- [intro] Instrument and software specification: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [intro] Downstream use case: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
