---
name: ms-peak-table-format-validation
description: Use when immediately after loading a raw GC-MS CSV file and before executing the spreadOut() function. Use it when you have received peak table data from an instrument vendor (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0199
  tools:
  - R
  - Agilent Unknowns Analysis
  - ChemmineR
  - fmcsR
  - webchem
  - uafR spreadOut()
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with simple modifications
- any software or utility that generates the necessary information can be used with simple modifications (e.g. changing the column names)
- The recommended software for generating the necessary data in the default format (i.e. with correct column names) is Unknowns Analysis
- uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_uafr
    doi: 10.1371/journal.pone.0306202
    title: uafr
  dedup_kept_from: coll_uafr
schema_version: 0.2.0
---

# MS Peak Table Format Validation

## Summary

Validates that a raw GC-MS peak table (typically CSV output from Agilent Unknowns Analysis) conforms to the required schema before downstream processing. This skill ensures input data integrity by confirming the presence and correctness of critical columns and data types needed for intelligent sorting and chemical identification.

## When to use

Apply this skill immediately after loading a raw GC-MS CSV file and before executing the spreadOut() function. Use it when you have received peak table data from an instrument vendor (e.g., Agilent Unknowns Analysis) and need to confirm that column names, data types, and row counts match expectations for the uafR pipeline.

## When NOT to use

- Input is already a processed list object (e.g., output from spreadOut()) — no re-validation needed
- Data has already been validated by upstream quality-control software; skip to spreadOut() directly
- CSV file is from a non-standard GC-MS instrument with different column names — requires custom schema mapping first

## Inputs

- Raw GC-MS peak table CSV file from Agilent Unknowns Analysis (or compatible export)
- Expected schema specification: column names and data types

## Outputs

- Boolean validation result (pass/fail)
- Data frame with validated schema if validation succeeds
- Error report listing missing columns, type mismatches, or null value counts if validation fails

## How to apply

Load the CSV file into R and verify the presence of exactly six required columns: 'Component.RT', 'Base.Peak.MZ', 'Component.Area', 'Compound.Name', 'Match.Factor', and 'File.Name' in any order. Check that Component.RT and Base.Peak.MZ contain numeric values representing retention times (in minutes) and mass-to-charge ratios, Component.Area contains non-negative numeric peak intensities, Match.Factor contains values between 0 and 100 (representing spectral library match quality), and Compound.Name and File.Name contain non-empty character strings. Confirm that the total row count is consistent with the number of detected peaks expected from your sample set. If any required column is missing or contains unexpected data types or null values, reject the file and request re-export from the instrument software with correct configuration.

## Related tools

- **R** (Programming environment for schema validation logic and data frame inspection)
- **Agilent Unknowns Analysis** (Source software that generates raw peak table CSV; validation confirms its output matches expected schema)
- **uafR spreadOut()** (Downstream function that accepts validated peak table as input; validation is prerequisite) — https://github.com/castratton/uafR

## Examples

```
input_dat = read.csv('gcms_dataset.csv'); stopifnot(all(c('Component.RT', 'Base.Peak.MZ', 'Component.Area', 'Compound.Name', 'Match.Factor', 'File.Name') %in% names(input_dat)))
```

## Evaluation signals

- All six required columns (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) are present with correct casing
- Component.RT and Base.Peak.MZ are numeric; Component.Area is numeric and non-negative; Match.Factor is numeric in range [0, 100]
- No null/NA values in any required column for rows with non-zero Component.Area
- Compound.Name and File.Name contain non-empty character strings for all rows
- Row count and column count match expected dimensions from instrument output metadata

## Limitations

- Validation does not check for biological plausibility or outlier retention times/masses — focus is syntax and schema only
- Does not validate uniqueness of Component.Name or File.Name; duplicates are permitted
- Cannot verify that Match.Factor values are accurate; assumes Agilent library matching was performed correctly
- No changelog available; version compatibility with different Agilent Unknowns Analysis releases is not documented

## Evidence

- [readme] The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"
- [methods] ensure columns match expected schema (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name): "ensuring columns match expected schema (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name)"
- [methods] confirm all eight components present, verify no null matrices for samples with detected peaks: "confirm all eight components present, verify no null matrices for samples with detected peaks"
- [methods] The recommended software for generating the necessary data in the default format (i.e. with correct column names) is Unknowns Analysis: "The recommended software for generating the necessary data in the default format (i.e. with correct column names) is Unknowns Analysis"
