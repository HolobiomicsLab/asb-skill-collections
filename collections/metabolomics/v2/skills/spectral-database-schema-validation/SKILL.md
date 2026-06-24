---
name: spectral-database-schema-validation
description: Use when when you have compiled raw mass spectrometry transition data
  (precursor m/z, product m/z, intensity, retention time, compound IDs) from experiments
  or external sources, and need to prepare it for ingestion into the EISA-EXPOSOME
  R Shiny platform for suspect screening.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - R Shiny
  - T3DB
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.3c02697
  title: EISA-EXPOSOME
evidence_spans:
- We provide a Rshiny program for EISA-EXPOSOME
- We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown
  below
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eisa_exposome_cq
    doi: 10.1021/acs.analchem.3c02697
    title: EISA-EXPOSOME
  dedup_kept_from: coll_eisa_exposome_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c02697
  all_source_dois:
  - 10.1021/acs.analchem.3c02697
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Database Schema Validation

## Summary

Validate and reformat mass spectrometry transition data into the EISA-EXPOSOME schema required for suspect chemical screening. This skill ensures database files conform to the exact column structure and data types needed for high-throughput peak extraction and chemical annotation.

## When to use

When you have compiled raw mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, compound IDs) from experiments or external sources, and need to prepare it for ingestion into the EISA-EXPOSOME R Shiny platform for suspect screening. Apply this skill before attempting any chemical annotation or peak extraction filtering.

## When NOT to use

- Your database is already in EISA-EXPOSOME format and has been validated—use this skill only for initial preparation or reformatting.
- You are performing peak extraction or filtering on raw spectra—this skill validates the *database*, not the analytical workflow.
- Your input is already a feature table or chromatogram matrix; this skill is for transition-list database curation, not spectral processing.

## Inputs

- Raw mass spectrometry transition data (CSV, XLSX, or tab-delimited text)
- Reference T3DB database file (.xlsx format) for validation cross-reference
- List of compound identifiers and expected transition pairs

## Outputs

- Validated spectral database file (.xlsx or .csv) conforming to EISA-EXPOSOME schema
- Validation report confirming presence, formatting, and consistency of NAME, PrecursorMZ, ProductMZ, Intensity, RT, and ID columns
- Verified file integrity confirmation

## How to apply

Obtain raw transition data in any tabular format (CSV, XLSX, or delimited text). Reformat into a table with exactly six columns: NAME (compound name), PrecursorMZ (numeric, e.g. 142.0086), ProductMZ (numeric, e.g. 94.0046), Intensity (numeric, typically 0–100 relative units), RT (numeric retention time in minutes; optional but recommended), and ID (integer or string identifier). Cross-reference your entries against the reference T3DB database file (provided in .xlsx format) to verify column alignment and confirm that well-known compounds like Methamidophos appear with expected transition pairs (e.g., PrecursorMZ 142.0086 → ProductMZ 94.0046 at Intensity 100, RT 2.182). Export the validated table as .xlsx or .csv and spot-check file integrity by reloading it into R or a spreadsheet editor to confirm no corruption or encoding errors occurred.

## Related tools

- **R Shiny** (Interactive platform for visualization and filtering of validated spectral database results; runs the EISA-EXPOSOME interface after database validation is complete) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **T3DB** (Reference database provided in .xlsx format; used as gold-standard cross-reference during column alignment and entry consistency checks) — https://github.com/Lab-XUE/EISA-EXPOSOME

## Examples

```
# Pseudo-code R workflow using tidyverse and readxl; load raw transitions, rename/reorder to EISA schema, cross-check against T3DB, export:
raw_db <- read.csv('transitions_raw.csv')
eia_schema <- raw_db %>% select(NAME = compound_name, PrecursorMZ = prec_mz, ProductMZ = prod_mz, Intensity = rel_int, RT = rt_min, ID = cpd_id)
T3DB_ref <- readxl::read_excel('T3DB.xlsx')
validated <- left_join(eia_schema, T3DB_ref %>% filter(NAME == 'Methamidophos'), by = 'NAME') %>% filter(!is.na(validated_flag))
writexl::write_xlsx(validated, 'database_validated.xlsx')
```

## Evaluation signals

- All six required columns (NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID) are present and correctly named (case-sensitive).
- PrecursorMZ and ProductMZ values are numeric and match expected mass-to-charge ratios (e.g., Methamidophos 142.0086 and 94.0046, respectively).
- Reference compound entries (e.g., Methamidophos with expected transition pairs and RT 2.182) match T3DB entries exactly.
- Intensity values are numeric and typically in the range 0–100 (relative units); no text or null values in intensity columns.
- File loads without encoding or corruption errors; reloaded data shows identical row counts and value distributions as the exported file.

## Limitations

- RT (retention time) is optional but strongly recommended; omitting it may reduce specificity in peak extraction workflows.
- The schema does not accommodate additional metadata columns (e.g., collision energy, instrument type, adduct type); extraneous columns should be dropped before export to avoid parser errors in EISA-EXPOSOME.
- Validation depends on availability of reference entries in T3DB; novel or rare compounds may lack cross-reference anchors.
- This skill validates schema and format only; it does not assess the scientific quality, accuracy, or completeness of transition data itself.

## Evidence

- [readme] Database schema requirement: "If you are building your own database, your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential."
- [other] Workflow steps for database preparation: "1. Obtain or prepare raw mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, and compound identifiers). 2. Format the data into a tabular structure with required"
- [other] Cross-reference and validation procedure: "3. Cross-reference entries against the compiled T3DB database file (provided in .xlsx format) to ensure column alignment and data consistency. 4. Validate presence and correct formatting of"
- [readme] Reference example entry: "|Methamidophos|142.0086|94.0046|100|2.182|1|"
- [other] Export and file integrity step: "5. Export the validated database as .xlsx or .csv format and verify file integrity."
- [readme] T3DB database availability: "We also provide the compiled T3DB database file in .xlsx format."
