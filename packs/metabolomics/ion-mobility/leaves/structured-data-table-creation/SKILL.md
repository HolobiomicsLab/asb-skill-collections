---
name: structured-data-table-creation
description: Use when you have obtained a raw reference library file (such as the DTCCS_N2 library for U13C labeled lipids) and need to validate its structure, verify that all expected lipid entries are present, and ensure CCS values fall within physically plausible ranges (typically 50–300 Ų for small lipids).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - R
  - MobiLipid
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.4c01253
  title: mobilipid
evidence_spans:
- Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows
- MobiLipid aims to streamline lipidomics workflows by offering a fully automated solution for assessing and correcting collision cross section (CCS) bias
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilipid_cq
    doi: 10.1021/acs.analchem.4c01253
    title: mobilipid
  dedup_kept_from: coll_mobilipid_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01253
  all_source_dois:
  - 10.1021/acs.analchem.4c01253
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# structured-data-table-creation

## Summary

Parse and validate a reference library file (CSV/TSV) into a structured table with standardized columns (lipid class, species identifier, CCS value) and numeric range checks. This skill ensures that curated lipidomics reference data conforms to schema expectations before downstream bias calculation and correction workflows.

## When to use

You have obtained a raw reference library file (such as the DTCCS_N2 library for U13C labeled lipids) and need to validate its structure, verify that all expected lipid entries are present, and ensure CCS values fall within physically plausible ranges (typically 50–300 Ų for small lipids) before using it for internal standardization and CCS bias assessment in ion mobility-mass spectrometry lipidomics.

## When NOT to use

- The reference library is already validated and in production use in an active MobiLipid workflow.
- You are importing measured experimental CCS data from mass spectrometry; use this skill only for reference/standard libraries, not raw measurements.
- The input is not a reference library but a curated measurement table; this skill assumes you are curating static reference data.

## Inputs

- Raw reference library file (CSV or TSV; e.g., U13C_DT_CCS_library.csv)
- Library metadata or schema documentation specifying expected columns and nomenclature

## Outputs

- Structured reference library table (CSV or TSV) with columns: lipid class, lipid species identifier, CCS reference value
- Validation report (pass/fail flags, count of entries, numeric range summary)

## How to apply

Extract the library file (e.g., U13C_DT_CCS_library.csv) from the MobiLipid package distribution. Parse the CSV/TSV into a table with explicit columns for lipid class, lipid species identifier, and CCS reference value. Validate that all rows contain non-null entries, CCS values are numeric, and fall within the expected range (50–300 Ų); reject or flag outliers. Verify nomenclature consistency (e.g., lipid class names match those accepted by MobiLipid: Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG, etc.). Export the validated table as the canonical output file (CSV or TSV) for use in downstream bias calculation and correction workflows.

## Related tools

- **R** (Programming language for parsing, validating, and exporting CSV/TSV tables with data.table or base R functions) — https://cran.r-project.org/
- **MobiLipid** (Parent lipidomics workflow that consumes the validated reference library table for CCS bias calculation and correction) — https://github.com/FelinaHildebrand/MobiLipid

## Examples

```
library(data.table); lib <- fread('U13C_DT_CCS_library.csv'); lib_validated <- lib[!is.na(LipidClass) & !is.na(LipidSpecies) & !is.na(CCS_value) & CCS_value >= 50 & CCS_value <= 300]; fwrite(lib_validated, 'U13C_DT_CCS_library_validated.csv')
```

## Evaluation signals

- All rows in the output table contain non-null values in lipid class, species identifier, and CCS value columns.
- CCS values are numeric and all fall within the plausible range 50–300 Ų; no outliers or physically implausible values remain.
- Lipid class nomenclature matches the set accepted by MobiLipid (Cer, DG, HexCer, LPC, PA, PC, PE, PI, PS, TG, etc.) with no unexpected or typo variants.
- Row count and entry distribution match expectations for a complete U13C labeled lipid library (comparison against source documentation or prior versions).
- The exported table can be successfully loaded by MobiLipid's data import step without parsing or schema errors.

## Limitations

- This skill assumes the source library file is well-formed CSV/TSV; corrupted or malformed files may fail parsing and require manual repair.
- CCS reference values are assumed to be pre-measured and stable; this skill does NOT measure or derive new CCS values.
- Nomenclature validation depends on a maintained list of accepted lipid classes; new or non-standard lipid types may not be recognized.
- The plausible CCS range (50–300 Ų) applies to small lipids; larger molecules or unusual lipid species may require adjusted thresholds.

## Evidence

- [other] Parse the library data into a structured table format (CSV or TSV) containing lipid class, lipid species identifier, and CCS reference value columns.: "Parse the library data into a structured table format (CSV or TSV) containing lipid class, lipid species identifier, and CCS reference value columns."
- [other] Validate that all U13C labeled lipid entries are present and CCS values are numeric and within physically plausible ranges (typically 50–300 Ų for small lipids).: "Validate that all U13C labeled lipid entries are present and CCS values are numeric and within physically plausible ranges (typically 50–300 Ų for small lipids)."
- [other] Locate and extract the DTCCS_N2 reference library file for U13C labeled lipids from the package distribution.: "Locate and extract the DTCCS_N2 reference library file for U13C labeled lipids from the package distribution."
- [readme] This needs to be a .csv file containing the DT CCS N2 library. It is provided with the code and called "U13C_DT_CCS_library.csv".: "This needs to be a .csv file containing the DT CCS N2 library. It is provided with the code and called "U13C_DT_CCS_library.csv"."
- [intro] Employing a newly established DT CCS N2 library for U13C labeled lipids, which is provided together with the code: "Employing a newly established DT CCS N2 library for U13C labeled lipids, which is provided together with the code"
