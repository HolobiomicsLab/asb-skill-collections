---
name: feature-table-standardization
description: Use when you have feature tables from external metabolomics software (MS-DIAL, XCMS, vendor tools) in CSV format and need to integrate them into JPA for cross-sample alignment and metabolite annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - JPA
  - R
  - MS-DIAL
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12030212
  all_source_dois:
  - 10.3390/metabo12030212
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-standardization

## Summary

Standardize individual sample feature tables into a uniform format compatible with JPA's alignment and downstream annotation modules. This skill converts heterogeneous feature table formats (e.g., MS-DIAL CSV output) into JPA's required column structure and units to enable multi-sample integration.

## When to use

You have feature tables from external metabolomics software (MS-DIAL, XCMS, vendor tools) in CSV format and need to integrate them into JPA for cross-sample alignment and metabolite annotation. Trigger: input feature tables lack standardized column ordering, retention time units are in minutes rather than seconds, or the schema does not match JPA's expected mz–rt–rtmin–rtmax–intensity format.

## When NOT to use

- Input is already a feature table in JPA's native format or has already been aligned across samples.
- Input data are raw LC-MS files (mzXML, mzML, etc.); use XCMS.featureTable() or MS1 peak picking directly instead.
- Feature tables are from full-scan or DIA (data-independent acquisition) experiments; these require different feature extraction workflows.

## Inputs

- Per-sample feature table in CSV format from external metabolomics software (e.g., MS-DIAL, XCMS output)
- Conversion mapping or helper script (e.g., convertCSV.R) tailored to source software

## Outputs

- Standardized per-sample feature table with columns: mz, rt, rtmin, rtmax, intensity (retention times in seconds)
- Unified directory containing all converted CSV files ready for JPA alignment

## How to apply

Convert each single-sample CSV feature table to a standardized format with five mandatory columns in order: m/z, retention time (seconds), min retention time (seconds), max retention time (seconds), and intensity. JPA provides a helper script (convertCSV.R) to transform MS-DIAL output; adapt this code for other vendor formats by remapping source columns and ensuring all retention time values are converted to seconds. Place all converted CSV files in a single directory with no other irrelevant CSV files. Verify the schema by checking the first few rows against the expected column order and data types before passing to JPA's custom.featureTable() function.

## Related tools

- **JPA** (Receives standardized feature tables via custom.featureTable() function to perform downstream alignment and annotation) — https://github.com/HuanLab/JPA.git
- **R** (Environment for running conversion scripts (convertCSV.R) and JPA functions)
- **MS-DIAL** (Common source software producing feature tables that require conversion via convertCSV.R)

## Examples

```
# In R, after preparing the converted CSV files in FTdir:
featureTable <- custom.featureTable(dir = "X:/Users/JPAtest_20210330/multiDDA", FTdir = "X:/Users/JPAtest_20210330/multiDDA")
```

## Evaluation signals

- Output CSV files have exactly 5 columns in the order: mz, rt, rtmin, rtmax, intensity (or equivalent after renaming).
- All retention time values (columns 2, 3, 4) are in seconds (typically > 100 for LC timescales); no mixed units.
- No NaN, null, or missing values in mandatory columns; all rows have valid numeric data.
- custom.featureTable() successfully reads the converted files and outputs a dataframe with columns: mz, rt, rtmin, rtmax, maxo, sample, level without errors or schema mismatches.
- Spot-check: first 3–5 rows match expected ranges (e.g., mz typically 50–2000, rt in seconds 500–5000 for typical LC-MS runs).

## Limitations

- Conversion is format-specific; each source software (MS-DIAL, XCMS, vendor tools) may require custom mapping logic. JPA provides convertCSV.R for MS-DIAL as a template but users must adapt for other formats.
- Retention time unit ambiguity is common; incorrect conversion (e.g., leaving RT in minutes) will cause downstream alignment failures or spurious clustering. Always verify units before and after conversion.
- Feature tables from full-scan or DIA experiments should not be standardized and passed to alignment without prior filtering; JPA's alignment workflow is optimized for DDA (data-dependent acquisition) with targeted feature extraction methods.

## Evidence

- [readme] The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity. Note: column 3 and column 4 are the retention time of the feature edges, and all three columns containing retention time information should be in seconds.: "The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity. Note: column 3 and column 4 are the retention time of the"
- [readme] An R code (convertCSV.R) is provided to help user transform the csv from MS-DIAL output to the format recognizable by 'JPA'. For other types of input, user can easily tune the code to adapt to converting different formats of csv files.: "An R code (convertCSV.R) is provided to help user transform the csv from MS-DIAL output to the format recognizable by 'JPA'. For other types of input, user can easily tune the code to adapt to"
- [readme] For multi-sample analysis, a CSV feature table for each single mzXML file needs to be provided. Aligned feature table is not acceptable. All CSV file(s) of interest need to be placed in the same folder containing no other irrelevant CSV files.: "For multi-sample analysis, a CSV feature table for each single mzXML file needs to be provided. Aligned feature table is not acceptable. All CSV file(s) of interest need to be placed in the same"
- [other] Load extracted feature tables from individual samples (output from MS1 peak picking, MS2 recognition, or targeted list extraction): "Load extracted feature tables from individual samples (output from MS1 peak picking, MS2 recognition, or targeted list extraction)"
