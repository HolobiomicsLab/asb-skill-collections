---
name: polarity-mode-filtering-lcms
description: Use when you have a comprehensive target list (containing compounds from both positive and negative ionization modes) but need to screen or detect peaks in a single LC-MS run acquired in a specific polarity mode.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - xcms
  - R
  - TARDIS
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- It makes use of an established retention time correction algorithm from the `xcms` package
- R package for *TArgeted Raw Data Integration In Spectrometry*
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis
schema_version: 0.2.0
---

# Polarity-mode filtering for LC-MS target lists

## Summary

This skill filters a target compound list by ionization polarity (positive or negative mode) to produce a subset of compounds matched to a specific MS acquisition mode. It is essential for targeted LC-MS workflows where different ionization modes are acquired separately and each analytical run requires only the compounds ionizable in that mode.

## When to use

Apply this skill when you have a comprehensive target list (containing compounds from both positive and negative ionization modes) but need to screen or detect peaks in a single LC-MS run acquired in a specific polarity mode. Trigger: the input target file spans multiple polarity modes, but the MS data file was acquired in only one mode (e.g., positive ionization only).

## When NOT to use

- The target list already contains compounds from only one polarity mode (filtering is redundant).
- MS data were acquired in both positive and negative modes simultaneously (e.g., switched-polarity or high-frequency polarity switching), requiring no upfront subsetting.
- The target file lacks a polarity indicator column or the polarity information is ambiguous.

## Inputs

- Target list file (xlsx or csv format) with columns: compound ID, compound name, m/z (theoretical or measured), expected RT (minutes), polarity indicator
- Polarity specification parameter (string: 'positive' or 'negative')
- Column name(s) indicating ionization mode in the target file

## Outputs

- Filtered target data.frame containing only compounds matching the specified polarity
- Standardized data.frame structure with columns: compound ID, compound name, m/z, RT, polarity

## How to apply

Read the target list file (xlsx or csv format) containing compound metadata including a polarity indicator column. Validate presence of required columns: compound ID, compound name, theoretical or measured m/z, expected RT in minutes, and the polarity field. Subset the data.frame to retain only rows matching the specified polarity (e.g., 'positive' or 'negative'). Reorder and select columns to match the standardized target data.frame structure expected by downstream peak detection (compound ID, name, m/z, RT, and polarity columns). The rationale is that applying only relevant targets reduces false positives and computational cost in peak detection by eliminating compounds that cannot be ionized in the current mode.

## Related tools

- **TARDIS** (R package that performs polarity filtering internally within createTargetList() and subsequent peak detection; input target file is passed to TARDIS with polarity parameter specified) — https://github.com/pablovgd/TARDIS
- **xcms** (Underlying retention time correction and peak detection framework used by TARDIS for targeted screening after polarity filtering is applied)
- **R** (Programming language and environment for implementing polarity filtering, data.frame subsetting, and column selection operations) — https://cloud.r-project.org/index.html

## Examples

```
library(TARDIS); targets <- createTargetList(input_file = 'compounds.xlsx', polarity_pos = 'positive', polarity_neg = 'negative', mode = 'positive', polarity_col = 'polarity', cols_of_interest = c('compound_id', 'name', 'mz', 'rt'))
```

## Evaluation signals

- Output data.frame row count equals the number of input targets matching the specified polarity (count verification).
- All rows in the filtered data.frame have the same polarity value as the filter parameter (polarity consistency check).
- Required columns (compound ID, name, m/z, RT, polarity) are present and in the correct order in the output data.frame (schema validation).
- No missing values (NA) in critical columns: m/z, RT, and polarity (completeness check).
- Downstream peak detection in tardisPeaks() runs without errors on the filtered target list and produces results for all retained targets (functional validation).

## Limitations

- Polarity filtering is only effective if the polarity indicator column is correctly populated in the input target file; ambiguous or missing polarity values will cause targets to be dropped or retained incorrectly.
- The filtering step assumes each target ionizes in only one polarity mode; compounds ionizable in both modes will be excluded when filtering for the non-primary mode.
- If the input file contains typos or inconsistent polarity labels (e.g., 'positive' vs. 'pos' vs. '+'), string matching will fail and targets will be misclassified.
- The skill filters based on the polarity column alone; it does not validate whether the m/z or RT values are appropriate for the chosen mode.

## Evidence

- [other] The createTargetList() function accepts an input file path, positive/negative ionization patterns, a polarity selection parameter, the column name indicating ionization mode, and columns of interest; it then produces a correctly structured target data.frame by applying these filters and selections.: "accepts an input file path, positive/negative ionization patterns, a polarity selection parameter, the column name indicating ionization mode"
- [other] Read targets file (xlsx or csv format) containing compound metadata. Validate presence of required columns: compound ID, compound name, theoretical or measured m/z, expected RT in minutes, and polarity indicator.: "Read targets file (xlsx or csv format) containing compound metadata. Validate presence of required columns: compound ID, compound name, theoretical or measured m/z, expected RT in minutes, and"
- [other] Apply polarity filtering to subset targets by ionization mode. Select and reorder columns to match the standardized target data.frame structure.: "Apply polarity filtering to subset targets by ionization mode. Select and reorder columns to match the standardized target data.frame structure"
- [intro] Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] perform a screening step to check if our targets are visible within our *m/z* and RT windows: "perform a screening step to check if our targets are visible within our m/z and RT windows"
